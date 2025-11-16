from fastapi import APIRouter, HTTPException
from datetime import datetime
from db.models import get_connection
import sqlite3

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("/", tags=["profile"])
async def get_profile(user_id: int = 1):
    try:
        conn = get_connection()
        c = conn.cursor()
        
        c.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
        profile = c.fetchone()
        
        if not profile:
            c.execute("""
                INSERT INTO user_profiles (user_id, fullname, email)
                VALUES (?, 'Administrator', 'admin@vigilantai.local')
            """, (user_id,))
            conn.commit()
            
            c.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
            profile = c.fetchone()
        
        conn.close()
        
        return {
            "id": profile[0],
            "user_id": profile[1],
            "fullname": profile[2],
            "email": profile[3],
            "bio": profile[4],
            "theme": profile[5],
            "sound_alerts": bool(profile[6]),
            "email_notifications": bool(profile[7]),
            "last_login": profile[8],
            "created_at": profile[9],
            "updated_at": profile[10]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    try:
        conn = get_connection()
        c = conn.cursor()
        
        updates = []
        params = []
        
        if fullname is not None:
            updates.append("fullname = ?")
            params.append(fullname)
        
        if email is not None:
            updates.append("email = ?")
            params.append(email)
        
        if bio is not None:
            updates.append("bio = ?")
            params.append(bio)
        
        if theme is not None:
            updates.append("theme = ?")
            params.append(theme)
        
        if sound_alerts is not None:
            updates.append("sound_alerts = ?")
            params.append(int(sound_alerts))
        
        if email_notifications is not None:
            updates.append("email_notifications = ?")
            params.append(int(email_notifications))
        
        if updates:
            updates.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            params.append(user_id)
            
            query = f"UPDATE user_profiles SET {', '.join(updates)} WHERE user_id = ?"
            c.execute(query, params)
            conn.commit()
        
        conn.close()
        
        return {"status": "success", "message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login-update", tags=["profile"])
async def update_last_login(user_id: int = 1):
    try:
        conn = get_connection()
        c = conn.cursor()
        
        c.execute(
            "UPDATE user_profiles SET last_login = ? WHERE user_id = ?",
            (datetime.now().isoformat(), user_id)
        )
        conn.commit()
        conn.close()
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/notifications", tags=["profile"])
async def get_notifications(user_id: int = 1, limit: int = 50):
    try:
        conn = get_connection()
        c = conn.cursor()
        
        c.execute(
            "SELECT * FROM notifications WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        )
        notifications = c.fetchall()
        conn.close()
        
        return [{
            "id": n[0],
            "user_id": n[1],
            "title": n[2],
            "message": n[3],
            "type": n[4],
            "read": bool(n[5]),
            "timestamp": n[6]
        } for n in notifications]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notifications", tags=["profile"])
async def add_notification(
    user_id: int = 1,
    title: str = "",
    message: str = "",
    notification_type: str = "info"
):
    try:
        conn = get_connection()
        c = conn.cursor()
        
        c.execute("""
            INSERT INTO notifications (user_id, title, message, type)
            VALUES (?, ?, ?, ?)
        """, (user_id, title, message, notification_type))
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Notification added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/notifications/{notification_id}", tags=["profile"])
async def delete_notification(notification_id: int):
    try:
        conn = get_connection()
        c = conn.cursor()
        
        c.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        conn.commit()
        conn.close()
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/notifications", tags=["profile"])
async def clear_notifications(user_id: int = 1):
    try:
        conn = get_connection()
        c = conn.cursor()
        
        c.execute("DELETE FROM notifications WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "All notifications cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
