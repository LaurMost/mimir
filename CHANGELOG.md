# Changelog

All notable changes to Mimir are documented here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-29

### Added
- Qdrant vector store via `docker-compose.yml` (REST on 6333, gRPC on 6334)
- Embeddings via `fastembed` with `BAAI/bge-small-en-v1.5` (384d) as default
- Typer-based `mimir` CLI with subcommands: `status`, `ingest`, `query`, `chat`, `reset`, `watch`, `version`
- Pydantic-settings configuration loaded from `MIMIR_*` environment variables and `.env`
- Per-file SHA-256 change detection — `mimir ingest` skips unchanged files automatically
- Markdown/text/PDF/RST/org file loaders
- Paragraph- and sentence-aware text chunker with configurable size and overlap
- Pre-indexed payload fields (`path`, `ext`, `folder`, `title`, `file_hash`) for fast filtered search
- Streaming RAG chat via local Ollama (`mimir chat`)
- Auto-reingest on file change via `mimir watch` (requires `fswatch`)
- Test suite covering chunking, config validation, loaders, and smoke imports
- CI workflow: lint + multi-Python-version tests + Qdrant integration smoke test
- Release workflow: triggered on `v*.*.*` tags, builds wheel/sdist, creates GitHub Release
- Dependabot for weekly Python/Actions and monthly Docker updates
- Pre-commit hooks (ruff, hygiene checks)
- Issue and PR templates

[Unreleased]: https://github.com/yourname/mimir/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourname/mimir/releases/tag/v0.1.0
