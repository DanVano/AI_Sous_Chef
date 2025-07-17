# wake_word.py

import pvporcupine
import pyaudio
import numpy as np
import wave

WAKE_WORDS = ["hey chef"]

def listen_for_wake_word():
    porcupine = pvporcupine.create(keywords=WAKE_WORDS)
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
                # Optionally, play a sound or say "Ready"
                return True
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()

def record_audio(filename="audio.mp3", record_seconds=6, rate=16000):
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=rate,
                     input=True,
                     frames_per_buffer=1024)
    print("Recording user prompt...")
    frames = []
    for _ in range(0, int(rate / 1024 * record_seconds)):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    pa.terminate()

    # Save as WAV for Whisper
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
