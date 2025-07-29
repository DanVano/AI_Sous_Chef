from ai.chatgpt_api import get_chatgpt_response
from recipes.recipe_manager import filter_recipes, prioritize_by_pantry
from storage.pantry import get_fresh_items
from storage.persistent_storage import load_user_profile
from storage.shopping_list import add_to_shopping_list
from utils.logger import log_event
from voice.tts import speak

def suggest_meal_plan():
    profile = load_user_profile()
    speak("Building a meal plan for the week using deals, pantry, and your preferences.")

    try:
        from utils.deal_finder import suggest_recipes_from_sales
        sale_recipes = suggest_recipes_from_sales()
    except Exception as e:
        log_event("error", f"Flipp deal finder failed: {e}")
        sale_recipes = []

    # Pull pantry items
    fresh, _ = get_fresh_items()
    pantry_ingredients = [item for item, _ in fresh]

    # Filter best local recipes
    local_matches = filter_recipes(pantry_ingredients, profile, num_options=12)
    local_matches = prioritize_by_pantry(local_matches)

    # Merge results: deals first, then pantry matches, then favorites
    plan = []
    seen = set()

    for group in [sale_recipes, local_matches]:
        for r in group:
            if r["name"] not in seen and len(plan) < 9:
                plan.append(r)
                seen.add(r["name"])

    if len(plan) < 9:
        from storage.persistent_storage import load_favorites
        favs = load_favorites()
        for rname, data in favs.items():
            if rname not in seen and len(plan) < 9:
                plan.append(data["recipe"])
                seen.add(rname)

    if not plan:
        speak("Sorry, I couldn't find enough recipes for planning.")
        return

    speak("Here’s your 3-day meal plan:")
    for i, r in enumerate(plan, 1):
        speak(f"{i}. {r['name']}")
        log_event("meal_plan", r["name"])

    # Auto-add ingredients to shopping list
    all_ingredients = []
    for r in plan:
        all_ingredients.extend(r["ingredients"])
    for item in set(all_ingredients):
        add_to_shopping_list(item)

    speak("I've added the ingredients to your shopping list for easier bulk shopping.")