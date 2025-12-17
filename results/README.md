## Results tables

This repo stores raw run logs under `runs*/` (JSON), but those folders are gitignored to keep the repo small.
Instead, we publish generated per-run and aggregated tables here so the results are visible on GitHub.

Key idea: `run_set` in the tables is just the folder name the JSON came from (e.g. `runs_core`, `runs_chat_credit_retest`).

### Core sweep (barter vs money/Exchange)

- Per-run: `results/runs_core_full.md`
- Aggregated: `results/runs_core_aggregate.md`

### All recorded runs (includes planner + credits)

- Per-run: `results/all_runs_full.md`
- Aggregated: `results/all_runs_aggregate.md`

To find specific variants in the “all runs” tables, search for:

- `central_planner` (hierarchy/planner baseline)
- `barter_credit` and `barter_chat_credit` (credit / chat+credit variants)

### Regenerating

- Core sweep: `make results-core`
- All runs: `make results-all`

