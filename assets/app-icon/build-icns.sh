#!/usr/bin/env bash
# Run on macOS to produce Mimir.icns from the iconset/
set -euo pipefail
cd "$(dirname "$0")"
iconutil -c icns Mimir.iconset
echo "✓ Mimir.icns built"
