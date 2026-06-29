Run a local end-to-end smoke test of the Mimir pipeline against a throwaway
collection (requires Docker). Use an isolated collection so real data is untouched:

```bash
docker compose up -d
export MIMIR_COLLECTION=local_smoke
mkdir -p notes
printf '# Hello\nA note about avellaneda-stoikov market making.\n' > notes/_smoke.md
uv run mimir status
uv run mimir ingest notes
uv run mimir query "market making" --k 1
uv run mimir reset --yes
rm -f notes/_smoke.md
unset MIMIR_COLLECTION
```

Report whether ingest produced points and the query returned a hit.
