# wake_word.py

import os
import pvporcupine
import pyaudio
import numpy as np
import wave

with open("config/picovoice_key.txt") as f:
    ACCESS_KEY = f.read().strip()
    
## WAKE_WORDS = ["hey chef", "Hello Chef", "Chef", "Hey Chef"]
WAKE_WORDS = ["porcupine"]

def listen_for_wake_word():
    porcupine = pvporcupine.create(access_key=ACCESS_KEY, keywords=WAKE_WORDS)
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    print("Listening for wake word...")
    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_np = np.frombuffer(pcm, dtype=np.int16)
            keyword_index = porcupine.process(pcm_np)
            if keyword_index >= 0:
                print("Wake word detected!")
                return True
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()

def record_audio(filename="audio.wav", record_seconds=6, rate=16000, folder="recordings"):
    """
    Records mono PCM and saves as WAV. Returns absolute path to the file.
    Creates the folder if needed and prints file size for verification.
    """
    os.makedirs(folder, exist_ok=True)
    if not filename.lower().endswith(".wav"):
        filename += ".wav"
    path = os.path.abspath(os.path.join(folder, filename))

    pa = pyaudio.PyAudio()
    try:
        stream = pa.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=rate,
                         input=True,
                         frames_per_buffer=1024)
        print(f"Recording user prompt for {record_seconds} seconds...")
        frames = []
        for _ in range(0, int(rate / 1024 * record_seconds)):
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
        print("Finished recording.")
    finally:
        try:
            stream.stop_stream()
            stream.close()
        except Exception:
            pass
        pa.terminate()

    try:
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
        size = os.path.getsize(path)
        print(f"Saved file: {path} ({size} bytes)")
    except Exception as e:
        print(f"Error saving WAV to {path}: {e}")
        return ""

    return path
