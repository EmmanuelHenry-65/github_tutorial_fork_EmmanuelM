from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import matplotlib

# Use a non-interactive backend so the plot can be saved without a display.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Save plots next to the project, not inside to_complete/.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PLOTS_DIR = PROJECT_ROOT / "artifacts" / "plots"


def create_visual_report(evaluation_bundle: Dict[str, Any]) -> Dict[str, Any]:
    """
    Turn model results into plots and visual summaries.

    Input contract:
    - evaluation_bundle["dataset_name"]: str
    - evaluation_bundle["metrics"]: dict
    - evaluation_bundle["sample_predictions"]: list[dict]
    - evaluation_bundle["confusion_matrix"]: list[list[int]]

    Expected work:
    - create at least one plot with matplotlib or seaborn
    - save the figure to disk
    - prepare chart notes for the dashboard step

    Tip:
    - confusion matrix plots work well for beginners

    Output contract:
    - dataset_name: str
    - metrics: dict
    - figure_paths: list[str]
    - chart_notes: list[str]
    - sample_predictions: list[dict]
    """
    dataset_name = evaluation_bundle["dataset_name"]
    metrics = evaluation_bundle.get("metrics", {})
    sample_predictions = evaluation_bundle.get("sample_predictions", [])
    confusion_matrix = evaluation_bundle.get("confusion_matrix", [])

    # Make sure the output folder exists before saving anything.
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    figure_paths: List[str] = []
    chart_notes: List[str] = []

    # 1) Confusion matrix heatmap -------------------------------------------
    if confusion_matrix:
        labels = _class_labels(sample_predictions, len(confusion_matrix))
        cm_path = _plot_confusion_matrix(confusion_matrix, labels, dataset_name)
        figure_paths.append(cm_path)
        chart_notes.append(
            "Confusion matrix: rows are the true water need, columns are the "
            "predicted water need. Big numbers on the diagonal mean good predictions."
        )

    # 2) Metric bar chart ----------------------------------------------------
    numeric_metrics = {k: v for k, v in metrics.items() if isinstance(v, (int, float))}
    if numeric_metrics:
        metrics_path = _plot_metrics_bar(numeric_metrics, dataset_name)
        figure_paths.append(metrics_path)
        note = ", ".join(f"{name} = {value:.2f}" for name, value in numeric_metrics.items())
        chart_notes.append(f"Model metrics: {note}.")

    if not chart_notes:
        chart_notes.append("No metrics or confusion matrix were available to plot.")

    return {
        "dataset_name": dataset_name,
        "metrics": metrics,
        "figure_paths": figure_paths,
        "chart_notes": chart_notes,
        "sample_predictions": sample_predictions,
    }


def _class_labels(sample_predictions: List[Dict[str, Any]], size: int) -> List[str]:
    """Guess readable class labels, falling back to numbered classes."""
    seen: List[str] = []
    for row in sample_predictions:
        for key in ("actual", "predicted"):
            value = row.get(key)
            if value is not None and value not in seen:
                seen.append(str(value))

    if len(seen) == size:
        return seen
    return [f"class {i}" for i in range(size)]


def _plot_confusion_matrix(
    confusion_matrix: List[List[int]], labels: List[str], dataset_name: str
) -> str:
    fig, ax = plt.subplots(figsize=(5, 4))
    image = ax.imshow(confusion_matrix, cmap="Blues")

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"Confusion matrix\n{dataset_name}")

    # Write the count inside each cell so the chart is readable on its own.
    for i, row in enumerate(confusion_matrix):
        for j, count in enumerate(row):
            ax.text(j, i, str(count), ha="center", va="center", color="black")

    fig.colorbar(image, ax=ax)
    fig.tight_layout()

    out_path = PLOTS_DIR / "confusion_matrix.png"
    fig.savefig(out_path, dpi=100)
    plt.close(fig)
    return _relative_path(out_path)


def _plot_metrics_bar(metrics: Dict[str, float], dataset_name: str) -> str:
    fig, ax = plt.subplots(figsize=(5, 4))
    names = list(metrics.keys())
    values = [metrics[name] for name in names]

    ax.bar(names, values, color="#2a9d8f")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Score")
    ax.set_title(f"Model metrics\n{dataset_name}")

    for i, value in enumerate(values):
        ax.text(i, value + 0.02, f"{value:.2f}", ha="center", va="bottom")

    fig.tight_layout()

    out_path = PLOTS_DIR / "metrics.png"
    fig.savefig(out_path, dpi=100)
    plt.close(fig)
    return _relative_path(out_path)


def _relative_path(path: Path) -> str:
    """Return a project-relative path when possible for tidy dashboard output."""
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(path)
