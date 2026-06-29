# Contributing to Mimir

Mimir is a personal project, but PRs and issues are welcome. Below is the dev workflow.

## Setup

```bash
git clone https://github.com/yourname/mimir.git
cd mimir
uv sync --extra dev
uv run pre-commit install
docker compose up -d   # start Qdrant for integration work
```

## Day-to-day

| Command | What it does |
|---|---|
| `make fmt` | Ruff format |
| `make lint` | Ruff check |
| `uv run pytest` | Run the test suite |
| `uv run mimir <cmd>` | Run the CLI from your working copy |

Pre-commit will auto-run ruff on staged files. If you bypass it, CI will catch the same issues.

## Branching & commits

- Branch from `main`. Name branches `<type>/<short-slug>` — e.g. `feat/sparse-vectors`, `fix/empty-pdf-crash`, `chore/dependabot-grouping`.
- Conventional commit prefixes: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`, `deps`.
- Keep commits atomic. A PR should tell one story.

## Tests

Add tests next to existing ones in `tests/`. The suite is fast and runs without external services thanks to `conftest.py` isolating the environment. Integration tests that need Qdrant live in `tests/test_integration_*.py` and only run in CI's `integration` job.

## Releasing

See [`RELEASING.md`](./RELEASING.md).
