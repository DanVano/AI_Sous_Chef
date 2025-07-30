##

def extract_substitute_ingredients(text):
    text = text.lower()
    if "substitute" in text:
        after = text.split("substitute")[1].strip()
        if "with" in after:
            old, new = after.split("with")
            return old.strip(), new.strip()
        return after.strip(), None  # Only 'substitute eggs'
    return None, None

def extract_rating(text):
    for word in text.split():
        if word.isdigit() and 1 <= int(word) <= 5:
            return int(word)
    return None

def is_unclear(text):
    if not text or len(text.strip()) < 3:
        return "unclear"
    if len(text.split()) < 2:
        return "repeat"
    bad_phrases = ["uh", "what", "sorry", "say again", "i don't know"]
    if any(p in text.lower() for p in bad_phrases):
        return "repeat"
    return None

def summarize_recipe(recipe):
    name = recipe.get("name", "a recipe")
    ingredients = recipe.get("ingredients", [])
    steps = recipe.get("steps", [])
    return f"You’re making {name}. It uses {len(ingredients)} ingredients and has {len(steps)} steps."

def sanitize_user_input(text):
    ignore_phrases = ["add", "to pantry", "to list", "please", "can you", "i want", "uh", "um"]
    text = text.lower()
    for phrase in ignore_phrases:
        text = text.replace(phrase, "")
    return text.strip()
