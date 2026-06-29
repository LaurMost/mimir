#!/usr/bin/env bash
# Claude Code PreToolUse(Bash) hook: gate destructive git commands.
# Exit 2 blocks the command (reason goes to Claude on stderr); a force push asks.
set -euo pipefail

input=$(cat)

command=$(printf '%s' "$input" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    print(""); sys.exit(0)
print((d.get("tool_input", {}) or {}).get("command", "") or "")
')

cmd=$(printf '%s' "$command" | tr -s ' ')

block() { echo "$1" >&2; exit 2; }

if printf '%s' "$cmd" | grep -Eq 'git +reset +--hard'; then
  block "Blocked by safety hook: git reset --hard is destructive. Run it manually if you really mean to."
fi

if printf '%s' "$cmd" | grep -Eq 'git +clean +-[a-zA-Z]*f'; then
  block "Blocked by safety hook: git clean -f deletes untracked files. Run it manually if intended."
fi

if printf '%s' "$cmd" | grep -Eq 'git +push +.*(--force|-f)([ =]|$)'; then
  cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Force push detected; confirm before continuing."}}
JSON
  exit 0
fi

exit 0
