---
title: Configuration
---

# Configuration

Mimir reads all configuration from environment variables prefixed with `MIMIR_`,
or from a `.env` file in the working directory. Every setting has a sensible
default, so a zero-config install works out of the box.

Copy the example file to get started:

```bash
cp .env.example .env
```

## Full reference

All variables, their defaults, and what they control:

| Variable | Default | Description |
|---|---|---|
| `MIMIR_QDRANT_URL` | `http://localhost:6333` | URL of the Qdrant instance. |
| `MIMIR_COLLECTION` | `mimir` | Name of the Qdrant collection to read/write. |
| `MIMIR_EMBED_MODEL` | `BAAI/bge-small-en-v1.5` | fastembed model used for embeddings. |
| `MIMIR_VECTOR_SIZE` | `384` | Dimensionality of the embedding vectors. **Must match the model.** |
| `MIMIR_CHUNK_SIZE` | `1200` | Target chunk size in characters (range `200`–`8000`). |
| `MIMIR_CHUNK_OVERLAP` | `150` | Overlap between adjacent chunks in characters (range `0`–`1000`). |
| `MIMIR_NOTES_DIR` | `./notes` | Default directory ingested when no path is given. |
| `MIMIR_BATCH_SIZE` | `256` | Number of points upserted to Qdrant per batch. |
| `MIMIR_OLLAMA_URL` | `http://localhost:11434` | URL of the Ollama server (used only by `chat`). |
| `MIMIR_OLLAMA_MODEL` | `qwen2.5:7b-instruct` | Ollama model used for RAG answers. |

!!! info "Validation"
    `MIMIR_CHUNK_SIZE` and `MIMIR_CHUNK_OVERLAP` are validated at startup. Values
    outside their ranges raise a configuration error rather than silently
    misbehaving.

## Example `.env`

```env title=".env"
# Qdrant
MIMIR_QDRANT_URL=http://localhost:6333
MIMIR_COLLECTION=mimir

# Embeddings
MIMIR_EMBED_MODEL=BAAI/bge-small-en-v1.5
MIMIR_VECTOR_SIZE=384

# Chunking
MIMIR_CHUNK_SIZE=1200
MIMIR_CHUNK_OVERLAP=150

# Ingestion
MIMIR_NOTES_DIR=./notes
MIMIR_BATCH_SIZE=256

# Ollama (only used by `mimir chat`)
MIMIR_OLLAMA_URL=http://localhost:11434
MIMIR_OLLAMA_MODEL=qwen2.5:7b-instruct
```

## Choosing an embedding model

If you change `MIMIR_EMBED_MODEL`, you almost certainly need a matching
`MIMIR_VECTOR_SIZE`, and the collection must be recreated:

```bash
uv run mimir reset
uv run mimir ingest
```

Good upgrade paths from the default:

| Model | Dims | Notes |
|---|---|---|
| `BAAI/bge-small-en-v1.5` | 384 | Default. Fast, good for ≤500k chunks. |
| `BAAI/bge-base-en-v1.5` | 768 | ~2× slower, noticeably better recall. |
| `BAAI/bge-m3` | 1024 | Multilingual; dense + sparse + multi-vector. |
| `intfloat/multilingual-e5-large` | 1024 | Strong multilingual option. |

!!! warning "Changing the model invalidates existing vectors"
    Embeddings from different models are not comparable. After swapping the model,
    always `reset` and re-`ingest`, otherwise queries return nonsense.

## Tuning chunking

- **Larger `MIMIR_CHUNK_SIZE`** keeps more context together (better for prose and
  long-form notes) but reduces retrieval precision.
- **Larger `MIMIR_CHUNK_OVERLAP`** reduces the chance of splitting a relevant
  passage across two chunks, at the cost of more vectors to store.

Defaults (`1200` / `150`) are a good balance for typical Markdown notes.
