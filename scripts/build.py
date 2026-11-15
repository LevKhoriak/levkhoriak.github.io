"""Assemble the published site in _site/.

Copies the public files and removes draft entries (<article ... data-draft>) from
index.html, so drafts show up in local preview but never on the live site.

Usage: python scripts/build.py
"""

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"

# Everything that belongs on the website. Anything else (README, docs, scripts) stays private to the repo.
PUBLIC = ["index.html", "stylesheet.css", "bio.txt", ".nojekyll", "images"]

DRAFT_ARTICLE = re.compile(r"[ \t]*<article\b[^>]*\bdata-draft\b.*?</article>\n?", re.DOTALL)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    for name in PUBLIC:
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, OUT / name)
        else:
            shutil.copy2(src, OUT / name)

    index = OUT / "index.html"
    html = index.read_text(encoding="utf-8")
    html, n_drafts = DRAFT_ARTICLE.subn("", html)
    index.write_text(html, encoding="utf-8")

    print(f"Built {OUT.relative_to(ROOT)}/ ({n_drafts} draft entr{'y' if n_drafts == 1 else 'ies'} removed)")


if __name__ == "__main__":
    main()
