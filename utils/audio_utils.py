import time

from utils.conversion_utils import sanitize_user_input
from utils.ingredient_matcher import match_ingredient
from voice.tts import speak
from voice.wake_word import record_audio
from voice.whisper_stt import transcribe_audio

def capture_command(filename="cmd.wav", prompt="Say your command", max_retries=2, record_seconds=3):
    """
    Reusable voice input handler with retries, feedback, and fallback.
    Returns lowercased transcription or empty string.
    """
    global _last_cmd_time, _last_cmd_text
    try:
        _last_cmd_time
        _last_cmd_text
    except NameError:
        _last_cmd_time = 0
        _last_cmd_text = ""

    for attempt in range(max_retries):
        speak(prompt)
        record_audio(filename, record_seconds=record_seconds)
        result = transcribe_audio(filename).strip().lower()

        now = time.time()
        if result and (result != _last_cmd_text or now - _last_cmd_time > 1):
            _last_cmd_time = now
            _last_cmd_text = result
            return result
        elif not result:
            speak("I didn’t catch that. Try again.")
        else:
            speak("Duplicate command detected. Ignoring.")

    speak("Still didn’t catch anything. Returning to main flow.")
    return ""

def capture_ingredient(filename="ingredient.wav", prompt="Say ingredients to add", max_retries=2, record_seconds=3):
    """
    Capture one or more ingredients from the user. Supports multiple, comma/and separated.
    Deduplicates and cleans input.
    Returns a list of clean ingredient names.
    """
    for _ in range(max_retries):
        raw = capture_command(filename, prompt, record_seconds=record_seconds)
        if not raw:
            continue

        # Standardize delimiters
        raw = raw.replace(" and ", ", ")
        items = [sanitize_user_input(x) for x in raw.split(",") if x.strip()]
        cleaned = []
        for item in items:
            match = match_ingredient(item)
            cleaned.append(match if match else item)

        # Remove blanks and deduplicate
        deduped = []
        for i in cleaned:
            if i and i not in deduped:
                deduped.append(i)
        if deduped:
            return deduped

    return []

_last_cmd_time = 0
_last_cmd_text = ""

def debounce_command(cmd, cooldown=1.0):
    global _last_cmd_time, _last_cmd_text
    now = time.time()

    if cmd == _last_cmd_text and (now - _last_cmd_time) < cooldown:
        return False

    _last_cmd_time = now
    _last_cmd_text = cmd
    return True

def capture_ingredient(filename="ingredient.wav", prompt="Say an ingredient to add", max_retries=2, record_seconds=3):
    """
    Specialized voice handler for capturing ingredient names.
    Includes voice retries, formatting, and fuzzy matching.
    """
    for _ in range(max_retries):
        raw = capture_command(filename, prompt, record_seconds=record_seconds)

        if not raw:
            continue

        # Remove common prefixes like "add", "to pantry", etc.
        for word in ["add", "to pantry", "to list", "please add"]:
            raw = sanitize_user_input(raw)

        cleaned = match_ingredient(raw)
        return cleaned if cleaned else raw  # fallback to raw if no match

    return ""

def confirm_yes_no(prompt="Do you want to proceed?", retries=2):
    for _ in range(retries):
        response = capture_command("confirm.wav", prompt)
        if any(word in response for word in ["yes", "sure", "yeah", "go ahead"]):
            return True
        elif any(word in response for word in ["no", "not now", "cancel"]):
            return False
        else:
            speak("Please say yes or no.")
    return False