# All results (one page)

Generated from committed CSVs:
- `results/all_runs_aggregate.csv`
- `results/all_runs_full.csv`

## Aggregated

| run_set | condition | n_agents | model | rounds_cap | history_limit | runs | success_rate_mean | success_rate_std | rounds_run_mean | rounds_run_std | total_messages_mean | total_messages_std | unique_pairs_mean | unique_pairs_std | exchange_inbox_messages_mean | exchange_outbox_messages_mean | exchange_price_update_count_mean | exchange_price_abs_change_mean | credit_proposals_mean | credit_accepts_mean | send_messages_mean | invalid_actions_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| runs | barter | 3 | gpt-5-mini | 12 | 10 | 2 | 1.0 | 0.0 | 4.0 | 0.0 | 7.0 | 1.414 | 3.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs | barter | 5 | gpt-5-mini | 12 | 10 | 1 | 1.0 |  | 5.0 |  | 13.0 |  | 6.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_51codex_smoke | barter | 3 | gpt-5.1-codex-mini | 6 | 10 | 1 | 0.333 |  | 6.0 |  | 2.0 |  | 1.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_51codex_smoke | barter | 5 | gpt-5.1-codex-mini | 6 | 10 | 1 | 0.2 |  | 6.0 |  | 9.0 |  | 4.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_51codex_smoke | money_exchange | 3 | gpt-5.1-codex-mini | 6 | 10 | 1 | 1.0 |  | 4.0 |  | 24.0 |  | 3.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_51codex_smoke | money_exchange | 5 | gpt-5.1-codex-mini | 6 | 10 | 1 | 1.0 |  | 4.0 |  | 40.0 |  | 5.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_credit_smoke | barter_credit | 5 | gpt-5-mini | 6 | 10 | 1 | 1.0 |  | 5.0 |  | 9.0 |  | 4.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_emergent | barter | 8 | gpt-5-mini | 8 | 10 | 3 | 0.5 | 0.0 | 8.0 | 0.0 | 35.0 | 4.0 | 9.333 | 2.082 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_emergent | barter_credit | 8 | gpt-5-mini | 8 | 10 | 3 | 0.542 | 0.072 | 8.0 | 0.0 | 34.667 | 4.163 | 8.667 | 1.528 | 0.0 | 0.0 | 0.0 | 0.0 | 1.667 | 0.0 | 0.0 | 0.0 |
| runs_5mini_full | barter | 3 | gpt-5-mini | 8 | 10 | 3 | 1.0 | 0.0 | 4.333 | 0.577 | 7.0 | 2.0 | 2.667 | 0.577 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_full | barter | 8 | gpt-5-mini | 8 | 10 | 1 | 0.5 |  | 8.0 |  | 36.0 |  | 7.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_full | central_planner | 8 | gpt-5-mini | 8 | 10 | 1 | 0.0 |  | 8.0 |  | 72.0 |  | 8.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_full | money_exchange | 3 | gpt-5-mini | 8 | 10 | 1 | 1.0 |  | 3.0 |  | 18.0 |  | 3.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_full | money_exchange | 8 | gpt-5-mini | 8 | 10 | 1 | 1.0 |  | 4.0 |  | 46.0 |  | 8.0 |  | 23.0 | 23.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_full_seed1 | barter | 8 | gpt-5-mini | 8 | 10 | 1 | 0.375 |  | 8.0 |  | 39.0 |  | 8.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_short | barter | 7 | gpt-5-mini | 6 | 10 | 1 | 1.0 |  | 6.0 |  | 20.0 |  | 8.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_short | money_exchange | 3 | gpt-5-mini | 6 | 10 | 1 | 0.0 |  | 6.0 |  | 32.0 |  | 3.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_short | money_exchange | 5 | gpt-5-mini | 6 | 10 | 1 | 0.0 |  | 6.0 |  | 58.0 |  | 5.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_short | money_exchange | 7 | gpt-5-mini | 4 | 10 | 1 | 0.0 |  | 4.0 |  | 54.0 |  | 7.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_smoke | barter | 3 | gpt-5-mini | 6 | 10 | 1 | 1.0 |  | 5.0 |  | 7.0 |  | 3.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_smoke | barter | 5 | gpt-5-mini | 6 | 10 | 1 | 0.6 |  | 6.0 |  | 22.0 |  | 6.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_smoke | central_planner | 3 | gpt-5-mini | 6 | 10 | 1 | 0.0 |  | 6.0 |  | 21.0 |  | 3.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_smoke | central_planner | 5 | gpt-5-mini | 6 | 10 | 1 | 0.4 |  | 6.0 |  | 37.0 |  | 5.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_smoke | money_exchange | 3 | gpt-5-mini | 6 | 10 | 1 | 1.0 |  | 4.0 |  | 24.0 |  | 3.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5mini_smoke | money_exchange | 5 | gpt-5-mini | 6 | 10 | 1 | 1.0 |  | 4.0 |  | 32.0 |  | 5.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5nano_smoke | barter | 3 | gpt-5-nano | 6 | 10 | 1 | 0.0 |  | 6.0 |  | 5.0 |  | 1.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5nano_smoke | barter | 5 | gpt-5-nano | 6 | 10 | 1 | 0.2 |  | 6.0 |  | 6.0 |  | 2.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_5nano_smoke | money_exchange | 3 | gpt-5-nano | 4 | 10 | 1 | 0.667 |  | 4.0 |  | 22.0 |  | 3.0 |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_chat_credit_retest | barter_chat_credit | 8 | gpt-5-mini | 12 | 12 | 2 | 0.438 | 0.088 | 12.0 | 0.0 | 65.0 | 7.071 | 8.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 11.5 | 0.0 | 26.0 | 1.5 |
| runs_chat_credit_retest | barter_credit | 8 | gpt-5-mini | 12 | 12 | 2 | 0.75 | 0.0 | 12.0 | 0.0 | 43.5 | 7.778 | 9.5 | 0.707 | 0.0 | 0.0 | 0.0 | 0.0 | 1.5 | 0.0 | 0.0 | 6.5 |
| runs_core | barter | 3 | gpt-5-mini | 8 | 10 | 2 | 0.667 | 0.471 | 6.5 | 2.121 | 11.0 | 4.243 | 2.5 | 0.707 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_core | barter | 5 | gpt-5-mini | 8 | 10 | 2 | 0.8 | 0.283 | 6.5 | 2.121 | 13.5 | 2.121 | 5.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 2.5 |
| runs_core | barter | 8 | gpt-5-mini | 8 | 10 | 2 | 0.625 | 0.177 | 8.0 | 0.0 | 32.0 | 4.243 | 9.5 | 2.121 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 3.0 |
| runs_core | barter | 10 | gpt-5-mini | 8 | 10 | 2 | 0.65 | 0.212 | 8.0 | 0.0 | 37.5 | 13.435 | 14.0 | 1.414 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.5 |
| runs_core | barter | 12 | gpt-5-mini | 8 | 10 | 2 | 0.417 | 0.0 | 8.0 | 0.0 | 61.0 | 2.828 | 20.5 | 3.536 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| runs_core | money_exchange | 3 | gpt-5-mini | 8 | 10 | 2 | 1.0 | 0.0 | 3.5 | 0.707 | 18.0 | 2.828 | 3.0 | 0.0 | 9.0 | 9.0 | 0.5 | 0.025 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_core | money_exchange | 5 | gpt-5-mini | 8 | 10 | 2 | 1.0 | 0.0 | 3.5 | 0.707 | 29.0 | 4.243 | 5.0 | 0.0 | 14.5 | 14.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_core | money_exchange | 8 | gpt-5-mini | 8 | 10 | 2 | 1.0 | 0.0 | 3.5 | 0.707 | 47.0 | 1.414 | 8.0 | 0.0 | 23.5 | 23.5 | 1.0 | 0.01 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_core | money_exchange | 10 | gpt-5-mini | 8 | 10 | 2 | 1.0 | 0.0 | 4.0 | 0.0 | 61.0 | 1.414 | 10.0 | 0.0 | 30.5 | 30.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| runs_core | money_exchange | 12 | gpt-5-mini | 8 | 10 | 2 | 1.0 | 0.0 | 4.0 | 0.0 | 73.0 | 1.414 | 12.0 | 0.0 | 36.5 | 36.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Per-run

| run_set | condition | n_agents | seed | model | rounds_cap | history_limit | success_rate | rounds_run | total_messages | unique_pairs | credit_proposals | credit_accepts | send_messages | invalid_actions | path |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| runs | barter | 3 | 0 | gpt-5-mini | 12 | 10 | 1.0 | 4 | 6 | 3 | 0 | 0 | 0 | 0 | runs/barter_N3_seed0.json |
| runs | barter | 3 | 1 | gpt-5-mini | 12 | 10 | 1.0 | 4 | 8 | 3 | 0 | 0 | 0 | 0 | runs/barter_N3_seed1.json |
| runs | barter | 5 | 0 | gpt-5-mini | 12 | 10 | 1.0 | 5 | 13 | 6 | 0 | 0 | 0 | 0 | runs/barter_N5_seed0.json |
| runs_51codex_smoke | barter | 3 | 0 | gpt-5.1-codex-mini | 6 | 10 | 0.33 | 6 | 2 | 1 | 0 | 0 | 0 | 0 | runs_51codex_smoke/barter_N3_seed0.json |
| runs_51codex_smoke | barter | 5 | 0 | gpt-5.1-codex-mini | 6 | 10 | 0.2 | 6 | 9 | 4 | 0 | 0 | 0 | 0 | runs_51codex_smoke/barter_N5_seed0.json |
| runs_51codex_smoke | money_exchange | 3 | 0 | gpt-5.1-codex-mini | 6 | 10 | 1.0 | 4 | 24 | 3 | 0 | 0 | 0 | 0 | runs_51codex_smoke/money_exchange_N3_seed0.json |
| runs_51codex_smoke | money_exchange | 5 | 0 | gpt-5.1-codex-mini | 6 | 10 | 1.0 | 4 | 40 | 5 | 0 | 0 | 0 | 0 | runs_51codex_smoke/money_exchange_N5_seed0.json |
| runs_5mini_credit_smoke | barter_credit | 5 | 0 | gpt-5-mini | 6 | 10 | 1.0 | 5 | 9 | 4 | 0 | 0 | 0 | 0 | runs_5mini_credit_smoke/barter_credit_N5_seed0.json |
| runs_5mini_emergent | barter | 8 | 0 | gpt-5-mini | 8 | 10 | 0.5 | 8 | 35 | 11 | 0 | 0 | 0 | 0 | runs_5mini_emergent/barter_N8_seed0.json |
| runs_5mini_emergent | barter | 8 | 1 | gpt-5-mini | 8 | 10 | 0.5 | 8 | 31 | 7 | 0 | 0 | 0 | 0 | runs_5mini_emergent/barter_N8_seed1.json |
| runs_5mini_emergent | barter | 8 | 2 | gpt-5-mini | 8 | 10 | 0.5 | 8 | 39 | 10 | 0 | 0 | 0 | 0 | runs_5mini_emergent/barter_N8_seed2.json |
| runs_5mini_emergent | barter_credit | 8 | 0 | gpt-5-mini | 8 | 10 | 0.5 | 8 | 38 | 7 | 2 | 0 | 0 | 0 | runs_5mini_emergent/barter_credit_N8_seed0.json |
| runs_5mini_emergent | barter_credit | 8 | 1 | gpt-5-mini | 8 | 10 | 0.5 | 8 | 36 | 9 | 1 | 0 | 0 | 0 | runs_5mini_emergent/barter_credit_N8_seed1.json |
| runs_5mini_emergent | barter_credit | 8 | 2 | gpt-5-mini | 8 | 10 | 0.62 | 8 | 30 | 10 | 2 | 0 | 0 | 0 | runs_5mini_emergent/barter_credit_N8_seed2.json |
| runs_5mini_full | barter | 3 | 0 | gpt-5-mini | 8 | 10 | 1.0 | 4 | 7 | 3 | 0 | 0 | 0 | 0 | runs_5mini_full/barter_N3_seed0.json |
| runs_5mini_full | barter | 3 | 1 | gpt-5-mini | 8 | 10 | 1.0 | 5 | 9 | 3 | 0 | 0 | 0 | 0 | runs_5mini_full/barter_N3_seed1.json |
| runs_5mini_full | barter | 3 | 2 | gpt-5-mini | 8 | 10 | 1.0 | 4 | 5 | 2 | 0 | 0 | 0 | 0 | runs_5mini_full/barter_N3_seed2.json |
| runs_5mini_full | barter | 8 | 0 | gpt-5-mini | 8 | 10 | 0.5 | 8 | 36 | 7 | 0 | 0 | 0 | 0 | runs_5mini_full/barter_N8_seed0.json |
| runs_5mini_full | central_planner | 8 | 0 | gpt-5-mini | 8 | 10 | 0.0 | 8 | 72 | 8 | 0 | 0 | 0 | 0 | runs_5mini_full/central_planner_N8_seed0.json |
| runs_5mini_full | money_exchange | 3 | 0 | gpt-5-mini | 8 | 10 | 1.0 | 3 | 18 | 3 | 0 | 0 | 0 | 0 | runs_5mini_full/money_exchange_N3_seed0.json |
| runs_5mini_full | money_exchange | 8 | 0 | gpt-5-mini | 8 | 10 | 1.0 | 4 | 46 | 8 | 0 | 0 | 0 | 0 | runs_5mini_full/money_exchange_N8_seed0.json |
| runs_5mini_full_seed1 | barter | 8 | 0 | gpt-5-mini | 8 | 10 | 0.38 | 8 | 39 | 8 | 0 | 0 | 0 | 0 | runs_5mini_full_seed1/barter_N8_seed0.json |
| runs_5mini_short | barter | 7 | 0 | gpt-5-mini | 6 | 10 | 1.0 | 6 | 20 | 8 | 0 | 0 | 0 | 0 | runs_5mini_short/barter_N7_seed0.json |
| runs_5mini_short | money_exchange | 3 | 0 | gpt-5-mini | 6 | 10 | 0.0 | 6 | 32 | 3 | 0 | 0 | 0 | 0 | runs_5mini_short/money_exchange_N3_seed0.json |
| runs_5mini_short | money_exchange | 5 | 0 | gpt-5-mini | 6 | 10 | 0.0 | 6 | 58 | 5 | 0 | 0 | 0 | 0 | runs_5mini_short/money_exchange_N5_seed0.json |
| runs_5mini_short | money_exchange | 7 | 0 | gpt-5-mini | 4 | 10 | 0.0 | 4 | 54 | 7 | 0 | 0 | 0 | 0 | runs_5mini_short/money_exchange_N7_seed0.json |
| runs_5mini_smoke | barter | 3 | 0 | gpt-5-mini | 6 | 10 | 1.0 | 5 | 7 | 3 | 0 | 0 | 0 | 0 | runs_5mini_smoke/barter_N3_seed0.json |
| runs_5mini_smoke | barter | 5 | 0 | gpt-5-mini | 6 | 10 | 0.6 | 6 | 22 | 6 | 0 | 0 | 0 | 0 | runs_5mini_smoke/barter_N5_seed0.json |
| runs_5mini_smoke | central_planner | 3 | 0 | gpt-5-mini | 6 | 10 | 0.0 | 6 | 21 | 3 | 0 | 0 | 0 | 0 | runs_5mini_smoke/central_planner_N3_seed0.json |
| runs_5mini_smoke | central_planner | 5 | 0 | gpt-5-mini | 6 | 10 | 0.4 | 6 | 37 | 5 | 0 | 0 | 0 | 0 | runs_5mini_smoke/central_planner_N5_seed0.json |
| runs_5mini_smoke | money_exchange | 3 | 0 | gpt-5-mini | 6 | 10 | 1.0 | 4 | 24 | 3 | 0 | 0 | 0 | 0 | runs_5mini_smoke/money_exchange_N3_seed0.json |
| runs_5mini_smoke | money_exchange | 5 | 0 | gpt-5-mini | 6 | 10 | 1.0 | 4 | 32 | 5 | 0 | 0 | 0 | 0 | runs_5mini_smoke/money_exchange_N5_seed0.json |
| runs_5nano_smoke | barter | 3 | 0 | gpt-5-nano | 6 | 10 | 0.0 | 6 | 5 | 1 | 0 | 0 | 0 | 0 | runs_5nano_smoke/barter_N3_seed0.json |
| runs_5nano_smoke | barter | 5 | 0 | gpt-5-nano | 6 | 10 | 0.2 | 6 | 6 | 2 | 0 | 0 | 0 | 0 | runs_5nano_smoke/barter_N5_seed0.json |
| runs_5nano_smoke | money_exchange | 3 | 0 | gpt-5-nano | 4 | 10 | 0.67 | 4 | 22 | 3 | 0 | 0 | 0 | 0 | runs_5nano_smoke/money_exchange_N3_seed0.json |
| runs_chat_credit_retest | barter_chat_credit | 8 | 0 | gpt-5-mini | 12 | 12 | 0.5 | 12 | 60 | 8 | 7 | 0 | 25 | 3 | runs_chat_credit_retest/barter_chat_credit_N8_seed0.json |
| runs_chat_credit_retest | barter_chat_credit | 8 | 1 | gpt-5-mini | 12 | 12 | 0.38 | 12 | 70 | 8 | 16 | 0 | 27 | 0 | runs_chat_credit_retest/barter_chat_credit_N8_seed1.json |
| runs_chat_credit_retest | barter_credit | 8 | 0 | gpt-5-mini | 12 | 12 | 0.75 | 12 | 38 | 9 | 1 | 0 | 0 | 3 | runs_chat_credit_retest/barter_credit_N8_seed0.json |
| runs_chat_credit_retest | barter_credit | 8 | 1 | gpt-5-mini | 12 | 12 | 0.75 | 12 | 49 | 10 | 2 | 0 | 0 | 10 | runs_chat_credit_retest/barter_credit_N8_seed1.json |
| runs_core | barter | 10 | 0 | gpt-5-mini | 8 | 10 | 0.5 | 8 | 47 | 13 | 0 | 0 | 0 | 1 | runs_core/barter_N10_seed0.json |
| runs_core | barter | 10 | 1 | gpt-5-mini | 8 | 10 | 0.8 | 8 | 28 | 15 | 0 | 0 | 0 | 0 | runs_core/barter_N10_seed1.json |
| runs_core | barter | 12 | 0 | gpt-5-mini | 8 | 10 | 0.42 | 8 | 59 | 23 | 0 | 0 | 0 | 2 | runs_core/barter_N12_seed0.json |
| runs_core | barter | 12 | 1 | gpt-5-mini | 8 | 10 | 0.42 | 8 | 63 | 18 | 0 | 0 | 0 | 0 | runs_core/barter_N12_seed1.json |
| runs_core | barter | 3 | 0 | gpt-5-mini | 8 | 10 | 1.0 | 5 | 8 | 3 | 0 | 0 | 0 | 0 | runs_core/barter_N3_seed0.json |
| runs_core | barter | 3 | 1 | gpt-5-mini | 8 | 10 | 0.33 | 8 | 14 | 2 | 0 | 0 | 0 | 0 | runs_core/barter_N3_seed1.json |
| runs_core | barter | 5 | 0 | gpt-5-mini | 8 | 10 | 0.6 | 8 | 15 | 5 | 0 | 0 | 0 | 4 | runs_core/barter_N5_seed0.json |
| runs_core | barter | 5 | 1 | gpt-5-mini | 8 | 10 | 1.0 | 5 | 12 | 5 | 0 | 0 | 0 | 1 | runs_core/barter_N5_seed1.json |
| runs_core | barter | 8 | 0 | gpt-5-mini | 8 | 10 | 0.5 | 8 | 35 | 8 | 0 | 0 | 0 | 3 | runs_core/barter_N8_seed0.json |
| runs_core | barter | 8 | 1 | gpt-5-mini | 8 | 10 | 0.75 | 8 | 29 | 11 | 0 | 0 | 0 | 3 | runs_core/barter_N8_seed1.json |
| runs_core | money_exchange | 10 | 0 | gpt-5-mini | 8 | 10 | 1.0 | 4 | 62 | 10 | 0 | 0 | 0 | 0 | runs_core/money_exchange_N10_seed0.json |
| runs_core | money_exchange | 10 | 1 | gpt-5-mini | 8 | 10 | 1.0 | 4 | 60 | 10 | 0 | 0 | 0 | 0 | runs_core/money_exchange_N10_seed1.json |
| runs_core | money_exchange | 12 | 0 | gpt-5-mini | 8 | 10 | 1.0 | 4 | 74 | 12 | 0 | 0 | 0 | 0 | runs_core/money_exchange_N12_seed0.json |
| runs_core | money_exchange | 12 | 1 | gpt-5-mini | 8 | 10 | 1.0 | 4 | 72 | 12 | 0 | 0 | 0 | 0 | runs_core/money_exchange_N12_seed1.json |
| runs_core | money_exchange | 3 | 0 | gpt-5-mini | 8 | 10 | 1.0 | 4 | 20 | 3 | 0 | 0 | 0 | 0 | runs_core/money_exchange_N3_seed0.json |
| runs_core | money_exchange | 3 | 1 | gpt-5-mini | 8 | 10 | 1.0 | 3 | 16 | 3 | 0 | 0 | 0 | 0 | runs_core/money_exchange_N3_seed1.json |
| runs_core | money_exchange | 5 | 0 | gpt-5-mini | 8 | 10 | 1.0 | 3 | 26 | 5 | 0 | 0 | 0 | 0 | runs_core/money_exchange_N5_seed0.json |
| runs_core | money_exchange | 5 | 1 | gpt-5-mini | 8 | 10 | 1.0 | 4 | 32 | 5 | 0 | 0 | 0 | 0 | runs_core/money_exchange_N5_seed1.json |
| runs_core | money_exchange | 8 | 0 | gpt-5-mini | 8 | 10 | 1.0 | 4 | 46 | 8 | 0 | 0 | 0 | 0 | runs_core/money_exchange_N8_seed0.json |
| runs_core | money_exchange | 8 | 1 | gpt-5-mini | 8 | 10 | 1.0 | 3 | 48 | 8 | 0 | 0 | 0 | 0 | runs_core/money_exchange_N8_seed1.json |

Regenerate with `make results-all`.
