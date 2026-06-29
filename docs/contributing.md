---
title: Contributing
---

# Contributing

Mimir is a personal project, but PRs and issues are welcome. This page covers the
dev workflow and how to work on the documentation site itself.

## Setup

```bash
git clone https://github.com/LaurMost/mimir.git
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

Pre-commit auto-runs ruff on staged files. If you bypass it, CI will catch the
same issues.

## Branching &amp; commits

- Branch from `main`. Name branches `<type>/<short-slug>` &mdash; e.g.
  `feat/sparse-vectors`, `fix/empty-pdf-crash`, `chore/dependabot-grouping`.
- Conventional commit prefixes: `feat`, `fix`, `chore`, `docs`, `refactor`,
  `test`, `ci`, `deps`.
- Keep commits atomic. A PR should tell one story.

## Tests

Add tests next to existing ones in `tests/`. The suite is fast and runs without
external services thanks to `conftest.py` isolating the environment. Integration
tests that need Qdrant live in `tests/test_integration_*.py` and only run in CI's
`integration` job.

## Working on the docs

The documentation is built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

```bash
# Install the docs toolchain
uv sync --extra docs

# Live-reload preview at http://127.0.0.1:8000
uv run mkdocs serve

# Production build (fails on broken links / refs)
uv run mkdocs build --strict
```

!!! note "Social cards are CI-only"
    The `social` plugin (which renders link-preview images) needs the Cairo
    graphics stack and only runs when the `CI` environment variable is set. Local
    `mkdocs serve` skips it, so you don't need Cairo installed to preview docs.

### Docs layout

```text
docs/
├── index.md                 # Landing page (custom hero template)
├── getting-started/         # Install, quickstart, configuration
├── guides/                  # Task-focused walkthroughs
├── reference/               # CLI (auto-generated) + architecture
├── blog/                    # Changelog / release posts
├── contributing.md
├── faq.md
├── assets/                  # Logo, favicon, brand.css
└── overrides/home.html      # Custom landing-page template
```

The CLI reference is generated from `mimir.cli:app` via `mkdocs-typer`, so adding
or changing a command updates the docs automatically.

## Deploying the docs

Docs deploy automatically. On every push to `main`, the
[`docs.yml`](https://github.com/LaurMost/mimir/blob/main/.github/workflows/docs.yml)
workflow builds the site and runs `mkdocs gh-deploy --force`, which publishes to
the `gh-pages` branch.

### One-time GitHub Pages setup

A maintainer needs to enable Pages once:

1. Push the `docs.yml` workflow to `main` (it creates the `gh-pages` branch on its
   first successful run).
2. In the repository, go to **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. Set the branch to **`gh-pages`** and the folder to **`/ (root)`**, then save.

The site goes live at `https://laurmost.github.io/mimir/` within a minute or two.

## Releasing

See [`RELEASING.md`](https://github.com/LaurMost/mimir/blob/main/RELEASING.md).
