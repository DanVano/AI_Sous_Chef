
def sanitize_list_input(raw_input):
    return [item.strip().lower() for item in raw_input.split(",") if item.strip()]

def validate_diet(diet):
    valid = {"vegan", "vegetarian", "meat eater", "pescatarian", "keto"}
    return diet.lower() in valid

def validate_postal(postal_code):
    return len(postal_code.strip()) >= 6 and postal_code[0].isalpha()

def clean_user_profile_input():
    print("Let’s set up your profile. Please be honest and clear.")
    allergies = input("Allergies (comma separated, or 'none'): ")
    diet = input("Diet (vegan, vegetarian, meat eater, pescatarian): ")
    postal_code = input("Postal code (e.g., V6B1A1): ")

    if not validate_diet(diet):
        print("Invalid diet choice. Please enter one of the supported diets.")
        return None

    if not validate_postal(postal_code):
        print("Invalid postal code format.")
        return None

    return {
        "allergies": sanitize_list_input(allergies) if allergies != "none" else [],
        "diet": diet.lower(),
        "postal_code": postal_code.upper()
    }
