# handlers/dynamic_recipe_builder.py

from ai.chatgpt_api import get_chatgpt_response
from ai.local_assistant import LocalAssistant
from voice.tts import speak
from voice.wake_word import record_audio
from voice.whisper_stt import transcribe_audio
from storage.persistent_storage import save_last_recipe
from handlers.recipe_flow import session_recipe_navigation
from utils.logger import log_event
from utils.ingredient_matcher import match_ingredients_bulk

local_ai = LocalAssistant()

def generate_dynamic_recipe(profile):
    speak("Tell me the ingredients you have.")
    record_audio("dynamic_ingredients.wav", record_seconds=6)
    ingredient_text = transcribe_audio("dynamic_ingredients.wav")
    log_event("input", f"Dynamic ingredients: {ingredient_text}")

    if not ingredient_text:
        speak("I didn't catch any ingredients.")
        return

    ingredients = [i.strip() for i in ingredient_text.lower().replace(" and ", ", ").split(",") if i.strip()]
    matched = match_ingredients_bulk(ingredients)
    if not matched:
        speak("Sorry, I couldn't match any usable ingredients.")
        return

    diet = profile.get("diet", "none")
    allergies = profile.get("allergies", [])
    restriction_text = f"Diet: {diet}. Avoid: {', '.join(allergies)}." if allergies else f"Diet: {diet}."

    prompt = (
        f"Create a custom recipe using only these ingredients: {', '.join(matched)}. "
        f"{restriction_text} Return the result in this format:\n\n"
        f"Recipe Name:\nEstimated Time:\nIngredients:\nSteps:\nTags:"
    )

    response = local_ai.get_response(prompt)
    if any(x in response.lower() for x in ["not sure", "unknown", "can't help"]):
        response = get_chatgpt_response(prompt)

    log_event("ai", f"Generated dynamic recipe: {response}")
    parsed = parse_recipe_response(response)

    if not parsed:
        speak("Sorry, I couldn’t understand the recipe. Please try again.")
        return

    speak(f"Here is a custom recipe: {parsed['name']}. Say 'next' to begin.")
    save_last_recipe(parsed)
    session_recipe_navigation(parsed)

def parse_recipe_response(text):
    lines = text.strip().splitlines()
    recipe = {
        "name": "",
        "ingredients": [],
        "steps": [],
        "tags": []
    }

    for i, line in enumerate(lines):
        l = line.strip()
        if l.lower().startswith("recipe name"):
            recipe["name"] = l.split(":", 1)[1].strip()
        elif l.lower().startswith("estimated time"):
            continue
        elif l.lower().startswith("ingredients"):
            recipe["ingredients"] = [x.strip("- ").strip() for x in lines[i + 1:] if x.strip().startswith("-")]
        elif l.lower().startswith("steps"):
            steps_start = i + 1
            while steps_start < len(lines) and not lines[steps_start].strip().startswith("Tags"):
                step_line = lines[steps_start].strip()
                if step_line and any(char.isalpha() for char in step_line):
                    recipe["steps"].append(step_line.lstrip("1234567890. ").strip())
                steps_start += 1
        elif l.lower().startswith("tags"):
            recipe["tags"] = [x.strip().lower() for x in l.split(":", 1)[1].split(",")]

    if recipe["name"] and recipe["steps"]:
        return recipe
    return None
