#  Figures out if user wants a step, a recipe, or gives a command ("next step", etc).
#  Detects if input is a navigation command or a chat query




COMMANDS = {
    "main_menu": ["main menu", "menu", "go to menu"],
    "find_recipe": ["find a recipe", "what can i make", "suggest recipe", "what should i cook"],
    "start_recipe": ["start a recipe", "begin recipe", "cook", "start cooking"],
    "user_settings": ["user settings", "settings", "profile", "preferences"],
    "help": ["help", "list commands"],
    "next_step": ["next step", "continue", "go next"],
    "previous_step": ["back a step", "previous step", "go back"],
    "repeat_step": ["repeat step", "say step again", "repeat"],
    "substitute": ["substitute", "replace"],
}

def parse_intent(user_text):
    user_text = user_text.lower().strip()
    for command, phrases in COMMANDS.items():
        for phrase in phrases:
            if phrase in user_text:
                return command
    return "unknown"