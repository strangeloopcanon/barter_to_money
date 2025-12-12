# Agentic economy experiment (barter vs money)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/strangeloopcanon/barter_to_money)

## Core question

In an agentic economy where many LLM agents trade with each other, do we still “need” money (or some hub/hierarchy), or can everyone just negotiate directly via barter?

The thesis we want to test empirically is:

- As the number of agents $N$ grows, the number of potential bilateral negotiations grows roughly like $N^2$.
- Under a fixed communication budget (limited rounds/messages), this bilateral search/negotiation burden makes it hard to clear markets via pure barter.
- Introducing a hub with a token (a money/clearing-house agent) collapses the communication graph into a star: each agent only needs to talk to the hub, and coordination load scales roughly linearly in $N$.

An informal theoretical claim behind this is:

- Under random endowments and targets, and a fixed per-agent communication budget (round cap $R$ that does not grow with $N$), the probability that a purely bilateral protocol (or a local hierarchy without a token) fully clears the market goes to 0 as $N \to \infty$.
- A star-shaped institution with a fungible token (money/Exchange) can, in contrast, keep success probability bounded away from 0 while using only $O(N)$ messages (roughly “sell once, buy once” per agent).

This repo implements a small, laptop-scale simulation of that contrast using OpenAI’s Responses API and GPT-5-mini class models. A slightly more formal model and communication-complexity sketch live in `theory.md`.

## Experimental setup

### Environment

- Agents: $N$ agents, indexed $A_0, \dots, A_{N-1}$.
- Goods:
  - There are $N$ goods $g_0, \dots, g_{N-1}$.
  - Each agent $A_i$ starts with 1 unit of $g_i$.
  - Each agent wants exactly 1 unit of a different good $g_{\pi(i)}$ (a derangement over goods, so no one wants what they already have).
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

5) **Barter with chat (experimental)**: like barter, but agents may send short free‑text coordination messages via `send_message` in addition to trade actions.

6) **Barter with chat + credits (experimental)**: chat-enabled barter plus mintable credits. This is the intended setting for stronger “emergent money / reputation” probes.

Across conditions, agents are identical GPT‑5‑mini models; only the institution changes.

### Metrics

Per run we track: `success_rate` (agents reaching targets), `rounds_run` (to clear or cap), and basic communication volume (`total_messages`, `unique_pairs`). Money/Exchange runs also log per‑round exchange traffic and price updates.

Run logs now also include:
- `events`: structured per‑round instrumentation of raw agent actions (including invalid/hallucinated actions), proposals, trades, credit issuance, and chat messages.
- `behavior_summary`: per‑agent counts of proposals, unique partners, repeated identical proposals, chat messages sent, and invalid actions.

## Empirical test (GPT-5-mini, core sweep)

To probe the core claim above without overfitting to any single random economy, we reran the two key institutions (barter vs money/Exchange) on **two independent economies** (seeds 0 and 1) across a small $N$ sweep under a fixed round cap $R=8$.

| Condition      | N  | # runs | Round cap | Success rate (avg) | Avg rounds run |
|----------------|----|--------|-----------|--------------------|----------------|
| Barter         | 3  | 2      | 8         | 0.67               | 6.5            |
| Barter         | 5  | 2      | 8         | 0.80               | 6.5            |
| Barter         | 8  | 2      | 8         | 0.63               | 8.0            |
| Barter         | 10 | 2      | 8         | 0.65               | 8.0            |
| Barter         | 12 | 2      | 8         | 0.42               | 8.0            |
| Money/Exchange | 3  | 2      | 8         | 1.00               | 3.5            |
| Money/Exchange | 5  | 2      | 8         | 1.00               | 3.5            |
| Money/Exchange | 8  | 2      | 8         | 1.00               | 3.5            |
| Money/Exchange | 10 | 2      | 8         | 1.00               | 4.0            |
| Money/Exchange | 12 | 2      | 8         | 1.00               | 4.0            |

What this shows (current code, GPT‑5‑mini, fixed communication budget):

- **Barter:** success is already sensitive to the economy at $N=3$ and does not scale: by $N=12$ fewer than half the agents clear on average and runs hit the round cap.
- **Money/Exchange:** clears at 1.0 for all tested $N$ with roughly constant rounds (≈3–4) and linear hub‑facing communication.

This is the qualitative pattern predicted by the communication‑complexity sketch: under fixed per‑agent communication, bilateral barter fails with high probability as $N$ grows, while a star‑shaped institution with a fungible token maintains high clearing probability.

## Emergent money probe (barter_credit)

To see whether money-like objects emerge endogenously, we ran `barter` vs `barter_credit` at $N=8$ (3 seeds, round cap 8). Results:

- `barter` success ≈ 0.50 (about 4/8 agents clear on average).
- `barter_credit` success ≈ 0.54, but credits were almost never used (5 total credit proposals across 3 runs) and **no credit was accepted**, so no shared medium of exchange emerged in this regime.

This is a preliminary negative result: simply allowing mintable IOUs is not enough for money to spontaneously appear without additional credibility or stronger coordination pressure.

### Retest with chat + credits (barter_chat_credit)

We reran the credits condition with an explicit coordination channel (`send_message`) so agents can negotiate credit semantics.

At $N=8$ (2 seeds, round cap 12), comparing `barter_credit` vs `barter_chat_credit`:

- `barter_credit`: success rate 0.75; mean credit proposals 1.5; **credit accepts 0.0**
- `barter_chat_credit`: success rate 0.44; mean credit proposals 11.5; **credit accepts 0.0**; mean messages sent 26

In this regime, chat makes agents propose credits far more often, but **still does not produce any accepted credit**, so we still do not see emergent money. It can also reduce clearing performance by consuming the per‑round action budget on messaging rather than trading.

## Exchange complexity note

Money/Exchange runs log per‑round exchange traffic and price updates. In the $N=8$ run, the exchange handled 23 inbound and 23 outbound messages total and prices stayed fixed (no updates), illustrating that coordination is absorbed into $O(N)$ hub-facing communication in this toy.
