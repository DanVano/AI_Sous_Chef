import json
import os
from datetime import datetime, timedelta

PANTRY_FILE = os.path.join("storage", "pantry.json")

def load_pantry():
    if not os.path.exists(PANTRY_FILE):
        return {}
    with open(PANTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_pantry(pantry):
    with open(PANTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(pantry, f, indent=2)

def add_to_pantry(item):
    pantry = load_pantry()
    pantry[item.lower()] = datetime.now().isoformat()
    save_pantry(pantry)

def clear_pantry():
    save_pantry({})

def get_fresh_items(days_fresh=3):
    pantry = load_pantry()
    fresh = []
    stale = []
    now = datetime.now()
    for item, iso_date in pantry.items():
        added = datetime.fromisoformat(iso_date)
        days_old = (now - added).days
        if days_old <= days_fresh:
            fresh.append((item, days_old))
        else:
            stale.append((item, days_old))
    return fresh, stale