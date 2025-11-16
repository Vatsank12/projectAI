#!/usr/bin/env python3

import os
import sys
from pathlib import Path

def check_structure():
    """Check if project structure is correct"""
    print("\n" + "="*60)
    print("VigilantAI - Setup Verification")
    print("="*60 + "\n")
    
    base_dir = Path(__file__).resolve().parent
    checks = {
        "Backend Directory": base_dir / "backend",
        "Frontend Directory": base_dir / "frontend",
        "Backend main.py": base_dir / "backend" / "main.py",
        "Backend requirements.txt": base_dir / "backend" / "requirements.txt",
        "Frontend index.html": base_dir / "frontend" / "index.html",
        "Frontend dashboard.html": base_dir / "frontend" / "dashboard.html",
        "Frontend styles.css": base_dir / "frontend" / "styles.css",
        "Frontend JS directory": base_dir / "frontend" / "js",
        "Frontend main.js": base_dir / "frontend" / "js" / "main.js",
        "Frontend charts.js": base_dir / "frontend" / "js" / "charts.js",
        "Frontend assistant.js": base_dir / "frontend" / "js" / "assistant.js",
        "Backend routers": base_dir / "backend" / "routers",
        "Backend routers metrics.py": base_dir / "backend" / "routers" / "metrics.py",
        "Backend routers scanner.py": base_dir / "backend" / "routers" / "scanner.py",
        "Backend routers processes.py": base_dir / "backend" / "routers" / "processes.py",
        "Backend routers alerts.py": base_dir / "backend" / "routers" / "alerts.py",
        "Backend routers assistant.py": base_dir / "backend" / "routers" / "assistant.py",
        "Backend core directory": base_dir / "backend" / "core",
        "Backend websocket_manager.py": base_dir / "backend" / "core" / "websocket_manager.py",
        "Backend db directory": base_dir / "backend" / "db",
        "Backend models.py": base_dir / "backend" / "db" / "models.py",
    }
    
    passed = 0
    failed = 0
    
    print("📁 Directory Structure Check:\n")
    
    for name, path in checks.items():
        if path.exists():
            status = "✅"
            passed += 1
        else:
            status = "❌"
            failed += 1
        print(f"{status} {name}")
        if not path.exists():
            print(f"   Expected: {path}")
    
    print(f"\n{'='*60}")
    print(f"Passed: {passed}/{len(checks)}")
    print(f"Failed: {failed}/{len(checks)}")
    print("="*60 + "\n")
    
    return failed == 0

def check_dependencies():
    """Check if Python dependencies are available"""
    print("📦 Dependency Check:\n")
    
    dependencies = [
        "fastapi",
        "uvicorn",
        "psutil",
        "watchdog",
        "aiofiles",
        "multipart",
        "websockets"
    ]
    
    passed = 0
    failed = 0
    
    for dep in dependencies:
        try:
            __import__(dep.replace("-", "_"))
            print(f"✅ {dep}")
            passed += 1
        except ImportError:
            print(f"❌ {dep} (not installed)")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Passed: {passed}/{len(dependencies)}")
    print(f"Failed: {failed}/{len(dependencies)}")
    print("="*60 + "\n")
    
    if failed > 0:
        print("💡 Install missing dependencies:")
        print("   cd backend")
        print("   pip install -r requirements.txt\n")
    
    return failed == 0

def check_file_contents():
    """Check if key files have content"""
    print("📄 File Content Check:\n")
    
    base_dir = Path(__file__).resolve().parent
    files_to_check = [
        base_dir / "backend" / "main.py",
        base_dir / "frontend" / "dashboard.html",
        base_dir / "frontend" / "styles.css",
        base_dir / "frontend" / "js" / "main.js",
    ]
    
    passed = 0
    failed = 0
    
    for file_path in files_to_check:
        try:
            if file_path.exists():
                size = file_path.stat().st_size
                if size > 100:
                    print(f"✅ {file_path.name} ({size} bytes)")
                    passed += 1
                else:
                    print(f"❌ {file_path.name} (empty or too small)")
                    failed += 1
            else:
                print(f"❌ {file_path.name} (not found)")
                failed += 1
        except Exception as e:
            print(f"❌ {file_path.name} (error: {e})")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Passed: {passed}/{len(files_to_check)}")
    print(f"Failed: {failed}/{len(files_to_check)}")
    print("="*60 + "\n")
    
    return failed == 0

def main():
    """Run all checks"""
    structure_ok = check_structure()
    files_ok = check_file_contents()
    deps_ok = check_dependencies()
    
    print("="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    print(f"Structure:  {'✅ PASS' if structure_ok else '❌ FAIL'}")
    print(f"Files:      {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    print("="*60 + "\n")
    
    if structure_ok and files_ok and deps_ok:
        print("✨ All checks passed! Ready to run.")
        print("\n📝 Next steps:")
        print("   1. cd backend")
        print("   2. python main.py")
        print("   3. Open http://localhost:8000")
        print("   4. Login with admin/admin\n")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
