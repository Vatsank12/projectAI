from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import psutil
import asyncio
import time
import os
from datetime import datetime

router = APIRouter(prefix="/api/metrics", tags=["metrics"])

metrics_history = {
    "cpu": [],
    "memory": [],
    "disk": [],
    "network": [],
    "temperature": []
}

MAX_HISTORY = 60

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return {
        "percent": mem.percent,
        "used": mem.used / (1024**3),
        "total": mem.total / (1024**3)
    }

def get_disk_usage():
    disk = psutil.disk_usage(os.path.sep)
    return {
        "percent": disk.percent,
        "used": disk.used / (1024**3),
        "total": disk.total / (1024**3),
        "read_count": psutil.disk_io_counters().read_count if psutil.disk_io_counters() else 0,
        "write_count": psutil.disk_io_counters().write_count if psutil.disk_io_counters() else 0
    }

def get_network_usage():
    net = psutil.net_io_counters()
    return {
        "bytes_sent": net.bytes_sent / (1024**2),
        "bytes_recv": net.bytes_recv / (1024**2),
        "packets_sent": net.packets_sent,
        "packets_recv": net.packets_recv
    }

def get_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            avg_temp = sum(temp.current for core_temps in temps.values() for temp in core_temps) / sum(len(core_temps) for core_temps in temps.values())
            return avg_temp
    except:
        return 0
    return 0

def get_all_metrics():
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu": get_cpu_usage(),
        "memory": get_memory_usage(),
        "disk": get_disk_usage(),
        "network": get_network_usage(),
        "temperature": get_temperature()
    }

@router.get("/current")
async def get_current_metrics():
    return get_all_metrics()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    try:
        while True:
            metrics = get_all_metrics()
            await websocket.send_json(metrics)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass

async def stream_metrics(manager):
    while True:
        metrics = get_all_metrics()
        await manager.broadcast({
            "type": "metrics",
            "data": metrics
        })
        await asyncio.sleep(1)
