from ai.intent_parser import parse_intent
from ai.local_assistant import LocalAssistant
from ai.chatgpt_api import get_chatgpt_response
from voice.tts import speak
from voice.wake_word import listen_for_wake_word, record_audio
from voice.whisper_stt import transcribe_audio
from storage.persistent_storage import load_user_profile
from storage.session_storage import save_session_transcription
from utils.logger import log_event
from onboarding_script import onboarding_flow
from handlers.recipe_flow import handle_find_recipe, handle_start_recipe, handle_power_search, session_recipe_navigation
from handlers.profile_flow import handle_show_favorites, handle_last_recipe, handle_shopping_list

local_ai = LocalAssistant()

def handle_ai_fallback(prompt):
    response = local_ai.get_response(prompt)
    fallback_triggers = ["i'm not sure", "unknown", "confused", "no idea", "can't help"]
    if any(trigger in response.lower() for trigger in fallback_triggers):
        response = get_chatgpt_response(prompt)
        log_event("ai", f"ChatGPT fallback used: {prompt} -> {response}")
    else:
        log_event("ai", f"LocalAssistant handled: {prompt} -> {response}")
    speak(response)

def main_menu():
    options = (
        "Main Menu: Say or select - Find a recipe, Start a recipe, Power search, "
        "User settings, Show my favorites, Last recipe I made, Shopping list, Help, Exit, Pause"
    )
    speak(options)
    print(options)

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
            record_audio("main_cmd.wav", record_seconds=4)
            user_text = transcribe_audio("main_cmd.wav")
            log_event("input", f"Main menu command: {user_text}")
            save_session_transcription(user_text)

            command = parse_intent(user_text)
            print(f"Intent: {command}")

            if command == "main_menu":
                main_menu()
            elif command == "find_recipe":
                handle_find_recipe(profile)
            elif command == "power_search":
                handle_power_search(profile)
            elif command == "start_recipe":
                handle_start_recipe()
            elif command == "user_settings":
                onboarding_flow()
                profile = load_user_profile()
            elif command == "help":
                speak("Commands: Main Menu, Find Recipe, Start Recipe, Power Search, User Settings, Show my favorites, Last recipe I made, Shopping list, Help, Next Step, Previous Step, Repeat Step, Substitute ingredient, Favorite, Rate, Exit, Pause.")
            elif command == "favorite":
                handle_show_favorites()
            elif command == "last_recipe":
                handle_last_recipe()
            elif command == "show_shopping":
                handle_shopping_list()
            elif command == "clear_shopping":
                from storage.shopping_list import clear_shopping_list
                clear_shopping_list()
                speak("Shopping list cleared.")
            elif command == "exit":
                speak("Goodbye!")
                log_event("system", "User exited main menu.")
                break
            elif command == "pause":
                speak("Pausing. Say resume or continue when you are ready.")
                log_event("system", "User paused at main menu.")
                while True:
                    record_audio("pause_cmd.wav", record_seconds=3)
                    pause_cmd = transcribe_audio("pause_cmd.wav")
                    if pause_cmd and ("resume" in pause_cmd.lower() or "continue" in pause_cmd.lower()):
                        speak("Resuming.")
                        log_event("system", "User resumed from main menu pause.")
                        break
                    else:
                        speak("Still paused. Say resume or continue when ready.")
            elif command in ("next_step", "previous_step", "repeat_step"):
                speak(f"{command.replace('_', ' ').capitalize()} command not implemented here.")
            elif command == "unknown":
                if user_text.strip():
                    speak("Let me think about that...")
                    handle_ai_fallback(user_text)
                else:
                    speak("Selection error. Please try again.")
                    log_event("error", "Selection error at main menu")
            else:
                speak("Selection error. Please try again.")
                log_event("error", f"Selection error: {user_text}")

if __name__ == "__main__":
    main()
