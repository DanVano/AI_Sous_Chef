# Save/load recipes, user data as text/JSON

# Handles long-term saving/loading of recipes and user preferences (text/JSON files).


import json
import os

from datetime import datetime

STORAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "storage")
PROFILE_FILE = os.path.join(STORAGE_DIR, "user_profile.json")
FAV_FILE = os.path.join(STORAGE_DIR, "favorites.json")
LAST_RECIPE_FILE = os.path.join(STORAGE_DIR, "last_recipe.json")

def save_user_profile(profile):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)

def load_user_profile():
    if not os.path.exists(PROFILE_FILE):
        return {}
    with open(PROFILE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_favorite(recipe, rating=None):
    favs = load_favorites()
    entry = {
        "recipe": recipe,
        "rating": rating if isinstance(rating, int) and 1 <= rating <= 5 else None
    }
    favs[recipe["name"]] = entry
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favs, f, indent=2)

def load_favorites():
    if not os.path.exists(FAV_FILE):
        return {}

    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Validate structure
            cleaned = {}
            for k, v in data.items():
                if isinstance(v, dict) and "recipe" in v:
                    rating = v.get("rating")
                    if isinstance(rating, int) and 1 <= rating <= 5:
                        cleaned[k] = v
                    else:
                        cleaned[k] = {"recipe": v["recipe"], "rating": None}
                elif isinstance(v, str):  # legacy format
                    cleaned[k] = {"recipe": v, "rating": None}
            return cleaned
    except Exception as e:
        print(f"Favorites file error: {e}")
        return {}

def save_last_recipe(recipe):
    with open(LAST_RECIPE_FILE, "w", encoding="utf-8") as f:
        json.dump(recipe, f, indent=2)

def load_last_recipe():
    if not os.path.exists(LAST_RECIPE_FILE):
        return None
    with open(LAST_RECIPE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

HISTORY_FILE = os.path.join(STORAGE_DIR, "recipe_history.json")

def log_recipe_usage(recipe_name, step_events=0, repeated_steps=0):
    if not os.path.exists(HISTORY_FILE):
        history = {}
    else:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)

    entry = history.get(recipe_name, {"times_cooked": 0, "steps_repeated": 0, "steps_total": 0})
    entry["times_cooked"] += 1
    entry["steps_total"] += step_events
    entry["steps_repeated"] += repeated_steps
    history[recipe_name] = entry

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def load_recipe_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)