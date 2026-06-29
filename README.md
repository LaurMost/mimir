<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/wordmark-on-dark.svg">
    <img src="assets/logo/wordmark.svg" alt="Mimir" width="460">
  </picture>
</p>

<p align="center"><em>"The well remembers."</em></p>

<p align="center">
  <a href="https://laurmost.github.io/mimir/"><img src="https://img.shields.io/badge/docs-mimir-F2EBDD?style=for-the-badge&labelColor=0B0B0D" alt="Documentation"></a>
  <a href="https://github.com/LaurMost/mimir/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/LaurMost/mimir/ci.yml?branch=main&style=for-the-badge" alt="CI status"></a>
  <a href="https://github.com/LaurMost/mimir/releases"><img src="https://img.shields.io/github/v/release/LaurMost/mimir?include_prereleases&style=for-the-badge" alt="Latest release"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.11+-blue?style=for-the-badge" alt="Python 3.11+"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge" alt="MIT License"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge" alt="Ruff"></a>
</p>

**Mimir is a local-first second brain.** Your notes are embedded into a Qdrant vector store running on your own Mac, and you ask Mimir questions about them — either as fast semantic search or as full RAG answers from a local LLM. Everything runs offline; no tokens ever leave your machine.

> *"And there sat Odin, before the well, and asked counsel of the head of Mimir."*

[Documentation](https://laurmost.github.io/mimir/) · [Quick start](#quick-start) · [Commands](#commands) · [Configuration](#configuration) · [Architecture](docs/reference/architecture.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [Security](.github/SECURITY.md)

## Highlights

- **Local-first, private by default** — runs entirely on your machine; no tokens leave your Mac.
- **Semantic search** across `.md`, `.pdf`, and more — top-k results with rich previews.
- **Full RAG chat** with citations back to your notes, powered by any local Ollama model.
- **Native Apple Silicon embeddings** via fastembed (`BAAI/bge-small-en-v1.5`, ONNX, no GPU required).
- **Incremental ingestion** — re-ingesting skips unchanged files automatically.
- **Live re-indexing** — `mimir watch` re-ingests on save.
- **Swappable models** — change the embedding model or LLM with a single `.env` value.

## Quick start

```bash
# 1. Prereqs
brew install --cask orbstack   # or Docker Desktop; OrbStack is lighter on M-series
brew install uv ollama         # ollama only if you want the chat command

# 2. Clone + install
git clone https://github.com/LaurMost/mimir.git && cd mimir
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

See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and [RELEASING.md](RELEASING.md) for cutting versions.

## Documentation

Full documentation lives at **[laurmost.github.io/mimir](https://laurmost.github.io/mimir/)** — getting-started guides, tutorials, a complete CLI reference, configuration, architecture, and an FAQ.

| I want to… | Go to |
|---|---|
| Read the full docs | [laurmost.github.io/mimir](https://laurmost.github.io/mimir/) |
| Get up and running | [Quickstart](https://laurmost.github.io/mimir/getting-started/quickstart/) |
| See every command | [CLI reference](https://laurmost.github.io/mimir/reference/cli/) |
| Tune models and chunking | [Configuration](https://laurmost.github.io/mimir/getting-started/configuration/) |
| Ingest an Obsidian vault | [Guide](https://laurmost.github.io/mimir/guides/ingest-obsidian/) |
| Understand how it fits together | [Architecture](https://laurmost.github.io/mimir/reference/architecture/) |
| Troubleshoot a problem | [FAQ](https://laurmost.github.io/mimir/faq/) |
| Contribute or set up the dev loop | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Cut a release | [RELEASING.md](RELEASING.md) |
| See what changed | [CHANGELOG.md](CHANGELOG.md) |
| Report a vulnerability | [SECURITY.md](.github/SECURITY.md) |

## License

[MIT](LICENSE)
