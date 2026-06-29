---
name: cut-release
description: Cut a Mimir release following SemVer and the repo's release workflow (bump pyproject version, update CHANGELOG, tag vX.Y.Z, push). Use when asked to release, bump the version, or tag a new version of Mimir.
---

# Cut a release (Mimir)

Mimir uses SemVer and Git tags `vMAJOR.MINOR.PATCH`. Full procedure is in
[RELEASING.md](../../../RELEASING.md); this skill is the operational summary.

## Steps

1. **Bump the version** in [pyproject.toml](../../../pyproject.toml) under
   `[project] version = "X.Y.Z"`.
2. **Update [CHANGELOG.md](../../../CHANGELOG.md)** (Keep a Changelog format):
   move `## [Unreleased]` content under a new `## [X.Y.Z] - YYYY-MM-DD` heading,
   and add fresh `[Unreleased]` / `[X.Y.Z]` compare links at the bottom.
3. **Verify the version matches** before tagging:
   ```bash
   make release-check
   ```
4. **Commit and push** (via the open-pr workflow, or directly if releasing):
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "chore: release vX.Y.Z"
   git push origin main
   ```
5. **Tag and push the tag** (this triggers the `Release` workflow):
   ```bash
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push origin vX.Y.Z
   ```

The `Release` workflow verifies the tag equals the `pyproject.toml` version,
builds wheel + sdist, extracts that version's changelog section, and creates the
GitHub Release.

## Pre-releases

Append `-rc.1`, `-beta.1`, or `-alpha.1` to the version; the workflow marks the
GitHub Release as a pre-release automatically.

## If the release workflow fails

Most often the tag does not match `pyproject.toml`. Fix the version, then:
```bash
git tag -fa vX.Y.Z -m "vX.Y.Z"
git push --force origin vX.Y.Z
```
(Force-pushing a tag is expected here; never force-push `main`.)
