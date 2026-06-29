"""Semantic search."""

from __future__ import annotations

from dataclasses import dataclass

from qdrant_client import models

from mimir.config import settings
from mimir.db import get_client
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
    must: list = []
    if folder:
        must.append(
            models.FieldCondition(key="folder", match=models.MatchValue(value=folder))
        )
    if ext:
        must.append(
            models.FieldCondition(key="ext", match=models.MatchValue(value=ext.lower()))
        )
    if title:
        must.append(
            models.FieldCondition(key="title", match=models.MatchValue(value=title))
        )
    qfilter = models.Filter(must=must) if must else None

    qvec = embed_query(query)
    result = get_client().query_points(
        collection_name=settings.collection,
        query=qvec,
        query_filter=qfilter,
        limit=k,
        with_payload=True,
    )

    return [
        Hit(
            score=p.score,
            text=p.payload["text"],
            path=p.payload["path"],
            title=p.payload["title"],
            folder=p.payload.get("folder", "."),
            chunk_idx=p.payload.get("chunk_idx", 0),
        )
        for p in result.points
    ]
