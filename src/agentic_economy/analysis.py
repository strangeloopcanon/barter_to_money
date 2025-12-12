"""Helpers to load and summarize run logs."""

from __future__ import annotations

import argparse
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
    for path in glob.glob(pattern):
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        messages = data.get("messages", [])
        total_messages = len(messages)
        unique_pairs = _unique_pairs(messages)
        agents = data.get("agents", {})
        inventory_final = data.get("inventory_final", {})
        goods = {f"g{i}" for i in range(int(data.get("N", 0)))}

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
        .sort_values(["condition", "n_agents"])
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize run logs.")
    parser.add_argument(
        "--pattern",
        type=str,
        default="runs/*.json",
        help="Glob pattern for run JSON logs.",
    )
    args = parser.parse_args()
    df = load_runs(args.pattern)
    if df.empty:
        print(f"No run logs found for pattern {args.pattern}")
        return
    print("Loaded runs:")
    print(df)
    print("\nAggregated:")
    print(aggregate_runs(df))


if __name__ == "__main__":
    main()
