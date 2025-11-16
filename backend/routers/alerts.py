from fastapi import APIRouter
from typing import List
from datetime import datetime
from enum import Enum

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(str, Enum):
    SYSTEM = "system"
    SECURITY = "security"
    PERFORMANCE = "performance"
    PROCESS = "process"

alerts_list = []

def create_alert(title: str, message: str, severity: AlertSeverity, alert_type: AlertType):
    alert = {
        "id": len(alerts_list),
        "title": title,
        "message": message,
        "severity": severity,
        "type": alert_type,
        "timestamp": datetime.now().isoformat(),
        "read": False
    }
    alerts_list.append(alert)
    return alert

@router.get("/")
async def get_alerts():
    return sorted(alerts_list, key=lambda x: x["timestamp"], reverse=True)

@router.get("/unread")
async def get_unread_alerts():
    return [a for a in alerts_list if not a["read"]]

@router.post("/{alert_id}/read")
async def mark_alert_read(alert_id: int):
    for alert in alerts_list:
        if alert["id"] == alert_id:
            alert["read"] = True
            return alert
    return {"error": "Alert not found"}

@router.delete("/{alert_id}")
async def delete_alert(alert_id: int):
    global alerts_list
    alerts_list = [a for a in alerts_list if a["id"] != alert_id]
    return {"status": "Alert deleted"}

@router.post("/create")
async def create_new_alert(title: str, message: str, severity: AlertSeverity = AlertSeverity.MEDIUM, alert_type: AlertType = AlertType.SYSTEM):
    return create_alert(title, message, severity, alert_type)

@router.delete("/clear-all")
async def clear_all_alerts():
    global alerts_list
    alerts_list = []
    return {"status": "All alerts cleared"}
