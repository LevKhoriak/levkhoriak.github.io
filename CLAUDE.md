# Project rules for levkhoriak.github.io

Personal research homepage of Lev Khoriak, served at https://levkhoriak.github.io.
These rules always apply. For the current task, read `docs/SPEC.md`.

## Stack
- Homepage: a single hand-written `index.html` + CSS, based on Jon Barron's template
  (https://github.com/jonbarron/jonbarron_website). No framework.
- Notes: Quarto, one folder per note in `notes/<name>/` (`index.qmd` + its own `images/`
  and `results/`), rendered to HTML at `/notes/<name>/`. Shared theme/partials/CSL live in
  `notes/_theme/`, shared Python (plotting) in `notes/_lib/`. `notes/template/` demos every feature.
- Papers (future): LaTeX → HTML (Pandoc or LaTeXML) in `papers/`.
- Shared bibliography: `references.bib` at the repo root, used by notes and papers.
- Prefer Python tooling. No npm / JS build step. Small vanilla JS files are fine.

## Non-negotiables
- Keep Jon Barron's credit link in the footer of the homepage.
- No Google Analytics or other tracking.
- Do not copy code from other people's sites; reimplement features yourself.
- My name is spelled **Lev Khoriak** everywhere (Russian: Лев Хоряк).
- This repo is public: never commit private notes, drafts of emails, or credentials.

## Content conventions
- The homepage "Research & Notes" list mixes papers, notes, and projects in one format
  (thumbnail, title, authors with my name in bold, venue/date, links, one-line summary)
  with a small tag: [paper], [note], or [project].
- Every note's front matter has: `title`, `authors`, `date`, `tags`, `takeaway`
  (one sentence, shown at the top), `thumbnail`, `draft`.
- `draft: true` notes are rendered locally but never listed or published.
- Notes keep code minimal: chunks only import plotting functions (from `notes/_lib/`) and
  read saved results from the note's own `results/`. Use `echo: false` and `freeze: auto`;
  commit `_freeze/`.
- Notes and the homepage share fonts and colors.

## Deployment
- GitHub Actions → GitHub Pages (Pages source: "GitHub Actions"). Keep `.nojekyll`.
- The workflow renders Quarto and publishes the whole site.

## Working style
- Commit in small, logical steps with clear messages.
- Keep things simple and readable; I maintain this myself.
- When working from `docs/SPEC.md`, tick off checklist items as you finish them and
  add a one-line note under any item where you made a decision or hit a problem.
- Keep `README.md` up to date: local preview, adding/publishing a note,
  adding a paper/project entry, how deployment works.
