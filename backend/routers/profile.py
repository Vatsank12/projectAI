from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter(prefix="/api/profile", tags=["profile"])

# Mock profile data since no database is used
mock_profile = {
    "id": 1,
    "user_id": 1,
    "fullname": "Administrator",
    "email": "admin@vigilantai.local",
    "bio": "System Administrator",
    "theme": "dark",
    "sound_alerts": True,
    "email_notifications": False,
    "last_login": datetime.now().isoformat(),
    "created_at": datetime.now().isoformat(),
    "updated_at": datetime.now().isoformat()
}

@router.get("/", tags=["profile"])
async def get_profile(user_id: int = 1):
    return mock_profile

@router.put("/", tags=["profile"])
async def update_profile(
    user_id: int = 1,
    fullname: str = None,
    email: str = None,
    bio: str = None,
    theme: str = None,
    sound_alerts: bool = None,
    email_notifications: bool = None
):
    global mock_profile
    if fullname is not None:
        mock_profile["fullname"] = fullname
    if email is not None:
        mock_profile["email"] = email
    if bio is not None:
        mock_profile["bio"] = bio
    if theme is not None:
        mock_profile["theme"] = theme
    if sound_alerts is not None:
        mock_profile["sound_alerts"] = sound_alerts
    if email_notifications is not None:
        mock_profile["email_notifications"] = email_notifications
    mock_profile["updated_at"] = datetime.now().isoformat()
    return {"status": "success", "message": "Profile updated successfully"}

@router.post("/login-update", tags=["profile"])
async def update_last_login(user_id: int = 1):
    global mock_profile
    mock_profile["last_login"] = datetime.now().isoformat()
    return {"status": "success"}

@router.get("/notifications", tags=["profile"])
async def get_notifications(user_id: int = 1, limit: int = 50):
    # Return empty list since no database
    return []

@router.post("/notifications", tags=["profile"])
async def add_notification(
    user_id: int = 1,
    title: str = "",
    message: str = "",
    notification_type: str = "info"
):
    # Mock success since no database
    return {"status": "success", "message": "Notification added"}

@router.delete("/notifications/{notification_id}", tags=["profile"])
async def delete_notification(notification_id: int):
    return {"status": "success"}

@router.delete("/notifications", tags=["profile"])
async def clear_notifications(user_id: int = 1):
    return {"status": "success", "message": "All notifications cleared"}
