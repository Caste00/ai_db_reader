from ollama import chat
from utils.config import config


class LLMGenerationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        

def generate(prompt: str, model: str = None) -> str:
    try: 
        response = chat(
            model=model or config.llm.model,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        raise LLMGenerationError(f"Error during the generation: {e}")

    return response