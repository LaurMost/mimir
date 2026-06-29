#!/usr/bin/env bash
# Claude Code PostToolUse hook: format edited Python files with black + ruff --fix.
# Fails open (advisory) and only touches .py files.
set -euo pipefail

input=$(cat)

file=$(printf '%s' "$input" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    print(""); sys.exit(0)
ti = d.get("tool_input", {}) or {}
print(ti.get("file_path") or ti.get("path") or "")
')

case "$file" in
  *.py) ;;
  *) exit 0 ;;
esac

[ -f "$file" ] || exit 0

uv run black --quiet "$file" >/dev/null 2>&1 || true
uv run ruff check --fix --quiet "$file" >/dev/null 2>&1 || true
exit 0
