##  App controller; starts/stops sessions, routes logic to modules.



import time
from ai.intent_parser import parse_intent
from ai.chatgpt_api import get_chatgpt_response
from storage.persistent_storage import save_user_profile, load_user_profile
from voice.tts import speak
from voice.whisper_stt import transcribe_audio
from voice.wake_word import listen_for_wake_word, record_audio
from storage.session_storage import save_session_transcription
from recipes.recipe_manager import filter_recipes, get_recipe_by_name, substitute_ingredient

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
    options = "Main Menu: Say or select - Find a recipe, Start a recipe, User settings, Help"
    speak(options)
    print(options)

def handle_find_recipe(profile):
    speak("What main ingredients do you have in your kitchen?")
    ingredients = input("Enter ingredients (comma separated): ")
    ingredients_list = [i.strip() for i in ingredients.split(",") if i.strip()]
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
    # Optionally: let user choose one
    selection = input("Which recipe do you want to start? Enter number or name: ")
    chosen = None
    try:
        idx = int(selection)
        if 1 <= idx <= len(options):
            chosen = options[idx - 1]
    except ValueError:
        # Not a number, treat as name
        for recipe in options:
            if selection.lower() in recipe["name"].lower():
                chosen = recipe
                break
    if chosen:
        speak(f"Great! Let's start {chosen['name']}. Say 'next step' to begin.")
        session_recipe_navigation(chosen)
    else:
        speak("Recipe selection error.")

def session_recipe_navigation(recipe):
    steps = recipe["steps"]
    current = 0
    while True:
        speak(f"Step {current + 1}: {steps[current]}")
        user_text = input("Say 'next step', 'repeat', 'previous', or 'substitute [ingredient]': ")
        command = parse_intent(user_text)
        if command == "next_step":
            if current < len(steps) - 1:
                current += 1
            else:
                speak("You have completed the recipe. Enjoy your meal!")
                break
        elif command == "repeat_step":
            continue
        elif command == "previous_step":
            if current > 0:
                current -= 1
        elif command == "substitute":
            # Get the ingredient to substitute and new ingredient
            parts = user_text.lower().split("substitute")
            if len(parts) > 1:
                args = parts[1].strip().split(" with ")
                if len(args) == 2:
                    old, new = args
                    recipe = substitute_ingredient(recipe, old.strip(), new.strip())
                    speak(f"Substituted {old} with {new}.")
        elif command == "main_menu":
            break
        else:
            speak("Command not recognized.")

def handle_start_recipe():
    speak("What recipe do you want to cook?")
    recipe_name = input("Recipe name: ")
    recipe = get_recipe_by_name(recipe_name)
    if recipe:
        speak(f"Let's start {recipe['name']}. Say 'next step' to begin.")
        session_recipe_navigation(recipe)
    else:
        speak("Recipe not found.")

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
            audio_path = "audio.wav"
            record_audio(audio_path)
            user_text = transcribe_audio(audio_path)
            print(f"Transcribed: {user_text}")
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
                speak("Commands: Main Menu, Find Recipe, Start Recipe, User Settings, Help, Next Step, Previous Step, Repeat Step.")
            elif command in ("next_step", "previous_step", "repeat_step"):
                speak(f"{command.replace('_', ' ').capitalize()} command not implemented yet.")
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