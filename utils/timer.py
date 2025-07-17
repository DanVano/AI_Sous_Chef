import threading
import time
import re
from voice.tts import speak

def timer_thread(seconds):
    time.sleep(seconds)
    for _ in range(3):
        speak("Timer is completed!")

def set_timer(seconds):
    t = threading.Thread(target=timer_thread, args=(seconds,))
    t.daemon = True
    t.start()
    speak(f"Timer for {seconds} seconds has started.")

def extract_timer_seconds(user_text):
    # Look for number + "minute" or "second"
    match = re.search(r'(\d+)\s*(second|seconds|minute|minutes)', user_text)
    if match:
        num = int(match.group(1))
        unit = match.group(2)
        if "minute" in unit:
            return num * 60
        else:
            return num
    return None