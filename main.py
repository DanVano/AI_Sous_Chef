##  App controller; starts/stops sessions, routes logic to modules.



import time
from voice.whisper_stt import transcribe_audio
from ai.chatgpt_api import get_chatgpt_response
from wake_word import listen_for_wake_word, record_audio
from storage.session_storage import save_session_transcription

def main():
    print("App started. Say 'Hey Chef' to begin...")
    while True:
        if listen_for_wake_word():
            print("Ready!")  # You could add TTS here
            # Record user's command/recipe as audio
            audio_path = "audio.mp3"
            record_audio(audio_path)
            # Transcribe the audio
            transcription = transcribe_audio(audio_path)
            print(f"Transcribed: {transcription}")
            # Save transcription to session storage (to save RAM)
            save_session_transcription(transcription)
            # Optionally, process with ChatGPT
            if transcription:
                answer = get_chatgpt_response(transcription)
                print(f"AI Response: {answer}")

            print("Say 'Hey Chef' to begin again, or Ctrl+C to quit.")

if __name__ == "__main__":
    main()