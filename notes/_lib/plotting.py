"""Plotting helpers for notes.

Notes only import these functions and read saved results from disk; experiments live elsewhere.

Every public plot function draws the figure twice: first in the light theme, then in the
dark theme, both on a transparent background. Put `#| renderings: [light, dark]` on the
chunk and Quarto shows the version matching the page theme (including the theme button).

Put the figure label, width class and caption on a surrounding ::: block, not on the chunk
(a `fig-` label on the chunk makes Quarto treat the two versions as sub-figures (a)/(b)):

    ::: {#fig-curves .column-page}
    ```{python}
    #| renderings: [light, dark]
    plot_curves("results/curves.csv")
    ```

    Caption.
    :::
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Colors mirror shared.css (light / dark). The first series color is the site's accent (link blue).
# `seq` is the sequential colormap for heatmaps: low values blend into the page background.
THEMES = {
    "light": {"text": "#1a1a1a", "muted": "#555555", "grid": "#e3e3e3",
              "series": ["#1772d0", "#e07b10", "#555555", "#2e9e5b"],
              "seq": plt.get_cmap("Blues")},
    "dark": {"text": "#e6e6e6", "muted": "#b4b4b4", "grid": "#33363c",
             "series": ["#6aa8ec", "#f5a95a", "#b4b4b4", "#6cc890"],
             "seq": LinearSegmentedColormap.from_list("dark_blues", ["#1f2733", "#24507f", "#4a8fd6", "#b9d7f7"])},
}


def _style(theme):
    c = THEMES[theme]
    return {
        "font.family": "sans-serif",
        "font.sans-serif": ["Lato", "Verdana", "DejaVu Sans"],
        "font.size": 10,
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
        "savefig.transparent": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": c["muted"],
        "axes.labelcolor": c["text"],
        "axes.titlecolor": c["text"],
        "axes.prop_cycle": plt.cycler(color=c["series"]),
        "xtick.color": c["muted"],
        "ytick.color": c["muted"],
        "xtick.labelcolor": c["text"],
        "ytick.labelcolor": c["text"],
        "grid.color": c["grid"],
        "legend.frameon": False,
        "legend.labelcolor": c["text"],
        "text.color": c["text"],
    }


def _in_both_themes(draw):
    """Call draw(theme) once per theme (light first), each inside its matplotlib style."""
    for theme in ("light", "dark"):
        with plt.rc_context(_style(theme)):
            draw(theme)


def read_csv(path):
    """Read a CSV with a header row into a dict of column name -> numpy array."""
    data = np.genfromtxt(Path(path), delimiter=",", names=True)
    return {name: data[name] for name in data.dtype.names}


def plot_curves(path, ylabel="loss", figsize=(6, 3.2)):
    """Line plot of every column against the first one (e.g. step)."""
    cols = read_csv(path)
    names = list(cols)

    def draw(theme):
        fig, ax = plt.subplots(figsize=figsize)
        for name in names[1:]:
            ax.plot(cols[names[0]], cols[name], label=name.replace("_", " "))
        ax.set_xlabel(names[0])
        ax.set_ylabel(ylabel)
        ax.legend()
        fig.tight_layout()

    _in_both_themes(draw)


def plot_grid(path, xlabel="", ylabel=""):
    """Heatmap of a 2-D grid saved as CSV (first row/column are labels)."""
    raw = np.genfromtxt(Path(path), delimiter=",", dtype=str)
    xticks, yticks = raw[0, 1:], raw[1:, 0]
    values = raw[1:, 1:].astype(float)

    def draw(theme):
        fig, ax = plt.subplots(figsize=(9, 3.2))
        cmap = THEMES[theme]["seq"]
        im = ax.imshow(values, cmap=cmap, aspect="auto")
        ax.set_xticks(range(len(xticks)), xticks)
        ax.set_yticks(range(len(yticks)), yticks)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        for i in range(values.shape[0]):
            for j in range(values.shape[1]):
                r, g, b, _ = cmap(im.norm(values[i, j]))
                light_cell = 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.45
                ax.text(j, i, f"{values[i, j]:.0f}", ha="center", va="center", fontsize=8,
                        color="black" if light_cell else "white")
        cbar = fig.colorbar(im, ax=ax, fraction=0.03)
        cbar.outline.set_edgecolor(THEMES[theme]["muted"])
        fig.tight_layout()

    _in_both_themes(draw)
