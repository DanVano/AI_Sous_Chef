import json
import os

SUB_FILE = os.path.join("recipes", "substitutions.json")

def load_substitutions():
    if not os.path.exists(SUB_FILE):
        return {}
    with open(SUB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_substitutes(ingredient):
    substitutions = load_substitutions()
    return substitutions.get(ingredient.lower(), [])