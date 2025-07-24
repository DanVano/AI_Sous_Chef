
from llama_cpp import Llama
import os

MODEL_PATH = os.path.join("local_ai", "tinyllama-1.1b-chat.Q4_K_M.gguf")

class LocalAssistant:
    def __init__(self, model_path=MODEL_PATH):
        if not os.path.exists(model_path):
            print(f"[Warning] Local model not found at {model_path}. Using mock response mode.")
            self.model = None
        else:
            self.model = Llama(
                model_path=model_path,
                n_ctx=512,
                n_threads=4,
                verbose=False
            )

    def get_response(self, prompt):
        """
        Provide a specialized local response based on TinyLlama. Fallbacks to mock if model missing.
        """
        if not self.model:
            return self._mock_response(prompt)

        prompt_template = f\"\"\"You are a helpful cooking assistant trained to give short, direct answers       about ingredients, substitutions, cooking steps, and timing.

        Here are some examples:
User: What can I cook with chicken and rice?
Assistant: Try chicken fried rice, chicken soup, or chicken biryani.

User: What's a substitute for milk?
Assistant: Use almond milk, oat milk, or soy milk.

User: How long does it take to cook pasta?
Assistant: About 10 minutes, depending on the type.

User: {prompt}
Assistant:\"\"\"
        output = self.model(prompt_template, max_tokens=150, stop=["User:", "Assistant:"])
        return output["choices"][0]["text"].strip()

    def _mock_response(self, prompt):
        # Simulate behavior for common queries
        lowered = prompt.lower()
        if "substitute" in lowered and "milk" in lowered:
            return "You can substitute milk with almond milk, oat milk, or soy milk."
        elif "how long" in lowered and "recipe" in lowered:
            return "This recipe should take around 30 minutes to complete."
        elif "what can i cook with" in lowered:
            return "You can make a stir-fry, a soup, or a casserole with those ingredients."
        elif "what step am i on" in lowered:
            return "You are currently on step 3 of your recipe."
        return "I'm not sure, but I can help with cooking questions, ingredients, or recipes."

# Example usage
if __name__ == "__main__":
    assistant = LocalAssistant()
    print(assistant.get_response("What can I cook with eggs and spinach?"))
    print(assistant.get_response("What's a good substitute for milk?"))
