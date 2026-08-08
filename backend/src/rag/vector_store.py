import chromadb
from utils.config import config

class VectorStore:
    """Generic wrapper for a collection on chromadb"""

    def __init__(self, collection_name: str):
        self.client = chromadb.PersistentClient(path=config.vector_store.path)
        self.collection = self.client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})

    def upsert(self, ids: list[str], documents: list[str], embeddings: list[list[float]], metadatas: list[dict]):
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def query(self, embedding: list[float], top_k: int = None, where: dict = None) -> dict:
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k or config.vector_store.top_k,
            where=where,
            include=["documents", "metadatas", "distances"]
        )

    def get(self, ids: list[str]) -> dict:
        return self.collection.get(ids=ids, include=["documents", "metadatas"])

    def delete(self, ids: list[str]):
        self.collection.delete(ids=ids)

    def count(self) -> int:
        return self.collection.count()