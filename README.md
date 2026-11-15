# levkhoriak.github.io

Personal research homepage of Lev Khoriak, live at https://levkhoriak.github.io.
Based on [Jon Barron's template](https://github.com/jonbarron/jonbarron_website).

## Layout

| Path | What it is |
| --- | --- |
| `index.html`, `stylesheet.css` | The homepage (hand-written). |
| `shared.css` | Fonts and colors shared by the homepage and the notes. |
| `theme-toggle.js` | Theme button on every page, cycling system → light → dark. The choice is remembered under Quarto's own setting, so it carries between homepage and notes. |
| `bio.txt` | Third-person bio, served at `/bio.txt`. |
| `images/` | Homepage photo and thumbnails. |
| `notes/<name>/` | One folder per note: `index.qmd`, `images/` (thumbnail, static images), `results/` (saved results the figures read). Published at `/notes/<name>/`. `notes/template/` shows every feature. |
| `notes/_lib/` | Shared Python for notes (`plotting.py`). Importable from any note via `_environment`. |
| `notes/_theme/` | Note theme (SCSS), title-block partial, citation style (IEEE CSL), and the small header/footer scripts (theme button, Copy BibTeX). |
| `_quarto.yml`, `_environment` | Quarto settings for all notes; `PYTHONPATH` for `notes/_lib`. |
| `_freeze/` | Saved output of note code (commit it; CI reuses it instead of re-running code). |
| `references.bib` | Shared bibliography for notes and (future) papers. |
| `papers/` | Placeholder for LaTeX → HTML papers. |
| `scripts/build.py` | Builds the whole site into `_site/`. |
| `.github/workflows/deploy.yml` | Builds and deploys to GitHub Pages on every push to `main`. |
| `docs/SPEC.md` | Build plan / checklist. Not published. |

## Setup (once)

```sh
uv venv --python 3.12
uv pip install -r requirements.txt     # Quarto, PyYAML, matplotlib, Jupyter
```

## Local preview

Whole site, drafts included (drafts have a dashed outline on the homepage and a "Draft" banner):

```sh
.venv/bin/python scripts/build.py --drafts
python3 -m http.server 8000 -d _site    # open http://localhost:8000
```

Exactly what will be published: same, without `--drafts`.

While writing a single note, live-reload it:

```sh
QUARTO_PYTHON=.venv/bin/python .venv/bin/quarto preview notes/my-note/index.qmd
```

## Adding a note

1. Copy the folder `notes/template/` to `notes/<short-name>/` (the folder name becomes the
   URL: `/notes/<short-name>/`). Replace `results/` with your own and `images/thumb.svg`
   with a 160×160 thumbnail.
2. Fill in the front matter: `title`, `authors` (with `affiliations`; add
   `attributes: {equal-contributor: true}` + `author-note` for alphabetical lists),
   `date`, `tags`, `takeaway` (one sentence, shown at the top and on the homepage),
   `thumbnail` (`images/...`, relative to the note folder), `draft: true`, and
   `citation: url: https://levkhoriak.github.io/notes/<short-name>/`.
3. Keep code minimal: chunks import from `plotting` (in `notes/_lib/`) and read files from
   the note's own `results/`, e.g. `plot_curves("results/curves.csv")`. Code is hidden by
   default (`echo: false`). Add new shared plotting functions to `notes/_lib/plotting.py`.
4. Cite with `[@key]` from `references.bib`; reference figures with `@fig-label`.
5. Render locally (`scripts/build.py --drafts`) so `_freeze/` is updated, and commit
   `_freeze/` together with the note.

The homepage entry is generated from the front matter: don't add notes to `index.html`.

## Publishing a note (draft → published)

1. Set `draft: false` and update `date`.
2. Run `.venv/bin/python scripts/build.py` and check the note and the homepage.
3. Commit (including `_freeze/`) and push. The note appears on the site in about a minute.

Drafts are in the public repo, but they are never rendered or listed on the website.

## Adding a paper or project entry

Copy an existing `<article class="paper" data-date="...">` block inside
`<section class="papers">` in `index.html` and edit it. Order doesn't matter: the build
sorts all entries (including notes) by `data-date`, newest first.

- tag: `<span class="tag tag-paper">paper</span>` or `<span class="tag tag-project">project</span>`
- authors: co-authors as `<span class="author">Name</span>` (or a link), my name as `<strong>Lev Khoriak</strong>`
- alphabetical author lists: mark each listed author with `<sup>*</sup>`, put the advisor last without a mark,
  and add `<div class="author-note"><sup>*</sup> Alphabetical order; NAME is the advisor.</div>` under the authors
- thumbnail: put a 160×160 image in `images/` and point the `<img>` at it
- venue/date, links (`/`-separated), and a one-line summary in `paper-desc`
- `data-draft` on the `<article>` hides it from the live site

## Deployment

Pushing to `main` runs `.github/workflows/deploy.yml`: it installs `requirements.txt`, runs
`scripts/build.py` (renders non-draft notes with Quarto, builds the homepage list), and
uploads `_site/` to GitHub Pages. Pages → Source must be "GitHub Actions" (it is).
Only the homepage files listed in `PUBLIC` in `scripts/build.py` and the rendered notes
are published.

Pushing changes to `.github/workflows/` over HTTPS needs a `gh` token with the
`workflow` scope (`gh auth refresh -s workflow`); pushing over SSH works as is.
