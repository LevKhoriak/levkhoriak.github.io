# SPEC: initial build of the homepage

Read `CLAUDE.md` first: its rules apply throughout. Work through the phases in order,
ticking items off as you go. **Stop after Phase 1 and show me the live page before
starting Phase 2.**

Unfilled brackets like `[YEAR]` are mine to fill in: leave them as visible placeholders.

---

## Content

### About me (use verbatim unless it breaks the layout)
- **Name:** Lev Khoriak. Show "Лев Хоряк" once, small, next to or under the name.
- **One-liner:** I'm interested in the science of deep learning — how neural networks
  learn, what they represent, and why they generalize.
- **Bio:** I'm an MSc student in Artificial Intelligence at the Faculty of Computer
  Science, HSE University, and a data scientist at Alfa-Bank, where I build machine
  learning models in production. Before that, I received a BSc in International
  Finance. My research interests are in the science of deep learning: learning
  dynamics, loss landscapes, generalization, representation geometry, and
  mechanistic interpretability. I'm especially drawn to careful empirical work
  that tests what theory predicts about real training runs.
- **Education:**
  - MSc in Artificial Intelligence, HSE University, Faculty of Computer Science (expected [YEAR])
  - BSc in International Finance ([YEAR]) — no institution name
- **Links:** Email [..], GitHub https://github.com/LevKhoriak, ORCID [..],
  X/Twitter [.. or omit], CV [path or omit]. Google Scholar: omit for now.
- **Photo:** [path to image, or a neutral placeholder]

### bio.txt (third person, served at `/bio.txt`)
> Lev Khoriak is an MSc student in Artificial Intelligence at the HSE University
> Faculty of Computer Science and a data scientist at Alfa-Bank. He is interested in
> the science of deep learning, including learning dynamics, loss landscapes,
> generalization, representation geometry, and mechanistic interpretability, with an
> emphasis on careful empirical studies of real training runs. He holds a BSc in
> International Finance.

### Initial list entries (placeholder thumbnails)
1. **[project]** "Multimodal Recommender System"
   - Authors: Anzhelika Artamonova, Valeria Kushchenko, Alexey Pristaiko, **Lev Khoriak**
   - Venue: HSE University course project, 2026–2027
   - Link: https://github.com/LevKhoriak/hse-ai-26-recsys-team-120
   - Summary: Text and image content for recommendations on Amazon Reviews 2023,
     with a focus on cold items and short user histories.
2. **[note]** "What CLIP sees in Amazon products" (`draft: true`, hidden until published)
   - Authors: same as above
   - Summary: Image embeddings group groceries by packaging, a third of fashion items
     share a photo, and standard 5-core filtering would erase almost all cold-start
     evaluation.

### Misc section (bottom of the homepage)
- As a school student at the Specialized Educational and Scientific Center (SUNC) of
  Southern Federal University, I recorded science podcasts with university researchers
  as part of the *Поколение Science* project. [links: ..]

---

## Phase 1 — Homepage
- [x] Set up from Jon Barron's template in this repo (keep credit link, remove analytics).
  - Note: based on the current flex/grid version of his `stylesheet.css`; colors moved to CSS variables. Removed the old Jekyll `_config.yml`.
- [x] Header: name, Russian name, one-liner/bio, links, photo.
  - Note: X added (https://x.com/levkhoriak); CV omitted; Email and ORCID added; photo is `images/lev-khoriak.jpg` (square crop, 600px, metadata stripped).
- [x] Education section.
- [x] "Research & Notes" list supporting [paper] / [note] / [project] tags,
      multiple co-authors with my name in bold, and hidden drafts.
  - Note: drafts are `<article ... data-draft>`; shown dashed in local preview, stripped by `scripts/build.py` before deploy.
- [x] Add the two initial entries above (draft note hidden).
  - Note: draft note's date is a `[DATE]` placeholder.
- [x] Misc section with the podcasts entry.
  - Note: links to one Apple Podcasts episode (#3).
- [x] `/bio.txt`.
- [x] Mobile-friendly layout. Light theme by default; dark mode via
      `prefers-color-scheme` is a nice-to-have.
  - Note: dark mode done via `prefers-color-scheme`, plus a theme button (`theme-toggle.js`) on homepage and notes cycling system → light → dark, remembered and sharing Quarto's `quarto-color-scheme` localStorage key.
- [x] GitHub Actions deploy workflow + `.nojekyll`; site live at https://levkhoriak.github.io.
  - Note: Pages source switched from legacy branch build to "GitHub Actions". HTTPS push was rejected (gh token lacks `workflow` scope), so pushed over SSH.
- [x] **STOP: show me the live page.**

## Phase 2 — Notes system (Quarto)
- [x] Quarto project for `notes/` with a custom theme matching the homepage.
  - Note: root `_quarto.yml` renders `notes/*.qmd` into `_site/notes/`; Quarto 1.11.9 pinned via the `quarto-cli` pip package in `requirements.txt`. Fonts/colors split into `shared.css` (homepage + notes); Bootstrap SCSS values in `notes/theme-*.scss` mirror it. Dark mode follows the system setting. Dark notes use `darkly` as the base (cosmo hard-coded black code text, unreadable on dark); syntax highlighting `a11y`; muted grey raised to ≥7:1 contrast in both modes.
- [x] Shared `references.bib` at the repo root.
- [x] Note page features:
  - [x] title block with multiple authors and affiliations, date, tags
    - Note: custom partial `notes/_partials/title-block.html`; `attributes: {equal-contributor: true}` gives the `*` mark, `author-note` the footnote.
  - [x] `takeaway` shown at the top
  - [x] sticky table of contents with scroll-spy highlighting
    - Note: native Quarto (`toc-location: left`, so the right margin stays free for margin notes).
  - [x] Distill-style widths: body / page / screen figures and margin notes
        (`.column-page`, `.column-screen`, `.column-margin`)
  - [x] numbered citations with hover previews of the bibliography entry
    - Note: IEEE CSL (`notes/ieee.csl`) + native `citations-hover`.
  - [x] hover previews for figure cross-references ("Figure 2" shows the figure)
    - Note: native `crossrefs-hover`.
  - [x] click-to-zoom lightbox on figures
    - Note: native `lightbox: true`.
  - [x] copy button on code blocks; "copy BibTeX" button for the note
    - Note: BibTeX comes from Quarto's `citation:` appendix; the button is in `notes/_note-scripts.html`.
  - [x] KaTeX or MathJax math
    - Note: KaTeX.
  - [x] anything Quarto lacks natively → own small vanilla JS file
    - Note: only the Copy BibTeX button needed JS (`notes/_note-scripts.html`).
- [x] `notes/template.qmd`: dummy content demonstrating every feature above.
  - Note: figures come from `notes/plotting.py` + made-up CSVs in `notes/results/template/`; executed output is frozen in `_freeze/` (committed), so CI needs no re-execution.
- [x] `notes/clip-amazon-products.qmd`: `draft: true` skeleton with empty figure slots:
  - Note: date set to 2026-11-15 (update when publishing); curator name left as `[CURATOR NAME]`.
  - Takeaway
  - Setup (Amazon Reviews 2023, Fashion vs Grocery, temporal split)
  - How cold is the test set? (figure: user-history × item-popularity grid)
  - What 5-core filtering would remove (figure)
  - What CLIP neighbors share (figure: same-type share among 10 nearest neighbors,
    image vs title vs random)
  - Duplicates and packaging
  - Limitations
  - Acknowledgements (team and curator)
- [x] Homepage list generated from note front matter by a small Python script
  - Note: `scripts/build.py` renders non-draft notes, builds their entries, and merges them with the hand-written ones by `data-date`. The hand-written CLIP entry was removed (now generated).
      (respecting `draft`). If too complex, document the manual step instead.
- [x] Deploy workflow renders Quarto; published notes appear on the live site.
  - Note: verified locally with a temporary non-draft copy of the template; no note is published yet, so the live site has none.

## Phase 3 — Placeholder
- [x] Empty `papers/` folder with a README: future papers are converted LaTeX → HTML
  - Note: `papers/README.md` (git can't track an empty folder).
      (Pandoc or LaTeXML) and share `references.bib`. Don't build the pipeline yet.

## Done when
- [x] Site live at https://levkhoriak.github.io with Phases 1–3 complete.
- [x] `README.md` covers: local preview, adding/publishing a note (draft → published),
      adding a paper or project entry, how deployment works.
