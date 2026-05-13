#!/usr/bin/env python3
"""SITE-GUIDE compliance checks for static HTML pages.

Current enforced rules:
- Every indexable HTML page has a non-empty <title>.
- Every indexable HTML page has a non-empty meta description.
- Titles are unique across indexable pages.
- Meta descriptions are unique across indexable pages.

Indexable means the page does not contain a robots meta tag with noindex.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


IGNORED_DIRS = {
    ".git",
    ".github",
    ".lighthouseci",
    ".vscode",
    "dist",
    "node_modules",
    "vendor",
    "build",
}


@dataclass
class PageMeta:
    title: str = ""
    description: str = ""
    robots: str = ""

    @property
    def is_indexable(self) -> bool:
        robots_value = self.robots.lower()
        return "noindex" not in robots_value


class MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.page = PageMeta()
        self._in_title = False
        self._title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs_dict = {k.lower(): (v or "") for k, v in attrs}
        t = tag.lower()
        if t == "title":
            self._in_title = True
            return
        if t != "meta":
            return

        name = attrs_dict.get("name", "").strip().lower()
        content = attrs_dict.get("content", "").strip()
        if name == "description":
            self.page.description = content
        elif name == "robots":
            self.page.robots = content

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False
            self.page.title = re.sub(r"\s+", " ", "".join(self._title_parts)).strip()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & IGNORED_DIRS)


def collect_html_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*.html"):
        rel = p.relative_to(root)
        if should_skip(rel):
            continue
        files.append(p)
    return sorted(files)


def parse_page(path: Path) -> PageMeta:
    parser = MetaParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    parser.close()
    return parser.page


def main() -> int:
    root = Path(os.getcwd())
    html_files = collect_html_files(root)

    if not html_files:
        print("No HTML files found. Nothing to check.")
        return 0

    errors: list[str] = []
    titles: dict[str, list[str]] = {}
    descriptions: dict[str, list[str]] = {}

    for page_file in html_files:
        rel = str(page_file.relative_to(root))
        meta = parse_page(page_file)

        if not meta.is_indexable:
            continue

        if not meta.title:
            errors.append(f"{rel}: missing <title>")
        else:
            titles.setdefault(meta.title, []).append(rel)

        if not meta.description:
            errors.append(f"{rel}: missing meta description")
        else:
            descriptions.setdefault(meta.description, []).append(rel)

    for value, files in titles.items():
        if len(files) > 1:
            errors.append(
                "duplicate title across pages: "
                + ", ".join(files)
                + f" | title=\"{value}\""
            )

    for value, files in descriptions.items():
        if len(files) > 1:
            errors.append(
                "duplicate meta description across pages: "
                + ", ".join(files)
                + f" | description=\"{value}\""
            )

    if errors:
        print("SITE-GUIDE compliance check failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("SITE-GUIDE compliance check passed.")
    print("Checked indexable HTML pages for title/meta-description presence and uniqueness.")
    return 0


if __name__ == "__main__":
    sys.exit(main())