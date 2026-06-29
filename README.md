# Mimir

[![CI](https://github.com/yourname/mimir/actions/workflows/ci.yml/badge.svg)](https://github.com/yourname/mimir/actions/workflows/ci.yml)
[![Release](https://github.com/yourname/mimir/actions/workflows/release.yml/badge.svg)](https://github.com/yourname/mimir/actions/workflows/release.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> *"And there sat Odin, before the well, and asked counsel of the head of Mimir."*

**A local-first second brain.** Your notes get embedded into a Qdrant vector store running on your Mac, and you ask Mimir questions about them — either as semantic search or full RAG with a local LLM.

Everything runs offline. No tokens leave your machine.

## Architecture

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

- **Qdrant** — vector store, single Docker container
- **fastembed** — embeddings via `BAAI/bge-small-en-v1.5` (384d, ONNX, runs natively on Apple Silicon)
- **Ollama** — local LLM for the chat command (optional)
- **Typer** — single `mimir` CLI for everything

## Quick start

```bash
# 1. Prereqs
brew install --cask orbstack   # or Docker Desktop; OrbStack is lighter on M-series
brew install uv ollama         # ollama only if you want the chat command

# 2. Clone + install
git clone <this-repo> mimir && cd mimir
uv sync

# 3. Start Qdrant
docker compose up -d

# 4. Point Mimir at your notes (symlink your Obsidian vault, or just drop files in)
ln -s ~/Documents/Obsidian/MyVault notes/vault

# 5. Ingest
uv run mimir ingest

# 6. Ask
uv run mimir query "what did I conclude about market making on Polymarket"

# 7. (optional) Full RAG chat
ollama pull qwen2.5:7b-instruct
uv run mimir chat "summarise my notes on tailoring fabric sourcing"
```

## Commands

| Command | What it does |
|---|---|
| `mimir status` | Collection stats — how many points, which model, disk size |
| `mimir ingest [PATH]` | Walk path, chunk, embed, upsert. Default: `./notes`. Skips unchanged files. |
| `mimir query "<text>"` | Top-k semantic search with rich previews |
| `mimir chat "<text>"` | Retrieve + ask local LLM with citations |
| `mimir watch [PATH]` | Re-ingest on file changes (needs `fswatch`) |
| `mimir reset` | Drop and recreate the collection (asks for confirmation) |

Each command takes `--help` for full options.

## Configuration

Everything is configurable via `.env` (copy `.env.example` to `.env`). Sensible defaults:

```env
MIMIR_QDRANT_URL=http://localhost:6333
MIMIR_COLLECTION=mimir
MIMIR_EMBED_MODEL=BAAI/bge-small-en-v1.5
MIMIR_VECTOR_SIZE=384
MIMIR_CHUNK_SIZE=1200
MIMIR_CHUNK_OVERLAP=150
MIMIR_OLLAMA_URL=http://localhost:11434
MIMIR_OLLAMA_MODEL=qwen2.5:7b-instruct
MIMIR_NOTES_DIR=./notes
```

## Upgrading the embedding model

If you swap `MIMIR_EMBED_MODEL`, you almost certainly need a new `MIMIR_VECTOR_SIZE` and the collection must be recreated:

```bash
uv run mimir reset
uv run mimir ingest
```

Good upgrade paths from the default:

| Model | Dims | Notes |
|---|---|---|
| `BAAI/bge-small-en-v1.5` | 384 | Default. Fast, good for ≤500k chunks. |
| `BAAI/bge-base-en-v1.5` | 768 | ~2× slower, noticeably better recall. |
| `BAAI/bge-m3` | 1024 | Multilingual, supports dense + sparse + multi-vector. |
| `intfloat/multilingual-e5-large` | 1024 | Strong multilingual option. |

## Backup

Mimir stores everything in `./qdrant_storage`. Stop the container and snapshot:

```bash
docker compose stop
tar czf mimir-backup-$(date +%F).tgz qdrant_storage
docker compose start
```

Or just re-ingest from your notes — embeddings are cheap to regenerate.

## Development

```bash
uv sync --extra dev          # install with dev deps
uv run pre-commit install    # set up git hooks
uv run pytest                # run tests
make lint && make fmt        # ruff
```

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the workflow and [RELEASING.md](./RELEASING.md) for cutting versions.

## Suggested GitHub repo settings

When you create the GitHub repo, paste this as the description:

> Local-first second brain — Qdrant + fastembed + Ollama on your Mac.

And add these topics so it's discoverable:

`vector-database` · `qdrant` · `rag` · `second-brain` · `local-first` · `embeddings` · `python` · `cli` · `personal-knowledge-management` · `obsidian` · `fastembed` · `ollama` · `apple-silicon`

## License

MIT
