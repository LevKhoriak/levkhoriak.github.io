# levkhoriak.github.io

Personal research homepage of Lev Khoriak, live at https://levkhoriak.github.io.
Based on [Jon Barron's template](https://github.com/jonbarron/jonbarron_website).

## Layout

| Path | What it is |
| --- | --- |
| `index.html`, `stylesheet.css` | The homepage (hand-written). Colors are CSS variables at the top of the stylesheet. |
| `bio.txt` | Third-person bio, served at `/bio.txt`. |
| `images/` | Photo and thumbnails. |
| `scripts/build.py` | Assembles the published site in `_site/` (copies public files, strips drafts). |
| `.github/workflows/deploy.yml` | Builds and deploys to GitHub Pages on every push to `main`. |
| `docs/SPEC.md` | Build plan / checklist. Not published. |

## Local preview

With drafts (what you're working on):

```sh
python3 -m http.server 8000      # then open http://localhost:8000
```

Exactly as it will be published (drafts removed):

```sh
python3 scripts/build.py
python3 -m http.server 8000 -d _site
```

## Adding a paper or project entry

Copy an existing `<article class="paper">` block inside `<section class="papers">` in
`index.html` (newest first) and edit it:

- tag: `<span class="tag tag-paper">paper</span>`, `tag-note` / `note`, or `tag-project` / `project`
- authors: co-authors as `<span class="author">Name</span>` (or a link), my name as `<strong>Lev Khoriak</strong>`
- alphabetical author lists: mark each listed author with `<sup>*</sup>`, put the advisor last without a mark,
  and add `<div class="author-note"><sup>*</sup> Alphabetical order; NAME is the advisor.</div>` under the authors
- thumbnail: put a 160×160 image in `images/` and point the `<img>` at it
- venue/date, links (`/`-separated), and a one-line summary in `paper-desc`

## Drafts

Add `data-draft` to an entry (`<article class="paper" data-draft>`). It shows up with a
dashed outline in local preview and is removed from the published site by
`scripts/build.py`. To publish, delete `data-draft` and push.

(Notes in Quarto are coming in Phase 2; this section will cover the `draft:` front matter then.)

## Deployment

Pushing to `main` runs `.github/workflows/deploy.yml`: it runs `scripts/build.py` and
uploads `_site/` to GitHub Pages. In the repo settings, Pages → Source must be
"GitHub Actions". Only files listed in `PUBLIC` in `scripts/build.py` are published,
so add new top-level files/folders there if they belong on the site.
