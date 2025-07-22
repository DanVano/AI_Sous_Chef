
import pytest
from utils.deal_finder import boost_recipes_by_sale

mock_recipes = [
    {"name": "Grilled Chicken", "ingredients": ["chicken", "salt", "pepper"]},
    {"name": "Beef Stew", "ingredients": ["beef", "carrot", "potato"]},
    {"name": "Tofu Stir Fry", "ingredients": ["tofu", "broccoli", "soy sauce"]}
]

def test_boost_recipes_by_sale():
    sales = {"chicken", "broccoli"}
    boosted = boost_recipes_by_sale(sales, mock_recipes)
    assert len(boosted) == 3
    assert boosted[0]["name"] in ["Grilled Chicken", "Tofu Stir Fry"]
