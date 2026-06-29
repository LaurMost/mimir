"""Embeddings via fastembed. Cached so we only load the model once per process."""

from __future__ import annotations

from collections.abc import Iterable
from functools import lru_cache
from typing import Protocol, runtime_checkable

from fastembed import TextEmbedding

from mimir.config import settings


@runtime_checkable
class Embedder(Protocol):
    """The seam every embedding adapter satisfies."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


@lru_cache(maxsize=1)
def get_embedder() -> TextEmbedding:
    return TextEmbedding(model_name=settings.embed_model)


def embed_documents(texts: list[str]) -> list[list[float]]:
    """Embed a batch of documents for indexing."""
    embedder = get_embedder()
    return [v.tolist() for v in embedder.embed(texts)]


def embed_query(text: str) -> list[float]:
    """Embed a single search query (BGE models use a different prefix internally)."""
    embedder = get_embedder()
    return next(iter(embedder.query_embed([text]))).tolist()


def embed_iter(texts: Iterable[str]):
    """Streaming embed for very large batches."""
    yield from get_embedder().embed(texts)
