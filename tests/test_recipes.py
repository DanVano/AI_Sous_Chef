
import pytest
from recipes.recipe_manager import get_recipe_by_name, substitute_ingredient, load_recipes

def test_get_recipe_by_name_found():
    recipe = get_recipe_by_name("Chicken Parmesan")
    assert recipe is not None
    assert recipe["name"] == "Chicken Parmesan"

def test_get_recipe_by_name_not_found():
    recipe = get_recipe_by_name("Unicorn Pie")
    assert recipe is None

def test_substitute_ingredient_exact_match():
    recipe = get_recipe_by_name("Chicken Parmesan")
    new_recipe = substitute_ingredient(recipe, "parmesan", "cheddar")
    assert "cheddar" in new_recipe["ingredients"]
    assert "parmesan" not in new_recipe["ingredients"]

def test_substitute_ingredient_case_insensitive():
    recipe = get_recipe_by_name("Chicken Parmesan")
    new_recipe = substitute_ingredient(recipe, "PaRMeSan", "cheddar")
    assert "cheddar" in new_recipe["ingredients"]

def test_substitute_ingredient_no_change_if_not_found():
    recipe = get_recipe_by_name("Chicken Parmesan")
    new_recipe = substitute_ingredient(recipe, "anchovies", "tofu")
    assert "tofu" not in new_recipe["ingredients"]
