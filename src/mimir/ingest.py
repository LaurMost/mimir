"""Ingestion: walk files, chunk, embed, upsert into Qdrant."""

from __future__ import annotations

import hashlib
from pathlib import Path

from qdrant_client import models
from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from mimir.chunking import chunk_text
from mimir.config import settings
from mimir.db import ensure_collection, get_client
from mimir.embeddings import embed_documents
from mimir.loaders import discover_files, load_text

console = Console()


def _file_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _point_id(path: Path, chunk_idx: int) -> int:
    h = hashlib.sha256(f"{path.resolve()}:{chunk_idx}".encode()).hexdigest()
    return int(h[:16], 16)  # 64-bit unsigned int


def _existing_hash_for_path(client, path: Path) -> str | None:
    """Look up any one point for this path to get its stored file_hash."""
    result, _ = client.scroll(
        collection_name=settings.collection,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="path",
                    match=models.MatchValue(value=str(path.resolve())),
                )
            ]
        ),
        limit=1,
        with_payload=["file_hash"],
        with_vectors=False,
    )
    if not result:
        return None
    return result[0].payload.get("file_hash")


def _delete_points_for_path(client, path: Path) -> None:
    client.delete(
        collection_name=settings.collection,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="path",
                        match=models.MatchValue(value=str(path.resolve())),
                    )
                ]
            )
        ),
    )


def ingest_path(root: Path, *, force: bool = False) -> dict:
    """
    Ingest all supported files under `root`.
    Returns stats: {files_seen, files_indexed, files_skipped, chunks_upserted}.
    """
    if not root.exists():
        raise FileNotFoundError(f"Notes directory not found: {root}")

    client = get_client()
    ensure_collection(client)

    files = discover_files(root)
    if not files:
        console.print(f"[yellow]No supported files found in {root}[/yellow]")
        return {"files_seen": 0, "files_indexed": 0, "files_skipped": 0, "chunks_upserted": 0}

    stats = {
        "files_seen": len(files),
        "files_indexed": 0,
        "files_skipped": 0,
        "chunks_upserted": 0,
    }
    buffer: list[models.PointStruct] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Ingesting", total=len(files))

        for path in files:
            progress.update(task, description=f"[cyan]{path.name}")
            try:
                text = load_text(path)
            except Exception as e:
                console.print(f"[red]  skip {path}: {e}[/red]")
                progress.advance(task)
                continue

            if not text.strip():
                progress.advance(task)
                continue

            file_hash = _file_hash(text)

            if not force:
                existing = _existing_hash_for_path(client, path)
                if existing == file_hash:
                    stats["files_skipped"] += 1
                    progress.advance(task)
                    continue
                if existing is not None:
                    # File changed — drop old chunks before re-indexing
                    _delete_points_for_path(client, path)

            chunks = chunk_text(text)
            if not chunks:
                progress.advance(task)
                continue

            vectors = embed_documents(chunks)

            try:
                folder = str(path.parent.relative_to(root))
            except ValueError:
                folder = "."

            for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
                buffer.append(
                    models.PointStruct(
                        id=_point_id(path, i),
                        vector=vec,
                        payload={
                            "text": chunk,
                            "path": str(path.resolve()),
                            "title": path.stem,
                            "folder": folder,
                            "ext": path.suffix.lower(),
                            "chunk_idx": i,
                            "file_hash": file_hash,
                        },
                    )
                )
                if len(buffer) >= settings.batch_size:
                    client.upsert(settings.collection, points=buffer)
                    stats["chunks_upserted"] += len(buffer)
                    buffer = []

            stats["files_indexed"] += 1
            progress.advance(task)

    if buffer:
        client.upsert(settings.collection, points=buffer)
        stats["chunks_upserted"] += len(buffer)

    return stats
