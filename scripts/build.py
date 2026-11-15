"""Build the whole site into _site/.

1. Renders every note (notes/<name>/index.qmd) with Quarto, skipping `draft: true` notes,
   and copies each note's images/ folder (thumbnails).
2. Copies the hand-written homepage and its files.
3. Adds one homepage entry per rendered note (from its front matter), merges them with
   the hand-written entries newest first (by `data-date`), and removes draft entries.

Usage:
    python scripts/build.py            # what gets published (no drafts)
    python scripts/build.py --drafts   # local preview, drafts included and marked
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
NOTES = ROOT / "notes"
MY_NAME = "Lev Khoriak"

# Homepage files that belong on the website. Anything else (README, docs, scripts) is not published.
PUBLIC = ["index.html", "stylesheet.css", "shared.css", "theme-toggle.js", "bio.txt", ".nojekyll", "images"]

ARTICLE = re.compile(r"[ \t]*<article\b.*?</article>\n?", re.DOTALL)
PAPERS_SECTION = re.compile(r'(<section class="papers">\n)(.*?)(\s*</section>)', re.DOTALL)


def front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    return yaml.safe_load(match.group(1)) if match else {}


def find_quarto() -> str:
    local = Path(sys.executable).parent / "quarto"
    return str(local) if local.exists() else (shutil.which("quarto") or sys.exit("quarto not found"))


def render_note(quarto: str, qmd: Path) -> None:
    env = dict(os.environ, QUARTO_PYTHON=sys.executable)
    subprocess.run([quarto, "render", str(qmd.relative_to(ROOT))], cwd=ROOT, env=env, check=True)


def author_html(author: dict) -> str:
    name = html.escape(author["name"])
    mark = "<sup>*</sup>" if (author.get("attributes") or {}).get("equal-contributor") else ""
    if author["name"] == MY_NAME:
        return f"<strong>{name}{mark}</strong>"
    if author.get("url"):
        return f'<a href="{html.escape(author["url"])}">{name}{mark}</a>'
    return f'<span class="author">{name}{mark}</span>'


def note_entry(qmd: Path, meta: dict) -> str:
    """Homepage <article> for one note, in the same format as the hand-written entries."""
    when = meta["date"] if isinstance(meta["date"], date) else date.fromisoformat(str(meta["date"]))
    folder = f"notes/{qmd.parent.name}/"
    page = folder
    title = html.escape(meta["title"])
    thumb = folder + meta.get("thumbnail", "images/thumb.svg")
    authors = ", ".join(author_html(a) for a in meta.get("authors", []))
    note = meta.get("author-note")
    lines = [
        f'      <article class="paper" data-date="{when.isoformat()}"{" data-draft" if meta.get("draft") else ""}>',
        '        <div class="paper-media">',
        f'          <img src="{thumb}" alt="{title}" width="160" height="160">',
        "        </div>",
        '        <div class="paper-info">',
        '          <span class="tag tag-note">note</span>',
        f'          <a href="{page}" class="papertitle">{title}</a>',
        f'          <div class="paper-authors">{authors}</div>',
        *([f'          <div class="author-note">{html.escape(note).replace("*", "<sup>*</sup>", 1)}</div>'] if note else []),
        f'          <div class="paper-venue"><em>Note</em>, {when.strftime("%B %Y")}</div>',
        f'          <div class="paper-links"><a href="{page}">note</a></div>',
        f'          <p class="paper-desc">{html.escape(meta.get("takeaway", ""))}</p>',
        "        </div>",
        "      </article>",
    ]
    return "\n".join(lines) + "\n"


def build_index(note_entries: list[str], drafts: bool) -> int:
    """Merge note entries into the homepage list, newest first. Returns the number of drafts removed."""
    index = OUT / "index.html"
    page = index.read_text(encoding="utf-8")
    section = PAPERS_SECTION.search(page)
    entries = ARTICLE.findall(section.group(2)) + note_entries

    def entry_date(entry: str) -> str:
        found = re.search(r'data-date="([^"]+)"', entry)
        return found.group(1) if found else ""

    entries.sort(key=entry_date, reverse=True)
    kept = [e for e in entries if drafts or "data-draft" not in e.split(">", 1)[0]]

    body = section.group(2)
    body = ARTICLE.sub("", body) + "".join(kept)
    index.write_text(page[: section.start(2)] + body + page[section.end(2):], encoding="utf-8")
    return len(entries) - len(kept)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--drafts", action="store_true", help="include draft notes and entries (local preview)")
    args = parser.parse_args()

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    # 1. Notes
    # One folder per note; folders starting with "_" (_theme, _lib) are not notes.
    notes = [(q, front_matter(q)) for q in sorted(NOTES.glob("*/index.qmd")) if not q.parent.name.startswith("_")]
    notes = [(q, m) for q, m in notes if args.drafts or not m.get("draft")]
    if notes:
        quarto = find_quarto()
        for qmd, _ in notes:
            render_note(quarto, qmd)
            if (qmd.parent / "images").is_dir():
                shutil.copytree(qmd.parent / "images", OUT / "notes" / qmd.parent.name / "images", dirs_exist_ok=True)

    # 2. Homepage files
    for name in PUBLIC:
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, OUT / name, dirs_exist_ok=True)
        else:
            shutil.copy2(src, OUT / name)

    # 3. Homepage list
    removed = build_index([note_entry(q, m) for q, m in notes], args.drafts)

    print(f"Built {OUT.relative_to(ROOT)}/: {len(notes)} note(s) rendered, {removed} draft entr{'y' if removed == 1 else 'ies'} removed")


if __name__ == "__main__":
    main()
