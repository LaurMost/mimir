# CLAUDE.md

@AGENTS.md

The shared project guide above is the source of truth. Claude Code specifics:

- Project hooks and permissions live in `.claude/settings.json` (a formatter runs
  after edits; a guard gates destructive git commands).
- Reusable slash commands are in `.claude/commands/` (`/check`, `/fix`, `/docs`,
  `/smoke`).
- Project skills are in `.claude/skills/` (`code-review`, `open-pr`, `cut-release`).
- Personal, uncommitted overrides go in `.claude/settings.local.json` (gitignored).
