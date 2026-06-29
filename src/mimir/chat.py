"""RAG chat backed by a local Ollama model."""

from __future__ import annotations

import json
from collections.abc import Iterator

import httpx

from mimir.config import settings
from mimir.query import Hit, search

SYSTEM_PROMPT = """You are Mimir, the user's personal second-brain assistant.
Answer using ONLY the provided context drawn from the user's own notes.
Cite sources inline using the format [title] after each claim.
If the context does not contain the answer, say so plainly. Do not invent.
Be concise and direct — these are the user's own thoughts coming back to them."""


def _build_prompt(question: str, hits: list[Hit]) -> str:
    context = "\n\n---\n\n".join(
        f"[{h.title}] ({h.path})\n{h.text}" for h in hits
    )
    return f"Context from your notes:\n\n{context}\n\nQuestion: {question}"


def stream_answer(question: str, k: int = 6) -> Iterator[tuple[str, list[Hit]]]:
    """
    Yields (token, hits) tuples. `hits` is the same list every yield —
    handy for the UI to show sources alongside the streaming answer.
    """
    hits = search(question, k=k)
    prompt = _build_prompt(question, hits)

    payload = {
        "model": settings.ollama_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": True,
    }

    with httpx.stream(
        "POST",
        f"{settings.ollama_url}/api/chat",
        json=payload,
        timeout=None,
    ) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            obj = json.loads(line)
            chunk = obj.get("message", {}).get("content", "")
            if chunk:
                yield chunk, hits
            if obj.get("done"):
                break
