#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CANONICAL_GUIDE="$ROOT_DIR/site-guide/SITE-GUIDE.md"
DEST="$SCRIPT_DIR/SITE-GUIDE.md"

if [[ ! -f "$CANONICAL_GUIDE" ]]; then
  echo "Canonical SITE-GUIDE.md not found at: $CANONICAL_GUIDE" >&2
  exit 1
fi

cp "$CANONICAL_GUIDE" "$DEST"
echo "Updated: $DEST"
echo "Source: $CANONICAL_GUIDE"
