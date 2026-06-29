# Releasing

Mimir follows [Semantic Versioning](https://semver.org/) and uses Git tags of the form `vMAJOR.MINOR.PATCH`.

## Cut a release

1. **Update the version** in `pyproject.toml`:
   ```toml
   [project]
   version = "0.2.0"
   ```

2. **Move `## [Unreleased]` content** in `CHANGELOG.md` under a new `## [0.2.0] - YYYY-MM-DD` heading. Add fresh `[Unreleased]` and `[0.2.0]` links at the bottom.

3. **Commit and push**:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "chore: release v0.2.0"
   git push origin main
   ```

4. **Tag and push the tag**:
   ```bash
   git tag -a v0.2.0 -m "v0.2.0"
   git push origin v0.2.0
   ```

5. The `Release` workflow runs automatically: it verifies the tag matches `pyproject.toml`, builds wheel + sdist, extracts the version's changelog section, and creates a GitHub Release.

## Pre-releases

Append `-rc.1`, `-beta.1`, or `-alpha.1` to the version. The release workflow detects these and marks the GitHub Release as a pre-release.

```bash
git tag -a v0.3.0-rc.1 -m "v0.3.0-rc.1"
git push origin v0.3.0-rc.1
```

## If the release workflow fails

The tag check is the most common cause: `pyproject.toml` version must equal the tag (minus the `v`). Bump `pyproject.toml`, force-update the tag, and re-push:

```bash
git tag -fa v0.2.0 -m "v0.2.0"
git push --force origin v0.2.0
```
