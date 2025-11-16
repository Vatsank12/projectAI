from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from typing import List, Dict, Any
import hashlib
import os
import asyncio
import tempfile
from datetime import datetime
import stat
import mimetypes
from concurrent.futures import ThreadPoolExecutor
import threading

router = APIRouter(prefix="/api/scanner", tags=["scanner"])

scanned_files = []
quarantine_files = []

# Global scanning state
scan_state = {
    "is_scanning": False,
    "progress": 0,
    "total_files": 0,
    "processed_files": 0,
    "current_file": "",
    "scan_id": None,
    "should_abort": False,
    "results": []
}

executor = ThreadPoolExecutor(max_workers=4)

def calculate_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def analyze_file(filepath):
    suspicious_keywords = [".exe", ".bat", ".cmd", ".com", ".scr", ".vbs", ".js", ".jar", ".msi", ".dmg", ".pkg"]
    suspicious_paths = ["temp", "tmp", "cache", "downloads", "desktop"]
    filename = os.path.basename(filepath).lower()
    file_path = os.path.dirname(filepath).lower()

    try:
        file_hash = calculate_file_hash(filepath)
        file_size = os.path.getsize(filepath)
        file_stats = os.stat(filepath)
        mime_type, _ = mimetypes.guess_type(filepath)

        # Get file permissions
        permissions = stat.filemode(file_stats.st_mode)

        # Get file modification time
        mod_time = datetime.fromtimestamp(file_stats.st_mtime).isoformat()

        threat_score = 0
        suspicious_indicators = []

        # Check for suspicious extensions
        if any(keyword in filename for keyword in suspicious_keywords):
            threat_score += 30
            suspicious_indicators.append("Executable extension detected")

        # Check for suspicious paths
        if any(path in file_path for path in suspicious_paths):
            threat_score += 15
            suspicious_indicators.append("Located in suspicious directory")

        # Check file size
        if file_size > 100 * 1024 * 1024:  # 100MB
            threat_score += 20
            suspicious_indicators.append("Unusually large file")
        elif file_size == 0:
            threat_score += 10
            suspicious_indicators.append("Empty file")

        # Check for hidden files
        if filename.startswith('.'):
            threat_score += 5
            suspicious_indicators.append("Hidden file")

        # Check for suspicious MIME types
        if mime_type and ('executable' in mime_type or 'application/x-' in mime_type):
            threat_score += 25
            suspicious_indicators.append("Suspicious MIME type")

        # Check file age (very new files might be suspicious)
        file_age_days = (datetime.now() - datetime.fromtimestamp(file_stats.st_mtime)).days
        if file_age_days < 1:
            threat_score += 10
            suspicious_indicators.append("Recently modified file")

        return {
            "filename": os.path.basename(filepath),
            "filepath": filepath,
            "hash": file_hash,
            "size": file_size,
            "size_human": f"{file_size / 1024:.2f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.2f} MB",
            "permissions": permissions,
            "mime_type": mime_type or "unknown",
            "modified_time": mod_time,
            "threat_score": threat_score,
            "threat_level": "CRITICAL" if threat_score >= 70 else "HIGH" if threat_score >= 50 else "MEDIUM" if threat_score >= 30 else "LOW",
            "suspicious_indicators": suspicious_indicators,
            "timestamp": datetime.now().isoformat(),
            "file_age_days": file_age_days
        }
    except Exception as e:
        return {
            "filename": os.path.basename(filepath),
            "filepath": filepath,
            "error": str(e),
            "threat_score": 0,
            "threat_level": "ERROR",
            "timestamp": datetime.now().isoformat()
        }

@router.get("/files")
async def get_scanned_files():
    return scanned_files

@router.get("/quarantine")
async def get_quarantine():
    return quarantine_files

@router.post("/scan")
async def scan_file(file: UploadFile = File(...)):
    try:
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
        
        try:
            analysis = analyze_file(temp_path)
            scanned_files.append(analysis)
            
            if analysis["threat_score"] >= 50:
                quarantine_files.append(analysis)
            
            return analysis
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
    except Exception as e:
        return {"error": str(e)}

@router.get("/progress")
async def get_scan_progress():
    return scan_state

@router.post("/abort")
async def abort_scan():
    if scan_state["is_scanning"]:
        scan_state["should_abort"] = True
        return {"status": "Scan abort requested"}
    return {"status": "No active scan to abort"}

@router.post("/scan-directory")
async def scan_directory(path: str, background_tasks: BackgroundTasks):
    if scan_state["is_scanning"]:
        raise HTTPException(status_code=409, detail="Scan already in progress")

    # Reset scan state
    scan_state.update({
        "is_scanning": True,
        "progress": 0,
        "total_files": 0,
        "processed_files": 0,
        "current_file": "",
        "scan_id": f"scan_{int(datetime.now().timestamp())}",
        "should_abort": False,
        "results": []
    })

    background_tasks.add_task(scan_directory_async, path)
    return {"status": "Scan started", "scan_id": scan_state["scan_id"], "path": path}

async def scan_directory_async(path: str):
    try:
        # First pass: count total files
        total_files = 0
        for root, dirs, files in os.walk(path):
            if scan_state["should_abort"]:
                break
            total_files += len(files)

        scan_state["total_files"] = total_files

        if scan_state["should_abort"]:
            scan_state["is_scanning"] = False
            return

        # Second pass: scan files with progress updates using concurrency
        processed = 0
        results = []
        file_batch = []
        batch_size = 4

        async def process_file_batch(batch):
            tasks = []
            for filepath in batch:
                if scan_state["should_abort"]:
                    return []
                task = asyncio.get_event_loop().run_in_executor(executor, analyze_file, filepath)
                tasks.append(task)
            return await asyncio.gather(*tasks, return_exceptions=True)

        for root, dirs, files in os.walk(path):
            if scan_state["should_abort"]:
                break

            for file in files:
                if scan_state["should_abort"]:
                    break

                filepath = os.path.join(root, file)
                file_batch.append(filepath)

                # Process batch when it reaches the batch size
                if len(file_batch) >= batch_size:
                    scan_state["current_file"] = f"Processing batch of {len(file_batch)} files"

                    batch_results = await process_file_batch(file_batch)

                    for i, result in enumerate(batch_results):
                        filepath = file_batch[i]

                        if isinstance(result, Exception):
                            error_result = {
                                "filename": os.path.basename(filepath),
                                "filepath": filepath,
                                "error": str(result),
                                "threat_score": 0,
                                "threat_level": "ERROR",
                                "timestamp": datetime.now().isoformat()
                            }
                            results.append(error_result)
                            scanned_files.append(error_result)
                        else:
                            results.append(result)
                            scanned_files.append(result)

                            if result.get("threat_score", 0) >= 50 and "error" not in result:
                                quarantine_files.append(result)

                    processed += len(file_batch)
                    scan_state["processed_files"] = processed
                    scan_state["progress"] = int((processed / total_files) * 100) if total_files > 0 else 0

                    file_batch = []

                    # Very small delay between batches
                    await asyncio.sleep(0.005)

        # Process remaining files in the last batch
        if file_batch and not scan_state["should_abort"]:
            scan_state["current_file"] = f"Processing final batch of {len(file_batch)} files"

            batch_results = await process_file_batch(file_batch)

            for i, result in enumerate(batch_results):
                filepath = file_batch[i]

                if isinstance(result, Exception):
                    error_result = {
                        "filename": os.path.basename(filepath),
                        "filepath": filepath,
                        "error": str(result),
                        "threat_score": 0,
                        "threat_level": "ERROR",
                        "timestamp": datetime.now().isoformat()
                    }
                    results.append(error_result)
                    scanned_files.append(error_result)
                else:
                    results.append(result)
                    scanned_files.append(result)

                    if result.get("threat_score", 0) >= 50 and "error" not in result:
                        quarantine_files.append(result)

            processed += len(file_batch)
            scan_state["processed_files"] = processed
            scan_state["progress"] = int((processed / total_files) * 100) if total_files > 0 else 0

        scan_state["results"] = results
        scan_state["is_scanning"] = False

    except Exception as e:
        print(f"Scan error: {e}")
        scan_state["is_scanning"] = False
        scan_state["results"] = [{"error": str(e), "timestamp": datetime.now().isoformat()}]

@router.post("/batch-scan")
async def batch_scan_files(files: List[UploadFile] = File(...)):
    if scan_state["is_scanning"]:
        raise HTTPException(status_code=409, detail="Scan already in progress")

    # Reset scan state
    scan_state.update({
        "is_scanning": True,
        "progress": 0,
        "total_files": len(files),
        "processed_files": 0,
        "current_file": "",
        "scan_id": f"batch_{int(datetime.now().timestamp())}",
        "should_abort": False,
        "results": []
    })

    async def process_single_file(file: UploadFile, index: int):
        if scan_state["should_abort"]:
            return None

        scan_state["current_file"] = file.filename

        try:
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"{index}_{file.filename}")

            with open(temp_path, "wb") as buffer:
                contents = await file.read()
                buffer.write(contents)

            try:
                # Use thread pool for CPU-intensive operations
                loop = asyncio.get_event_loop()
                analysis = await loop.run_in_executor(executor, analyze_file, temp_path)
                return analysis

            finally:
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except:
                        pass

        except Exception as e:
            return {
                "filename": file.filename,
                "error": str(e),
                "threat_score": 0,
                "threat_level": "ERROR",
                "timestamp": datetime.now().isoformat()
            }

    # Process files concurrently in batches
    batch_size = 4  # Process 4 files at a time
    results = []

    for i in range(0, len(files), batch_size):
        if scan_state["should_abort"]:
            break

        batch = files[i:i + batch_size]
        batch_tasks = [process_single_file(file, i + j) for j, file in enumerate(batch)]
        batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

        for result in batch_results:
            if result is not None:
                if isinstance(result, Exception):
                    # Handle exceptions from gather
                    error_result = {
                        "filename": "unknown",
                        "error": str(result),
                        "threat_score": 0,
                        "threat_level": "ERROR",
                        "timestamp": datetime.now().isoformat()
                    }
                    results.append(error_result)
                    scanned_files.append(error_result)
                else:
                    results.append(result)
                    scanned_files.append(result)

                    if result.get("threat_score", 0) >= 50 and "error" not in result:
                        quarantine_files.append(result)

        scan_state["processed_files"] = len(results)
        scan_state["progress"] = int((len(results) / len(files)) * 100)

        # Very small delay between batches to prevent overwhelming
        await asyncio.sleep(0.01)

    scan_state["results"] = results
    scan_state["is_scanning"] = False

    return {"results": results, "scan_id": scan_state["scan_id"]}

@router.post("/quarantine/{file_hash}")
async def quarantine_file(file_hash: str):
    for file in scanned_files:
        if file["hash"] == file_hash:
            if file not in quarantine_files:
                quarantine_files.append(file)
            return {"status": "File quarantined", "file": file}
    return {"error": "File not found"}

@router.delete("/quarantine/{file_hash}")
async def restore_from_quarantine(file_hash: str):
    for file in quarantine_files:
        if file["hash"] == file_hash:
            quarantine_files.remove(file)
            return {"status": "File restored"}
    return {"error": "File not found"}
