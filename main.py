from ai.intent_parser import parse_intent
from ai.local_assistant import LocalAssistant
from ai.chatgpt_api import get_chatgpt_response
from handlers.dynamic_recipe_builder import generate_dynamic_recipe
from handlers.profile_flow import handle_show_favorites, handle_last_recipe, handle_shopping_list
from handlers.meal_planner import suggest_meal_plan
from handlers.recipe_flow import handle_find_recipe, handle_start_recipe, handle_power_search, session_recipe_navigation
from voice.tts import speak
from voice.wake_word import listen_for_wake_word, record_audio
from voice.whisper_stt import transcribe_audio
from storage.pantry import add_to_pantry, load_pantry, clear_pantry, get_fresh_items
from storage.persistent_storage import load_user_profile
from storage.session_storage import save_session_transcription
from storage.shopping_list import add_to_shopping_list
from utils.audio_utils import capture_command, capture_ingredient
from utils.convo_memory import recall
from utils.onboarding_script import onboarding_flow
from utils.logger import log_event



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
		fresh, stale = get_fresh_items()
		for item, days in stale:
			if days == 3:
				speak(f"Reminder: {item.capitalize()} may start to spoil. Consider using it today.")

		if not first_run:
			main_menu()

		if listen_for_wake_word():
			speak("Ready!")
			user_text = capture_command("main_cmd.wav", "How can I help you?")
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
					pause_cmd = capture_command("pause_cmd.wav", "Say resume or continue.")
					if pause_cmd and ("resume" in pause_cmd.lower() or "continue" in pause_cmd.lower()):
						speak("Resuming.")
						log_event("system", "User resumed from main menu pause.")
						break
					else:
						speak("Still paused. Say resume or continue when ready.")
			elif command in ("next_step", "previous_step", "repeat_step"):
				speak(f"{command.replace('_', ' ').capitalize()} command not implemented here.")
			elif command == "dynamic_recipe":
				generate_dynamic_recipe(profile)
			elif command == "add_pantry":
				items = capture_ingredient("add_pantry.wav", "What ingredients should I add to your pantry?")
				if items:
					for item in items:
						add_to_pantry(item)
					speak(f"{', '.join(items)} added to your pantry.")
				else:
					speak("I didn’t catch any ingredient to add.")
			elif command == "show_pantry":
					pantry = load_pantry()
					if pantry:
						speak("These items are in your pantry:")
						for item in pantry:
							speak(item)
					else:
						speak("Your pantry is empty.")
			elif command == "add_shopping":
				items = capture_ingredient("add_shop.wav", "What should I add to your shopping list?")
				if items:
					for item in items:
						add_to_shopping_list(item)
					speak(f"{', '.join(items)} added to your shopping list.")
				else:
					speak("I didn’t catch any item to add.")
			elif command == "clear_pantry":
				clear_pantry()
				speak("Pantry cleared.")
			elif command == "meal_plan":
				suggest_meal_plan()
			elif command == "repeat_last":
				speak(recall())
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
