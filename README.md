# AI Sous Chef (Alpha)
**A voice-controlled Python cooking assistant that recommends, navigates, and reads recipes—all hands-free**

---

## Status
**Alpha Release** (active development)  
**Python Version:** 3.8+

---

## About

AI Sous Chef is a modular, voice-driven cooking assistant designed to make meal planning and cooking completely hands-free. It combines speech-to-text, intent recognition, recipe management, and conversational AI to help you discover, prepare, and navigate recipes using only your voice.

- **Recipe Discovery:** Suggests 3–5 recipes based on your available ingredients, preferences, and skill level.
- **Step-by-Step Guidance:** Reads out each recipe step and listens for navigation commands ("next step", "repeat", "substitute [ingredient]").
- **Personalized Filtering:** Remembers dietary restrictions (vegan, keto, gluten-free), allergies, favorite cuisines, and cooking skill.
- **ChatGPT Fallback:** Handles unrecognized questions or requests with conversational AI (optional, requires OpenAI key).
- **Session Memory:** Saves your active cooking session and recent requests.

> **NOTE:** This tool is in ALPHA. Expect bugs and limited features. Test with caution!

---

## Folder Organization
```
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
├── README.md                # This file
```

---

## How to Use

1. **Install Dependencies:**

pip install pyttsx3 openai pvporcupine pyaudio numpy


2. **Set Up:**
 - All core `.py` files are organized by feature (see folder structure above).
 - User preferences and session data are stored in `/storage/`.
 - Recipes are stored in `/recipes/recipes.json` (edit or add your own!).
 - *(Optional)* For ChatGPT features, add your OpenAI API key as instructed in `ai/chatgpt_api.py`.

3. **Run the Program:**

python main.py

- **Say "Hey Chef" to begin!**

---

## Features

- **Ingredient-Based Search:** Say what you have, and get recipe ideas.
- **Step Navigation:** Control the recipe flow with voice commands.
- **Custom User Profile:** Set allergies, diet, cuisine, restrictions, and skill.
- **Ingredient Substitution:** Ask for alternatives during cooking.
- **Hands-Free:** Wake word, TTS, and STT provide a fully voice-powered experience.
- **Session Memory:** Remembers your progress and recent activity.
- **ChatGPT Fallback:** Conversational support for broader questions (with OpenAI key).

---

## Dependencies

- `pyttsx3` (text-to-speech)
- `pvporcupine` (wake word detection)
- `pyaudio` (audio input)
- `numpy`
- `openai` *(optional, for ChatGPT fallback)*
- Python libraries: `os`, `json`, `wave`

---

## Configuration

- **No config file is required for basic use.**
- For ChatGPT functionality, place your OpenAI API key as described in `ai/chatgpt_api.py`.

---

## Project Status

**Alpha Release:**  
Active development for Windows. Android support is planned once core functionality is complete.  
Expect rapid feature additions and possible breaking changes—feedback welcome!
