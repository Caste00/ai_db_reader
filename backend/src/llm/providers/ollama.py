from ollama import chat
from utils.config import config


class LLMGenerationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        

def generate(prompt: str | list[dict], model: str = None, json_mode: bool = False) -> str:
    message = prompt if isinstance(prompt, list) else [{"role": "user", "content": prompt}]

    try: 
        response = chat(
            model=model or config.llm.model,
            messages=message,
            format="json" if json_mode else None,
        )
    except Exception as e:
        raise LLMGenerationError(f"Error during the generation: {e}")

    return response.message.content