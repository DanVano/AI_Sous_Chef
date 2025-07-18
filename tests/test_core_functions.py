import os

# Prepare a pytest test file for the given functions
test_code = '''
import pytest
from ai.intent_parser import parse_intent
from recipes.recipe_manager import filter_recipes
from recipes.substitutions import get_substitutes
from utils.timer import extract_timer_seconds

def test_parse_intent_known():
    assert parse_intent("next step") == "next_step"
    assert parse_intent("add to shopping list") == "add_shopping"
    assert parse_intent("main menu") == "main_menu"

def test_parse_intent_unknown():
    assert parse_intent("abracadabra") == "unknown"

def test_extract_timer_seconds():
    assert extract_timer_seconds("set a timer for 2 minutes") == 120
    assert extract_timer_seconds("timer for 30 seconds") == 30
    assert extract_timer_seconds("no time mentioned") is None

def test_get_substitutes():
    subs = get_substitutes("eggs")
    assert isinstance(subs, list)
    assert "applesauce" in subs

def test_filter_recipes_basic():
    dummy_profile = {
        "diet": "vegetarian",
        "allergies": [],
        "restrictions": []
    }
    results = filter_recipes(["tofu", "rice"], dummy_profile)
    assert isinstance(results, list)
    assert any("tofu" in recipe["ingredients"] for recipe in results)
'''

# Save it to the expected /tests directory
tests_dir = "/mnt/data/tests"
os.makedirs(tests_dir, exist_ok=True)
test_file_path = os.path.join(tests_dir, "test_core_functions.py")

with open(test_file_path, "w") as f:
    f.write(test_code)

test_file_path