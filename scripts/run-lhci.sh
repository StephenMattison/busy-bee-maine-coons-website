#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${LHCI_GITHUB_TOKEN:-}" && -z "${LHCI_GITHUB_APP_TOKEN:-}" ]] && command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    LHCI_GITHUB_TOKEN="$(gh auth token)"
    export LHCI_GITHUB_TOKEN
  fi
fi

exec npx -y @lhci/cli@0.14.x autorun "$@"