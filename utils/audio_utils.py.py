import time
from voice.tts import speak
from voice.wake_word import record_audio
from voice.whisper_stt import transcribe_audio

def capture_command(filename="cmd.wav", prompt="Say your command", max_retries=2, record_seconds=3):
    """
    Voice input handler with retries, feedback, and duplicate debounce.
    Returns cleaned command or "".
    """
    global _last_cmd_time, _last_cmd_text

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