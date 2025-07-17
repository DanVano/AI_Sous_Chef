# Save/load recipes, user data as text/JSON

# Handles long-term saving/loading of recipes and user preferences (text/JSON files).


import json
import os

PROFILE_FILE = "storage/user_profile.json"
FAV_FILE = "storage/favorites.json"
LAST_RECIPE_FILE = "storage/last_recipe.json"

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
    if rating:
        favs[recipe['name']] = rating
    else:
        favs[recipe['name']] = None
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favs, f, indent=2)

def load_favorites():
    if not os.path.exists(FAV_FILE):
        return {}
    with open(FAV_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_last_recipe(recipe):
    with open(LAST_RECIPE_FILE, "w", encoding="utf-8") as f:
        json.dump(recipe, f, indent=2)

def load_last_recipe():
    if not os.path.exists(LAST_RECIPE_FILE):
        return None
    with open(LAST_RECIPE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)