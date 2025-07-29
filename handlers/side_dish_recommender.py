from ai.chatgpt_api import get_chatgpt_response
from voice.tts import speak

def suggest_side_dishes(recipe):
    name = recipe.get("name", "this dish")
    ingredients = ", ".join(recipe.get("ingredients", []))

    prompt = (
        f"Suggest 2 or 3 simple side dishes that pair well with {name}. "
        f"The main dish includes: {ingredients}. "
        f"Respond in this format:\n1. Side dish name: Short description."
    )

    response = get_chatgpt_response(prompt)
    speak("Here are some side dishes you could serve with this:")
    for line in response.split("\n"):
        if line.strip():
            speak(line.strip())