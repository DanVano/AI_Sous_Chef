## Loads the audio, sends to Whisper, returns text.
## Transcribe speech to text using Whisper



import whisper

def transcribe_audio(audio_path="audio.mp3", model_name="base"):
    """Transcribe audio file using Whisper."""
    try:
        model = whisper.load_model(model_name)
        result = model.transcribe(audio_path, fp16=False)
        return result.get("text", "")
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""