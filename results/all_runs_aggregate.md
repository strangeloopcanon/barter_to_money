# Aggregated results

Grouped summary (means/std) from `runs*/*.json`.

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
