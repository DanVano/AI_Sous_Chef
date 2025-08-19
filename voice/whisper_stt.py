## Loads the audio, sends to Whisper, returns text.
## Transcribe speech to text using Whisper

import os
import shutil
import whisper

def transcribe_audio(audio_path="audio.wav", model_name="base"):
    """Transcribe audio file using Whisper. Requires ffmpeg in PATH."""
    try:
        if not audio_path or not os.path.exists(audio_path):
            print(f"Transcription error: audio file not found: {audio_path}")
            return ""

        if shutil.which("ffmpeg") is None:
            print("Transcription error: FFmpeg not found in PATH. Install FFmpeg and ensure 'ffmpeg -version' works.")
            return ""

        model = whisper.load_model(model_name)
        result = model.transcribe(audio_path, fp16=False)
        return result.get("text", "")
    except FileNotFoundError as e:
        # Often ctypes/ffmpeg path errors end up here on Windows
        print(f"Transcription error (FileNotFoundError): {e}")
        return ""
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""