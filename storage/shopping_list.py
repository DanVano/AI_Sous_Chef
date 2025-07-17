import json
import os

SHOPPING_LIST_FILE = "storage/shopping_list.json"

def load_shopping_list():
    if not os.path.exists(SHOPPING_LIST_FILE):
        return []
    with open(SHOPPING_LIST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_shopping_list(lst):
    with open(SHOPPING_LIST_FILE, "w", encoding="utf-8") as f:
        json.dump(lst, f, indent=2)

def add_to_shopping_list(item):
    lst = load_shopping_list()
    if item.lower() not in [i.lower() for i in lst]:
        lst.append(item)
        save_shopping_list(lst)

def remove_from_shopping_list(item):
    lst = load_shopping_list()
    lst = [i for i in lst if i.lower() != item.lower()]
    save_shopping_list(lst)

def clear_shopping_list():
    save_shopping_list([])

def get_shopping_list():
    return load_shopping_list()
