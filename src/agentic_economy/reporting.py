"""Generate blog/paper-friendly figures and tables from result CSVs.

This intentionally operates on the committed `results/*_aggregate.csv` files so the output
can be reproduced without requiring raw `runs*/` logs.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def _configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def _required_columns(df: pd.DataFrame, columns: list[str], label: str) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"{label} missing columns: {missing}")


def _condition_label(condition: str) -> str:
    mapping = {
        "money_exchange": "Money/Exchange",
        "central_planner": "Central planner",
        "barter_chat_credit": "Barter + chat + credits",
        "barter_chat": "Barter + chat",
        "barter_credit": "Barter + credits",
        "barter": "Barter",
    }
    return mapping.get(condition, condition)


def _plot_line(
    ax: plt.Axes,
    df: pd.DataFrame,
    condition: str,
    y_col: str,
    yerr_col: str | None,
    *,
    color: str,
    marker: str,
) -> None:
    cond_df = df[df["condition"] == condition].sort_values("n_agents")
    x = cond_df["n_agents"]
    y = cond_df[y_col]
    yerr = cond_df[yerr_col] if yerr_col and yerr_col in cond_df.columns else None
    ax.errorbar(
        x,
        y,
        yerr=yerr,
        label=_condition_label(condition),
        color=color,
        marker=marker,
        linewidth=2.0,
        markersize=5.0,
        capsize=3,
    )


def generate_core_sweep_overview(core_df: pd.DataFrame, out_dir: Path) -> list[Path]:
    required = [
        "condition",
        "n_agents",
        "success_rate_mean",
        "success_rate_std",
        "rounds_run_mean",
        "rounds_run_std",
        "total_messages_mean",
        "total_messages_std",
        "unique_pairs_mean",
        "unique_pairs_std",
        "rounds_cap",
    ]
    _required_columns(core_df, required, "core_df")

    df = core_df.copy()
    df = df[df["condition"].isin(["barter", "money_exchange"])]
    if df.empty:
        raise ValueError("core_df contains no rows for barter/money_exchange")

    rounds_cap = int(df["rounds_cap"].max())
    n_values = sorted(df["n_agents"].unique().tolist())

    try:
        plt.style.use("seaborn-v0_8-colorblind")
    except (OSError, ValueError):
        plt.style.use("tableau-colorblind10")
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)
    (ax_success, ax_rounds), (ax_msgs, ax_pairs) = axes

    colors = {"barter": "#1f77b4", "money_exchange": "#ff7f0e"}
    markers = {"barter": "o", "money_exchange": "s"}
    for condition in ["barter", "money_exchange"]:
        _plot_line(
            ax_success,
            df,
            condition,
            "success_rate_mean",
            "success_rate_std",
            color=colors[condition],
            marker=markers[condition],
        )
        _plot_line(
            ax_rounds,
            df,
            condition,
            "rounds_run_mean",
            "rounds_run_std",
            color=colors[condition],
            marker=markers[condition],
        )
        _plot_line(
            ax_msgs,
            df,
            condition,
            "total_messages_mean",
            "total_messages_std",
            color=colors[condition],
            marker=markers[condition],
        )
        _plot_line(
            ax_pairs,
            df,
            condition,
            "unique_pairs_mean",
            "unique_pairs_std",
            color=colors[condition],
            marker=markers[condition],
        )

    ax_success.set_title("Success rate (mean ± std)")
    ax_success.set_xlabel("N agents")
    ax_success.set_ylabel("Success rate")
    ax_success.set_ylim(-0.02, 1.02)
    ax_success.set_xticks(n_values)
    ax_success.grid(True, alpha=0.25)

    ax_rounds.set_title("Rounds run (mean ± std)")
    ax_rounds.set_xlabel("N agents")
    ax_rounds.set_ylabel("Rounds")
    ax_rounds.set_ylim(0, max(rounds_cap, int(df["rounds_run_mean"].max())) + 1)
    ax_rounds.set_xticks(n_values)
    ax_rounds.grid(True, alpha=0.25)

    ax_msgs.set_title("Total messages (mean ± std)")
    ax_msgs.set_xlabel("N agents")
    ax_msgs.set_ylabel("Messages")
    ax_msgs.set_xticks(n_values)
    ax_msgs.grid(True, alpha=0.25)

    ax_pairs.set_title("Unique pairs contacted (mean ± std)")
    ax_pairs.set_xlabel("N agents")
    ax_pairs.set_ylabel("Unique pairs")
    ax_pairs.set_xticks(n_values)
    ax_pairs.grid(True, alpha=0.25)

    handles, labels = ax_success.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False)
    fig.suptitle(f"Core sweep overview (round cap R={rounds_cap})", y=1.02)

    out_dir.mkdir(parents=True, exist_ok=True)
    png_path = out_dir / "core_sweep_overview.png"
    pdf_path = out_dir / "core_sweep_overview.pdf"
    fig.savefig(png_path, dpi=200, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)

    return [png_path, pdf_path]


def write_core_sweep_latex_table(core_df: pd.DataFrame, out_path: Path) -> Path:
    required = [
        "condition",
        "n_agents",
        "runs",
        "rounds_cap",
        "success_rate_mean",
        "success_rate_std",
        "rounds_run_mean",
        "rounds_run_std",
        "model",
    ]
    _required_columns(core_df, required, "core_df")

    df = core_df.copy()
    df = df[df["condition"].isin(["barter", "money_exchange"])]
    df = df.sort_values(["condition", "n_agents"])
    if df.empty:
        raise ValueError("core_df contains no rows for barter/money_exchange")

    rounds_cap = int(df["rounds_cap"].max())
    model = str(df["model"].mode().iloc[0]) if "model" in df.columns and not df.empty else "unknown"

    lines: list[str] = []
    lines.append("% Generated by agentic_economy.reporting")
    lines.append("\\begin{table}[t]")
    lines.append("\\centering")
    lines.append("\\begin{tabular}{llrrrr}")
    lines.append("\\hline")
    lines.append(
        "Condition & N & runs & R & success (mean $\\pm$ std) & rounds (mean $\\pm$ std)\\\\"
    )
    lines.append("\\hline")
    for _, row in df.iterrows():
        condition = _condition_label(str(row["condition"]))
        n_agents = int(row["n_agents"])
        runs = int(row["runs"])
        success_mean = float(row["success_rate_mean"])
        success_std = float(row.get("success_rate_std", 0.0) or 0.0)
        rounds_mean = float(row["rounds_run_mean"])
        rounds_std = float(row.get("rounds_run_std", 0.0) or 0.0)
        lines.append(
            f"{condition} & {n_agents} & {runs} & {rounds_cap} & "
            f"{success_mean:.3f} $\\pm$ {success_std:.3f} & "
            f"{rounds_mean:.2f} $\\pm$ {rounds_std:.2f}\\\\"
        )
    lines.append("\\hline")
    lines.append("\\end{tabular}")
    caption = (
        "Core sweep results for barter vs Money/Exchange "
        f"(model={model}, round cap R={rounds_cap}). "
        "Error bars are std across seeds."
    )
    lines.append(f"\\caption{{{caption}}}")
    lines.append("\\label{tab:core-sweep}")
    lines.append("\\end{table}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate figures/tables for blogposts or papers.")
    parser.add_argument(
        "--core-aggregate",
        type=Path,
        default=Path("results/runs_core_aggregate.csv"),
        help="Path to core sweep aggregated CSV.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("results/figures"),
        help="Directory to write figures (PNG/PDF).",
    )
    parser.add_argument(
        "--paper-dir",
        type=Path,
        default=Path("results/paper"),
        help="Directory to write paper artifacts (e.g., LaTeX tables).",
    )
    return parser.parse_args()


def main() -> None:
    _configure_logging()
    args = parse_args()
    core_path: Path = args.core_aggregate
    if not core_path.exists():
        raise FileNotFoundError(
            f"Core aggregate CSV not found at {core_path}. Run `make results-core` first."
        )
    core_df = pd.read_csv(core_path)

    created: list[Path] = []
    created.extend(generate_core_sweep_overview(core_df, args.out_dir))
    created.append(write_core_sweep_latex_table(core_df, args.paper_dir / "core_sweep_table.tex"))

    logging.info(
        json.dumps(
            {
                "event": "report_generated",
                "core_aggregate": str(core_path),
                "outputs": [str(path) for path in created],
            }
        )
    )


if __name__ == "__main__":
    main()
