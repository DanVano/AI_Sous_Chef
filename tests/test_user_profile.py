
import pytest
import os
from storage.persistent_storage import save_user_profile, load_user_profile

def test_save_and_load_user_profile(tmp_path):
    profile = {
        "diet": "vegetarian",
        "allergies": ["nuts", "shellfish"],
        "restrictions": ["gluten-free"],
        "skill": "confident homecook",
        "cuisines": ["thai", "italian"]
    }

    # Patch file path
    test_file = tmp_path / "user_profile.json"
    original_path = "storage/user_profile.json"
    os.makedirs(os.path.dirname(original_path), exist_ok=True)

    # Save and load
    save_user_profile(profile)
    loaded = load_user_profile()

    assert loaded == profile
