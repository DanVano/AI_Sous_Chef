#  Figures out if user wants a step, a recipe, or gives a command ("next step", etc).
#  Detects if input is a navigation command or a chat query




COMMANDS = {
    "main_menu": ["main menu", "menu", "go to menu"],
    "find_recipe": ["find a recipe", "what can i make", "suggest recipe", "what should i cook", "what can i cook today", "got anything with", "suggest a dish", "what’s for dinner"],
    "start_recipe": ["start a recipe", "begin recipe", "cook", "start cooking", "let's get cooking", "begin the recipe", "i'm ready to cook", "start now"],
    "user_settings": ["user settings", "settings", "profile", "preferences"],
    "help": ["help", "list commands"],
    "next_step": ["next step", "continue", "go next", "what's next", "what is next", "what’s next", "okay next", "keep going", "what now", "move on", "next part"],
    "previous_step": ["back a step", "previous step", "go back", "last step", "last part", "what did i just miss", "rewind that"],
    "repeat_step": ["repeat step", "say step again", "repeat", "repeat that", "repeat that please", "can you say that again", "say that again", "pardon", "what was that"],
    "substitute": ["substitute", "replace"],
    "favorite": ["favorite", "save to favorites"],
    "rate": ["rate", "stars"],
    "last_recipe": ["last recipe", "recent recipe", "resume last", "continue last"],
    "show_favorites": ["show my favorites", "favorites", "list favorites"],
    "list_ingredients": ["list ingredients", "what are the ingredients", "ingredients"],
    "list_all_steps": ["repeat all steps", "list all steps", "read all steps"],
    "current_step": [ "what step am i on", "current step", "step number", "what step am i at", "where am i", "what’s happening now"],
    "total_steps": ["how many steps", "number of steps", "how long is this recipe", "how many steps are there", "is this a long recipe"],
    "describe_step": ["describe this step", "explain this step", "more detail", "what does that mean", "elaborate please", "explain that"],
    "set_timer": ["set a timer", "start a timer", "timer for", "remind me in", "can you set a timer", "countdown"],
    "add_shopping": ["add to shopping list", "add to list", "shopping list"],
    "show_shopping": ["show shopping list", "what's on my shopping list", "read shopping list"],
    "clear_shopping": ["clear shopping list", "empty shopping list"],
    "power_search": ["what can i cook with", "what should i cook with", "recipes with", "show recipes with", "what meals can i make with these", "search by ingredients", "recipes using"],
    "exit": ["exit", "quit", "goodbye", "close program", "i'm done", "that's enough", "close app", "shut it down", "bye chef"],
    "pause": ["pause", "wait", "hold on", "give me a sec", "one moment", "hang on a second", "pause for now"],
    "dynamic_recipe": ["build me a recipe", "what can i make with", "custom recipe", "make me a meal", "generate recipe"],
    "add_pantry": ["add to pantry", "store in pantry", "pantry add"],
    "show_pantry": ["what's in my pantry", "show pantry", "list pantry"],
    "clear_pantry": ["clear pantry", "empty pantry"],
    "repeat_last": ["what did you just say", "say that again", "repeat last", "repeat that", "what was that"],
    "summarize_steps": ["summarize steps", "repeat all steps", "what are the steps again", "go over steps again"],
    "recap_recipe": ["what am i making", "what am i cooking", "what are we making", "remind me what this recipe is", "what am i making again", "what's the recipe"],
    "suggest_side": ["what goes with this", "suggest side dish", "what sides go with this", "recommend a side"],
     "meal_plan": ["plan meals", "meal plan", "prepare for the week", "give me dinner ideas for the week"],
     "add_shopping": ["add to shopping list", "add to list", "shopping list add"],
     "why_this_recipe": ["why did you suggest this", "why this recipe", "explain this choice", "why am I making this"]


}

def parse_intent(user_text):
    user_text = user_text.lower().strip()
    for command, phrases in COMMANDS.items():
        for phrase in phrases:
            if phrase in user_text:
                return command
    return "unknown"