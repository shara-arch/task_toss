import os
import json

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
STORAGE_FILE = os.path.join(DATA_DIR, "storage.json")

def initialize_storage():
    """Guarantees the storage file and data directory exist safely."""
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if not os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, "w") as f:
                json.dump({"users": {}, "projects": {}, "tasks": {}}, f, indent=4)
    except Exception as e:
        print(f"[Storage Error] Initialization failed: {e}")

def load_db() -> dict:
    """Reads and parses the raw JSON schema."""
    initialize_storage()
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
        # Graceful error fallback for malformed data
        return {"users": {}, "projects": {}, "tasks": {}}