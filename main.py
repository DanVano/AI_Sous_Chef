import time
from ai.intent_parser import parse_intent, extract_timer_seconds
from ai.chatgpt_api import get_chatgpt_response
from storage.persistent_storage import save_user_profile, load_user_profile, save_favorite, load_favorites, save_last_recipe, load_last_recipe
from voice.tts import speak
from voice.whisper_stt import transcribe_audio
from voice.wake_word import listen_for_wake_word, record_audio
from storage.session_storage import save_session_transcription
from recipes.recipe_manager import filter_recipes, get_recipe_by_name, substitute_ingredient
from recipes.substitutions import get_substitutes
from utils.timer import set_timer
from storage.shopping_list import add_to_shopping_list, get_shopping_list, clear_shopping_list

def ask_and_save_user_settings():
    profile = load_user_profile()
    speak("Let's set up your user profile.")
    allergies = input("Do you have any allergies? (comma separated, or none): ")
    diet = input("Are you vegan, vegetarian, or meat eater? (choose one): ")
    restrictions = input("Do you have any dietary restrictions like gluten-free, keto, nut-free, etc? (comma separated, or none): ")
    skill = input("How would you rank your cooking skill? (eggs only, beginner, intermediate, confident homecook, great homecook): ")

    if diet.lower() == "meat eater":
        meats = input("What types of meat do you eat? (comma separated): ")
        profile["meats"] = [m.strip() for m in meats.split(",")]

    cuisines = input("What cuisines do you like? (comma separated): ")

    profile["allergies"] = [a.strip() for a in allergies.split(",") if a.strip()]
    profile["diet"] = diet.lower()
    profile["restrictions"] = [r.strip() for r in restrictions.split(",") if r.strip()]
    profile["skill"] = skill
    profile["cuisines"] = [c.strip() for c in cuisines.split(",") if c.strip()]
    save_user_profile(profile)
    speak("Your preferences have been saved.")

def main_menu():
    options = (
        "Main Menu: Say or select - Find a recipe, Start a recipe, "
        "User settings, Show my favorites, Last recipe I made, Help"
    )
    speak(options)
    print(options)

def listen_for_ingredients():
    speak("Listening for your ingredients. Please say them clearly, separated by and or commas.")
    audio_path = "ingredients.wav"
    record_audio(audio_path, record_seconds=7)
    user_text = transcribe_audio(audio_path)
    print(f"Ingredients heard: {user_text}")
    save_session_transcription(user_text)
    # Split by 'and' or ',' for more natural phrasing
    user_text = user_text.replace(" and ", ", ")
    ingredients_list = [i.strip() for i in user_text.split(",") if i.strip()]
    return ingredients_list

def handle_find_recipe(profile):
    # No need to prompt, just listen for ingredients after intent detected
    ingredients_list = listen_for_ingredients()
    options = filter_recipes(ingredients_list, profile)
    if not options:
        speak("Sorry, I couldn't find any recipes with those ingredients.")
        return
    speak("Here are some recipes you could try:")
    for idx, recipe in enumerate(options, 1):
        speak(f"{idx}. {recipe['name']}")
    print("Options: ")
    for idx, recipe in enumerate(options, 1):
        print(f"{idx}: {recipe['name']}")
    # Listen for user choice
    speak("Which recipe do you want to start? Please say the name or number.")
    audio_path = "recipe_choice.wav"
    record_audio(audio_path, record_seconds=4)
    selection = transcribe_audio(audio_path)
    print(f"Recipe choice heard: {selection}")
    chosen = None
    try:
        idx = int(selection)
        if 1 <= idx <= len(options):
            chosen = options[idx - 1]
    except ValueError:
        for recipe in options:
            if selection.lower() in recipe["name"].lower():
                chosen = recipe
                break
    if chosen:
        speak(f"Great! Let's start {chosen['name']}. Say 'next step' to begin.")
        save_last_recipe(chosen)
        session_recipe_navigation(chosen)
    else:
        speak("Recipe selection error.")

def is_unclear(text):
    # Too short or silence
    if not text or len(text.strip()) < 3:
        return "unclear"
    # Heuristic: very few words
    if len(text.split()) < 2:
        return "repeat"
    # If text is mostly garbage (not matching any known command)
    return None

# In your main while loop, after transcribe_audio:
uncertainty = is_unclear(user_text)
if uncertainty == "unclear":
    speak("Sorry, I didn't catch that. Please repeat your command.")
    continue
elif uncertainty == "repeat":
    speak("Could you say that again, more clearly?")
    continue

# ...then proceed to parse_intent and handle as normal...

# If parse_intent returns 'unknown' and your transcription is plausible:
if command == "unknown":
    speak("I'm not sure what you meant. Can you rephrase or clarify?")
    # Listen again
    audio_path = "clarify_cmd.wav"
    record_audio(audio_path, record_seconds=3)
    clarify_text = transcribe_audio(audio_path)
    # Try again:
    command = parse_intent(clarify_text)
    if command == "unknown":
        # Use ChatGPT as fallback
        speak("Let me see if AI can help.")
        ai_response = get_chatgpt_response(clarify_text)
        speak(ai_response)
        continue
    else:
        user_text = clarify_text  # Continue as usual with new text

def session_recipe_navigation(recipe):
    steps = recipe["steps"]
    current = 0
    while True:
        speak(f"Step {current + 1}: {steps[current]}")
        audio_path = "step_cmd.wav"
        record_audio(audio_path, record_seconds=3)
        user_text = transcribe_audio(audio_path)
        print(f"Step command heard: {user_text}")

        uncertainty = is_unclear(user_text)
        if uncertainty == "unclear":
            speak("Sorry, I didn't catch that. Please repeat your command.")
            continue
        elif uncertainty == "repeat":
            speak("Could you say that again, more clearly?")
            continue

        command = parse_intent(user_text)

        # Clarification & fallback
        if command == "unknown":
            speak("I'm not sure what you meant. Can you rephrase or clarify?")
            audio_path = "clarify_cmd.wav"
            record_audio(audio_path, record_seconds=3)
            clarify_text = transcribe_audio(audio_path)
            print(f"Clarify command heard: {clarify_text}")
            if is_unclear(clarify_text):
                # If still unclear, try Whisper API fallback (just re-transcribe) or skip
                speak("Sorry, I still didn't catch that. Please try again.")
                continue
            command = parse_intent(clarify_text)
            if command == "unknown":
                speak("Let me see if AI can help.")
                ai_response = get_chatgpt_response(clarify_text)
                speak(ai_response)
                continue
            else:
                user_text = clarify_text

        if command == "next_step":
            if current < len(steps) - 1:
                current += 1
            else:
                speak("You have completed the recipe. Enjoy your meal!")
                save_last_recipe(recipe)
                break
        elif command == "repeat_step":
            continue
        elif command == "previous_step":
            if current > 0:
                current -= 1
        elif command == "substitute":
            old, new = extract_substitute_ingredients(user_text)
            if old and not new:
                subs = get_substitutes(old)
                if subs:
                    speak(f"Possible substitutes for {old} are: {', '.join(subs)}.")
                else:
                    speak(f"No local substitute for {old}. Asking AI for ideas.")
                    suggestion = get_chatgpt_response(
                        f"What is a good substitute for {old} in {recipe['name']}?"
                    )
                    speak(suggestion)
            elif old and new:
                if old.lower() in [i.lower() for i in recipe["ingredients"]]:
                    recipe = substitute_ingredient(recipe, old, new)
                    speak(f"Substituted {old} with {new}.")
                else:
                    speak(f"No local substitution for {old}. Asking AI for ideas.")
                    suggestion = get_chatgpt_response(
                        f"What is a good substitute for {old} in {recipe['name']}?"
                    )
                    speak(suggestion)
            else:
                speak("Sorry, I couldn't understand which ingredient to substitute.")
        elif command == "main_menu":
            break
        elif command == "favorite":
            save_favorite(recipe)
            speak("Recipe saved to favorites.")
        elif command == "rate":
            rating = extract_rating(user_text)
            if rating:
                save_favorite(recipe, rating=rating)
                speak(f"Recipe rated {rating} stars and saved.")
            else:
                speak("Please say a rating from one to five stars.")
        elif command == "list_ingredients":
            speak("The ingredients for this recipe are:")
            speak(", ".join(recipe["ingredients"]))
        elif command == "list_all_steps":
            for i, step in enumerate(recipe["steps"], 1):
                speak(f"Step {i}: {step}")
        elif command == "current_step":
            speak(f"You are on step {current + 1}.")
        elif command == "total_steps":
            speak(f"This recipe has {len(steps)} steps.")
        elif command == "describe_step":
            speak(steps[current])
        elif command == "set_timer":
            seconds = extract_timer_seconds(user_text)
            if seconds:
                set_timer(seconds)
            else:
                speak("I didn't understand the timer length. Please say, for example, 'set a timer for 5 minutes'.")
        elif command == "add_shopping":
            item = user_text.replace("add to shopping list", "").replace("add to list", "").strip()
            if not item:
                speak("What would you like to add to your shopping list?")
                audio_path = "add_shopping.wav"
                record_audio(audio_path, record_seconds=3)
                item = transcribe_audio(audio_path)
            add_to_shopping_list(item)
            speak(f"{item} added to your shopping list.")
        elif command == "show_shopping":
            lst = get_shopping_list()
            if lst:
                speak("Your shopping list items are:")
                for x in lst:
                    speak(x)
            else:
                speak("Your shopping list is empty.")
        elif command == "clear_shopping":
            clear_shopping_list()
            speak("Shopping list cleared.")
        else:
            speak("Command not recognized.")

def extract_substitute_ingredients(text):
    text = text.lower()
    if "substitute" in text:
        after = text.split("substitute")[1].strip()
        if "with" in after:
            old, new = after.split("with")
            return old.strip(), new.strip()
        return after.strip(), None  # Only 'substitute eggs'
    return None, None

def extract_rating(text):
    for word in text.split():
        if word.isdigit() and 1 <= int(word) <= 5:
            return int(word)
    return None



def handle_start_recipe():
    speak("What recipe do you want to cook?")
    audio_path = "start_recipe.wav"
    record_audio(audio_path, record_seconds=4)
    recipe_name = transcribe_audio(audio_path)
    recipe = get_recipe_by_name(recipe_name)
    if recipe:
        speak(f"Let's start {recipe['name']}. Say 'next step' to begin.")
        save_last_recipe(recipe)
        session_recipe_navigation(recipe)
    else:
        speak("Recipe not found.")

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

def main():
    print("App started. Say 'Hey Chef' to begin...")
    profile = load_user_profile()
    first_run = not bool(profile)
    while True:
        if first_run:
            speak("Welcome to AI Chef!")
            main_menu()
            first_run = False
        else:
            main_menu()

        if listen_for_wake_word():
            speak("Ready!")
            audio_path = "main_cmd.wav"
            record_audio(audio_path, record_seconds=4)
            user_text = transcribe_audio(audio_path)
            print(f"Command heard: {user_text}")
            save_session_transcription(user_text)

            command = parse_intent(user_text)
            print(f"Intent: {command}")

            if command == "main_menu":
                main_menu()
            elif command == "find_recipe":
                handle_find_recipe(profile)
            elif command == "start_recipe":
                handle_start_recipe()
            elif command == "user_settings":
                ask_and_save_user_settings()
            elif command == "help":
                speak("Commands: Main Menu, Find Recipe, Start Recipe, User Settings, Show my favorites, Last recipe I made, Help, Next Step, Previous Step, Repeat Step, Substitute ingredient, Favorite, Rate.")
            elif command == "favorite":
                handle_show_favorites()
            elif command == "last_recipe":
                handle_last_recipe()
            elif command in ("next_step", "previous_step", "repeat_step"):
                speak(f"{command.replace('_', ' ').capitalize()} command not implemented here.")
            elif command == "unknown":
                if user_text.strip():
                    speak("Let me think about that...")
                    ai_response = get_chatgpt_response(user_text)
                    speak(ai_response)
                else:
                    speak("Selection error. Please try again.")
            else:
                speak("Selection error. Please try again.")

            print("Say 'Hey Chef' to begin again, or Ctrl+C to quit.")

if __name__ == "__main__":
    main()