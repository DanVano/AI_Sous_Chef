from ai.chatgpt_api import get_chatgpt_response
from recipes.recipe_manager import filter_recipes, prioritize_by_pantry, smart_recipe_picker
from storage.pantry import get_fresh_items
from storage.persistent_storage import load_user_profile
from storage.shopping_list import add_to_shopping_list
from utils.logger import log_event
from voice.tts import speak

def suggest_meal_plan():
    profile = load_user_profile()
    speak("Building a meal plan for the week using deals, pantry, and your preferences.")

    # Use pantry freshness
    fresh, _ = get_fresh_items()
    pantry_items = [item for item, _ in fresh]

    # Get 6–9 best-fit recipes using all sources
    plan = smart_recipe_picker(profile, pantry_items)

    if not plan:
        speak("Sorry, I couldn't find enough recipes for planning.")
        return

    speak("Here’s your 3-day meal plan:")
    for i, r in enumerate(plan, 1):
        speak(f"{i}. {r['name']}")
        log_event("meal_plan", r["name"])

    # Auto-add all ingredients to shopping list
    all_ingredients = []
    for r in plan:
        all_ingredients.extend(r["ingredients"])

    for item in set(all_ingredients):
        add_to_shopping_list(item)

    speak("I've added the ingredients to your shopping list for easier bulk shopping.")