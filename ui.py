
import tkinter as tk
from tkinter import scrolledtext
from voice.tts import speak
from ai.intent_parser import parse_intent
from recipes.recipe_manager import get_recipe_by_name, load_recipes
from storage.persistent_storage import load_user_profile, save_last_recipe
from main import session_recipe_navigation

class AIChefGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chef - GUI Testing")
        self.profile = load_user_profile()
        self.current_recipe = None

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack(padx=10, pady=10)

        self.command_entry = tk.Entry(root, width=50)
        self.command_entry.pack(padx=10, pady=5)

        self.submit_button = tk.Button(root, text="Send Command", command=self.handle_command)
        self.submit_button.pack(pady=5)

        self.recipe_button = tk.Button(root, text="Start Test Recipe", command=self.load_test_recipe)
        self.recipe_button.pack(pady=5)

        self.output("Welcome to AI Chef (GUI Test Mode)")

    def output(self, text):
        self.text_area.insert(tk.END, f"{text}\n")
        self.text_area.see(tk.END)
        speak(text)

    def handle_command(self):
        user_input = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        if not user_input.strip():
            return
        self.output(f"You said: {user_input}")
        command = parse_intent(user_input)

        if command == "next_step" and self.current_recipe:
            self.output("Advancing to next step...")
            session_recipe_navigation(self.current_recipe)
        elif command == "help":
            self.output("Try commands like 'next step', 'start recipe', or click buttons below.")
        else:
            self.output(f"Command received: {command}")

    def load_test_recipe(self):
        recipes = load_recipes()
        if not recipes:
            self.output("No recipes available.")
            return
        self.current_recipe = recipes[0]
        save_last_recipe(self.current_recipe)
        self.output(f"Loaded recipe: {self.current_recipe['name']}")
        session_recipe_navigation(self.current_recipe)

if __name__ == "__main__":
    root = tk.Tk()
    app = AIChefGUI(root)
    root.mainloop()
