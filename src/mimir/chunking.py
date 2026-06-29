"""Text chunking. Tries to respect paragraph / sentence boundaries."""

from __future__ import annotations

from mimir.config import settings


def chunk_text(
    text: str,
    max_chars: int | None = None,
    overlap: int | None = None,
) -> list[str]:
    """
    Sliding-window chunker that prefers to break on paragraph, then newline,
    then sentence boundaries. Works fine for prose and markdown.
    """
    max_chars = max_chars or settings.chunk_size
    overlap = overlap or settings.chunk_overlap

    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + max_chars, n)

        # If we're not at the end, look back for a clean break.
        if end < n:
            for sep in ("\n\n", "\n", ". ", " "):
                idx = text.rfind(sep, start + max_chars // 2, end)
                if idx != -1:
                    end = idx + len(sep)
                    break

        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)

        if end >= n:
            break
        start = max(end - overlap, start + 1)

    return chunks
