"""Generate consolidated Markdown pages for results.

These pages are designed for readers (blogposts / papers), and are generated from the
committed CSVs in `results/` so they can be reproduced without raw `runs*/` logs.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd


def _configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def _stringify_cell(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).replace("|", "\\|")


def _write_markdown_table(df: pd.DataFrame, columns: list[str]) -> list[str]:
    lines: list[str] = []
    lines.append("| " + " | ".join(columns) + " |")
    lines.append("| " + " | ".join(["---"] * len(columns)) + " |")
    for _, row in df.iterrows():
        cells = [_stringify_cell(row[col]) for col in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def _round_float_columns(df: pd.DataFrame, decimals: int) -> pd.DataFrame:
    rounded = df.copy()
    float_cols = [col for col in rounded.columns if rounded[col].dtype.kind == "f"]
    for col in float_cols:
        rounded[col] = rounded[col].round(decimals)
    return rounded


def write_all_results_page(
    all_runs_full_csv: Path,
    all_runs_aggregate_csv: Path,
    out_path: Path,
) -> Path:
    full_df = pd.read_csv(all_runs_full_csv)
    agg_df = pd.read_csv(all_runs_aggregate_csv)

    full_df = _round_float_columns(full_df, decimals=3)
    if "success_rate" in full_df.columns:
        full_df["success_rate"] = full_df["success_rate"].round(2)

    agg_df = _round_float_columns(agg_df, decimals=3)

    full_columns = [
        "run_set",
        "condition",
        "n_agents",
        "seed",
        "model",
        "rounds_cap",
        "history_limit",
        "success_rate",
        "rounds_run",
        "total_messages",
        "unique_pairs",
        "credit_proposals",
        "credit_accepts",
        "send_messages",
        "invalid_actions",
        "path",
    ]
    full_columns = [col for col in full_columns if col in full_df.columns]

    agg_columns = [
        "run_set",
        "condition",
        "n_agents",
        "model",
        "rounds_cap",
        "history_limit",
        "runs",
        "success_rate_mean",
        "success_rate_std",
        "rounds_run_mean",
        "rounds_run_std",
        "total_messages_mean",
        "total_messages_std",
        "unique_pairs_mean",
        "unique_pairs_std",
        "exchange_inbox_messages_mean",
        "exchange_outbox_messages_mean",
        "exchange_price_update_count_mean",
        "exchange_price_abs_change_mean",
        "credit_proposals_mean",
        "credit_accepts_mean",
        "send_messages_mean",
        "invalid_actions_mean",
    ]
    agg_columns = [col for col in agg_columns if col in agg_df.columns]

    lines: list[str] = []
    lines.append("# All results (one page)")
    lines.append("")
    lines.append("Generated from committed CSVs:")
    lines.append(f"- `{all_runs_aggregate_csv.as_posix()}`")
    lines.append(f"- `{all_runs_full_csv.as_posix()}`")
    lines.append("")
    lines.append("## Aggregated")
    lines.append("")
    lines.extend(_write_markdown_table(agg_df, agg_columns))
    lines.append("")
    lines.append("## Per-run")
    lines.append("")
    lines.extend(_write_markdown_table(full_df, full_columns))
    lines.append("")
    lines.append("Regenerate with `make results-all`.")
    lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def _format_mean_std(mean: Any, std: Any, decimals: int) -> str:
    if pd.isna(mean):
        return ""
    mean_f = float(mean)
    if pd.isna(std):
        return f"{mean_f:.{decimals}f}"
    std_f = float(std)
    return f"{mean_f:.{decimals}f} ± {std_f:.{decimals}f}"


def _select_showcase_row(
    df: pd.DataFrame,
    *,
    condition: str,
    n_agents: int,
    rounds_cap: int,
    model: str,
    preferred_run_sets: list[str],
) -> pd.Series:
    filtered = df[
        (df["condition"] == condition)
        & (df["n_agents"] == n_agents)
        & (df["rounds_cap"] == rounds_cap)
        & (df["model"] == model)
    ].copy()

    if filtered.empty:
        raise ValueError(
            "No aggregated rows found for showcase selection",
            {
                "condition": condition,
                "n_agents": n_agents,
                "rounds_cap": rounds_cap,
                "model": model,
            },
        )

    for run_set in preferred_run_sets:
        match = filtered[filtered["run_set"] == run_set]
        if not match.empty:
            return match.sort_values("runs", ascending=False).iloc[0]

    return filtered.sort_values("runs", ascending=False).iloc[0]


def write_showcase_page(
    all_runs_aggregate_csv: Path,
    out_path: Path,
    *,
    n_agents: int,
    rounds_cap: int,
    model: str,
    latex_out_path: Path,
) -> tuple[Path, Path]:
    agg_df = pd.read_csv(all_runs_aggregate_csv)
    agg_df = _round_float_columns(agg_df, decimals=3)

    selections = [
        ("barter", ["runs_core", "runs_5mini_emergent", "runs_5mini_full"]),
        ("money_exchange", ["runs_core", "runs_5mini_full", "runs_5mini_smoke"]),
        ("central_planner", ["runs_5mini_full", "runs_5mini_smoke"]),
        ("barter_credit", ["runs_5mini_emergent", "runs_chat_credit_retest"]),
    ]

    rows: list[dict[str, Any]] = []
    latex_rows: list[dict[str, Any]] = []
    condition_labels = {
        "money_exchange": "Money/Exchange",
        "central_planner": "Central planner",
        "barter_credit": "Barter + credits",
        "barter": "Barter",
    }
    for condition, preferred in selections:
        row = _select_showcase_row(
            agg_df,
            condition=condition,
            n_agents=n_agents,
            rounds_cap=rounds_cap,
            model=model,
            preferred_run_sets=preferred,
        )

        rows.append(
            {
                "condition": condition_labels.get(condition, condition),
                "run_set": row["run_set"],
                "runs": int(row["runs"]),
                "success_rate": _format_mean_std(
                    row.get("success_rate_mean"), row.get("success_rate_std"), 3
                ),
                "rounds_run": _format_mean_std(
                    row.get("rounds_run_mean"), row.get("rounds_run_std"), 2
                ),
                "total_messages": _format_mean_std(
                    row.get("total_messages_mean"), row.get("total_messages_std"), 1
                ),
                "unique_pairs": _format_mean_std(
                    row.get("unique_pairs_mean"), row.get("unique_pairs_std"), 2
                ),
                "credit_accepts": _format_mean_std(
                    row.get("credit_accepts_mean"), row.get("credit_accepts_std"), 2
                ),
            }
        )

        latex_rows.append(
            {
                "condition": condition,
                "runs": int(row["runs"]),
                "success_rate_mean": row.get("success_rate_mean"),
                "success_rate_std": row.get("success_rate_std"),
                "rounds_run_mean": row.get("rounds_run_mean"),
                "rounds_run_std": row.get("rounds_run_std"),
                "total_messages_mean": row.get("total_messages_mean"),
                "total_messages_std": row.get("total_messages_std"),
            }
        )

    showcase_df = pd.DataFrame(rows)
    columns = [
        "condition",
        "run_set",
        "runs",
        "success_rate",
        "rounds_run",
        "total_messages",
        "unique_pairs",
        "credit_accepts",
    ]

    lines: list[str] = []
    lines.append("# Showcase results (the 4-condition table)")
    lines.append("")
    lines.append(
        "This is the curated 4-condition summary table intended for the writeup. "
        "It selects the most comparable available `N`, `R`, and `model` rows for each institution "
        "and includes `run_set` so the provenance is explicit."
    )
    lines.append("")
    lines.append(f"- Source: `{all_runs_aggregate_csv.as_posix()}`")
    lines.append(f"- N = {n_agents}, R = {rounds_cap}, model = `{model}`")
    lines.append(f"- LaTeX version: `{latex_out_path.as_posix()}`")
    lines.append("")
    lines.extend(_write_markdown_table(showcase_df, columns))
    lines.append("")
    lines.append("Full details: `results/all_results.md`.")
    lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")

    latex_out_path.parent.mkdir(parents=True, exist_ok=True)
    latex_lines: list[str] = []
    latex_lines.append("% Generated by agentic_economy.results_pages")
    latex_lines.append("\\begin{table}[t]")
    latex_lines.append("\\centering")
    latex_lines.append("\\begin{tabular}{lrrrr}")
    latex_lines.append("\\hline")
    latex_lines.append(
        "Condition & runs & success (mean $\\pm$ std) & rounds (mean $\\pm$ std) & messages (mean $\\pm$ std)\\\\"
    )
    latex_lines.append("\\hline")
    for entry in latex_rows:
        condition = entry["condition"]
        label = {
            "money_exchange": "Money/Exchange",
            "central_planner": "Central planner",
            "barter_credit": "Barter + credits",
            "barter": "Barter",
        }.get(condition, condition)

        success = _format_mean_std(
            entry["success_rate_mean"], entry["success_rate_std"], 3
        ).replace("±", "$\\pm$")
        rounds = _format_mean_std(entry["rounds_run_mean"], entry["rounds_run_std"], 2).replace(
            "±", "$\\pm$"
        )
        msgs = _format_mean_std(
            entry["total_messages_mean"], entry["total_messages_std"], 1
        ).replace("±", "$\\pm$")
        latex_lines.append(f"{label} & {entry['runs']} & {success} & {rounds} & {msgs}\\\\")
    latex_lines.append("\\hline")
    latex_lines.append("\\end{tabular}")
    latex_lines.append(
        f"\\caption{{Showcase results at N={n_agents}, round cap R={rounds_cap} (model={model}).}}"
    )
    latex_lines.append("\\label{tab:showcase}")
    latex_lines.append("\\end{table}")
    latex_lines.append("")
    latex_out_path.write_text("\n".join(latex_lines), encoding="utf-8")

    return out_path, latex_out_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate consolidated results pages (comprehensive + showcase)."
    )
    parser.add_argument(
        "--all-full",
        type=Path,
        default=Path("results/all_runs_full.csv"),
        help="Path to per-run results CSV.",
    )
    parser.add_argument(
        "--all-aggregate",
        type=Path,
        default=Path("results/all_runs_aggregate.csv"),
        help="Path to aggregated results CSV.",
    )
    parser.add_argument(
        "--out-all",
        type=Path,
        default=Path("results/all_results.md"),
        help="Path to write the combined one-page results Markdown.",
    )
    parser.add_argument(
        "--out-showcase",
        type=Path,
        default=Path("results/showcase.md"),
        help="Path to write the 4-condition showcase Markdown.",
    )
    parser.add_argument(
        "--out-showcase-tex",
        type=Path,
        default=Path("results/paper/showcase_table.tex"),
        help="Path to write the LaTeX showcase table.",
    )
    parser.add_argument("--n", type=int, default=8, help="N to use for the showcase table.")
    parser.add_argument(
        "--rounds-cap", type=int, default=8, help="Round cap R for the showcase table."
    )
    parser.add_argument(
        "--model", type=str, default="gpt-5-mini", help="Model name for the showcase table."
    )
    return parser.parse_args()


def main() -> None:
    _configure_logging()
    args = parse_args()

    if not args.all_full.exists():
        raise FileNotFoundError(
            f"Missing {args.all_full}. Run `make results-all` first (or pass --all-full)."
        )
    if not args.all_aggregate.exists():
        raise FileNotFoundError(
            f"Missing {args.all_aggregate}. Run `make results-all` first (or pass --all-aggregate)."
        )

    created: list[Path] = []
    created.append(write_all_results_page(args.all_full, args.all_aggregate, args.out_all))
    showcase_md, showcase_tex = write_showcase_page(
        args.all_aggregate,
        args.out_showcase,
        n_agents=args.n,
        rounds_cap=args.rounds_cap,
        model=args.model,
        latex_out_path=args.out_showcase_tex,
    )
    created.extend([showcase_md, showcase_tex])

    logging.info(
        json.dumps(
            {
                "event": "results_pages_generated",
                "inputs": {
                    "all_full": str(args.all_full),
                    "all_aggregate": str(args.all_aggregate),
                },
                "outputs": [str(path) for path in created],
            }
        )
    )


if __name__ == "__main__":
    main()
