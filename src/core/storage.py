import json
import os
from typing import Dict, Any, Optional
from src.core.schemas import UserProgress

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
PROGRESS_FILE = os.path.join(DATA_DIR, "user_progress.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_progress(progress: UserProgress):
    ensure_data_dir()
    with open(PROGRESS_FILE, "w") as f:
        f.write(progress.model_dump_json(indent=2))

def load_progress() -> UserProgress:
    ensure_data_dir()
    if not os.path.exists(PROGRESS_FILE):
        return UserProgress()
    
    try:
        with open(PROGRESS_FILE, "r") as f:
            data = json.load(f)
            return UserProgress(**data)
    except Exception:
        return UserProgress()

def save_settings(settings: Dict[str, Any]):
    ensure_data_dir()
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

def load_settings() -> Dict[str, Any]:
    ensure_data_dir()
    if not os.path.exists(SETTINGS_FILE):
        return {}
    
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}
