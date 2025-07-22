
from utils.user_profile_tools import clean_user_profile_input
from storage.persistent_storage import save_user_profile
from voice.tts import speak

def onboarding_flow():
    speak("Welcome to AI Chef! Let's get started with a quick setup.")
    profile = clean_user_profile_input()
    if not profile:
        speak("There was a problem with your input. Please try again.")
        return
    cuisines = input("What cuisines do you like? (e.g., Italian, Thai): ")
    skill = input("What is your cooking skill? (beginner, intermediate, confident): ")
    profile["cuisines"] = [c.strip().lower() for c in cuisines.split(",") if c.strip()]
    profile["skill"] = skill.strip()
    meats = input("What meats do you eat (if any)? (e.g., chicken, beef): ")
    profile["meats"] = [m.strip().lower() for m in meats.split(",") if m.strip()]
    profile["favorites"] = []
    save_user_profile(profile)
    speak("Thanks! Your preferences have been saved. You're ready to cook with AI Chef!")
