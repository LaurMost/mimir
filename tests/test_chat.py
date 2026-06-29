"""Tests for the RAG chat seam (no Ollama, Qdrant, or ONNX required)."""

from __future__ import annotations

from collections.abc import Iterator

import mimir.chat
from mimir.chat import build_prompt, stream_answer
from mimir.query import Hit


class FakeLLMAdapter:
    def __init__(self, tokens: list[str]) -> None:
        self._tokens = tokens
        self.seen_messages: list[dict] | None = None

    def stream(self, messages: list[dict]) -> Iterator[str]:
        self.seen_messages = messages
        yield from self._tokens


def _hit(title: str = "Note", text: str = "body") -> Hit:
    return Hit(
        score=1.0,
        text=text,
        path=f"/notes/{title}.md",
        title=title,
        folder=".",
        chunk_idx=0,
    )


def test_build_prompt_includes_title_and_question():
    prompt = build_prompt("What is X?", [_hit("Alpha", "alpha body")])
    assert "[Alpha]" in prompt
    assert "alpha body" in prompt
    assert "What is X?" in prompt


def test_stream_answer_uses_injected_adapter(monkeypatch):
    hits = [_hit("Alpha")]
    monkeypatch.setattr(mimir.chat, "search", lambda question, k: hits)

    fake = FakeLLMAdapter(["tok1", "tok2"])
    out = list(stream_answer("question", k=3, llm=fake))

    assert out == [("tok1", hits), ("tok2", hits)]
    assert fake.seen_messages is not None
    assert fake.seen_messages[0]["role"] == "system"
    assert "question" in fake.seen_messages[1]["content"]
