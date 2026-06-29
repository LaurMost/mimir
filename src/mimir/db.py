"""Qdrant client and collection lifecycle."""

from functools import lru_cache

from qdrant_client import QdrantClient, models

from mimir.config import settings


@lru_cache(maxsize=1)
def get_client() -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url)


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
