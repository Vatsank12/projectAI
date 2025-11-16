from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
import psutil
import os
import json

# Load environment variables
try:
    from dotenv import load_dotenv
    from pathlib import Path
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment variables from {env_path}")
    else:
        print("No .env file found")
except ImportError:
    print("python-dotenv not installed")

router = APIRouter(prefix="/api/assistant", tags=["assistant"])

conversations = []

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

def get_system_health():
    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(os.path.sep)
    
    health_score = 100
    
    if cpu > 80:
        health_score -= 30
    elif cpu > 50:
        health_score -= 15
    
    if memory.percent > 80:
        health_score -= 30
    elif memory.percent > 50:
        health_score -= 15
    
    if disk.percent > 80:
        health_score -= 20
    
    return {
        "score": max(0, health_score),
        "status": "CRITICAL" if health_score < 30 else "WARNING" if health_score < 60 else "HEALTHY",
        "cpu": cpu,
        "memory": memory.percent,
        "disk": disk.percent
    }

def get_system_info():
    health = get_system_health()
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        uptime_str = f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds//60)%60}m"
    except:
        uptime_str = "Unknown"
    
    return {
        "health": health,
        "uptime": uptime_str,
        "cpu_cores": psutil.cpu_count(),
        "total_ram": f"{psutil.virtual_memory().total / (1024**3):.1f}GB",
        "disk_total": f"{psutil.disk_usage('/').total / (1024**3):.1f}GB",
        "processes": len(psutil.pids())
    }

def generate_local_ai_response(user_message: str):
    user_msg_lower = user_message.lower().strip()

    # Cache system info to avoid multiple calls
    health = get_system_health()
    system_info = get_system_info()

    # Pre-compute common values
    cpu_usage = health['cpu']
    mem_usage = health['memory']
    disk_usage = health['disk']
    health_status = health['status']
    health_score = health['score']

    # Quick keyword matching with exact matches first
    keyword_responses = {
        "health": f"Your system is currently {health_status}. Overall health score: {health_score}/100. CPU usage: {cpu_usage:.1f}%, Memory: {mem_usage:.1f}%, Disk: {disk_usage:.1f}%. System uptime: {system_info['uptime']}.",

        "performance": f"Performance Analysis: Your system is running {'smoothly' if health_status == 'HEALTHY' else 'with some strain'}. Current CPU load is {cpu_usage:.1f}% and memory is at {mem_usage:.1f}%. {'CPU is high, consider closing background applications.' if cpu_usage > 70 else ''} {'Memory usage is high, close unnecessary programs.' if mem_usage > 70 else 'Memory usage is acceptable.'}",

        "cpu": f"CPU Status: Current usage is {cpu_usage:.1f}%. You have {system_info['cpu_cores']} CPU cores. {'High CPU usage detected - check Processes tab.' if cpu_usage > 75 else 'CPU usage is normal.'}",

        "memory": f"Memory Status: Using {mem_usage:.1f}% of {system_info['total_ram']}. {'Critical memory usage!' if mem_usage > 90 else 'High memory usage!' if mem_usage > 75 else 'Memory usage is healthy.'}",

        "disk": f"Disk Status: {disk_usage:.1f}% full ({system_info['disk_total']} total). {'Disk space critically low!' if disk_usage > 90 else 'Disk space adequate.' if disk_usage < 70 else 'Disk space getting low.'}",

        "security": "Security: Use File Scanner regularly, monitor Alerts, review processes, enable notifications.",

        "scan": "File Scanning: Go to Scanner section. Drag & drop files or browse. Each file gets threat analysis.",

        "processes": "Process Management: Check Processes tab for running apps, CPU/memory usage, resource-heavy programs.",

        "alerts": "Security Alerts: Review Alerts section. Each shows severity (Critical/High/Medium/Low) and details.",

        "help": "I'm VigilantAI Assistant. I help with: System Health, Performance, Security, File scanning, Process management, Recommendations. What do you need?",

        "settings": "Settings: Configure monitoring intervals, alert thresholds, notifications in Settings section.",

        "profile": "Profile: Set name, email, bio, preferences. Change password and theme.",

        "recommendation": f"Smart Recommendations ({health_status}): {get_smart_recommendations(health, system_info)}",
    }

    # Exact keyword match (fastest)
    if user_msg_lower in keyword_responses:
        return keyword_responses[user_msg_lower]

    # Partial keyword matching
    for keyword, response in keyword_responses.items():
        if keyword in user_msg_lower:
            return response

    # Greeting responses
    if any(word in user_msg_lower for word in ["hi", "hello", "hey", "greetings"]):
        return "👋 Hello! I'm VigilantAI Assistant, your cybersecurity AI. I help monitor system security and performance. Ask about health, security, or performance!"

    # Thanks responses
    if any(word in user_msg_lower for word in ["thanks", "thank you", "appreciate"]):
        return "You're welcome! Happy to help with your system's security and performance."

    # Question handling
    if any(word in user_msg_lower for word in ["how", "what", "explain", "why", "overheat", "hot", "temperature", "heating"]):
        if "cpu" in user_msg_lower or "processor" in user_msg_lower:
            return keyword_responses["cpu"]
        elif "memory" in user_msg_lower or "ram" in user_msg_lower:
            return keyword_responses["memory"]
        elif "disk" in user_msg_lower or "storage" in user_msg_lower:
            return keyword_responses["disk"]
        elif any(word in user_msg_lower for word in ["overheat", "hot", "temperature", "heating", "warm"]):
            overheating_reasons = []
            if cpu_usage > 70:
                overheating_reasons.append(f"High CPU usage ({cpu_usage:.1f}%) - close background applications")
            if mem_usage > 80:
                overheating_reasons.append(f"High memory usage ({mem_usage:.1f}%) - free up RAM")
            if len(psutil.pids()) > 200:
                overheating_reasons.append(f"Too many processes running ({len(psutil.pids())})")

            if overheating_reasons:
                return f"PC Overheating Analysis: {', '.join(overheating_reasons)}. Additional tips: Clean dust from vents/fans, ensure proper ventilation, update drivers, check for malware. Current: CPU {cpu_usage:.1f}%, Memory {mem_usage:.1f}%."
            else:
                return f"Temperature Check: Your system shows CPU {cpu_usage:.1f}%, Memory {mem_usage:.1f}%. If overheating persists: 1) Clean internal dust, 2) Check fan operation, 3) Ensure proper airflow, 4) Update BIOS/firmware, 5) Monitor with hardware tools."

    # Default response with current status
    return f"System Status: {health_status} ({health_score}/100) | CPU: {cpu_usage:.1f}% | Memory: {mem_usage:.1f}%. Ask about health, security, or performance!"

def get_smart_recommendations(health: dict, system_info: dict) -> str:
    recommendations = []
    
    if health['cpu'] > 80:
        recommendations.append("Close background applications - High CPU usage detected")
    elif health['cpu'] > 50:
        recommendations.append("Monitor CPU - Usage is moderately high")
    else:
        recommendations.append("CPU is performing well")
    
    if health['memory'] > 85:
        recommendations.append("Restart system immediately - Critical memory")
    elif health['memory'] > 70:
        recommendations.append("Free up memory - Usage is high")
    else:
        recommendations.append("Memory usage is optimal")
    
    if health['disk'] > 90:
        recommendations.append("Clean disk urgently - Very low free space")
    elif health['disk'] > 75:
        recommendations.append("Free up disk space - Running low")
    else:
        recommendations.append("Disk space is sufficient")
    
    recommendations.append(f"System has been up for {system_info['uptime']}")
    recommendations.append(f"Monitor {system_info['processes']} active processes")
    
    return " | ".join(recommendations)

def generate_ai_response_with_groq(user_message: str):
    try:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return None

        client = Groq(api_key=api_key)
        system_info = get_system_info()

        system_prompt = f"""You are VigilantAI Assistant, an intelligent cybersecurity and system monitoring AI for the VigilantAI dashboard.
Current System Status:
- Health Score: {system_info['health']['score']}/100 ({system_info['health']['status']})
- CPU Usage: {system_info['health']['cpu']:.1f}%
- Memory Usage: {system_info['health']['memory']:.1f}%
- Disk Usage: {system_info['health']['disk']:.1f}%
- Uptime: {system_info['uptime']}

You provide expert advice on system security, performance optimization, threat analysis, and monitoring. Be concise, professional, and actionable in your responses. Focus on cybersecurity and system health."""

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.1-8b-instant",
            max_tokens=512,
            temperature=0.7,
            timeout=10  # Increased timeout
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Groq API error: {e}")
        return None

def generate_ai_response(user_message: str):
    try:
        # Try Groq API first if available
        if GROQ_AVAILABLE:
            response = generate_ai_response_with_groq(user_message)
            if response and len(response.strip()) > 10:  # Ensure we got a meaningful response
                return response

        # Fallback to local AI
        return generate_local_ai_response(user_message)

    except Exception as e:
        print(f"Error in generate_ai_response: {e}")
        # Emergency fallback
        return "I'm experiencing technical difficulties. Please try again or ask about system health, security, or performance."

@router.post("/message")
async def send_message(message: str):
    try:
        if not message or len(message.strip()) == 0:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        print(f"Processing AI message: '{message[:50]}...'")

        response = generate_ai_response(message)

        if not response:
            response = "I apologize, but I'm unable to generate a response right now. Please try again or ask about system health."

        conversation = {
            "id": len(conversations),
            "user_message": message,
            "ai_response": response,
            "timestamp": datetime.now().isoformat()
        }
        conversations.append(conversation)

        print(f"AI response generated successfully ({len(response)} chars)")
        return conversation

    except Exception as e:
        print(f"Error in send_message endpoint: {e}")
        error_response = "I'm experiencing technical difficulties. Please check your connection and try again."
        conversation = {
            "id": len(conversations),
            "user_message": message,
            "ai_response": error_response,
            "timestamp": datetime.now().isoformat(),
            "error": True
        }
        conversations.append(conversation)
        return conversation

@router.get("/history")
async def get_conversation_history():
    return sorted(conversations, key=lambda x: x["timestamp"])

@router.get("/health-insight")
async def get_health_insight():
    health = get_system_health()
    system_info = get_system_info()
    insights = []
    
    if health["cpu"] > 80:
        insights.append("⚠️ High CPU usage detected. Consider closing unnecessary applications.")
    if health["memory"] > 85:
        insights.append("🔴 Critical memory usage. Consider restarting your system.")
    elif health["memory"] > 70:
        insights.append("⚠️ Memory usage is high. Close some applications.")
    if health["disk"] > 90:
        insights.append("🔴 Disk space critically low! Delete files or clean up.")
    elif health["disk"] > 80:
        insights.append("⚠️ Disk space is running low.")
    
    if health["status"] == "HEALTHY":
        insights.append("✅ Your system is running smoothly!")
    
    return {
        "health": health,
        "system_info": system_info,
        "insights": insights,
        "recommendations": get_smart_recommendations(health, system_info)
    }

@router.get("/quick-actions")
async def get_quick_actions():
    return [
        {"id": 1, "label": "🔍 Run Full Scan", "action": "scan", "description": "Scan files for threats"},
        {"id": 2, "label": "⚙️ Analyze Processes", "action": "processes", "description": "View active processes"},
        {"id": 3, "label": "📊 View System Info", "action": "info", "description": "System information"},
        {"id": 4, "label": "💚 Check Health", "action": "health", "description": "System health status"},
        {"id": 5, "label": "🚨 View Alerts", "action": "alerts", "description": "Security alerts"},
        {"id": 6, "label": "📈 View Analytics", "action": "analytics", "description": "System analytics"}
    ]

@router.get("/status")
async def get_assistant_status():
    """Check AI assistant status and capabilities"""
    groq_status = "available" if GROQ_AVAILABLE else "not_available"
    groq_key_set = bool(os.getenv('GROQ_API_KEY'))

    return {
        "status": "operational",
        "groq_api": groq_status,
        "groq_key_configured": groq_key_set,
        "local_ai": "available",
        "conversations_count": len(conversations),
        "last_activity": conversations[-1]["timestamp"] if conversations else None
    }
