# Theory: Communication and Coordination in the Agentic Economy

This note states a stylized model and communication‑complexity results that motivate the experiments in this repo. The goal is to formalize the claim that, under bounded communication, bilateral barter (and naive hierarchy without a token) fails to clear with high probability as the economy scales, while a hub plus fungible token can clear with only linear communication.

## 1. Model

### 1.1 Environment

- Agents: $N$ agents $A_1,\dots,A_N$.
- Goods: $N$ indivisible goods $g_1,\dots,g_N$.
- Endowment: at $t=0$, agent $A_i$ holds one unit of $g_i$.
- Targets: a permutation $\pi$ is drawn uniformly from derangements on $\{1,\dots,N\}$ (no fixed points). Agent $A_i$ wants one unit of $g_{\pi(i)}$.
- Utility: $u_i=1$ iff $A_i$ ends with $g_{\pi(i)}$, otherwise $u_i=0$.

Let $C(\pi)$ denote the (directed) cycle decomposition of $\pi$.

### 1.2 Communication‑bounded bilateral protocols

Fix constants $R\in\mathbb{N}$ and $b\in\mathbb{N}$.

A **bilateral protocol** $P$ consists of local decision rules for each agent under the following constraints:

1. **Rounds:** time is synchronous rounds $t=1,\dots,R$ where $R$ does not scale with $N$.
2. **Local information:** at $t=0$, agent $A_i$ knows only $(i,g_i,\pi(i))$. At any time, its actions depend only on this private type, its received messages, and private randomness.
3. **Message budget:** in each round an agent may initiate contact with at most one other agent and send a message of at most $b$ bits (or idle). An agent participates in at most one trade per round.
4. **Trades:** goods can move only through trades between agents that have contacted each other. A trade exchanges at most one unit of each item.

Let $\mathsf{Clear}(P,\pi)$ be the event that after $R$ rounds under $P$, every agent holds its target good.

### 1.3 Hub institutions

We compare bilateral protocols to two hubbed variants:

- **Money/Exchange:** a hub $H$ posts prices $P[g]$ and trades any good for a fungible token $M$. Agents trade only with $H$.
- **Local planner without token:** a hub $P$ receives agents’ reports and can execute only obvious pairwise swaps (no global cycle search, no token).

## 2. Theorems

### Lemma 1 (Long cycles are typical)

For a uniformly random derangement $\pi$ on $N$ elements, there exists a constant $c_0>0$ such that for all sufficiently large $N$,

$$
\Pr_{\pi}\big[\text{$C(\pi)$ contains a cycle of length at least $N/2$}\big]\;\ge\;c_0 .
$$

This follows from standard results on random permutation cycle lengths; conditioning on no fixed points does not change the $\Theta(N)$ tail.

### Theorem 1 (Bilateral clearing lower bound)

Fix constants $R,b$. For any bilateral protocol $P$ satisfying Section 1.2,

$$
\Pr_{\pi}\big[\mathsf{Clear}(P,\pi)\big]\;\xrightarrow[N\to\infty]{}\;0 .
$$

More sharply, there exists $c=c(R,b)>0$ such that

$$
\Pr_{\pi}\big[\mathsf{Clear}(P,\pi)\big]\;\le\;\exp\!\big(-c\,N\log N\big)
$$

for all large $N$.

**Proof sketch.**

1. Condition on the event from Lemma 1 that $\pi$ has a cycle $C$ of length $L\ge N/2$; this happens with probability at least $c_0$.
2. Consider any agent $A_i$ on $C$. For the target allocation on $C$ to be realized, $A_i$ must either:
   - receive its target good from its predecessor on $C$, or
   - trade directly with its successor on $C$ to pass along its current good.
   In both cases, at least one of the two cycle edges incident to $A_i$ must be activated by a directed contact between the endpoints within the $R$ rounds.
3. Fix a cycle edge $\{A_i,A_j\}$ of $C$. From the agents’ perspectives at $t=0$, the neighbor $A_j$ is uniformly random among the $N-1$ others. Even allowing adaptivity, $A_i$ initiates at most $R$ contacts and $A_j$ initiates at most $R$ contacts, so the probability that either endpoint ever contacts the other is at most $2R/(N-1)$.
4. Therefore the probability that **every** one of the $L$ edges of the long cycle is activated is at most
   $$
   \Big(\frac{2R}{N-1}\Big)^{L}\;\le\;\Big(\frac{4R}{N}\Big)^{N/2},
   $$
   which is $\exp(-\Omega(N\log N))$.
5. Multiplying by the constant probability of Lemma 1 yields the stated bound. ∎

**Corollary 1.** To keep $\Pr[\mathsf{Clear}(P,\pi)]$ bounded away from $0$ as $N$ grows, the per‑agent round/message budget must scale at least like $R=\Omega(\log N)$ (equivalently total communication $\Omega(N\log N)$).

### Theorem 2 (Hub + token upper bound)

Suppose the Exchange hub $H$:

- posts fixed prices $P[g]\equiv 1$ for all goods,
- has sufficient liquidity to buy any endowment and sell any requested good,
- confirms any buy/sell at posted prices.

Then there is a strategy profile for agents that clears the market in at most two rounds with probability $1$:

1. Round 1: each agent sells its endowment $g_i$ to $H$ for one unit of $M$.
2. Round 2: each agent buys its target $g_{\pi(i)}$ from $H$ for one unit of $M$.

Total hub‑facing communication is at most $2N$ messages, so clearing uses $O(N)$ communication.

### Proposition 3 (Local planner without token)

A hub that is restricted to local pairwise swaps and cannot search for long cycles does not circumvent Theorem 1. Under a fixed round cap, its probability of full clearing under random derangements also tends to $0$ (and can be strictly worse than barter for small $N$).

## 3. Measuring exchange complexity

To quantify how much coordination/computation is absorbed by the Exchange in the money institution:

- **Message volume to/from the exchange:** count `request_quote`, `buy`, `sell`, and the Exchange’s `quote/confirm/deny` replies.
- **Price dynamics:** track how often and how far prices $P[g]$ move before trades stabilize (update counts and total variation).
- **Compare to barter lower bounds:** relate observed hub traffic to the $\Omega(N\log N)$ communication implied by Corollary 1 for bilateral protocols.

This maps where combinatorial search lives across institutions: in the bilateral graph for barter, partly at the planner for naive hierarchy, and largely inside the hub’s price/clearing logic for money/Exchange.

## 4. To be done later

1. **Formal theory**
   - Write a full model section matching the simulation.
   - Prove the bilateral lower bound and hub+token upper bound with explicit assumptions and rates.
   - Characterize when local hierarchy cannot clear.

2. **Empirical identification**
   - Regenerate a clean GPT‑5‑mini dataset with current code only for $N=3,5,8,10,12$ and $\ge 5$ seeds each.
   - Pre‑specify primary outcomes and hypotheses; report confidence intervals/regressions.

3. **Robustness and extensions**
   - Appendix reruns on other models and prompt variants.
   - Ablations: hub‑without‑token with global cycle search; token‑without‑hub (peer‑to‑peer token trades).
   - Emergent money with credible redemption semantics and higher‑pressure regimes.

4. **Exchange complexity analysis**
   - Rerun money/Exchange with instrumentation for all $N$/seeds.
   - Plot hub inbox/outbox volume, price‑update counts, and absolute price change versus $N$.
   - Compare hub‑side communication to the $\Omega(N\log N)$ bilateral lower bound.
