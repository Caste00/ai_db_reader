from pathlib import Path
import yaml
from pydantic import BaseModel, ConfigDict

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"

class LLMConfig(BaseModel):
    provider: str
    model: str
    ollama_host: str

class EmbeddingConfig(BaseModel):
    provider: str
    model: str

class VectorStoreConfig(BaseModel):
    path: str
    top_k: int

class DatabaseConfig(BaseModel):
    sqlite_path: str

class TargetDatabaseConfig(BaseModel):
    model_config = ConfigDict(extra="allow")   
    type: str

class AppConfig(BaseModel):
    llm: LLMConfig
    embedding: EmbeddingConfig
    vector_store: VectorStoreConfig
    database: DatabaseConfig
    target_database: TargetDatabaseConfig


def load_config(path: Path = CONFIG_PATH) -> AppConfig:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
    return AppConfig(**raw)

# Singleton
config = load_config()