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
    return None