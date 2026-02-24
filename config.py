import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "db", "orders.db")
JSON_PATH = os.path.join(DATA_DIR, "orders.json")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Автоматическое создание директорий
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "process.log")