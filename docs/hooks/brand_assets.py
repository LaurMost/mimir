"""MkDocs hook: serve the shared brand assets from the repo-root ``assets/``.

MkDocs only bundles files that live under ``docs_dir``. Rather than keep copies
of the logo, favicon, and wordmark inside ``docs/assets/`` (which drift out of
sync with the canonical brand assets), this hook injects them into the build at
their expected site-relative URIs straight from ``assets/``.
"""

from __future__ import annotations

from pathlib import Path

from mkdocs.structure.files import File

# site-relative URI (under the built site) -> source path relative to repo root
_BRAND_ASSETS = {
    "assets/logo.svg": "assets/logo/logo.svg",
    "assets/favicon.svg": "assets/favicons/favicon.svg",
    "assets/wordmark.svg": "assets/logo/wordmark-bone.svg",
}


def on_files(files, config):
    repo_root = Path(config.config_file_path).parent
    for site_uri, source in _BRAND_ASSETS.items():
        abs_src_path = repo_root / source
        files.append(
            File.generated(config, site_uri, abs_src_path=str(abs_src_path))
        )
    return files
