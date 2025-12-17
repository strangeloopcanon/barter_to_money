## Results tables

This repo stores raw run logs under `runs*/` (JSON), but those folders are gitignored to keep the repo small.
Instead, we publish generated per-run and aggregated tables here so the results are visible on GitHub.

Key idea: `run_set` in the tables is just the folder name the JSON came from (e.g. `runs_core`, `runs_chat_credit_retest`).

### One-page views

- All results (aggregated + per-run): [all_results.md](all_results.md)
- Showcase table (4 conditions): [showcase.md](showcase.md) (+ LaTeX: [paper/showcase_table.tex](paper/showcase_table.tex))

### Core sweep (barter vs money/Exchange)

- Per-run: [runs_core_full.md](runs_core_full.md)
- Aggregated: [runs_core_aggregate.md](runs_core_aggregate.md)

### All recorded runs (includes planner + credits)

- Per-run: [all_runs_full.md](all_runs_full.md)
- Aggregated: [all_runs_aggregate.md](all_runs_aggregate.md)

To find specific variants in the “all runs” tables, search for:

- `central_planner` (hierarchy/planner baseline)
- `barter_credit` and `barter_chat_credit` (credit / chat+credit variants)

### Regenerating

- Core sweep: `make results-core`
- All runs: `make results-all`
- One-page views: `make results-pages`

### Blog/paper assets

- Core sweep overview figure: [PNG](figures/core_sweep_overview.png), [PDF](figures/core_sweep_overview.pdf)
- Core sweep LaTeX table: [paper/core_sweep_table.tex](paper/core_sweep_table.tex)
- Generate: `make figures-core`
