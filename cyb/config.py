import os
from pathlib import Path

# Base remote (production)
BASE_REMOTE = os.environ.get("CODEHOUSE_BASE", "https://cli.codehouse.cloud/cli")

# Public website endpoints (Django)
API_REGISTER_USER = f"{BASE_REMOTE}/cybersecurity/challenge/users"   # registration endpoint
API_LOGIN = f"{BASE_REMOTE}/api/login"
API_QUESTIONS = f"{BASE_REMOTE}/api/questions/cyb"
API_LOG = f"{BASE_REMOTE}/api/log_results"
API_TOP_USERS = f"{BASE_REMOTE}/api/top_users"  # endpoint to fetch top 20 users
API_VERIFY_TOKEN = f"{BASE_REMOTE}/cybersecurity/challenge/verify-token"  # endpoint to fetch top 20 users

# Local storage
LOCAL_DIR = Path.home() / ".codehouse_cyb"
LOCAL_DIR.mkdir(parents=True, exist_ok=True)
LOCAL_DB = LOCAL_DIR / "results.db"

# Behavior
MAX_LOGIN_ATTEMPTS = 5
SESSION_QUESTION_COUNT = 10
REMOTE_TIMEOUT = int(os.environ.get("REMOTE_TIMEOUT", 5))
TEMP_TOKEN_EXPIRY_SECONDS = 1200  # 20 minutes
