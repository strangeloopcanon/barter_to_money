"""Helpers to load and summarize run logs."""

from __future__ import annotations

import glob
import json
from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class RunSummary:
    condition: str
    n_agents: int
    total_messages: int
    unique_pairs: int
    success_rate: float
    rounds_run: int
    path: str
    exchange_inbox_messages: int = 0
    exchange_outbox_messages: int = 0
    exchange_price_update_count: int = 0
    exchange_price_abs_change: float = 0.0


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
    for path in glob.glob(pattern):
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        messages = data.get("messages", [])
        total_messages = len(messages)
        unique_pairs = _unique_pairs(messages)
        agents = data.get("agents", {})
        inventory_final = data.get("inventory_final", {})

        success_count = 0
        for agent_name, agent_meta in agents.items():
            target = agent_meta.get("target")
            inventory = inventory_final.get(agent_name, {})
            if inventory.get(target, 0) >= 1:
                success_count += 1

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
                condition=data.get("condition", "unknown"),
                n_agents=data.get("N", 0),
                total_messages=total_messages,
                unique_pairs=unique_pairs,
                success_rate=success_count / max(len(agents), 1),
                rounds_run=data.get("rounds_run", 0),
                path=path,
                exchange_inbox_messages=exchange_inbox_messages,
                exchange_outbox_messages=exchange_outbox_messages,
                exchange_price_update_count=exchange_price_update_count,
                exchange_price_abs_change=exchange_price_abs_change,
            ).__dict__
        )

    return pd.DataFrame(rows)


def aggregate_runs(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    return (
        df.groupby(["condition", "n_agents"])
        .agg(
            total_messages_mean=("total_messages", "mean"),
            total_messages_std=("total_messages", "std"),
            unique_pairs_mean=("unique_pairs", "mean"),
            unique_pairs_std=("unique_pairs", "std"),
            success_rate_mean=("success_rate", "mean"),
            rounds_run_mean=("rounds_run", "mean"),
            exchange_inbox_messages_mean=("exchange_inbox_messages", "mean"),
            exchange_inbox_messages_std=("exchange_inbox_messages", "std"),
            exchange_outbox_messages_mean=("exchange_outbox_messages", "mean"),
            exchange_outbox_messages_std=("exchange_outbox_messages", "std"),
            exchange_price_update_count_mean=("exchange_price_update_count", "mean"),
            exchange_price_update_count_std=("exchange_price_update_count", "std"),
            exchange_price_abs_change_mean=("exchange_price_abs_change", "mean"),
            exchange_price_abs_change_std=("exchange_price_abs_change", "std"),
        )
        .reset_index()
        .sort_values(["condition", "n_agents"])
    )


def main() -> None:
    df = load_runs()
    if df.empty:
        print("No run logs found in runs/*.json")
        return
    print("Loaded runs:")
    print(df)
    print("\nAggregated:")
    print(aggregate_runs(df))


if __name__ == "__main__":
    main()
