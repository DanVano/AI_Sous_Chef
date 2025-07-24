from storage.persistent_storage import load_favorites, load_last_recipe
from voice.tts import speak
from handlers.recipe_flow import session_recipe_navigation
from storage.shopping_list import get_shopping_list

def handle_show_favorites():
    favorites = load_favorites()
    if not favorites:
        speak("You have no favorite recipes yet.")
        return
    speak("Your favorite recipes are:")
    for recipe, rating in favorites.items():
        if rating:
            speak(f"{recipe}, rated {rating} stars.")
        else:
            speak(recipe)

def handle_last_recipe():
    recipe = load_last_recipe()
    if recipe:
        speak(f"Your last recipe was {recipe['name']}. Say 'next step' to resume or 'main menu' to go back.")
        session_recipe_navigation(recipe)
    else:
        speak("No recent recipe found.")

def handle_shopping_list():
    lst = get_shopping_list()
    if lst:
        speak("Your shopping list items are:")
        for x in lst:
            speak(x)
    else:
        speak("Your shopping list is empty.")
