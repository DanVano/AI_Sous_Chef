import os
import logging
import openai
from openai.error import OpenAIError

logging.basicConfig(level=logging.INFO)

def get_chatgpt_response(question: str) -> str:
    key_path = os.path.join("config", "key.txt")
    try:
        with open(key_path, "r", encoding="utf-8") as file:
            openai.api_key = file.read().strip()
    except Exception as e:
        logging.error("Could not read OpenAI key at %s: %s", key_path, e)
        return "API key not found."

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": question}
    ]

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        text = resp.choices[0].message["content"].strip()
        logging.info("Q: %s", question)
        logging.info("A: %s", text)
        return text
    except OpenAIError as e:
        logging.error("OpenAI API error: %s", str(e))
        return f"OpenAI API error: {str(e)}"
