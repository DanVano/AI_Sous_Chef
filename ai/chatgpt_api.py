## Handles chat completions, recipe recommendations.
## Handles all OpenAI API interactions



import openai
import logging
from openai.error import OpenAIError

logging.basicConfig(level=logging.INFO)

def get_chatgpt_response(question):
    with open("key.txt", "r") as file:
        openai.api_key = file.read().strip()

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": question}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        logging.info("Question: %s", question)
        logging.info("Response: %s", response)
        return response.choices[0].message["content"].strip()
    except OpenAIError as e:
        logging.error("OpenAI API error: %s", str(e))
        return f"OpenAI API error: {str(e)}"