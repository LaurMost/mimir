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
