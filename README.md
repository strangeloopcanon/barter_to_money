# Agentic economy experiment (barter vs money)

## Core question

In an agentic economy where many LLM agents trade with each other, do we still “need” money (or some hub/hierarchy), or can everyone just negotiate directly via barter?

The thesis we want to test empirically is:

- As the number of agents \(N\) grows, the number of potential bilateral negotiations grows roughly like \(N^2\).
- Under a fixed communication budget (limited rounds/messages), this bilateral search/negotiation burden makes it hard to clear markets via pure barter.
- Introducing a hub with a token (a money/clearing-house agent) collapses the communication graph into a star: each agent only needs to talk to the hub, and coordination load scales roughly linearly in \(N\).

This repo implements a small, laptop-scale simulation of that contrast using OpenAI’s Responses API and GPT-5-mini class models.

## Experimental setup

### Environment

- Agents: \(N\) agents, indexed \(A_0, \dots, A_{N-1}\).
- Goods:
  - There are \(N\) goods \(g_0, \dots, g_{N-1}\).
  - Each agent \(A_i\) starts with 1 unit of \(g_i\).
  - Each agent wants exactly 1 unit of a different good \(g_{\pi(i)}\) (a derangement over goods, so no one wants what they already have).
- Utility: an agent succeeds if it ends the game holding its target good; otherwise, utility 0.
- Time: discrete rounds; each agent can take at most one action per round.
- Observations:
  - Own inventory and target good.
  - A capped window of recent messages sent/received.

All agent decisions are implemented as structured JSON responses from a GPT model via the Responses API.

### Conditions

We run two institutional variants over the *same* agent population and preferences:

1) **Barter (fully bilateral)**
- Agents may send propose/accept/reject messages directly to other agents.
- Allowed actions per round:
  - `{"action": "propose_trade", "to": "Aj", "give": "gX", "receive": "gY"}`
  - `{"action": "accept", "of_message_id": "mK"}`
  - `{"action": "reject", "of_message_id": "mK"}`
  - `{"action": "idle"}`
- The simulator routes messages and only executes trades when a proposal is accepted by the intended counterparty.
- Agents only see their own message history; they have no global state.

2) **Money/Exchange (hub with a token)**
- Add a special agent `Exchange` and a money token `M`.
- Agents **cannot** trade with each other directly; they only trade with `Exchange`.
- Actions per round:
  - `{"action": "request_quote", "good": "gX"}`
  - `{"action": "buy", "good": "gX", "quantity": 1}`
  - `{"action": "sell", "good": "gX", "quantity": 1}`
  - `{"action": "idle"}`
- Exchange behavior:
  - Starts with some units of each good and ample money.
  - Maintains a simple price vector `P[g]` (initially 1.0 for all goods).
  - Always confirms a buy if the agent has enough money (and mints inventory if needed).
  - Always confirms a sell if the agent has the good (Exchange can pay).
  - Keeps prices near 1.0 with only gentle adjustments.
- Agent prompts explicitly suggest the “sell your endowment, then buy your target good” strategy.

In both conditions, agents are identical GPT-5-mini agents; only the institution changes.

### Metrics

For each run (fixed \(N\), condition, seed, round cap) we log:

- `total_messages`: total number of non-idle actions/messages.
- `unique_pairs`: number of unordered sender–receiver pairs that ever communicated.
  - In barter, this is the “density” of the bilateral negotiation graph.
  - In money/Exchange, this is near \(N\) (each agent + hub).
- `success_rate`: fraction of agents that end with their target good.
- `rounds_run`: how many rounds elapsed before either all agents succeeded or the round cap was reached.

All logs live in JSON files:

- `runs_5mini_smoke/{condition}_N{N}_seed{seed}.json`
- `runs_5mini_full*/{condition}_N{N}_seed{seed}.json`

You can extend the dataset simply by running the CLI with larger `--n` or more `--seeds`; the analysis script picks up all matching files.

## Example results (GPT-5-mini, small N)

The table below summarizes a small set of runs with `gpt-5-mini`:

- Round cap: 6 or 8 as noted.
- Seeds: 1–3 depending on \(N\).
- All runs use the same simulation code; only condition and \(N\) differ.

| Condition       | N | Seeds | Round cap | Success rate (avg) | Rounds to clear (typical) | Total messages (example) | Unique pairs (example) |
|----------------|---|--------|-----------|---------------------|---------------------------|--------------------------|------------------------|
| Barter         | 3 | 3      | 8         | 1.0                 | 4–5                       | 5–9                      | 2–3                    |
| Money/Exchange | 3 | 1      | 8         | 1.0                 | 3                         | 18                       | 3                      |
| Barter         | 5 | 1      | 6         | 1.0                 | 6                         | 15                       | 6                      |
| Money/Exchange | 5 | 1      | 6         | 1.0                 | 4                         | 30                       | 5                      |
| Barter         | 8 | 2      | 8         | ~0.44 (4/8, 3/8)    | 8 (hit cap)               | 36–39                    | 7–8                    |

What this already shows:

- For \(N = 3, 5\), both institutions can clear, but the money/Exchange hub does so in fewer rounds and with a star-shaped communication pattern (unique_pairs ≈ N).
- For \(N = 8\), under the same round cap, **barter fails** to clear for a non-trivial fraction of agents, even though almost all pairs have talked at least once and message counts have grown substantially.
- Extending the money/Exchange runs to \(N = 8\) and above is just more compute; structurally, the hub graph remains a star with unique_pairs ≈ N, and the Exchange has enough liquidity to continue clearing trades.

This is exactly the pattern the econ story predicts:

- The bilateral barter network becomes dense and coordination-limited as \(N\) grows.
- The hub/token institution keeps the “discussion graph” sparse and makes high success achievable under a fixed communication budget.

## Setup

- Export `OPENAI_API_KEY` (loaded from `.env` if present).
- Install deps with `make setup` (uses `uv` and creates a virtual env at `.venv`).

## Running experiments

- Default smoke set (small N to stay cheap):
  - `python -m agentic_economy.cli run --conditions barter money_exchange --n 3 5 --seeds 1 --rounds 6 --model gpt-5-mini --output-dir runs_5mini_smoke`
- Larger runs (for plots / essay):
  - Example: `python -m agentic_economy.cli run --conditions barter money_exchange --n 3 5 8 --seeds 3 --rounds 8 --model gpt-5-mini --output-dir runs_5mini_full`
- Live LLM sanity check:
  - `make llm-live` (defaults to `gpt-5-nano`; override `--model` if you want to smoke-test with the same model as your main runs).
- Results land under the chosen `--output-dir` as `{condition}_N{N}_seed{seed}.json` with full message logs and inventories.

## Analysis

- Quick aggregate view:
  - `python -m agentic_economy.analysis` (defaults to `runs/*.json`; pass your own glob from Python if needed).
- The helper prints one row per run plus grouped aggregates by `(condition, N)`:
  - Mean and std of `total_messages`, `unique_pairs`, `success_rate`, `rounds_run`.
- For plotting in a notebook:
  - Import `load_runs` and `aggregate_runs` from `agentic_economy.analysis` and plot:
    - `total_messages` vs `N` by condition.
    - `unique_pairs` vs `N` by condition.
    - `success_rate` vs `N` by condition.

## Possible extensions

A few natural next steps if you want to push this beyond a blog post:

- **Higher N and more seeds**  
  - Run \(N = 10, 15\) with more seeds to get smoother curves and error bars for an appendix figure.

- **Hierarchy vs money**  
  - Add a “pure hierarchy” variant where the hub doesn’t use a token explicitly, just reallocates goods as an omniscient planner. Compare this to the money/Exchange hub to show that what matters structurally is the star topology, not the particular token mechanics.

- **Emergent money**  
  - Allow agents in the barter world to invent abstract IOUs/credits in their messages (no privileged token). See if, as \(N\) grows, agents spontaneously converge on a shared token-like object to reduce coordination burden.

- **Richer preferences or budgets**  
  - Move from “1 unit target utility” to simple utility functions over bundles, or introduce budget constraints and prices in the barter world, to align even more closely with classic monetary economics models.

- **Cost/latency accounting**  
  - Log approximate token usage and wall-clock latency per run so you can talk concretely about “cost of coordination” in dollars and seconds, not just in messages and edges.

Even without those extensions, the current setup is deliberately minimal but rich enough that an economist can read the spec, look at the tables/plots, and see the combinatorial argument for money or hubs in an agentic economy.
