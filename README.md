# Agentic economy experiment (barter vs money)

## Core question

In an agentic economy where many LLM agents trade with each other, do we still “need” money (or some hub/hierarchy), or can everyone just negotiate directly via barter?

The thesis we want to test empirically is:

- As the number of agents \(N\) grows, the number of potential bilateral negotiations grows roughly like \(N^2\).
- Under a fixed communication budget (limited rounds/messages), this bilateral search/negotiation burden makes it hard to clear markets via pure barter.
- Introducing a hub with a token (a money/clearing-house agent) collapses the communication graph into a star: each agent only needs to talk to the hub, and coordination load scales roughly linearly in \(N\).

An informal theoretical claim behind this is:

- Under random endowments and targets, and a fixed per-agent communication budget (round cap \(R\) that does not grow with \(N\)), the probability that a purely bilateral protocol (or a local hierarchy without a token) fully clears the market goes to 0 as \(N \to \infty\).
- A star-shaped institution with a fungible token (money/Exchange) can, in contrast, keep success probability bounded away from 0 while using only \(O(N)\) messages (roughly “sell once, buy once” per agent).

This repo implements a small, laptop-scale simulation of that contrast using OpenAI’s Responses API and GPT-5-mini class models. A slightly more formal model and communication-complexity sketch live in `theory.md`.

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

We run several institutional variants over the *same* agent population and preferences:

1) **Barter (fully bilateral)**: agents negotiate directly with each other; trades require bilateral agreement.

2) **Money/Exchange (hub with a token)**: agents trade only with an Exchange hub using a fungible token and near‑stable posted prices (suggested strategy: sell endowment, buy target).

3) **Central planner / pure hierarchy (local, no token)**: agents report inventory and targets to a planner that can only execute obvious pairwise swaps; it does not solve global cycles. Empirically this often fails to clear where money/Exchange clears.

4) **Barter with credits (experimental)**: barter plus mintable/transferable IOU labels (any non‑`g*` string) that can circulate as tokens.

Across conditions, agents are identical GPT‑5‑mini models; only the institution changes.

### Metrics

Per run we track: `success_rate` (agents reaching targets), `rounds_run` (to clear or cap), and basic communication volume (`total_messages`, `unique_pairs`). Money/Exchange runs also log per‑round exchange traffic and price updates.

## Empirical test (GPT-5-mini, small N)

To probe the claim above, we run GPT-5-mini agents under the three main institutions (barter, money/Exchange, local central planner) for small \(N\), tight round caps, and a handful of seeds. The table below summarizes the `gpt-5-mini` runs in `runs/`, `runs_5mini_smoke/`, `runs_5mini_full/`, and `runs_5mini_full_seed1/`:

- Round caps: 6 or 8 as noted.
- All rows below use the same simulation code; only institution, \(N\), and seeds differ.

| Condition           | N | # runs | Round cap (typical) | Success rate (avg) | Avg rounds run |
|---------------------|---|--------|---------------------|--------------------|----------------|
| Barter              | 3 | 6      | 6–8                 | 1.00               | ≈4.3           |
| Barter              | 5 | 2      | 6–8                 | 0.80               | ≈5.5           |
| Barter              | 8 | 2      | 8                   | 0.44               | 8.0            |
| Money/Exchange      | 3 | 2      | 6–8                 | 1.00               | ≈3.5           |
| Money/Exchange      | 5 | 1      | 6                   | 1.00               | 4.0            |
| Money/Exchange      | 8 | 1      | 8                   | 1.00               | 4.0            |
| Central planner     | 3 | 1      | 6                   | 0.00               | 6.0            |
| Central planner     | 5 | 1      | 6                   | 0.40               | 6.0            |
| Central planner     | 8 | 1      | 8                   | 0.00               | 8.0            |

What this already shows (for GPT-5-mini under tight communication budgets):

- **Barter:** success is high at \(N=3\), but drops by \(N=5\) and further by \(N=8\), with runs typically hitting the round cap at higher \(N\).
- **Money/Exchange:** success stays at 1.0 for \(N=3,5,8\), with average rounds essentially flat in \(N\) (≈3–4); the communication graph stays star-shaped around the hub.
- **Local central planner (no token):** with only simple pairwise swaps, the planner fails at \(N=3\), partially succeeds at \(N=5\), and fails again at \(N=8\); “just adding hierarchy” without a token does not solve the coordination problem.

Taken together, this is exactly the qualitative pattern the theoretical story predicts: under a fixed communication budget, bilateral barter and a naive hierarchy without money struggle more as \(N\) grows, while a star-shaped institution with a token maintains high success with roughly linear coordination load in \(N\).
