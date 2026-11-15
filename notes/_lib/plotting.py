"""Plotting helpers for notes.

Notes only import these functions and read saved results from disk; experiments live elsewhere.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Lato", "Verdana", "DejaVu Sans"],
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

BLUE, ORANGE, GREY = "#1772d0", "#f09228", "#888888"


def read_csv(path):
    """Read a CSV with a header row into a dict of column name -> numpy array."""
    data = np.genfromtxt(Path(path), delimiter=",", names=True)
    return {name: data[name] for name in data.dtype.names}


def plot_curves(path, ylabel="loss", figsize=(6, 3.2)):
    """Line plot of every column against the first one (e.g. step)."""
    cols = read_csv(path)
    names = list(cols)
    fig, ax = plt.subplots(figsize=figsize)
    for name, color in zip(names[1:], [BLUE, ORANGE, GREY, "black"]):
        ax.plot(cols[names[0]], cols[name], label=name.replace("_", " "), color=color)
    ax.set_xlabel(names[0])
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False)
    fig.tight_layout()
    return fig


def plot_grid(path, xlabel="", ylabel="", cmap="Blues"):
    """Heatmap of a 2-D grid saved as CSV (first row/column are labels)."""
    raw = np.genfromtxt(Path(path), delimiter=",", dtype=str)
    xticks, yticks = raw[0, 1:], raw[1:, 0]
    values = raw[1:, 1:].astype(float)
    fig, ax = plt.subplots(figsize=(9, 3.2))
    im = ax.imshow(values, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(xticks)), xticks)
    ax.set_yticks(range(len(yticks)), yticks)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            ax.text(j, i, f"{values[i, j]:.0f}", ha="center", va="center", fontsize=8,
                    color="white" if values[i, j] > values.max() / 2 else "black")
    fig.colorbar(im, ax=ax, fraction=0.03)
    fig.tight_layout()
    return fig
