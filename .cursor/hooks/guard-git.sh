#!/usr/bin/env bash
# Cursor beforeShellExecution hook: gate destructive git commands.
# Denies clearly destructive operations and asks before a force push.
set -euo pipefail

input=$(cat)

command=$(printf '%s' "$input" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    print(""); sys.exit(0)
print(d.get("command", "") or "")
')

emit() { printf '%s\n' "$1"; exit 0; }

cmd=$(printf '%s' "$command" | tr -s ' ')

if printf '%s' "$cmd" | grep -Eq 'git +reset +--hard'; then
  emit '{"permission":"deny","user_message":"Blocked: git reset --hard is destructive. Run it manually if you really mean to.","agent_message":"A safety hook blocked git reset --hard."}'
fi

if printf '%s' "$cmd" | grep -Eq 'git +clean +-[a-zA-Z]*f'; then
  emit '{"permission":"deny","user_message":"Blocked: git clean -f deletes untracked files. Run it manually if intended.","agent_message":"A safety hook blocked git clean -f."}'
fi

if printf '%s' "$cmd" | grep -Eq 'git +push +.*(--force|-f)([ =]|$)'; then
  emit '{"permission":"ask","user_message":"This is a force push. Confirm before continuing.","agent_message":"A safety hook flagged a force push for review."}'
fi

emit '{"permission":"allow"}'
