from ai.chatgpt_api import get_chatgpt_response 
from ai.intent_parser import parse_intent
from ai.local_assistant import LocalAssistant
from handlers.side_dish_recommender import suggest_side_dishes
from storage.pantry import get_fresh_items
from storage.persistent_storage import save_favorite, log_recipe_usage
from utils.audio_utils import capture_command, debounce_command
from utils.conversion_utils import extract_ratin
from utils.logger import log_event
from voice.tts import speak
from voice.wake_word import record_audio
from voice.whisper_stt import transcribe_audio

local_ai = LocalAssistant()

def find_step_by_keyword(steps, user_text):
    lowered = user_text.lower()
    for i, step in enumerate(steps):
        if any(word in step.lower() for word in lowered.split()):
            return i
    return None

def handle_ai_fallback(prompt):
    response = local_ai.get_response(prompt)
    fallback_triggers = ["i'm not sure", "unknown", "confused", "no idea", "can't help"]
    if any(trigger in response.lower() for trigger in fallback_triggers):
        response = get_chatgpt_response(prompt)
        log_event("ai", f"ChatGPT fallback used: {prompt} -> {response}")
    else:
        log_event("ai", f"LocalAssistant handled: {prompt} -> {response}")
    speak(response)

def handle_find_recipe(profile):
    ingredients_list = listen_for_ingredients()
    options = filter_recipes(ingredients_list, profile)
    if not options:
        speak("Sorry, I couldn't find any recipes with those ingredients.")
        return
    fresh, stale = get_fresh_items()
    for item, days in stale:
        if days == 3:
            speak(f"{item.capitalize()} may start to spoil. Recommended to cook today.")
    speak("Here are some recipes you could try:")
    for idx, recipe in enumerate(options, 1):
        speak(f"{idx}. {recipe['name']}")
    print("Options: ")
    for idx, recipe in enumerate(options, 1):
        print(f"{idx}: {recipe['name']}")
    speak("Which recipe do you want to start? Please say the name or number.")
    audio_path = "recipe_choice.wav"
    record_audio(audio_path, record_seconds=4)
    selection = transcribe_audio(audio_path)
    log_event("input", f"Recipe choice: {selection}")
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

def handle_power_search(profile):
    speak("Tell me the main ingredients you have. Please say them separated by and or commas.")
    audio_path = "power_search_ingredients.wav"
    record_audio(audio_path, record_seconds=7)
    user_text = transcribe_audio(audio_path)
    log_event("input", f"Power search ingredients: {user_text}")
    if not user_text or len(user_text.split()) < 2:
        speak("I didn't catch enough ingredients. Please try again.")
        return
    user_text = user_text.replace(" and ", ", ")
    ingredients_list = [i.strip() for i in user_text.split(",") if i.strip()]
    options = filter_recipes(ingredients_list, profile)
    if not options or len(options) < 3:
        restrictions = f"Allergies: {', '.join(profile.get('allergies', []))}. " \
                       f"Diet: {profile.get('diet', 'None')}. " \
                       f"Restrictions: {', '.join(profile.get('restrictions', []))}. " \
                       f"Skill level: {profile.get('skill', 'unknown')}."
        gpt_prompt = (
            f"User has the following main ingredients: {', '.join(ingredients_list)}. "
            f"{restrictions} Suggest 3 popular home-cooking recipes they can make, even if not all ingredients match. "
            "Return only the recipe name and a one-line description for each, in this format: "
            "1. Recipe Name: Description."
        )
        chatgpt_results = handle_ai_fallback(gpt_prompt)
        log_event("ai", f"ChatGPT power search: {gpt_prompt}\nResponse: {chatgpt_results}")
        speak("Here are some recipes I found:")
        for line in chatgpt_results.split("\n"):
            if line.strip():
                speak(line.strip())
        return
    fresh, stale = get_fresh_items()
    for item, days in stale:
        if days == 3:
            speak(f"{item.capitalize()} may start to spoil. Recommended to cook today.")
    speak("Here are some recipes you can try:")
    for idx, recipe in enumerate(options[:3], 1):
        speak(f"{idx}. {recipe['name']}")
        log_event("output", f"Local recipe option: {recipe['name']}")

def find_step_by_keyword(steps, user_text):
    lowered = user_text.lower()
    for i, step in enumerate(steps):
        if any(word in step.lower() for word in lowered.split()):
            return i
    return None

def session_recipe_navigation(recipe, resume_step=0):
    steps = recipe.get("steps", [])
    if not steps:
        speak("This recipe has no steps.")
        return

    current_index = resume_step

    while current_index < len(steps):
        step = steps[current_index]
        step_num = current_index + 1
        speak(f"Step {step_num}: {step}")
        log_event("recipe_step", f"Step {step_num}: {step}")

        while True:
            speak("Say 'next', 'repeat', 'back', 'pause', or 'go to step'.")
            step_cmd = capture_command("step_cmd.wav", "Say 'next', 'repeat', 'back', or a step.")
            if not debounce_command(step_cmd):
                speak("Duplicate command detected. Ignoring.")
                continue
            log_event("step_command", step_cmd)

            command = parse_intent(step_cmd)

            if command == "next_step":
                current_index += 1
                break
            elif command == "repeat_step":
                speak(f"Repeating Step {step_num}: {step}")
            elif command == "previous_step":
                if current_index > 0:
                    current_index -= 1
                    break
                else:
                    speak("You're already at the first step.")
            elif command == "pause":
                speak("Paused. Say resume when ready.")
                while True:
                    record_audio("resume_cmd.wav", record_seconds=2)
                    resume_cmd = transcribe_audio("resume_cmd.wav").lower()
                    if "resume" in resume_cmd or "continue" in resume_cmd:
                        speak("Resuming.")
                        break
            elif command == "rate":
                rating = extract_rating(step_cmd)
                if rating:
                    save_favorite(recipe, rating=rating)
                    speak(f"Recipe rated {rating} stars and saved.")
                    log_event("user_action", f"Recipe rated {rating}")
                else:
                    speak("Please say a number from one to five stars.")
            elif command == "favorite":
                save_favorite(recipe)
                speak("Recipe saved to favorites.")
                log_event("user_action", "Recipe favorited")
            elif command == "exit":
                speak("Exiting the recipe.")
                log_event("system", "Recipe navigation exited")
                return
            elif command == "main_menu":
                speak("Returning to main menu.")
                log_event("system", "User returned to main menu")
                return
            elif command == "current_step":
                speak(f"You are on step {step_num}.")
            elif command == "total_steps":
                speak(f"This recipe has {len(steps)} steps.")
            elif command == "list_all_steps":
                for i, s in enumerate(steps, 1):
                    speak(f"Step {i}: {s}")
            elif command == "summarize_steps":
                speak("Here's a summary of the steps:")
                for i, s in enumerate(steps, 1):
                    speak(f"Step {i}: {s}")
            elif command == "suggest_side":
                suggest_side_dishes(recipe)     
            elif command == "recap_recipe":
                speak(f"You are making {recipe.get('name', 'a recipe')}.")
                if recipe.get("ingredients"):
                    speak("Ingredients include:")
                    speak(", ".join(recipe["ingredients"]))
                    speak(f"This recipe has {len(steps)} steps.")
            elif command == "describe_step":
                speak(step)
            elif command == "list_ingredients":
                speak("The ingredients for this recipe are:")
                speak(", ".join(recipe.get("ingredients", [])))
            elif command == "set_timer":
                seconds = extract_timer_seconds(step_cmd)
                if seconds:
                    set_timer(seconds)
                else:
                    speak("Please say a timer like 'set a timer for 5 minutes'.")
            elif command == "unknown":
                # Handle jump to step by number or keyword
                if "step" in step_cmd:
                    for word in step_cmd.split():
                        if word.isdigit():
                            target = int(word) - 1
                            if 0 <= target < len(steps):
                                current_index = target
                                speak(f"Jumping to step {target + 1}.")
                                break
                    else:
                        speak("Please say a step number like 'step 2'.")
                        continue
                    break
                elif any(x in step_cmd for x in ["go to", "jump to", "take me to"]):
                    match = find_step_by_keyword(steps, step_cmd)
                    if match is not None:
                        current_index = match
                        speak(f"Jumping to step {match + 1}.")
                        break
                    else:
                        speak("I couldn't find a matching step.")
                else:
                    speak("Sorry, I didn’t catch that. Say next, repeat, back, pause, or step number.")
            else:
                speak("Sorry, I didn’t catch that. Say next, repeat, back, pause, or step number.")

    log_recipe_usage(recipe.get("name", "unknown"), step_events=len(steps), repeated_steps=repeats)
    # Post-recipe save prompt
    speak("Would you like to save this recipe?")
    response = capture_command("save_recipe.wav", "Would you like to save this recipe?")
    if "yes" in response or "save" in response or "favorite" in response:
        save_favorite(recipe)
        speak("Recipe saved.")
    else:
        speak("Okay, not saving the recipe.")


def handle_start_recipe():
    speak("What recipe do you want to cook?")
    audio_path = "start_recipe.wav"
    record_audio(audio_path, record_seconds=4)
    recipe_name = transcribe_audio(audio_path)
    log_event("input", f"Start recipe: {recipe_name}")
    recipe = get_recipe_by_name(recipe_name)
    if recipe:
        speak(f"Let's start {recipe['name']}. Say 'next step' to begin.")
        save_last_recipe(recipe)
        session_recipe_navigation(recipe)
    else:
        speak("Recipe not found.")

