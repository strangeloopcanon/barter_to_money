from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from agentic_economy import results_pages


def test_write_all_results_page(tmp_path: Path) -> None:
    out_path = tmp_path / "all_results.md"
    results_pages.write_all_results_page(
        Path("results/all_runs_full.csv"),
        Path("results/all_runs_aggregate.csv"),
        out_path,
    )
    contents = out_path.read_text(encoding="utf-8")
    assert "# All results (one page)" in contents
    assert "## Aggregated" in contents
    assert "## Per-run" in contents


def test_write_showcase_page(tmp_path: Path) -> None:
    out_md = tmp_path / "showcase.md"
    out_tex = tmp_path / "showcase_table.tex"
    results_pages.write_showcase_page(
        Path("results/all_runs_aggregate.csv"),
        out_md,
        n_agents=8,
        rounds_cap=8,
        model="gpt-5-mini",
        latex_out_path=out_tex,
    )
    md = out_md.read_text(encoding="utf-8")
    assert "Barter" in md
    assert "Money/Exchange" in md
    assert "Central planner" in md
    assert "Barter + credits" in md

    tex = out_tex.read_text(encoding="utf-8")
    assert "\\begin{table}" in tex
    assert "\\label{tab:showcase}" in tex
    assert "Money/Exchange" in tex


def test_main_generates_pages(tmp_path: Path, monkeypatch: Any) -> None:
    out_all = tmp_path / "all_results.md"
    out_showcase = tmp_path / "showcase.md"
    out_showcase_tex = tmp_path / "showcase_table.tex"
    argv = [
        "agentic_economy.results_pages",
        "--all-full",
        "results/all_runs_full.csv",
        "--all-aggregate",
        "results/all_runs_aggregate.csv",
        "--out-all",
        str(out_all),
        "--out-showcase",
        str(out_showcase),
        "--out-showcase-tex",
        str(out_showcase_tex),
        "--n",
        "8",
        "--rounds-cap",
        "8",
        "--model",
        "gpt-5-mini",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    results_pages.main()

    assert out_all.exists()
    assert out_showcase.exists()
    assert out_showcase_tex.exists()
