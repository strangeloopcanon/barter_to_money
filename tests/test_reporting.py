from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pandas as pd

from agentic_economy import reporting


def test_generate_core_sweep_overview(tmp_path: Path) -> None:
    core_df = pd.read_csv(Path("results/runs_core_aggregate.csv"))
    outputs = reporting.generate_core_sweep_overview(core_df, tmp_path)

    expected = {tmp_path / "core_sweep_overview.png", tmp_path / "core_sweep_overview.pdf"}
    assert set(outputs) == expected
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0


def test_write_core_sweep_latex_table(tmp_path: Path) -> None:
    core_df = pd.read_csv(Path("results/runs_core_aggregate.csv"))
    out_path = tmp_path / "core_sweep_table.tex"
    written = reporting.write_core_sweep_latex_table(core_df, out_path)

    assert written == out_path
    contents = out_path.read_text(encoding="utf-8")
    assert "\\begin{table}" in contents
    assert "\\caption{" in contents
    assert "Money/Exchange" in contents


def test_main_generates_outputs(tmp_path: Path, monkeypatch: Any) -> None:
    out_dir = tmp_path / "figures"
    paper_dir = tmp_path / "paper"
    argv = [
        "agentic_economy.reporting",
        "--core-aggregate",
        "results/runs_core_aggregate.csv",
        "--out-dir",
        str(out_dir),
        "--paper-dir",
        str(paper_dir),
    ]
    monkeypatch.setattr(sys, "argv", argv)
    reporting.main()

    assert (out_dir / "core_sweep_overview.png").exists()
    assert (out_dir / "core_sweep_overview.pdf").exists()
    assert (paper_dir / "core_sweep_table.tex").exists()
