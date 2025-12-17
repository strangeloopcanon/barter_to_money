# Showcase results (the 4-condition table)

This is the curated 4-condition summary table intended for the writeup. It selects the most comparable available `N`, `R`, and `model` rows for each institution and includes `run_set` so the provenance is explicit.

- Source: `results/all_runs_aggregate.csv`
- N = 8, R = 8, model = `gpt-5-mini`
- LaTeX version: `results/paper/showcase_table.tex`
- Note: `rounds_run` is rounds until termination (clearing or hitting the round cap); lower is better.

| condition | run_set | runs | success_rate | rounds_run | total_messages | unique_pairs | credit_accepts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Barter | runs_core | 2 | 0.625 ± 0.177 | 8.00 ± 0.00 | 32.0 ± 4.2 | 9.50 ± 2.12 | 0.00 ± 0.00 |
| Money/Exchange | runs_core | 2 | 1.000 ± 0.000 | 3.50 ± 0.71 | 47.0 ± 1.4 | 8.00 ± 0.00 | 0.00 ± 0.00 |
| Central planner | runs_5mini_full | 1 | 0.000 | 8.00 | 72.0 | 8.00 | 0.00 |
| Barter + credits | runs_5mini_emergent | 3 | 0.542 ± 0.072 | 8.00 ± 0.00 | 34.7 ± 4.2 | 8.67 ± 1.53 | 0.00 ± 0.00 |

Full details: `results/all_results.md`.
