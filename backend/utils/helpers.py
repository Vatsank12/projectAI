import hashlib
import json
from typing import Dict, Any, List

def format_bytes(bytes: float) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

def calculate_health_score(cpu: float, memory: float, disk: float) -> int:
    score = 100
    score -= cpu * 0.4
    score -= memory * 0.4
    score -= disk * 0.2
    return max(0, min(100, int(score)))

def get_threat_level(score: int) -> str:
    if score >= 70:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"

def sanitize_data(data: Dict[str, Any]) -> Dict[str, Any]:
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, (str, int, float, bool, type(None))):
            sanitized[key] = value
        elif isinstance(value, dict):
            sanitized[key] = sanitize_data(value)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_data(item) if isinstance(item, dict) else item for item in value]
    return sanitized

def create_alert_message(title: str, message: str, severity: str, alert_type: str) -> Dict[str, str]:
    return {
        "title": title,
        "message": message,
        "severity": severity,
        "type": alert_type
    }

def check_thresholds(current: Dict[str, float], thresholds: Dict[str, float]) -> List[Dict[str, Any]]:
    alerts = []
    
    if current.get("cpu", 0) > thresholds.get("cpu", 80):
        alerts.append(create_alert_message(
            "High CPU Usage",
            f"CPU usage is at {current['cpu']:.1f}%",
            "high",
            "performance"
        ))
    
    if current.get("memory", 0) > thresholds.get("memory", 85):
        alerts.append(create_alert_message(
            "High Memory Usage",
            f"Memory usage is at {current['memory']:.1f}%",
            "high",
            "performance"
        ))
    
    if current.get("disk", 0) > thresholds.get("disk", 90):
        alerts.append(create_alert_message(
            "Low Disk Space",
            f"Disk usage is at {current['disk']:.1f}%",
            "medium",
            "system"
        ))
    
    return alerts
