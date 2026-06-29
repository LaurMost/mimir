"""Text chunking. Tries to respect paragraph / sentence boundaries."""

from __future__ import annotations

DEFAULT_CHUNK_SIZE = 1200
DEFAULT_OVERLAP = 150


def chunk_text(
    text: str,
    max_chars: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[str]:
    """
    Sliding-window chunker that prefers to break on paragraph, then newline,
    then sentence boundaries. Works fine for prose and markdown.
    """
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
