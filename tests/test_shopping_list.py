
import pytest
from storage.shopping_list import add_to_shopping_list, remove_from_shopping_list, clear_shopping_list, get_shopping_list

def test_add_to_shopping_list():
    clear_shopping_list()
    add_to_shopping_list("Tomatoes")
    add_to_shopping_list("Milk")
    lst = get_shopping_list()
    assert "Tomatoes" in lst
    assert "Milk" in lst

def test_no_duplicates_case_insensitive():
    clear_shopping_list()
    add_to_shopping_list("Milk")
    add_to_shopping_list("milk")
    lst = get_shopping_list()
    assert lst.count("Milk") + lst.count("milk") == 1

def test_remove_from_shopping_list():
    clear_shopping_list()
    add_to_shopping_list("Onions")
    remove_from_shopping_list("onions")
    lst = get_shopping_list()
    assert "Onions" not in lst

def test_clear_shopping_list():
    add_to_shopping_list("Bread")
    clear_shopping_list()
    assert get_shopping_list() == []
