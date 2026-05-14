#!/usr/bin/env python3
"""Refresh Product schema priceValidUntil dates to today + 1 year.

Scans all HTML files for `"priceValidUntil": "YYYY-MM-DD"` inside JSON-LD
Product schema and bumps any date that's within 6 months of expiring to
today + 1 year. Idempotent: no-op when all dates are already fresh.

Designed to be run from a GitHub Actions cron job (monthly) so the merchant-
listings rich-result eligibility never silently drops.

Exit code is always 0 so the workflow's "commit if changed" step decides
whether anything needs to be pushed.
"""
from __future__ import annotations

import re
import sys
from datetime import date, timedelta
from pathlib import Path

# Same exclusion model as scripts/check-site-guide-compliance.py
IGNORED_DIRS = {
    ".git", ".github", ".lighthouseci", ".vscode",
    "dist", "node_modules", "vendor", "build",
}
IGNORED_FILE_SUFFIXES = ("_tpl.html",)
IGNORED_PATH_PREFIXES = ("sitemap/pages/mods/",)

PVU_RE = re.compile(r'"priceValidUntil"\s*:\s*"(\d{4}-\d{2}-\d{2})"')


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & IGNORED_DIRS:
        return True
    s = path.as_posix()
    if s.endswith(IGNORED_FILE_SUFFIXES):
        return True
    return any(s.startswith(p) for p in IGNORED_PATH_PREFIXES)


def main() -> int:
    today = date.today()
    new_date = (today + timedelta(days=365)).isoformat()
    threshold = today + timedelta(days=183)  # 6 months out

    root = Path.cwd()
    files_changed = 0
    dates_bumped = 0

    for html in sorted(root.rglob("*.html")):
        rel = html.relative_to(root)
        if should_skip(rel):
            continue
        text = html.read_text(encoding="utf-8")
        if '"priceValidUntil"' not in text:
            continue

        def bump(m: re.Match) -> str:
            nonlocal dates_bumped
            current = date.fromisoformat(m.group(1))
            if current > threshold:
                return m.group(0)
            dates_bumped += 1
            return f'"priceValidUntil": "{new_date}"'

        new_text = PVU_RE.sub(bump, text)
        if new_text != text:
            html.write_text(new_text, encoding="utf-8")
            files_changed += 1

    print(f"Files changed: {files_changed}")
    print(f"Dates bumped:  {dates_bumped}")
    print(f"New value:     {new_date}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
