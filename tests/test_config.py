"""Tests for mimir.config.Settings."""

from __future__ import annotations

from mimir.config import Settings


def test_defaults():
    s = Settings()
    assert s.qdrant_url == "http://localhost:6333"
    assert s.collection == "mimir"
    assert s.embed_model == "BAAI/bge-small-en-v1.5"
    assert s.vector_size == 384
    assert s.chunk_size == 1200
    assert s.chunk_overlap == 150


def test_env_override(monkeypatch):
    monkeypatch.setenv("MIMIR_COLLECTION", "test_collection")
    monkeypatch.setenv("MIMIR_VECTOR_SIZE", "768")
    monkeypatch.setenv("MIMIR_CHUNK_SIZE", "2000")
    s = Settings()
    assert s.collection == "test_collection"
    assert s.vector_size == 768
    assert s.chunk_size == 2000


def test_chunk_size_validated(monkeypatch):
    import pytest
    from pydantic import ValidationError

    monkeypatch.setenv("MIMIR_CHUNK_SIZE", "100")  # below min
    with pytest.raises(ValidationError):
        Settings()
