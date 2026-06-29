"""Semantic search."""

from __future__ import annotations

from dataclasses import dataclass

from mimir.db import search_chunks
from mimir.embeddings import embed_query


@dataclass
class Hit:
    score: float
    text: str
    path: str
    title: str
    folder: str
    chunk_idx: int


def search(
    query: str,
    k: int = 5,
    folder: str | None = None,
    ext: str | None = None,
    title: str | None = None,
) -> list[Hit]:
    qvec = embed_query(query)
    points = search_chunks(qvec, folder=folder, ext=ext, title=title, k=k)

    hits: list[Hit] = []
    for p in points:
        payload = p.payload or {}
        hits.append(
            Hit(
                score=p.score,
                text=payload["text"],
                path=payload["path"],
                title=payload["title"],
                folder=payload.get("folder", "."),
                chunk_idx=payload.get("chunk_idx", 0),
            )
        )
    return hits
