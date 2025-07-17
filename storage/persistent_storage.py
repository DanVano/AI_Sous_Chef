# Save/load recipes, user data as text/JSON

# Handles long-term saving/loading of recipes and user preferences (text/JSON files).


import json
import os

PROFILE_FILE = "storage/user_profile.json"

def save_user_profile(profile):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)

def load_user_profile():
    if not os.path.exists(PROFILE_FILE):
        return {}
    with open(PROFILE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)