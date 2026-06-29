---
title: FAQ
---

# FAQ &amp; troubleshooting

## General

### Does anything leave my machine?

No. Embeddings run locally via fastembed, vectors are stored in a Qdrant
container on your machine, and `chat` uses a local Ollama model. There are no API
keys and no outbound calls for ingest, query, or chat.

### What file types can Mimir ingest?

`.md`, `.markdown`, `.txt`, `.pdf`, `.rst`, and `.org`. Other files (images,
audio, binaries) are ignored.

### Where is my data stored?

In Qdrant's storage volume, mounted at `./qdrant_storage` by the bundled
`docker-compose.yml`. Your original notes are never modified.

## Setup &amp; ingest

### `mimir status` says the collection doesn't exist

That's expected before your first ingest. Run `uv run mimir ingest` to create and
populate it.

### Ingest is slow the first time

The very first run downloads the fastembed model (a one-time cost) and embeds
every chunk. Subsequent ingests are incremental &mdash; unchanged files are
skipped via SHA-256 hashing.

### I edited notes but search shows the old content

Re-run `uv run mimir ingest`. Only changed files are re-embedded. To keep things
in sync automatically, use [`mimir watch`](guides/watching-files.md).

### How do I force a full re-index?

```bash
uv run mimir ingest --force
```

This bypasses the change-detection hash and re-embeds everything.

## Search &amp; chat

### Query results look irrelevant

A few common causes:

- The collection was built with a **different embedding model** than is currently
  configured. After changing `MIMIR_EMBED_MODEL`, you must `reset` and re-`ingest`.
- Your `MIMIR_CHUNK_SIZE` is very large, reducing retrieval precision. Try the
  defaults.
- Try increasing `--k` or removing `--folder` / `--ext` filters.

### `mimir chat` errors with an Ollama connection problem

Make sure Ollama is running and the model is pulled:

```bash
ollama serve
ollama pull qwen2.5:7b-instruct
```

`query` works without Ollama &mdash; only `chat` requires it.

### Can I use a different LLM?

Yes. Any model available to Ollama works &mdash; set `MIMIR_OLLAMA_MODEL`. See
[Local RAG chat](guides/rag-chat.md#choosing-a-model).

## Vectors &amp; models

### I changed the embedding model and everything broke

Embeddings from different models aren't comparable, and the vector dimensionality
must match `MIMIR_VECTOR_SIZE`. After swapping models:

```bash
uv run mimir reset
uv run mimir ingest
```

### How do I back up my index?

```bash
docker compose stop
tar czf mimir-backup-$(date +%F).tgz qdrant_storage
docker compose start
```

Or just re-ingest from your notes &mdash; embeddings are cheap to regenerate.

## Watching

### `mimir watch` says `fswatch not found`

Install it:

```bash
brew install fswatch
```

## Still stuck?

Open an issue on [GitHub](https://github.com/LaurMost/mimir/issues) with your OS,
Python version, and the output of `uv run mimir status`.
