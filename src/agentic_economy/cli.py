"""Command-line interface for running agentic economy experiments."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from dotenv import load_dotenv

from .llm_client import LLMClient
from .simulation import (
    BarterChatCreditSimulation,
    BarterChatSimulation,
    BarterSimulation,
    BarterWithCreditSimulation,
    BaseSimulation,
    CentralPlannerSimulation,
    MoneyExchangeSimulation,
)

DEFAULT_N_VALUES = [3, 5, 7]
DEFAULT_MODEL = "gpt-5-mini"


def configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
    )


def run_experiment(
    condition: str,
    n: int,
    seed: int,
    rounds: int,
    history_limit: int,
    model: str,
    output_dir: Path,
) -> Path:
    llm_client = LLMClient(model=model)
    simulation: BaseSimulation
    if condition == "barter":
        simulation = BarterSimulation(
            n_agents=n,
            rounds=rounds,
            seed=seed,
            history_limit=history_limit,
            llm_client=llm_client,
            model_name=model,
        )
    elif condition == "barter_chat":
        simulation = BarterChatSimulation(
            n_agents=n,
            rounds=rounds,
            seed=seed,
            history_limit=history_limit,
            llm_client=llm_client,
            model_name=model,
        )
    elif condition == "barter_credit":
        simulation = BarterWithCreditSimulation(
            n_agents=n,
            rounds=rounds,
            seed=seed,
            history_limit=history_limit,
            llm_client=llm_client,
            model_name=model,
        )
    elif condition == "barter_chat_credit":
        simulation = BarterChatCreditSimulation(
            n_agents=n,
            rounds=rounds,
            seed=seed,
            history_limit=history_limit,
            llm_client=llm_client,
            model_name=model,
        )
    elif condition == "money_exchange":
        simulation = MoneyExchangeSimulation(
            n_agents=n,
            rounds=rounds,
            seed=seed,
            history_limit=history_limit,
            llm_client=llm_client,
            model_name=model,
        )
    elif condition == "central_planner":
        simulation = CentralPlannerSimulation(
            n_agents=n,
            rounds=rounds,
            seed=seed,
            history_limit=history_limit,
            llm_client=llm_client,
            model_name=model,
        )
    else:
        raise ValueError(f"Unknown condition {condition}")

    result = simulation.run()
    path = output_dir / f"{condition}_N{n}_seed{seed}.json"
    result.write_json(path)
    logging.info(
        json.dumps(
            {
                "event": "run_complete",
                "condition": condition,
                "N": n,
                "seed": seed,
                "rounds_run": result.rounds_run,
                "successful_agents": result.successful_agents,
                "output": str(path),
            }
        )
    )
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run agentic economy experiments.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run barter and/or money-exchange experiments.")
    run_parser.add_argument(
        "--conditions",
        nargs="+",
        choices=[
            "barter",
            "barter_chat",
            "barter_credit",
            "barter_chat_credit",
            "money_exchange",
            "central_planner",
        ],
        default=["barter", "money_exchange"],
        help="Which conditions to run.",
    )
    run_parser.add_argument(
        "--n",
        dest="n_values",
        type=int,
        nargs="+",
        default=DEFAULT_N_VALUES,
        help="Agent counts to simulate.",
    )
    run_parser.add_argument(
        "--seeds",
        type=int,
        default=2,
        help="Number of seeds (0..seeds-1) to run per N.",
    )
    run_parser.add_argument(
        "--rounds",
        type=int,
        default=12,
        help="Max rounds per simulation.",
    )
    run_parser.add_argument(
        "--history-limit",
        type=int,
        default=10,
        help="How many prior messages each agent sees.",
    )
    run_parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help="Model name for responses API.",
    )
    run_parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs"),
        help="Directory to store run JSON logs.",
    )
    run_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )

    llm_parser = subparsers.add_parser("llm-live", help="Tiny live sanity check run.")
    llm_parser.add_argument(
        "--condition",
        choices=["barter", "barter_chat", "barter_chat_credit", "money_exchange"],
        default="barter",
        help="Condition to run for the smoke test.",
    )
    llm_parser.add_argument("--n", type=int, default=3, help="Number of agents.")
    llm_parser.add_argument("--seed", type=int, default=0, help="Random seed.")
    llm_parser.add_argument("--rounds", type=int, default=4, help="Rounds to simulate.")
    llm_parser.add_argument(
        "--history-limit",
        type=int,
        default=6,
        help="Messages to show each agent.",
    )
    llm_parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help="Model name for responses API.",
    )
    llm_parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs"),
        help="Directory to store run JSON logs.",
    )
    llm_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv()
    configure_logging(args.verbose)

    if args.command == "run":
        seeds = list(range(args.seeds))
        for condition in args.conditions:
            for n in args.n_values:
                for seed in seeds:
                    run_experiment(
                        condition=condition,
                        n=n,
                        seed=seed,
                        rounds=args.rounds,
                        history_limit=args.history_limit,
                        model=args.model,
                        output_dir=args.output_dir,
                    )
    elif args.command == "llm-live":
        run_experiment(
            condition=args.condition,
            n=args.n,
            seed=args.seed,
            rounds=args.rounds,
            history_limit=args.history_limit,
            model=args.model,
            output_dir=args.output_dir,
        )
    else:
        raise ValueError(f"Unknown command {args.command}")


if __name__ == "__main__":
    main()
