#!/usr/bin/env python3
"""SITE-GUIDE compliance checks for static HTML pages + agent discovery.

Current enforced rules:
- Every indexable HTML page has a non-empty <title>.
- Every indexable HTML page has a non-empty meta description.
- Titles are unique across indexable pages.
- Meta descriptions are unique across indexable pages.
- Deploy-root llms.txt exists, has a Markdown H1 (# …), and at least one Markdown link.

Indexable means the page does not contain a robots meta tag with noindex.

Pages root detection (important for Cloudflare Pages):
- If public/llms.txt or public/index.html → check only public/
- Else if web/llms.txt or web/index.html → check only web/
- Else → check the git/repo cwd (root HTML sites)

This avoids false failures on builder fragments, email HTML, PHP sources,
Pi apps, and other non-shipped trees when only SITE-GUIDE.md changes on a PR.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


# Extra safety if someone runs the checker without Pages-root detection.
IGNORED_DIRS = {
    ".git",
    ".github",
    ".lighthouseci",
    ".vscode",
    "dist",
    "node_modules",
    "vendor",
    "build",
    "venv",
    ".venv",
    "functions",
    "pi-app",
    "email",
    "_hubs",
    "templates",
    "tests",
    "hardware",
    "docs",
}

IGNORED_PATH_PREFIXES = (
    "sitemap/pages/mods/",
    "growbru/",  # Python package / non-Pages demos when scanning from monorepo root
)

IGNORED_FILE_SUFFIXES = (
    "_tpl.html",
)

IGNORED_BASENAME_PATTERNS = (
    r"google[0-9a-f]{16}\.html",
    r"Gensw_[0-9a-fA-F]+\.html",
)


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


def detect_pages_root(cwd: Path) -> Path:
    """Return the directory that Cloudflare Pages (or static host) actually ships."""
    public = cwd / "public"
    web = cwd / "web"

    if (public / "llms.txt").is_file() or (public / "index.html").is_file():
        return public
    if (web / "llms.txt").is_file() or (web / "index.html").is_file():
        return web
    if (cwd / "llms.txt").is_file() or (cwd / "index.html").is_file():
        return cwd
    # Last resort: prefer a known Pages output dir if present
    if public.is_dir():
        return public
    if web.is_dir():
        return web
    return cwd


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & IGNORED_DIRS:
        return True

    path_str = path.as_posix()
    if path_str.endswith(IGNORED_FILE_SUFFIXES):
        return True

    if any(path_str.startswith(prefix) for prefix in IGNORED_PATH_PREFIXES):
        return True

    basename = path.name
    return any(re.fullmatch(pattern, basename) for pattern in IGNORED_BASENAME_PATTERNS)


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


def check_llms_txt(root: Path) -> list[str]:
    """SITE-GUIDE §5.3.3.2a — deploy-root llms.txt for agentic browsing."""
    path = root / "llms.txt"
    errors: list[str] = []
    if not path.is_file():
        return [
            f"llms.txt: missing under deploy root ({root}) "
            "(mandatory for agentic browsing / AI discovery; see SITE-GUIDE §5.3.3.2a)"
        ]

    text = path.read_text(encoding="utf-8", errors="ignore").lstrip("\ufeff")
    stripped = text.lstrip()
    if stripped.lower().startswith("<!doctype") or stripped.lower().startswith("<html"):
        errors.append(
            "llms.txt: file looks like HTML, not Markdown plain text "
            "(live soft-404 often means the file was never deployed)"
        )

    has_h1 = bool(re.search(r"(?m)^#\s+\S+", text))
    if not has_h1:
        errors.append(
            'llms.txt: missing required Markdown H1 (first line should be "# Site Name")'
        )

    has_md_link = bool(re.search(r"\[[^\]]+\]\((?:https?:\/\/|mailto:|tel:)[^)]+\)", text))
    if not has_md_link:
        errors.append(
            "llms.txt: missing Markdown links — use [Label](https://example.com/) "
            "(bare URLs alone fail agentic 'contains links' checks)"
        )

    has_summary = bool(re.search(r"(?m)^>\s+\S+", text))
    if not has_summary:
        errors.append(
            'llms.txt: missing blockquote summary line (e.g. "> One sentence about the business")'
        )

    return errors


def main() -> int:
    cwd = Path(os.getcwd())
    root = detect_pages_root(cwd)
    print(f"SITE-GUIDE compliance: scanning deploy root → {root}")

    html_files = collect_html_files(root)

    if not html_files:
        print("No HTML files found under deploy root. Nothing to check.")
        return 0

    errors: list[str] = []
    errors.extend(check_llms_txt(root))
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
                + f' | title="{value}"'
            )

    for value, files in descriptions.items():
        if len(files) > 1:
            errors.append(
                "duplicate meta description across pages: "
                + ", ".join(files)
                + f' | description="{value}"'
            )

    if errors:
        print("SITE-GUIDE compliance check failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("SITE-GUIDE compliance check passed.")
    print(
        "Checked llms.txt (H1 + Markdown links + summary) and indexable HTML "
        "title/meta-description presence and uniqueness under the deploy root."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
