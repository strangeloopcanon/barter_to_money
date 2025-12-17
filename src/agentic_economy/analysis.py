"""Helpers to load and summarize run logs."""

from __future__ import annotations

import argparse
import glob
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd


@dataclass
class RunSummary:
    run_set: str
    condition: str
    n_agents: int
    seed: int
    model: str
    rounds_cap: int
    history_limit: int
    total_messages: int
    unique_pairs: int
    success_count: int
    success_rate: float
    rounds_run: int
    path: str
    exchange_inbox_messages: int = 0
    exchange_outbox_messages: int = 0
    exchange_price_update_count: int = 0
    exchange_price_abs_change: float = 0.0
    credit_proposals: int = 0
    credit_accepts: int = 0
    send_messages: int = 0
    invalid_actions: int = 0


def _unique_pairs(messages: List[dict]) -> int:
    pairs = set()
    for msg in messages:
        sender = msg.get("sender")
        receiver = msg.get("receiver")
        if not sender or not receiver or sender == receiver:
            continue
        pairs.add(tuple(sorted((sender, receiver))))
    return len(pairs)


def load_runs(pattern: str = "runs/*.json") -> pd.DataFrame:
    rows = []
    for path in sorted(glob.glob(pattern)):
        log_path = Path(path)
        run_set = log_path.parent.name
        with log_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        messages = data.get("messages", [])
        total_messages = len(messages)
        unique_pairs = _unique_pairs(messages)
        agents = data.get("agents", {})
        inventory_final = data.get("inventory_final", {})
        goods = {f"g{i}" for i in range(int(data.get("N", 0)))}
        parameters = data.get("parameters") or {}
        seed = int(data.get("seed", 0))

        success_count = 0
        for agent_name, agent_meta in agents.items():
            target = agent_meta.get("target")
            inventory = inventory_final.get(agent_name, {})
            if inventory.get(target, 0) >= 1:
                success_count += 1

        proposals = {
            msg.get("message_id"): msg
            for msg in messages
            if msg.get("payload", {}).get("action") == "propose_trade"
        }
        credit_proposal_ids = [
            pid
            for pid, msg in proposals.items()
            if msg
            and (
                msg.get("payload", {}).get("give") not in goods
                or msg.get("payload", {}).get("receive") not in goods
            )
        ]
        credit_proposals = len(credit_proposal_ids)
        credit_accepts = sum(
            1
            for msg in messages
            if msg.get("payload", {}).get("action") == "accept"
            and msg.get("payload", {}).get("of_message_id") in credit_proposal_ids
        )
        send_messages = sum(
            1 for msg in messages if msg.get("payload", {}).get("action") == "send_message"
        )
        events = data.get("events") or []
        invalid_actions = 0
        if isinstance(events, list):
            invalid_actions = sum(
                1 for ev in events if isinstance(ev, dict) and ev.get("event") == "invalid_action"
            )

        exchange_round_metrics = data.get("exchange_round_metrics") or []
        exchange_inbox_messages = 0
        exchange_outbox_messages = 0
        exchange_price_update_count = 0
        exchange_price_abs_change = 0.0
        if isinstance(exchange_round_metrics, list):
            for metric in exchange_round_metrics:
                if not isinstance(metric, dict):
                    continue
                exchange_inbox_messages += int(metric.get("inbox_total", 0))
                exchange_outbox_messages += int(metric.get("outbox_total", 0))
                exchange_price_update_count += int(metric.get("price_update_count", 0))
                exchange_price_abs_change += float(metric.get("price_total_abs_change", 0.0))

        rows.append(
            RunSummary(
                run_set=run_set,
                condition=data.get("condition", "unknown"),
                n_agents=data.get("N", 0),
                seed=seed,
                model=str(parameters.get("model") or data.get("model") or "unknown"),
                rounds_cap=int(parameters.get("rounds") or data.get("round_cap") or 0),
                history_limit=int(parameters.get("history_limit") or 0),
                total_messages=total_messages,
                unique_pairs=unique_pairs,
                success_count=success_count,
                success_rate=success_count / max(len(agents), 1),
                rounds_run=data.get("rounds_run", 0),
                path=str(log_path.as_posix()),
                exchange_inbox_messages=exchange_inbox_messages,
                exchange_outbox_messages=exchange_outbox_messages,
                exchange_price_update_count=exchange_price_update_count,
                exchange_price_abs_change=exchange_price_abs_change,
                credit_proposals=credit_proposals,
                credit_accepts=credit_accepts,
                send_messages=send_messages,
                invalid_actions=invalid_actions,
            ).__dict__
        )

    return pd.DataFrame(rows)


def aggregate_runs(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    return (
        df.groupby(["run_set", "condition", "n_agents", "model", "rounds_cap", "history_limit"])
        .agg(
            runs=("path", "count"),
            total_messages_mean=("total_messages", "mean"),
            total_messages_std=("total_messages", "std"),
            unique_pairs_mean=("unique_pairs", "mean"),
            unique_pairs_std=("unique_pairs", "std"),
            success_count_mean=("success_count", "mean"),
            success_count_std=("success_count", "std"),
            success_rate_mean=("success_rate", "mean"),
            success_rate_std=("success_rate", "std"),
            rounds_run_mean=("rounds_run", "mean"),
            rounds_run_std=("rounds_run", "std"),
            exchange_inbox_messages_mean=("exchange_inbox_messages", "mean"),
            exchange_inbox_messages_std=("exchange_inbox_messages", "std"),
            exchange_outbox_messages_mean=("exchange_outbox_messages", "mean"),
            exchange_outbox_messages_std=("exchange_outbox_messages", "std"),
            exchange_price_update_count_mean=("exchange_price_update_count", "mean"),
            exchange_price_update_count_std=("exchange_price_update_count", "std"),
            exchange_price_abs_change_mean=("exchange_price_abs_change", "mean"),
            exchange_price_abs_change_std=("exchange_price_abs_change", "std"),
            credit_proposals_mean=("credit_proposals", "mean"),
            credit_proposals_std=("credit_proposals", "std"),
            credit_accepts_mean=("credit_accepts", "mean"),
            credit_accepts_std=("credit_accepts", "std"),
            send_messages_mean=("send_messages", "mean"),
            send_messages_std=("send_messages", "std"),
            invalid_actions_mean=("invalid_actions", "mean"),
            invalid_actions_std=("invalid_actions", "std"),
        )
        .reset_index()
        .sort_values(["run_set", "condition", "n_agents"])
    )


def _stringify_cell(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).replace("|", "\\|")


def _write_markdown_table(
    df: pd.DataFrame, path: Path, columns: List[str], title: str, subtitle: str
) -> None:
    display_df = df.loc[:, columns].copy()
    display_df = display_df.where(pd.notnull(display_df), "")

    lines = [f"# {title}", "", subtitle, ""]
    lines.append("| " + " | ".join(columns) + " |")
    lines.append("| " + " | ".join(["---"] * len(columns)) + " |")

    for _, row in display_df.iterrows():
        cells = [_stringify_cell(row[col]) for col in columns]
        lines.append("| " + " | ".join(cells) + " |")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_outputs(
    runs_df: pd.DataFrame,
    aggregate_df: pd.DataFrame,
    out_csv: str | None,
    out_md: str | None,
    out_aggregate_csv: str | None,
    out_aggregate_md: str | None,
    pattern: str,
) -> None:
    if out_csv:
        out_path = Path(out_csv)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        runs_df.to_csv(out_path, index=False)

    if out_aggregate_csv:
        out_path = Path(out_aggregate_csv)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        aggregate_df.to_csv(out_path, index=False)

    if out_md:
        out_path = Path(out_md)
        markdown_df = runs_df.copy()
        if "success_rate" in markdown_df.columns:
            markdown_df["success_rate"] = markdown_df["success_rate"].round(2)
        markdown_columns = [
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
        ]
        markdown_columns = [col for col in markdown_columns if col in markdown_df.columns]
        _write_markdown_table(
            markdown_df.sort_values(["run_set", "condition", "n_agents", "seed"]),
            out_path,
            markdown_columns,
            title="Full per-run results",
            subtitle=f"Generated from `{pattern}` (raw run logs are not committed by default).",
        )

    if out_aggregate_md:
        out_path = Path(out_aggregate_md)
        markdown_df = aggregate_df.copy()
        float_columns = [col for col in markdown_df.columns if col.endswith(("_mean", "_std"))]
        for col in float_columns:
            markdown_df[col] = markdown_df[col].round(3)
        markdown_columns = [
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
        markdown_columns = [col for col in markdown_columns if col in markdown_df.columns]
        _write_markdown_table(
            markdown_df,
            out_path,
            markdown_columns,
            title="Aggregated results",
            subtitle=f"Grouped summary (means/std) from `{pattern}`.",
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize run logs.")
    parser.add_argument(
        "--pattern",
        type=str,
        default="runs/*.json",
        help="Glob pattern for run JSON logs.",
    )
    parser.add_argument("--out-csv", type=str, default="", help="Write per-run CSV to this path.")
    parser.add_argument(
        "--out-aggregate-csv",
        type=str,
        default="",
        help="Write aggregated CSV to this path.",
    )
    parser.add_argument(
        "--out-md",
        type=str,
        default="",
        help="Write per-run Markdown table to this path.",
    )
    parser.add_argument(
        "--out-aggregate-md",
        type=str,
        default="",
        help="Write aggregated Markdown table to this path.",
    )
    args = parser.parse_args()
    df = load_runs(args.pattern)
    if df.empty:
        print(f"No run logs found for pattern {args.pattern}")
        return
    aggregated = aggregate_runs(df)

    if args.out_csv or args.out_md or args.out_aggregate_csv or args.out_aggregate_md:
        _write_outputs(
            runs_df=df,
            aggregate_df=aggregated,
            out_csv=args.out_csv or None,
            out_md=args.out_md or None,
            out_aggregate_csv=args.out_aggregate_csv or None,
            out_aggregate_md=args.out_aggregate_md or None,
            pattern=args.pattern,
        )
        return

    print("Loaded runs:")
    print(df)
    print("\nAggregated:")
    print(aggregated)


if __name__ == "__main__":
    main()
