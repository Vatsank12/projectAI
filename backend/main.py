from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pathlib import Path
import sys

try:
    from routers import metrics, scanner, processes, alerts, profile
    from core.websocket_manager import ConnectionManager
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

app = FastAPI(
    title="VigilantAI",
    version="1.0.0",
    description="Advanced System Monitoring & Security Dashboard"
)

manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = Path(__file__).resolve().parent.parent / "frontend"

@app.on_event("startup")
async def startup_event():
    if not frontend_path.exists():
        print(f"⚠️  Warning: Frontend directory not found at {frontend_path}")
    asyncio.create_task(metrics.stream_metrics(manager))

app.include_router(metrics.router)
app.include_router(scanner.router)
app.include_router(processes.router)
app.include_router(alerts.router)
app.include_router(profile.router)

@app.get("/", tags=["pages"])
async def root():
    index_path = frontend_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path), media_type="text/html")
    return {"error": "Index not found", "path": str(index_path)}

@app.get("/dashboard", tags=["pages"])
async def dashboard():
    dashboard_path = frontend_path / "dashboard.html"
    if dashboard_path.exists():
        return FileResponse(str(dashboard_path), media_type="text/html")
    raise HTTPException(status_code=404, detail="Dashboard not found")

@app.get("/styles.css", tags=["static"])
async def styles():
    css_path = frontend_path / "styles.css"
    if css_path.exists():
        return FileResponse(str(css_path), media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS file not found")

@app.get("/js/{filename}", tags=["static"])
async def get_js(filename: str):
    if not filename.endswith(".js"):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    js_path = frontend_path / "js" / filename
    if not js_path.exists():
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    
    return FileResponse(str(js_path), media_type="application/javascript")

@app.get("/favicon.ico", tags=["static"], include_in_schema=False)
async def favicon():
    return {"message": "VigilantAI"}

@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": "VigilantAI", "version": "1.0.0"}

@app.get("/info", tags=["info"])
async def info():
    return {
        "name": "VigilantAI",
        "version": "1.0.0",
        "description": "Advanced System Monitoring & Security Dashboard",
        "frontend_path": str(frontend_path),
        "frontend_exists": frontend_path.exists()
    }

if frontend_path.exists() and (frontend_path / "js").exists():
    try:
        app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    except Exception as e:
        print(f"Warning: Could not mount static files: {e}")

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("  VigilantAI - System Monitoring & Security Dashboard v1.0.0")
    print("="*70)
    print("Access Dashboard:")
    print("   -> http://localhost:8000")
    print("\nDemo Credentials:")
    print("   Username: admin")
    print("   Password: admin")
    print("\nAPI Documentation:")
    print("   -> http://localhost:8000/docs")
    print("   -> http://localhost:8000/redoc")
    print("\nHealth Check:")
    print("   -> http://localhost:8000/health")
    print("\nFrontend Path:")
    print(f"   {frontend_path}")
    print(f"   Status: {'Found' if frontend_path.exists() else 'Not Found'}")
    print("\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        access_log=True
    )
