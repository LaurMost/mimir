#!/usr/bin/env bash
# Cursor afterFileEdit hook: format edited Python files with black + ruff --fix.
# Fails open (never blocks an edit) and only touches .py files.
set -euo pipefail

input=$(cat)

file=$(printf '%s' "$input" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    print(""); sys.exit(0)
for k in ("file_path", "path", "filePath"):
    v = d.get(k)
    if isinstance(v, str) and v:
        print(v); break
else:
    print("")
')

case "$file" in
  *.py) ;;
  *) exit 0 ;;
esac

[ -f "$file" ] || exit 0

uv run black --quiet "$file" >/dev/null 2>&1 || true
uv run ruff check --fix --quiet "$file" >/dev/null 2>&1 || true
exit 0
