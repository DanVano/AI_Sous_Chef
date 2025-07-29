# Reads text out loud through device speaker.
# Text-to-speech (pyttsx3/gTTS/Android/iOS TTS hooks)


import pyttsx3

from utils.convo_memory import remember

# Initialize the TTS engine once at module load
_engine = pyttsx3.init()
_engine.setProperty('rate', 180)  # You can adjust speech rate if you want (default 200)
_engine.setProperty('volume', 1.0)  # Volume: 0.0 to 1.0

def speak(text):
    """
    Speaks the provided text aloud using the system's TTS engine, and prints it to the console.
    """
    print(f"(TTS) {text}")
    _engine.say(text)
    _engine.runAndWait()
    remember(text)