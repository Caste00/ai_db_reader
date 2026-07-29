# chiamate a basso livello per generare gli embedding
from ollama import embed
from functools import lru_cache

class EmbeddingError(Exception):
    """Error during embedding generation."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

@lru_cache(maxsize=1000)
def get_embedding(message: str, model: str = 'mxbai-embed-large:latest') -> list[float]:
    if not isinstance(message, str):
        raise ValueError("Message must be a string.")
    if not message.strip():
        raise ValueError("Message cannot be empty.")

    try:
        response = embed(
            model=model,
            input=message
        )
    except Exception as e:
        raise EmbeddingError(f"Something wrong during embedding: {e}") 

    embedding = response['embeddings'][0]

    if not isinstance(embedding, list):
        raise EmbeddingError("Not valid format for the embedding")

    return embedding

