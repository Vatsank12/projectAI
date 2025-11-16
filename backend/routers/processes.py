from fastapi import APIRouter
import psutil
import time
from typing import List

router = APIRouter(prefix="/api/processes", tags=["processes"])

@router.get("/list")
async def get_processes():
    processes = []
    try:
        for proc in psutil.process_iter(["pid", "name", "memory_percent", "cpu_percent"]):
            try:
                pinfo = proc.as_dict(attrs=["pid", "name", "memory_percent", "cpu_percent"])
                if pinfo["memory_percent"] is not None and pinfo["memory_percent"] > 0.1:
                    processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except:
        pass
    
    processes.sort(key=lambda x: x["memory_percent"] or 0, reverse=True)
    return processes[:30]

@router.post("/kill/{pid}")
async def kill_process(pid: int):
    try:
        process = psutil.Process(pid)
        process.kill()
        return {"status": "Process killed", "pid": pid}
    except Exception as e:
        return {"error": str(e)}

@router.get("/details/{pid}")
async def get_process_details(pid: int):
    try:
        process = psutil.Process(pid)
        return {
            "pid": process.pid,
            "name": process.name(),
            "status": process.status(),
            "memory_info": process.memory_info()._asdict(),
            "cpu_num": process.cpu_num(),
            "create_time": process.create_time(),
            "exe": process.exe() if process.exe() else "N/A",
            "cwd": process.cwd() if process.cwd() else "N/A"
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/system-info")
async def get_system_info():
    return {
        "cpu_count": psutil.cpu_count(),
        "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        "boot_time": psutil.boot_time(),
        "uptime_seconds": int(time.time() - psutil.boot_time()),
    }
