# AGENTS.md

Guidance for AI coding agents (Cursor, Claude Code, Codex, and others) working in
this repository. This file is the single source of truth; tool-specific files
(`CLAUDE.md`, `.cursor/rules/`, `.codex/config.toml`) point back here.

## What Mimir is

Mimir is a local-first "second brain" CLI. It ingests a folder of notes into a
local [Qdrant](https://qdrant.tech/) vector store and answers questions about
them, either as fast semantic search or full RAG via a local
[Ollama](https://ollama.ai/) model. Everything runs offline; nothing leaves the
machine.

## Stack

- Python 3.11+ (CI matrix: 3.11, 3.12, 3.13)
- [Typer](https://typer.tiangolo.com/) CLI + [Rich](https://rich.readthedocs.io/) output
- [Qdrant](https://qdrant.tech/) vector store (Docker)
- [fastembed](https://github.com/qdrant/fastembed) embeddings (`BAAI/bge-small-en-v1.5`, 384d, ONNX)
- [Ollama](https://ollama.ai/) for the `chat` command (optional)
- [pydantic-settings](https://docs.pydantic.dev/) config from `MIMIR_*` env / `.env`
- Tooling: [uv](https://github.com/astral-sh/uv), ruff, black, mypy, pytest
- Docs: MkDocs + Material (`mkdocs.yml`, `docs/`)

## Setup

```bash
uv sync --extra dev        # install with dev deps
uv run pre-commit install  # git hooks
docker compose up -d        # start Qdrant (REST 6333, gRPC 6334)
```

## Canonical commands

Always run tools through `uv`. Prefer the `make` targets when they exist.

| Task | Command |
|---|---|
| Format | `make fmt` (`uv run black src tests`) |
| Lint | `make lint` (`uv run ruff check src tests` + `black --check`) |
| Type check | `make typecheck` (`uv run mypy src`) |
| Tests | `make test` (`uv run pytest -v --cov=mimir --cov-report=term-missing`) |
| Run the CLI | `uv run mimir <command>` |
| Build docs (strict) | `uv run mkdocs build --strict` |
| Serve docs | `uv run mkdocs serve` |

Before committing, code must pass: `ruff check`, `black --check`, `mypy src`,
and `pytest`. CI enforces all four plus a Qdrant integration smoke test on `main`.

## Repo layout

```
src/mimir/
  cli.py         Typer app + all subcommands
  config.py      pydantic-settings Settings (MIMIR_* / .env)
  db.py          Qdrant client + collection lifecycle
  embeddings.py  cached fastembed wrapper
  loaders.py     file loaders (.md .txt .pdf .rst .org)
  chunking.py    sliding-window chunker
  ingest.py      walk -> chunk -> embed -> upsert pipeline
  query.py       semantic search + Hit dataclass
  chat.py        RAG: retrieve -> prompt -> stream Ollama
tests/           pytest suite (conftest isolates env)
docs/            MkDocs site (see docs/contributing.md)
```

CLI commands: `status`, `ingest`, `query`, `chat`, `watch`, `reset`, `version`.

## Code style

- **black**, line length 88. Formatting is black's job; do not hand-format.
- **ruff** rule set: `E F I B UP RUF SIM PL S`. `E501` is ignored (black owns
  line length). Respect the existing per-file ignores in
  [pyproject.toml](pyproject.toml) and understand why they exist before changing
  them:
  - `cli.py`: `B008` (Typer's `typer.Argument(...)`/`Option(...)` in defaults is
    the canonical pattern), `S603`/`S607` (the `watch` command deliberately
    shells out to `fswatch`), `S101`, `PLC0415` (intentional lazy imports).
  - `loaders.py`: `PLC0415` (lazy `pypdf` import), `S112` (skip corrupt PDF page).
  - `chat.py`: `S113` (Ollama streaming is intentionally untimed).
  - tests: `S101`, `PLR2004`, `PLC0415`.
- **Type hints** on public functions; `from __future__ import annotations` at the
  top of modules. mypy targets 3.12 but runtime floor is 3.11.
- **Lazy heavy imports**: import expensive/optional deps (`pypdf`, `shutil.which`)
  inside the function that needs them, not at module top. Follow the existing
  pattern rather than "fixing" it.
- Comments explain non-obvious intent only; don't narrate the code.

## Testing conventions

- Tests live in `tests/`, next to existing ones. The suite is fast and runs
  without external services (`conftest.py` isolates the environment).
- Integration tests that need Qdrant are named `tests/test_integration_*.py` and
  only run in CI's `integration` job.
- Coverage floor is 35% (`fail_under = 35`); ratchet up, never down.
- Don't import a module two ways in one file (CodeQL `py/import-and-import-from`).

## Configuration

All config is `MIMIR_*` env vars or `.env` (see `.env.example`). Defaults live in
[src/mimir/config.py](src/mimir/config.py). Changing `MIMIR_EMBED_MODEL` requires a
matching `MIMIR_VECTOR_SIZE` and a `mimir reset` + re-ingest.

## Git & PR workflow

- Branch from `main`: `<type>/<short-slug>` (e.g. `feat/sparse-vectors`,
  `fix/empty-pdf-crash`, `docs/quickstart`).
- **Conventional commits**: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`,
  `ci`, `deps`. PR titles are validated by a CI workflow. Keep commits atomic.
- `main` is protected: required checks (Lint, Test 3.11/3.12/3.13, CodeQL) must
  pass and **1 approving review** is required. An author cannot approve their own
  PR; maintainers land their own PRs with an admin squash-merge.
- Flow: create branch -> commit -> `git push -u origin <branch>` ->
  `gh pr create` -> wait for checks -> squash-merge -> delete branch.
- Pass commit messages and PR bodies via a heredoc to preserve formatting.

## Never commit

- `.env` or any secrets
- `qdrant_storage/` (vector DB data)
- `notes/` contents (personal data; only `notes/.gitkeep` is tracked)
- `site/`, `.cache/` (MkDocs build output)

## Safety

- Don't run destructive git commands (`push --force` to `main`, `reset --hard`,
  `clean -fd`) unless explicitly asked.
- Don't change `git` config, skip hooks, or weaken CI/branch protection.
- Don't commit unless explicitly asked.
