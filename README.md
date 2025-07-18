AI Sous Chef (Alpha)

A voice-controlled Python cooking assistant that recommends, navigates, and reads recipes—all hands-free.
Status

Alpha Release (active development)
Python Version: 3.8+
About

AI Chef is a smart, modular voice assistant that helps you plan and cook meals without ever touching your phone or computer. It uses speech-to-text, intent recognition, and local recipe filtering to make home cooking easier.

It provides:

    Recipe Discovery: Suggests 3–5 recipes based on your available ingredients, preferences, and skill level

    Step-by-Step Guidance: Reads out each recipe step and listens for navigation commands ("next step", "repeat", "substitute [ingredient]")

    Personalized Filtering: Remembers dietary restrictions (vegan, keto, gluten-free, etc.), allergies, favorite cuisines, and skill level

    ChatGPT Fallback: Handles unrecognized questions or requests with conversational AI (optional)

    Session Memory: Saves your active cooking session and recent requests

    NOTE: This tool is in ALPHA. Expect bugs and limited features. Test with caution!

/AI_Chef/
│
├── main.py                  # Main entry point
│
├── ai/                      # AI and NLP logic
│   ├── chatgpt_api.py
│   └── intent_parser.py
│
├── voice/                   # Voice features (TTS, STT, wake word)
│   ├── tts.py
│   ├── wake_word.py
│   └── whisper_stt.py
│
├── recipes/                 # Recipes and manager
│   ├── recipes.json
│   └── recipe_manager.py
│
├── storage/                 # Storage modules
│   ├── persistent_storage.py
│   └── session_storage.py
│
├── requirements.txt         # Dependencies
├── README.md                # Project documentation
How to Use

    Install Dependencies:

pip install pyttsx3 openai pvporcupine pyaudio numpy

Set Up:

    All core .py files are located in the main folders (see above).

    User preferences and session info are stored in /storage/.

    Recipes are stored in /recipes/recipes.json (edit or add your own).

    (Optional) Add your OpenAI key if using ChatGPT features.

Run the Program:

    python main.py

        Speak "Hey Chef" to begin!

Features

    Ingredient-Based Search: Just say what you have, and get recipe ideas.

    Step Navigation: Control the cooking process with your voice.

    Custom User Profile: Set allergies, diet, cuisine, restrictions, and cooking skill.

    Ingredient Substitution: Request substitutions on the fly.

    Hands-Free: Wake word, TTS, and STT for a full voice experience.

Dependencies

    pyttsx3

    pvporcupine

    pyaudio

    numpy

    openai (optional, for ChatGPT fallback)

    Python libraries: os, json, wave

Configuration

No config file is required for basic use.
For ChatGPT access, place your OpenAI API key in a file as instructed in ai/chatgpt_api.py.
Project Status

Alpha Release:
Actively developed for Windows, will switch to Android once base is built. Feedback welcome!
Expect rapid feature additions and possible breaking changes.
