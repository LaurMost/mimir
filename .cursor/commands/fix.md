Auto-format and auto-fix the Mimir codebase, then report what changed:

```bash
uv run black src tests
uv run ruff check --fix src tests
```

After running, show a short summary of the files black/ruff modified and flag any
remaining ruff issues that require a manual fix.
