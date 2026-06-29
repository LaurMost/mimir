"""Configuration loaded from environment / .env."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="MIMIR_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    collection: str = "mimir"

    # Embeddings
    embed_model: str = "BAAI/bge-small-en-v1.5"
    vector_size: int = 384

    # Chunking
    chunk_size: int = Field(default=1200, ge=200, le=8000)
    chunk_overlap: int = Field(default=150, ge=0, le=1000)

    # Ingestion
    notes_dir: Path = Path("./notes")
    batch_size: int = 256

    # Ollama
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b-instruct"


settings = Settings()
