---
name: code-review
description: Review code changes against Mimir's repository standards (ruff/black/mypy, tests and coverage, conventional commits, security rule rationale, and what must never be committed). Use when reviewing a PR, a branch, or local changes in the Mimir repo.
---

# Code review (Mimir standards)

Review changes against this repo's actual conventions, not generic advice. Source
of truth is [AGENTS.md](../../../AGENTS.md).

## What to check

1. Quality gate passes:
   ```bash
   uv run ruff check src tests
   uv run black --check src tests
   uv run mypy src
   uv run pytest -q --cov=mimir --cov-report=term-missing
   ```
2. Style: black line length 88; type hints on public functions;
   `from __future__ import annotations` at module top.
3. Heavy/optional imports (`pypdf`, `shutil.which`) stay lazy inside the function
   that uses them, matching `cli.py` / `loaders.py`. Flag any hoisted to module top.
4. `ruff` per-file ignores in `pyproject.toml` are respected and not silently
   widened (Typer `B008`, `S603/S607` fswatch shell-out, `S113` Ollama streaming,
   `PLC0415` lazy imports).
5. Tests: new behavior has tests; suite stays runnable without external services;
   integration tests are `test_integration_*.py`; coverage stays >= 35%.
6. No module imported two ways in one file (CodeQL `py/import-and-import-from`).
7. Commit/PR hygiene: conventional commit types, branch `<type>/<short-slug>`.
8. Nothing forbidden is committed: `.env`, `qdrant_storage/`, `notes/` contents,
   `site/`, `.cache/`.

## Output format

Group findings by severity:

- **Critical**: must fix before merge (bugs, security, broken gate, secrets).
- **Suggestion**: should improve (style drift, missing tests, unclear naming).
- **Nice to have**: optional polish.

End with a one-line verdict: ready to merge, or the blocking items.
