
from rapidfuzz import process, fuzz

# Load or define a clean set of known ingredient keywords
# In practice, you might pull this from your recipes.json or a master list
KNOWN_INGREDIENTS = [
    "chicken", "chicken breast", "chicken thigh", "beef", "ground beef", "pork",
    "salmon", "eggs", "milk", "butter", "olive oil", "flour", "sugar", "rice", "tofu",
    "zucchini", "carrot", "onion", "garlic", "bread", "cheese", "mozzarella", "parmesan",
    "tomato", "tomato sauce", "spinach", "lettuce", "broccoli", "bell pepper", "potato"
]

def match_ingredient(user_ingredient, known_ingredients=KNOWN_INGREDIENTS, threshold=85):
    """
    Match a user input to a known ingredient using fuzzy logic.
    Returns the best match if above threshold, else returns None.
    """
    match, score, _ = process.extractOne(user_ingredient, known_ingredients, scorer=fuzz.token_sort_ratio)
    return match if score >= threshold else None

def match_ingredients_bulk(user_ingredients, known_ingredients=KNOWN_INGREDIENTS, threshold=85):
    """
    Run match_ingredient across a list of user-provided ingredients.
    Returns a list of matched ingredients.
    """
    matched = []
    for item in user_ingredients:
        result = match_ingredient(item, known_ingredients, threshold)
        if result:
            matched.append(result)
    return matched

# Example usage (for testing)
if __name__ == "__main__":
    user_list = ["chiken", "onions", "mozzarela", "potatos", "salmn", "beaf"]
    corrected = match_ingredients_bulk(user_list)
    print("Corrected:", corrected)
