 ## Temp session storage (for current recipe steps)

## Caches recipe steps and current progress during an active session.


def save_session_transcription(transcription, session_id="current_session"):
    filename = f"storage/{session_id}_transcription.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(transcription)

def load_session_transcription(session_id="current_session"):
    filename = f"storage/{session_id}_transcription.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""