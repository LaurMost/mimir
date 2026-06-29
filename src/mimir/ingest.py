"""Ingestion: walk files, chunk, embed, upsert into Qdrant."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from pathlib import Path

from qdrant_client.http.models import PointStruct

from mimir.chunking import chunk_text
from mimir.config import settings
from mimir.db import (
    build_chunk_point,
    delete_file_chunks,
    ensure_collection,
    get_file_hash,
    upsert_chunks,
)
from mimir.embeddings import embed_documents
from mimir.loaders import discover_files, load_text

ProgressCallback = Callable[[str, int, int], None]


def _file_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _point_id(path: Path, chunk_idx: int) -> int:
    h = hashlib.sha256(f"{path.resolve()}:{chunk_idx}".encode()).hexdigest()
    return int(h[:16], 16)  # 64-bit unsigned int


def _empty_stats() -> dict:
    return {
        "files_seen": 0,
        "files_indexed": 0,
        "files_skipped": 0,
        "chunks_upserted": 0,
        "errors": [],
    }


def ingest_path(
    root: Path,
    *,
    force: bool = False,
    on_progress: ProgressCallback | None = None,
) -> dict:
    """
    Ingest all supported files under `root`.

    `on_progress(filename, current, total)` is called once per file as it is
    processed; pass None to run silently. The pipeline produces no console
    output of its own — the caller renders progress, errors, and summary.

    Returns stats:
    {files_seen, files_indexed, files_skipped, chunks_upserted, errors}.
    `errors` is a list of (path, message) tuples for files that failed to load.
    """
    if not root.exists():
        raise FileNotFoundError(f"Notes directory not found: {root}")

    ensure_collection()

    files = discover_files(root)
    if not files:
        return _empty_stats()

    stats = _empty_stats()
    stats["files_seen"] = len(files)
    total = len(files)
    buffer: list[PointStruct] = []

    for current, path in enumerate(files, 1):
        if on_progress is not None:
            on_progress(path.name, current, total)

        try:
            text = load_text(path)
        except Exception as e:
            stats["errors"].append((str(path), str(e)))
            continue

        if not text.strip():
            continue

        file_hash = _file_hash(text)

        if not force:
            existing = get_file_hash(path)
            if existing == file_hash:
                stats["files_skipped"] += 1
                continue
            if existing is not None:
                # File changed — drop old chunks before re-indexing
                delete_file_chunks(path)

        chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)
        if not chunks:
            continue

        vectors = embed_documents(chunks)

        try:
            folder = str(path.parent.relative_to(root))
        except ValueError:
            folder = "."

        for i, (chunk, vec) in enumerate(zip(chunks, vectors, strict=True)):
            buffer.append(
                build_chunk_point(
                    _point_id(path, i),
                    vec,
                    {
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
                upsert_chunks(buffer)
                stats["chunks_upserted"] += len(buffer)
                buffer = []

        stats["files_indexed"] += 1

    if buffer:
        upsert_chunks(buffer)
        stats["chunks_upserted"] += len(buffer)

    return stats
