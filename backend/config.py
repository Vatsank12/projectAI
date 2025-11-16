from pathlib import Path
import os

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment variables from {env_path}")
    else:
        print("⚠️  No .env file found, using system environment variables")
except ImportError:
    print("⚠️  python-dotenv not installed, using system environment variables only")

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
BACKEND_DIR = BASE_DIR / "backend"

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))

ALLOWED_HOSTS = ["*"] if DEBUG else ["localhost", "127.0.0.1"]

DATABASE_URL = BACKEND_DIR / "vigilant_ai.db"

ALERT_THRESHOLDS = {
    "cpu": 80,
    "memory": 85,
    "disk": 90,
    "temperature": 85
}

MONITORING_INTERVAL = 1

MAX_FILE_SIZE = 100 * 1024 * 1024

METRIC_HISTORY_LIMIT = 60
