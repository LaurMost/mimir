---
name: open-pr
description: Open and land a pull request using Mimir's exact workflow (branch naming, conventional commits, gh pr create, waiting for required checks, then squash-merge). Use when asked to commit, open a PR, or merge changes in the Mimir repo.
---

# Open a PR (Mimir workflow)

Only commit when explicitly asked. Source of truth is
[AGENTS.md](../../../AGENTS.md).

## Steps

```
- [ ] 1. Branch
- [ ] 2. Commit (conventional)
- [ ] 3. Push
- [ ] 4. Create PR
- [ ] 5. Wait for checks
- [ ] 6. Squash-merge + delete branch
```

1. **Branch** from `main`: `git switch -c <type>/<short-slug>`
   (`feat`/`fix`/`chore`/`docs`/`refactor`/`test`/`ci`/`deps`).
2. **Commit** with a conventional message via heredoc to preserve formatting:
   ```bash
   git add <paths>
   git commit -m "$(cat <<'EOF'
   <type>: <summary>

   <why, not just what>
   EOF
   )"
   ```
   Do not stage `.env`, `qdrant_storage/`, `notes/` contents, `site/`, `.cache/`.
3. **Push**: `git push -u origin <branch>`.
4. **Create PR** with a Summary + Test plan body via heredoc:
   ```bash
   gh pr create --base main --head <branch> --title "<type>: <summary>" --body "$(cat <<'EOF'
   ## Summary
   - ...

   ## Test plan
   - [ ] ...
   EOF
   )"
   ```
5. **Wait for required checks**: Lint, Test (3.11/3.12/3.13), CodeQL, and the
   conventional-commit title check. `gh pr checks <n>`.
6. **Merge**: `main` requires 1 approving review. An author cannot approve their
   own PR, so maintainers land their own work with an admin squash-merge:
   ```bash
   gh pr merge <n> --squash --admin --delete-branch
   ```
   Do not bypass review for someone else's PR; get a real approval instead.

## Notes

- Never force-push `main` or weaken branch protection.
- If a pre-commit hook modifies files, create a new commit (don't `--amend`
  pushed history).
