# Logic for recipe storage, retrieval, and step handling

# Loads/stores recipes, splits into steps, handles current step state.

import json
import os

RECIPE_FILE = os.path.join("recipes", "recipes.json")

def load_recipes():
    if not os.path.exists(RECIPE_FILE):
        return []
    with open(RECIPE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def filter_recipes(ingredients, user_profile=None, num_options=5):
    recipes = load_recipes()
    if not recipes:
        return []

    # Lowercase for matching
    user_ingredients = set(i.strip().lower() for i in ingredients)
    filtered = []
    for recipe in recipes:
        rec_ingredients = set(i.lower() for i in recipe["ingredients"])
        # Score: how many user ingredients match recipe
        match_count = len(rec_ingredients & user_ingredients)
        dietary_ok = True
        if user_profile:
            # Check dietary restrictions
            diet = user_profile.get("diet", "")
            allergies = set(a.lower() for a in user_profile.get("allergies", []))
            restrictions = set(r.lower() for r in user_profile.get("restrictions", []))
            if diet == "vegan" and not "vegan" in recipe["tags"]:
                dietary_ok = False
            if diet == "vegetarian" and not ("vegetarian" in recipe["tags"] or "vegan" in recipe["tags"]):
                dietary_ok = False
            if allergies and (allergies & rec_ingredients):
                dietary_ok = False
            if restrictions:
                for r in restrictions:
                    if r in recipe["tags"]:
                        continue
                    else:
                        dietary_ok = False
        if match_count > 0 and dietary_ok:
            filtered.append((match_count, recipe))
    # Sort by # of matching ingredients (desc)
    filtered.sort(reverse=True, key=lambda tup: tup[0])
    # Return top N
    return [r for _, r in filtered[:num_options]]

def get_recipe_by_name(name):
    recipes = load_recipes()
    name = name.strip().lower()
    for recipe in recipes:
        if recipe["name"].lower() == name:
            return recipe
    return None

def substitute_ingredient(recipe, old_ingredient, new_ingredient):
    # Return a copy of recipe with substitution
    new_recipe = recipe.copy()
    new_ingredients = [new_ingredient if i.lower() == old_ingredient.lower() else i
                       for i in recipe["ingredients"]]
    new_recipe["ingredients"] = new_ingredients
    # Optionally: update steps if you want, for now keep as is
    return new_recipe