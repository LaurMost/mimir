"""Qdrant repository: client, collection lifecycle, and all vector-store access."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, ScoredPoint

from mimir.config import settings


@lru_cache(maxsize=1)
def get_client() -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url)


def _path_filter(path: Path) -> models.Filter:
    return models.Filter(
        must=[
            models.FieldCondition(
                key="path",
                match=models.MatchValue(value=str(path.resolve())),
            )
        ]
    )


def ensure_collection(client: QdrantClient | None = None) -> None:
    """Create the collection if it doesn't exist, plus payload indexes."""
    client = client or get_client()
    if client.collection_exists(settings.collection):
        return

    client.create_collection(
        collection_name=settings.collection,
        vectors_config=models.VectorParams(
            size=settings.vector_size,
            distance=models.Distance.COSINE,
        ),
    )

    # Pre-index payload fields we'll filter on so it's cheap at query time.
    for field in ("path", "ext", "folder", "title"):
        client.create_payload_index(
            collection_name=settings.collection,
            field_name=field,
            field_schema=models.PayloadSchemaType.KEYWORD,
        )
    # file_hash is used for change detection — keep it indexed for fast lookup
    client.create_payload_index(
        collection_name=settings.collection,
        field_name="file_hash",
        field_schema=models.PayloadSchemaType.KEYWORD,
    )


def drop_collection(client: QdrantClient | None = None) -> None:
    client = client or get_client()
    if client.collection_exists(settings.collection):
        client.delete_collection(settings.collection)


def collection_info(client: QdrantClient | None = None):
    client = client or get_client()
    if not client.collection_exists(settings.collection):
        return None
    return client.get_collection(settings.collection)


def count_chunks() -> int:
    return get_client().count(settings.collection).count


def get_file_hash(path: Path) -> str | None:
    """Return the stored file_hash for any one chunk of `path`, if indexed."""
    result, _ = get_client().scroll(
        collection_name=settings.collection,
        scroll_filter=_path_filter(path),
        limit=1,
        with_payload=["file_hash"],
        with_vectors=False,
    )
    if not result:
        return None
    return result[0].payload.get("file_hash") if result[0].payload else None


def delete_file_chunks(path: Path) -> None:
    """Drop every chunk previously indexed for `path`."""
    get_client().delete(
        collection_name=settings.collection,
        points_selector=models.FilterSelector(filter=_path_filter(path)),
    )


def build_chunk_point(point_id: int, vector: list[float], payload: dict) -> PointStruct:
    """Construct a point for upsert. Keeps the Qdrant type behind the seam."""
    return PointStruct(id=point_id, vector=vector, payload=payload)


def upsert_chunks(points: list[PointStruct]) -> None:
    get_client().upsert(settings.collection, points=points)


def search_chunks(
    vec: list[float],
    *,
    folder: str | None = None,
    ext: str | None = None,
    title: str | None = None,
    k: int = 5,
) -> list[ScoredPoint]:
    """Vector search with optional payload filters. Returns scored points."""
    must: list[models.Condition] = []
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

    result = get_client().query_points(
        collection_name=settings.collection,
        query=vec,
        query_filter=qfilter,
        limit=k,
        with_payload=True,
    )
    return result.points
