"""Shared test fixtures."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _isolate_env(monkeypatch, tmp_path):
    """Strip all MIMIR_* vars and point at a tmp dir so tests are hermetic."""
    for k in list(os.environ):
        if k.startswith("MIMIR_"):
            monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("MIMIR_NOTES_DIR", str(tmp_path / "notes"))
    (tmp_path / "notes").mkdir()
    # Prevent pydantic-settings from finding a .env file in cwd
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def notes_dir(tmp_path) -> Path:
    d = tmp_path / "notes"
    d.mkdir(exist_ok=True)
    return d


VECTOR_SIZE = 384


class FakeEmbedder:
    """Deterministic embedder satisfying the Embedder seam. No ONNX model load."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * VECTOR_SIZE for _ in texts]

    def embed_query(self, text: str) -> list[float]:
        return [0.0] * VECTOR_SIZE


@pytest.fixture
def fake_embedder(monkeypatch) -> FakeEmbedder:
    """Swap the embeddings seam for a fake so tests never load the ONNX model.

    Patches the module-level seam functions (`embed_documents` / `embed_query`)
    rather than `get_embedder`, since those are what callers cross. Also guards
    `get_embedder` so an accidental real load fails loudly instead of silently
    downloading the model.
    """
    fake = FakeEmbedder()
    monkeypatch.setattr("mimir.embeddings.embed_documents", fake.embed_documents)
    monkeypatch.setattr("mimir.embeddings.embed_query", fake.embed_query)

    def _no_load():
        raise AssertionError("get_embedder() called while fake_embedder is active")

    monkeypatch.setattr("mimir.embeddings.get_embedder", _no_load)
    return fake
