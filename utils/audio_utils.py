import time

from utils.conversion_utils import sanitize_user_input
from utils.ingredient_matcher import match_ingredient
from voice.tts import speak
from voice.wake_word import record_audio
from voice.whisper_stt import transcribe_audio

# Cooldown memory
_last_cmd_time = 0.0
_last_cmd_text = ""

def debounce_command(cmd: str, cooldown: float = 1.0) -> bool:
    """
    Returns False if the same command was received less than `cooldown` seconds ago.
    """
    global _last_cmd_time, _last_cmd_text
    now = time.time()
    if cmd and cmd == _last_cmd_text and (now - _last_cmd_time) < cooldown:
        return False
    _last_cmd_text = cmd
    _last_cmd_time = now
    return True

def capture_command(filename: str = "cmd.wav",
                    prompt: str = "Say your command",
                    max_retries: int = 2,
                    record_seconds: int = 6) -> str:
    """
    Voice capture with retries, WAV saving, and Whisper transcription.
    Returns lowercased text ('' on failure).
    """
    for attempt in range(max_retries):
        speak(prompt)
        path = record_audio(filename, record_seconds=record_seconds)  # returns absolute path or ''
        if not path:
            speak("Recording failed. Let’s try again.")
            continue

        text = transcribe_audio(path).strip().lower()
        if not text:
            speak("I didn’t catch that. Try again.")
            continue

        # cooldown check (prevent accidental double-triggers)
        if not debounce_command(text, cooldown=1.0):
            speak("Duplicate command detected. Ignoring.")
            continue

        return text

    speak("Still didn’t catch anything. Returning to main flow.")
    return ""

def _split_multi(text: str) -> list[str]:
    """
    Normalize separators ('and' → ',', remove filler), return list.
    """
    text = text.replace(" and ", ", ")
    parts = [sanitize_user_input(x) for x in text.split(",")]
    return [p for p in parts if p]

def capture_ingredient(filename: str = "ingredient.wav",
                       prompt: str = "Say ingredients to add",
                       max_retries: int = 2,
                       record_seconds: int = 4) -> list[str]:
    """
    Capture one or more ingredients. Supports comma/and-separated input.
    - Cleans filler words (sanitize_user_input)
    - Fuzzy matches known pantry items
    - Deduplicates results (case-insensitive)
    Returns a list (possibly length 1). Empty list on failure.
    """
    for _ in range(max_retries):
        raw = capture_command(filename, prompt, record_seconds=record_seconds)
        if not raw:
            continue

        # Parse possible multiple ingredients
        items = _split_multi(raw)

        mapped = []
        for item in items:
            matched = match_ingredient(item)
            mapped.append(matched if matched else item)

        # Deduplicate (case-insensitive)
        seen = set()
        deduped = []
        for m in mapped:
            key = m.lower()
            if key not in seen:
                deduped.append(m)
                seen.add(key)

        if deduped:
            return deduped

    return []

def confirm_yes_no(prompt: str = "Do you want to proceed?", retries: int = 2) -> bool:
    """
    Simple voice yes/no confirm using capture_command.
    """
    for _ in range(retries):
        response = capture_command("confirm.wav", prompt)
        if any(word in response for word in ["yes", "sure", "yeah", "go ahead", "confirm"]):
            return True
        if any(word in response for word in ["no", "not now", "cancel", "stop"]):
            return False
        speak("Please say yes or no.")
    return False