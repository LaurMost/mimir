# Architecture

Mimir is a small, local-first pipeline. Notes go in, embeddings get stored in a
local vector database, and you query them either as semantic search or as full
RAG with a local LLM. Nothing leaves your machine.

```
┌─────────────────┐       ┌──────────────┐       ┌──────────────┐
│  notes/         │──────▶│  ingest      │──────▶│  Qdrant      │
│  (.md .pdf ...) │       │  chunk+embed │       │  (Docker)    │
└─────────────────┘       └──────────────┘       └──────┬───────┘
                                                        │
                          ┌──────────────┐              │
                          │  query       │◀─────────────┘
                          │  (semantic)  │
                          └──────────────┘
                                                        │
                          ┌──────────────┐       ┌──────▼───────┐
                          │  chat        │◀──────│  Ollama      │
                          │  (RAG)       │       │  (local LLM) │
                          └──────────────┘       └──────────────┘
```

## Components

- **Qdrant** — vector store, single Docker container.
- **fastembed** — embeddings via `BAAI/bge-small-en-v1.5` (384d, ONNX, runs
  natively on Apple Silicon).
- **Ollama** — local LLM for the chat command (optional).
- **Typer** — single `mimir` CLI for everything.

## Data flow

1. **Ingest** walks the notes directory, chunks each document, embeds the chunks
   with fastembed, and upserts the vectors into Qdrant. Unchanged files are
   skipped on re-ingest.
2. **Query** embeds your search text and returns the top-k most similar chunks
   straight from Qdrant — no LLM involved.
3. **Chat** retrieves the relevant chunks, then passes them to a local Ollama
   model as context, returning an answer with citations back to your notes.
