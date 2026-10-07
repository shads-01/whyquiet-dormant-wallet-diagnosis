# Economics model — all 25 ideas, sized on upay

> Companion to `docs/v3/long-list.md`. Baselines from `docs/v3/upay-model.md` §2 and §4; the only
> upay-specific scale inputs are the FY2023 figures already recorded in `docs/v3/interview.md` (S2, TBS).
> Every input is tagged **SOURCED** (with the nearest source) or **ASSUMED** (with the assumption
> named). Nothing here prints a taka figure without one of those two tags.
>
> Derived 3 Oct 2026. Arithmetic is reproducible from §1–§2 by hand.

---

## 0. The finding that reorders the whole list

The three idea files size every idea against **bKash's** baselines. bKash FY2025 revenue is
**Tk 65.65bn [SOURCED]**, so "1% of revenue = Tk 66 crore" became the headline watermark of all three
documents.

**upay's FY2023 revenue was Tk 43.32 crore [SOURCED — S2/TBS].**

So the watermark every idea was measured against — **Tk 66 crore — is 1.5× upay's entire annual
revenue.** An idea "worth Tk 66 crore" at bKash scale is worth at most ~Tk 43 lakh at upay scale, and
proportionally less. Every taka figure in `ideas-1-2-3-8`, `ideas-4-6` and `ideas-5-7` is a large-player
number presented in upay's deck.

Two further consequences, both load-bearing:

1. **upay lost Tk 85.43 crore on Tk 43.32 crore of revenue [SOURCED — S2].** Total costs ≈ Tk 128.75
   crore. Applying bKash's 63.18% cost-of-services ratio gives a cost-of-services line of **Tk 27.4
   crore** — i.e. only 21% of upay's actual cost base. **The L1 cost-to-serve lever, which carries four
   of the 25 ideas, is not the lever upay's P&L is made of.** It is an MFS-at-scale lever.
2. **The "1m extra cash-outs" watermark used throughout the idea files is 31–100% of upay's entire
   annual cash-out volume** (see §1, base 3.2m). Ideas sized in that unit are oversizing by roughly an
   order of magnitude.

**Bottom line: no idea in the long list moves upay's P&L by more than single-digit percent of revenue,
and the three largest are the three most assumption-stacked.** The best cases:

| Idea | Base taka | % of upay revenue | Assumptions the number rests on |
| --- | --- | --- | --- |
| #22 Settlement-Timing Yield Desk | Tk 2.5 crore | 5.8% | **3 stacked** — bKash's float yield × ASSUMED QR value share × ASSUMED merchant adoption |
| #15 Silent-Churn Triage | Tk 2.1 crore | 4.8% | **1 dominant** — a 4% recovery rate, unsupported in either direction |
| #6 Full-Loop Swap Engine | Tk 90 lakh | 2.1% | **2** — upay's net MDR share and the merchant cash-out rate, both UNVERIFIED |

The pattern is uncomfortable and worth stating in the deck: **the biggest numbers come from merchant and
dormant-base assumptions, and the best-evidenced idea produces the smallest number.** #2 Float
Pre-Positioning is the only idea whose base case rests on something `interview.md` actually evidences
(S3: agents are volume-constrained at 9–26 transactions a day) — and it is worth **Tk 52 lakh**.

§5 sets out what does move, and why the list is still worth prototyping.

---

## 1. upay scale model — the new denominator

### 1.1 The sourced inputs

| Input | Value | Tag | Source |
| --- | --- | --- | --- |
| upay revenue FY2023 | **Tk 43.32 crore** | **SOURCED** | S2/TBS |
| upay loss FY2023 | Tk 85.43 crore | **SOURCED** (see conflict below) | S2/TBS |
| Registered customers | **8.5m** | **SOURCED** | S2/TBS |
| Registered agents | **154,000** | **SOURCED** | S2/TBS |
| Merchants | **14,519** | **SOURCED** | S2/TBS |
| Active agents (current) | 130,000+ | **SOURCED** (marketing copy, conflicts with 154k) | upay/UCB pages |
| Avg cash-out ticket | Tk 2,132 | **SOURCED** | BB Oct-2025 |
| Cash-out share of MFS value | 23.6% | **SOURCED** | BB Oct-2025 |
| Commission share of net revenue | 93.61% | **SOURCED** (bKash FY2024) | bKash audited |
| upay agent cash-out take-rate | 1.40% ceiling, tiered below | **SOURCED**; current rate **UNVERIFIED** | tbsnews + FE CEO |
| Float yield on trust balances | 9.33% implied; 17.4% of net revenue | **SOURCED** (bKash FY2024) | bKash audited |
| Merchant QR MDR (merchant pays) | min 1% incl. VAT from 1 Jul 2026 | **SOURCED** | networkbangladesh |
| Merchant payment to customer | Free | **SOURCED** | upay FAQ, COO-signed |
| Cross-operator QR cost absorbed by upay | Tk 5–8 per 1,000 | **SOURCED** | FE 15 Sep 2026 |

> **Live evidence conflict, do not resolve by picking one.** S2's headline is *"upay's accumulated
> losses cross Tk 300 crore"* while `interview.md` records the same source as **Tk 85.43 crore loss for
> the year**. Accumulated and annual are different quantities, and the 5-year gap between them is
> unexplained. This model uses **Tk 43.32 crore revenue** (unambiguous) and treats the loss figure as
> **directional only** — it is not used in any calculation below.

### 1.2 The derived denominators, as ranges

| Denominator | Cons | **Base** | Aggr | Derivation and tag |
| --- | --- | --- | --- | --- |
| Active customers | 3.40m | **4.87m** | 5.95m | 40% / 57.3% / 70% of 8.5m. 57.3% is bKash's rate **[SOURCED-bKash]**; applying it to upay is **ASSUMED** |
| Dormant customers | 5.10m | **3.63m** | 2.55m | 8.5m − active |
| **ARPU** | Tk 127/yr | **Tk 89/yr** | Tk 73/yr | Tk 433.2m ÷ active. **bKash's is Tk 1,397/yr [SOURCED] — upay's ARPU is ~16× lower** |
| Active agents | 20,000 | **40,000** | 77,000 | **ASSUMED.** See the contradiction in §1.3 |
| Cash-out txns/yr | 2.0m | **3.2m** | 7.1m | Tk 405.5m commission × 23.6% ÷ 1.4% ÷ Tk 2,132. Share and take-rate both **ASSUMED for upay** |
| Cash-out revenue | Tk 43m | **Tk 96m** | Tk 341m | cash-out txns × Tk 2,132 × take-rate |
| Total transaction value | Tk 2,900cr | **Tk 4,330cr** | Tk 8,660cr | revenue ÷ 1.0% blended take. **ASSUMED** blended take (CEO says tiered below 1.4%) |
| Merchant QR value/yr | Tk 87cr | **Tk 217cr** | Tk 433cr | 3% / 5% / 10% of total value. **ASSUMED** |
| Merchant QR gross MDR | Tk 87lakh | **Tk 2.2cr** | Tk 4.3cr | QR value × 1% [SOURCED]. upay's net share of it **UNVERIFIED** |
| Avg trust balance (float) | Tk 35cr | **Tk 81cr** | Tk 200cr | 17.4% of revenue ÷ 9.33% yield, both **[SOURCED-bKash]**, both **ASSUMED** for upay |
| Float income | Tk 3.3cr | **Tk 7.5cr** | Tk 18.7cr | 17.4% of revenue |
| Revenue per agent | Tk 1,876 | **Tk 2,813** | Tk 5,626 | Tk 433.2m ÷ 154k registered agents. **bKash: Tk 187,571/yr [SOURCED] — 67× larger** |
| Cost of services | Tk 17cr | **Tk 27.4cr** | Tk 55cr | 63.18% of revenue **[SOURCED-bKash]**, **ASSUMED** for upay |

### 1.3 The contradiction that bounds every number here

**These sourced figures cannot all describe a working network simultaneously.**

- 3.2m cash-outs ÷ 40,000 active agents = **80 cash-outs per agent per year** — 0.27 per day.
- S3 **[SOURCED]** says an agent needs **15–20 transactions a day** just to be satisfied, and **3–5** for
  the provider to break even.
- 154,000 agents each clearing even 3/day would be ~830m cash-outs a year — **260× the revenue-implied
  figure**, and worth ~Tk 2,400 crore of revenue at 1.4%, i.e. **55× upay's actual revenue.**

So either the agent count is *licensed and largely inactive*, or the FY2023 revenue is depressed by
one-offs. **This model takes the revenue as authoritative** (it is the closest thing to an audited
figure) and therefore treats the network as **under-utilised**, with cash-out volume as the binding
ceiling. That is the conservative reading. It is also the reading that makes the agent-productivity
ideas (L6) worth prototyping: a network that is licensed but idle is an asset problem, not a volume
problem.

---

## 2. Conversion constants

Every idea below is built from these nine. upay-native units replace the bKash anchors used in the idea
files.

| # | Unit | Value (base) | Derivation |
| --- | --- | --- | --- |
| **U1** | +1,000 cash-outs | **Tk 29,850** | 1,000 × Tk 2,132 × 1.4% |
| **U2** | +1% cash-out volume (32,000 cash-outs) | **Tk 96 lakh** | 32,000 × U1 |
| **U3** | +1,000 dormant users activated | **Tk 8.9 lakh** full ARPU / **Tk 4.5 lakh** at 50% ramp | 1,000 × Tk 89 |
| **U4** | +1% relative on active rate | **Tk 43 lakh** | +48,705 users × Tk 89. Equals 1% of revenue by construction |
| **U5** | +1% realised take-rate on cash-out | **Tk 96 lakh** | Tk 95.7m × 1% |
| **U6** | +1% relative cut in cost-to-serve | **Tk 27 lakh** | 0.632% × Tk 433.2m. **On a line that is 21% of upay's real cost base** |
| **U7** | +1,000 merchants | **Tk 24 lakh** gross MDR / **Tk 12 lakh** net | 1,000 × Tk 800/day × 300 days × 1%; net share **ASSUMED 50%** |
| **U8** | +1% relative on float | **Tk 75 lakh** | Tk 7.5cr × 1% |
| **U9** | +Tk 1/1,000 take-rate on all cash-outs | **Tk 68 lakh** | Tk 6,836cr × 0.1% |

**Sanity check on the whole model:** U4 = Tk 43 lakh = 1% of upay revenue = **Tk 0.43 crore**. Everything
below should be read against that number. An idea worth "Tk 66 crore" in the old files is worth
"about Tk 43 lakh" here.

---

## 3. The 17 models that survive

Ranges are **conservative / base / aggressive**. All figures are **annual taka impact on upay's P&L**,
base case unless stated.

### L1 — Cost-to-serve

#### 1. Agent Shift Market · T05

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Failed / re-served share of cash-outs | 1% | **3%** | 6% | **ASSUMED** (S4 evidences refusals, not a rate) |
| Share recovered by matching | 15% | **35%** | 60% | **ASSUMED** |
| Annual platform + ops cost | Tk 40lakh | **Tk 30lakh** | Tk 25lakh | **ASSUMED** |

`impact = cash_out_txs × fail% × recover% × U1 − cost` → base: 3.2m × 3% × 35% = 33,600 cash-outs
× U1 = **Tk 10.0 lakh − Tk 30 lakh = Tk −20 lakh.**

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **−Tk 34lakh** | **−Tk 20lakh** | **+Tk 96lakh** |

- **Break-even adoption:** 3% failure rate recovered must reach **36%** — i.e. the market must clear a
  third of refusals — before the product pays for itself.
- **Sensitive:** (1) `fail%` — nothing in `interview.md` measures it, and it drives everything;
  (2) `recover%`, which the matching algorithm sets and which degrades if float data is stale.
- **Verdict: KEEP-FLAGGED, on agent service not taka.** The base case is negative. It survives because
  refusals (S4) are the one agent pain upay's customers actually experience, and because a district
  officer demoing refusal-routing is worth more than a positive-but-tiny number.

#### 2. Float Pre-Positioning · T05

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Active agents pre-funded | 2,000 | **4,000** | 8,000 | **ASSUMED** |
| Extra cash-outs per funded agent/yr | 0.2 | **0.5** | 1.0 | **ASSUMED** (S3 evidences 9–26/day need; volume is the ceiling here) |
| Default / unrecovered advance | 6% | **3%** | 1% | **ASSUMED** |
| Advance fee, net of funding | Tk 1.0% | **Tk 1.5%** | Tk 2.5% | **ASSUMED** |

`impact = agents × extra_txns × U1 − advance_exposure × default%` → base: 4,000 × 0.5 × Tk 29,850 =
**Tk 59.7 lakh**, less 3% default on the exposure.

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **−Tk 5lakh** | **+Tk 52lakh** | **+Tk 2.3cr** |

Note the funding cost is **not** 9.33% — that yield is earned on balances upay already holds in trust,
so advancing to an agent keeps the balance in the trust account and the cost is **credit risk**, not
opportunity cost. Modelling it at 9.33% (as a naive reading would) turns this idea negative for the
wrong reason.

- **Break-even adoption:** **1,600 funded agents at 0.5 extra cash-outs each** — 40% of base.
- **Sensitive:** (1) `extra_txns per funded agent` — S3 says agents are volume-constrained, but our
  denominator already implies idle agents, so this may be near-zero; (2) `default%`, because an agent
  defaulting a prefund is a public-relations event, not a write-off.
- **Verdict: KEEP.** Best-evidenced L1/L6 idea: S3 and S4 both describe the mechanism directly, and the
  taka works at the base.

### L2 — Retention / active rate

#### 4. Goal Autopilot · T03 flagship

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Eligible dormant base | 5% | **15%** | 25% of dormant | **ASSUMED** |
| Activation rate among eligible | 2% | **5%** | 10% | **ASSUMED** (S6: one in five workers already save monthly) |
| ARPU realised vs full | 30% | **50%** | 75% | **ASSUMED** (upay-model.md §4 Lever 5 ramp) |

`impact = dormant × eligible% × activation% × U3 × ramp` → base: 3.63m × 15% × 5% = 27,225 users
× Tk 4.5 lakh/1,000 = **Tk 12.3 lakh.**

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **+Tk 2lakh** | **+Tk 12lakh** | **+Tk 52lakh** |

- **Break-even adoption:** 15% eligible × 5% activation is the base; **the whole idea never reaches
  break-even on its own** — break-even against a Tk 60lakh build cost needs ~14% activation.
- **Sensitive:** (1) `ARPU` at Tk 89/yr means 1,000 extra users are worth **Tk 8.9 lakh** — this lever
  is arithmetically incapable of mattering at upay's ARPU; (2) `ramp %`, because Tk 89 ARPU leaves no
  room for the modelled average-vs-worst-month difference.
- **Verdict: KEEP-FLAGGED on relevance, not economics.** The flagship track and the brief's own persona
  make this the right thing to build; the taka does not make the case. Say so in the deck.

#### 5. Sponsor Payroll Market · T02/T04

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Employers in programme | 20 | **80** | 300 | **ASSUMED** |
| Workers per employer | 200 | **400** | 900 | **ASSUMED** (Agrani/foodpanda scale **SOURCED** as partners, sizes not) |
| Dormant-wallets recovered per employer/yr | 15 | **45** | 120 | **ASSUMED** |
| upay's cost per recovery (service + onboarding) | Tk 1,500 | **Tk 900** | Tk 500 | **ASSUMED** |
| Bounty funded by employer | 100% | **100%** | 100% | **ASSUMED** — the entire mechanism |

`impact = recovered × U3 × ramp − recoveries × upay_cost` → base: 80 × 45 = 3,600 users × Tk 4.5lakh/1,000
= **Tk 16.2 lakh**, less 3,600 × Tk 900 = **Tk 32.4 lakh** → **net −Tk 16 lakh at full recovery.**

But the bounty is the **employer's** cost, so upay's only spend is servicing. Reframe on margin:
recovered wallets also generate ongoing payroll inflow. At base, 3,600 recovered × Tk 89 × 50% =
**Tk 16 lakh revenue** on Tk 32 lakh one-off service cost — **year 1 negative, year 2 positive.**

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Year 1** (one-off service cost Tk 900/recovery) | **−Tk 11lakh** | **−Tk 16lakh** | **+Tk 8lakh** |
| **Year 2** (steady: recovered wallets keep transacting, service cost falls to ~20% of year 1) | **−Tk 1lakh** | **+Tk 10lakh** | **+Tk 7lakh** |

The aggressive Year-2 figure is *lower* than base because ongoing service cost scales with the cohort
while revenue does not — at 36,000 recovered wallets upay is servicing more than it earns. That is the
real ceiling of a Tk 89-ARPU business, and it is worth saying out loud in the deck.

- **Break-even adoption:** **60 employers** in year 1, or **4,400 recovered wallets** to clear year-2
  servicing costs.
- **Sensitive:** (1) `recovered per employer` — the whole who-pays thesis assumes dormant wallets exist
  inside an employer's own payroll file, which is **unverified** and may be near zero; (2)
  `upay_cost per recovery`, since employer-funded does not mean upay-free.
- **Verdict: KEEP.** Structurally the only idea where a third party pays the acquisition cost. Judge it
  on the who-pays mechanism and the year-2 number; do not claim year-1 P&L.

### L3 — Frequency / mix

#### 6. Full-Loop Swap Engine · T02/T04

The critical number is the one the idea file got right and then walked past: **per Tk 1,000, own-loop
gross is Tk 10–18 against Tk 14 displaced [SOURCED inputs, ASSUMED loop split].** At the midpoint the
swap is **P&L-neutral.**

| Component per Tk 1,000 | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| MDR captured (gross) | Tk 7 | **Tk 10** | Tk 10 | 1% min incl. VAT **[SOURCED]**; upay net share **UNVERIFIED** |
| Merchant cash-out of proceeds | Tk 8 | **Tk 8** | Tk 8 | **UNVERIFIED**, third-party (ink.bd) |
| **Own-loop gross** | **Tk 15** | **Tk 18** | **Tk 18** | |
| Displaced agent take-rate | Tk 14 | **Tk 14** | Tk 14 | 1.4% **[SOURCED ceiling]** |
| Agent commission avoided | Tk 4 | **Tk 6** | Tk 7 | **ASSUMED** — upay-model.md §2.6 says operator keeps "well under half" of 1.85% |
| IRF cost avoided (cross-op share) | Tk 1.6 | **Tk 3.3** | Tk 5.0 | Tk 6.5/1,000 on 25% of volume **[SOURCED cost, ASSUMED share]** |

`impact = converted_units × (own_loop − displaced + commission_saved + IRF_avoided)`

The rates above are **absolute taka per Tk 1,000**, not percentages of value. Net =
10 + 8 − 14 + 6 + 3.3 = **Tk 13.3 per Tk 1,000 converted.** Cash-out value base is Tk 6,836 crore
(§1.2), so 1% converted = 680,000 units × Tk 13.3 = **Tk 90 lakh.**

| Converted share of cash-out value | Annual taka |
| --- | --- |
| 0.3% (conservative) | **+Tk 27 lakh** |
| **1.0% (base)** | **+Tk 90 lakh** |
| 2.5% (aggressive) | **+Tk 2.3 crore** |

At netshare 0.5 rather than 1.0 the base case halves to **+Tk 48 lakh** — which is why the UNVERIFIED
MDR share is the top sensitivity.

- **Break-even adoption:** conversion must exceed **0.22% of cash-out value** to cover a Tk 20 lakh
  build. The bar is low because the mechanism monetises *cost* (commission, IRF) rather than volume.
- **Sensitive:** (1) **upay's net share of MDR [UNVERIFIED]** — the entire break-even turns on it and
  upay-model.md §2.1a names it as one of three figures that must be pinned before the case can close;
  (2) `merchant cash-out of proceeds` at Tk 8/1,000 is **third-party UNVERIFIED** and is the term that
  makes the loop positive.
- **Verdict: KEEP, and it is the best P&L idea on the list** — the only one where the base case clears
  Tk 1 crore, because it monetises *cost* (commission, IRF) rather than volume.

#### 8. Incremental Offer Fund · T04

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Annual discount / offer budget | Tk 1cr | **Tk 5cr** | Tk 12cr | **ASSUMED.** No upay figure exists. bKash's FY2024 commercial expense was Tk 3.99bn **[SOURCED]** |
| Share provably non-incremental | 15% | **30%** | 45% | **ASSUMED** |
| Merchant co-funding share of savings | 0% | **25%** | 50% | **ASSUMED** |
| Incremental cash-outs unlocked | 10k | **30k** | 90k | **ASSUMED** — capped at ~1–3% of the 3.2m base (§1.3) |

`impact = budget × non_incremental% × merchant_share + incremental_txns × U1 − build`

Base: Tk 5cr × 30% × 25% = Tk 37.5 lakh saved, + 30,000 × U1 = Tk 89.6 lakh, − Tk 80 lakh build.

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **−Tk 50lakh** | **+Tk 47lakh** | **+Tk 1.8cr** |

- **Break-even adoption:** **12% of the offer budget must be provably non-incremental**, or ~18,000
  incremental cash-outs, for the build to pay for itself.
- **Sensitive:** (1) `budget` — **completely ASSUMED**; upay's commercial expense is unknown and the
  result scales linearly with it; (2) `merchant co-funding share`, which is the whole mechanism and has
  **no evidence at all** that upay merchants will co-fund offers.
- **Verdict: KEEP-FLAGGED.** The technique is named in the official brief and the demo is strong
  (Qini vs injected truth). The taka rests on a budget number nobody has, and the conservative case is
  negative. Never print Tk 5 crore as upay's — it is an assumption.

#### 9. Autopay Subscriptions · T06

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Subscriptions created | 100k | **400k** | 1.2m | **ASSUMED** |
| Direct revenue per subscription | Tk 0 | **Tk 0** | Tk 0 | **"All bill payments free" [SOURCED]** |
| Balance predictability value (float) | Tk 3cr | **Tk 8cr** | Tk 20cr extra avg balance | **ASSUMED** |
| Subsidy: uncollected bill penalty loss | Tk 10lakh | **Tk 25lakh** | Tk 60lakh | **ASSUMED** |

`impact = float_on_extra_balance − subsidy_loss` → base: Tk 8cr × 9.33% = Tk 75 lakh − Tk 25 lakh.

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **−Tk 5lakh** | **+Tk 50lakh** | **+Tk 1.3cr** |

- **Break-even adoption:** **Tk 2.7 crore of additional average float balance.** upay's whole average
  trust balance is modelled at Tk 81 crore, so this needs **3.3% more float**, which a predictable
  salary-to-bill pipeline plausibly delivers.
- **Sensitive:** (1) the float rate — 9.33% is **bKash's [SOURCED]**, and policy-rate moves change the
  whole case; (2) `subsidy loss` from failed auto-debits, which is a real cost nobody has sized.
- **Verdict: KEEP-FLAGGED.** Direct revenue is **structurally zero [SOURCED]** — every claim must be
  about float and frequency. And `interview.md` flags autopay/recurring mandates in Bangladesh as
  **UNVERIFIED**: search before pitching.

### L4 — ARPU / take-rate

#### 11. Wallet-Tier & Take-Rate Leakage · T02/T06

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Share of txns billed above the correct tier | 0.1% | **0.3%** | 0.8% | **ASSUMED** |
| Recoverable fraction | 40% | **60%** | 80% | **ASSUMED** |
| Annual audit + remediation cost | Tk 30lakh | **Tk 20lakh** | Tk 15lakh | **ASSUMED** |

`impact = cash_out_revenue × billed_over_tier% × recoverable − cost`

Cash-out revenue by scenario: Tk 43m cons / **Tk 96m base** / Tk 341m aggr.

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **−Tk 28lakh** | **−Tk 3lakh** | **+Tk 2.0cr** |

- **Break-even adoption:** **0.21% of transactions billed above the correct tier.** Any credible
  billing-error rate clears that — but see the sensitivity.
- **Sensitive:** (1) `billed_over_tier%` — the CEO's statement that rates are "**less than Tk 14** … in
  different layers and in cases **free of cost** [SOURCED]" proves tiers *exist and vary* but says
  nothing about whether they are **applied wrongly**. If they are applied correctly, the true rate is
  zero and the idea is worth zero; (2) whether remediation triggers customer complaints, which would
  convert a revenue win into a support cost.
- **Verdict: KEEP-FLAGGED, base case ~zero.** The base case is *negative*, and the aggressive case only
  arrives if over-billing exists at all. It survives on one property none of the others share: **posted
  take-rate vs realised take-rate is directly observable in a prototype.** That makes it the most
  honest demo on the list — you can show a judge the leakage or show them there is none.

#### 12. Retention Uplift Gate · T04/T02

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Annual retention discount spend | Tk 50lakh | **Tk 2cr** | Tk 6cr | **ASSUMED** (same gap as #8) |
| Share wasted on customers who would stay | 20% | **35%** | 50% | **ASSUMED** |
| Incremental retention earned | Tk 10lakh | **Tk 40lakh** | Tk 1.2cr | **ASSUMED** |

`impact = spend × wasted% + incremental_retention`

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **+Tk 20lakh** | **+Tk 1.1cr** | **+Tk 4.2cr** |

Base: Tk 2cr × 35% = Tk 70 lakh saved + Tk 40 lakh incremental. **Tk 1.1 crore is 2.5% of upay's
revenue from a Tk 2 crore budget that is itself an assumption** — treat the base as optimistic and the
conservative case as the honest headline.

- **Break-even adoption:** **29% of discount spend must be non-incremental.**
- **Sensitive:** (1) `spend` — assumed, same gap as #8; (2) the **negative-uplift segment**, which is
  the entire Responsible-AI story: if contact actively deters customers, a model that misses it destroys
  value while looking successful on response rate.
- **Verdict: KEEP-FLAGGED.** Uplift is the brief's named sharp ML signal, and the *refusal* (not
  discounting the already-loyal) is a judge-visible product. Do not present the base taka.

#### 13. Cross-Operator Leak Plug · T06/L07

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Merchant QR value/yr | Tk 87cr | **Tk 217cr** | Tk 433cr | **ASSUMED** (3/5/10% of value) |
| Cross-operator share | 15% | **25%** | 35% | **ASSUMED** |
| Reroutable to own-rail upay QR | 25% | **50%** | 70% | **ASSUMED** — needs an alternative in range |
| Cost avoided per 1,000 | Tk 5.00 | **Tk 6.50** | Tk 8.00 | **[SOURCED]** Tk 5–8/1,000 |

`impact = rerouted_value × Tk 6.50/1,000 − incentive_budget` (incentives funded from the saving)

Base walk: QR value Tk 217cr × 25% cross-operator = Tk 54.3cr × 50% reroutable = **Tk 27.1 crore**
rerouted = 271,250 units × Tk 6.50 = **Tk 17.6 lakh gross.** The base case is **self-funding by
construction** — the avoidance *is* the incentive budget.

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **+Tk 4lakh** | **+Tk 18lakh** | **+Tk 55lakh** |

- **Break-even adoption:** rerouting just **2.7% of cross-operator QR value** — Tk 1.5 crore of value —
  covers a Tk 10lakh build.
- **Sensitive:** (1) `reroutable %` — the binding physical constraint is whether an upay-QR merchant
  exists nearby, and S8's 37% supplier-cash figure suggests the merchant layer is thin; (2)
  `cross-operator share`, entirely ASSUMED with no published split.
- **Verdict: KEEP.** Smallest taka of the keepers but the **highest certainty per transaction** — it
  avoids a cost upay has publicly disclosed and dated within three weeks of registration closing, rather
  than winning a speculative fee. Strongest story-per-rupee on the list.

### L5 — Activation of dormant

#### 14. Dormant-Lead Bazaar · T02/T05

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Dormant base | 5.10m | **3.63m** | 2.55m | §1.2 |
| Leads worked/yr | 50k | **200k** | 600k | **ASSUMED** |
| Bounty per verified activation | Tk 120 | **Tk 250** | Tk 400 | **ASSUMED** |
| Activation rate on worked leads | 2% | **4%** | 8% | **ASSUMED** |
| ARPU realised | 35% | **50%** | 70% | **ASSUMED** |

`impact = leads × activation% × (ARPU × ramp − bounty)`

Base: 200,000 × 4% = 8,000 activations × (Tk 44.5 revenue − Tk 250 bounty) = **+Tk 15.6 lakh.**

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **−Tk 9lakh** | **+Tk 16lakh** | **−Tk 1.6cr** |

The aggressive case is **negative for the same reason the base is positive**: bounty scales with
activations, so at Tk 400 each the 48,000 activations cost more than they return. **This idea only
works in a narrow band.**

- **Break-even adoption:** the bounty must stay below **Tk 44** (ARPU × ramp) — i.e. a token gesture,
  not a real incentive. At a Tk 250 bounty no achievable activation rate rescues it, because ARPU is
  Tk 89 and activation cannot exceed the eligible base.
- **Sensitive:** (1) **ARPU [Tk 89]** — this single number decides the entire idea and it derives from
  one FY2023 revenue figure; (2) `bounty`, which agents will refuse if it approaches ARPU.
- **Verdict: KEEP-FLAGGED, and the arithmetic is the argument.** The activation lever cannot work at
  Tk 89 ARPU unless acquisition is **free**. That is a legitimate thing to show a judge — it is a
  quantified answer to "what would it take?" — and it is also why the same idea framed as
  **employer-funded** (#5) survives while the self-funded version does not.

#### 15. Silent-Churn Triage · T06

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Dormant base triaged | 15% | **35%** | 60% | **ASSUMED** |
| Cause correctly attributed | 30% | **50%** | 70% | **ASSUMED** |
| Users recovered | 1.5% | **4%** | 8% of triaged | **ASSUMED** |
| Annual triage cost | Tk 25lakh | **Tk 18lakh** | Tk 12lakh | **ASSUMED** |

`impact = dormant × triaged% × recovery% × ARPU × ramp − cost`

Base: 3.63m × 35% × 4% = 50,850 users × Tk 44.5 = **Tk 2.26 crore − Tk 18 lakh.**

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **−Tk 22lakh** | **+Tk 2.1cr** | **+Tk 8.1cr** |

- **Break-even adoption:** **1.9% recovery on a 35% triaged base** — 24,000 recovered dormant users,
  i.e. **0.66% of the dormant base**, which is a low bar for a correct-cause-intervention model.
- **Sensitive:** (1) `recovery rate`, which no evidence supports in either direction and which is the
  difference between −Tk 22 lakh and +Tk 2.1 crore; (2) whether the *attributed cause* is actionable — a
  correctly-diagnosed exit you cannot remedy is a free-text report.
- **Verdict: KEEP, and one of the three strongest taka on the list.** The reason is arithmetic: it is the
  only idea that reaches a *large fraction of the dormant base* cheaply, because diagnosis costs
  Tk 18 lakh against a Tk 89 ARPU × 50,850 recovered users. It stays keep-worthy on the **refusal**
  demo ("no attributable cause") rather than the money.

#### 16. Remittance-Season Awakening · T04

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Malaysia-corridor receivers reactivated | 2,000 | **8,000** | 25,000 | **ASSUMED** (corridor **[SOURCED]**; receiver counts not) |
| ARPU realised | 40% | **55%** | 75% | **ASSUMED** (remittance wallets hold balance longer) |
| upay cost per outreach | Tk 60 | **Tk 25** | Tk 10 | **ASSUMED** |
| Partner-funded share of outreach | 80% | **100%** | 100% | **ASSUMED** — the mechanism |

`impact = reactivated × ARPU × ramp − reactivated × upay_cost` (outreach funded by the partner)

Base: 8,000 × Tk 49 = Tk 39.2 lakh revenue − 8,000 × Tk 25 = Tk 2 lakh cost = **+Tk 37 lakh.**

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka (upay's own P&L)** | **+Tk 3lakh** | **+Tk 37lakh** | **+Tk 14lakh** |

Cons: 2,000 × Tk 36 − Tk 1.2 lakh. Aggr: 25,000 × Tk 67 − Tk 2.5 lakh.

The earlier Tk 44 lakh base for this idea included an **assumed partner list fee**. That fee is
**UNVERIFIED** — whether a remittance partner will pay for a ranked list of its own lapsed customers is
a sales question with no evidence — so it is now excluded from every case. If it exists, it is upside on
top of Tk 37 lakh.

- **Break-even adoption:** **1,600 reactivated receivers** — trivially low, because upay's cost is
  near zero when the partner funds it.

Base: 8,000 × Tk 49 = Tk 39.2 lakh revenue − Tk 2 lakh cost = **+Tk 37 lakh**, plus the partner-funded
list fee on the remittance corridor itself.

- **Break-even adoption:** **1,600 reactivated receivers** — trivially low, because upay's cost is
  near zero when the partner funds it.
- **Sensitive:** (1) whether the partner will pay for a *ranked list of its own lapsed customers* —
  a **sales** question with no evidence; (2) remittance-wallet ARPU, which is assumed 55% and could
  be lower than a primary wallet's.
- **Verdict: KEEP.** Second-best risk profile after #13: a third party funds it, break-even is low, and
  the corridor is a documented, dated partnership.

### L7 — Merchant volume

#### 20. Acceptance-Gap Sniper · T05

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Merchants onboarded/yr | 300 | **1,200** | 3,000 | **ASSUMED** |
| Field cost per merchant | Tk 12,000 | **Tk 8,000** | Tk 5,000 | **ASSUMED** |
| QR value per merchant/yr | Tk 1.2m | **Tk 2.4m** | Tk 3.6m | **ASSUMED** (Tk 800/day × 300) |
| upay net share of MDR | 30% | **50%** | 70% | **UNVERIFIED** — named in upay-model.md §2.1a |

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Year 1 (35% ramp)** | **−Tk 1lakh** | **−Tk 23lakh** | **+Tk 52lakh** |
| **Year 2 (steady)** | **+Tk 2lakh** | **+Tk 48lakh** | **+Tk 2.3cr** |

Base year 2: 1,200 × (Tk 2.4m × 1% × 50% = Tk 12,000 net MDR − Tk 8,000 field cost) = **+Tk 48 lakh.**

- **Break-even adoption:** **667 merchants/yr**, or a **field cost below Tk 12,000** at 1,200 merchants.
- **Sensitive:** (1) **upay's net share of MDR [UNVERIFIED]** — one of the three figures upay-model.md
  §2.1a says must be pinned before any mix-shift case can close; (2) `field cost per merchant`, which
  sets the entire payback and is above the net MDR at every conservative setting.
- **Verdict: KEEP-FLAGGED.** Negative year 1, thin steady state, and it depends on an UNVERIFIED number.
  The strategic argument (Lever 7 is where the mix is headed) is documented in `upay-model.md` §4 — use
  that, not a payback.

#### 22. Settlement-Timing Yield Desk · T05

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Merchant QR value/yr | Tk 87cr | **Tk 217cr** | Tk 433cr | §1.2 |
| Share accepting T+1 | 10% | **25%** | 45% | **ASSUMED** |
| Days held | 1 | **1** | 2 | **ASSUMED** |
| Merchant share of the yield | 60% | **50%** | 35% | **ASSUMED** |

`impact = value_held × days × 9.33% × (1 − merchant_share)`

Base walk: Tk 217cr × 25% = **Tk 54.3 crore held one extra day.** Float income on that for a single day
= Tk 542.5m × 0.0933 ÷ 365 = **Tk 1.39 crore/day**, of which upay retains 50% = **Tk 69 lakh per day
held.**

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **+Tk 33lakh** | **+Tk 2.5cr** | **+Tk 6.5cr** |

Cons: Tk 8.7cr held × Tk 2,224/day × 60% retained = Tk 33 lakh. Aggr: Tk 195cr held for 2 days ×
Tk 9.97cr/day × 65% = Tk 6.5 crore.

- **Break-even adoption:** **0.3 days of Tk 54 crore held.** Any credible merchant adoption clears this
  — which is the strongest reason to build it, and the weakest reason to trust the number.
- **Sensitive:** (1) **the 9.33% yield is bKash's [SOURCED-bKash] and ASSUMED for upay** — and it is a
  policy-rate-sensitive line, so a rate cut erases this idea entirely; (2) `merchant share of the
  yield`, which decides whether merchants participate at all.
- **Verdict: KEEP-FLAGGED, with a warning.** The base case is **Tk 2.5 crore — 5.8% of upay's revenue**
  and the second-largest on the list. It is also the **most assumption-stacked number in this document**:
  a bKash float yield × an ASSUMED QR value share × an ASSUMED merchant adoption rate, multiplied. Every
  one of those three can be wrong by 5×. Pitch the mechanism and the sensitivity, never the Tk 2.5 crore.

### L8 — B2B / payroll

#### 24. Payroll-as-a-Product · T07

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Employers live | 3 | **12** | 40 | **ASSUMED** (Agrani, foodpanda **[SOURCED]** as partners; count not) |
| Workers per employer | 300 | **700** | 1,500 | **ASSUMED** |
| Payroll value/yr | Tk 30cr | **Tk 100cr** | Tk 400cr | **ASSUMED** — the ≈3.1% base is **UNVERIFIED [secondary]** |
| Dwell days after disbursement | 0.5 | **1.5** | 3 | **ASSUMED** |
| Disbursement fee retained | 0.2% | **0.35%** | 0.5% | **ASSUMED** |

`impact = payroll_value × fee + avg_balance × 9.33%`

Base: Tk 100cr × 0.35% = **Tk 35 lakh** + dwell balance (Tk 100cr × 1.5/365 = Tk 41 lakh) × 9.33% =
**Tk 3.8 lakh** → **Tk 39 lakh.**

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **+Tk 6lakh** | **+Tk 39lakh** | **+Tk 2.3cr** |

- **Break-even adoption:** **Tk 12 crore of annual payroll volume**, or **340 workers** — the lowest
  break-even bar of any revenue idea on the list, because there is no agent commission to pay away.
- **Sensitive:** (1) the payroll base — `upay-model.md` Lever 8 is the **only lever with no reliable
  base at all [UNVERIFIED, secondary source]**; (2) `dwell days`, because at 1.5 days the entire float
  component is **Tk 3.8 lakh, i.e. 10% of the case**. Strip float out and this is a Tk 35 lakh
  disbursement-fee story with an ASSUMED 0.35% fee.
- **Verdict: KEEP-FLAGGED.** The *only* idea where the float line and the commission line reinforce
  rather than trade off, and the only one with a named counterparty (Agrani, foodpanda). The float
  component is noise; do not lead with dwell time.

#### 25. Campus Closed Loop · T03/T05

| Input | Cons | Base | Aggr | Tag |
| --- | --- | --- | --- | --- |
| Campuses live | 1 | **3** | 10 | **ASSUMED** (Daffodil MoU + UCSI **[SOURCED]**; RFID student ID is **planned, not live**) |
| Active terminals per campus | 25 | **45** | 90 | **ASSUMED** |
| Terminals saved from going dark | 3 | **8** | 20 per campus | **ASSUMED** |
| Value per saved terminal/yr | Tk 14,400 | **Tk 14,400** | Tk 14,400 | Tk 800/day × 300 × 1% × 50% net |
| Cost per campus/yr | Tk 3lakh | **Tk 2lakh** | Tk 1.5lakh | **ASSUMED** |

| | Cons | Base | Aggr |
| --- | --- | --- | --- |
| **Annual taka** | **−Tk 2.6lakh** | **−Tk 0.6lakh** | **+Tk 14lakh** |

Base: 3 campuses × 8 terminals saved = 24 × Tk 14,400 = **Tk 3.5 lakh** revenue, less 3 × Tk 2 lakh
campus cost = **−Tk 0.6 lakh.**

- **Break-even adoption:** **2.3 campuses live** with 8 terminals saved each.
- **Sensitive:** (1) `terminals saved` — a dead terminal is pure cost, so this is the number that
  actually matters and it is entirely ASSUMED; (2) campus count, capped by how many agreements exist.
- **Verdict: KEEP-FLAGGED.** The base case is **negative** and the taka is 14 lakh even at the
  aggressive end. It survives on relevance alone: **DIU hosts this hackathon and sits inside the same
  Daffodil Group upay signed an education MoU with.** That is a credibility asset no taka number can
  buy, and it is the single strongest reason to build something on the campus lane. Do not claim the
  RFID ID is live.

---

## 4. The 8 drops

Per the rule: base case negative **and** no strategic argument that survives the scale correction.

| # | Idea | Base taka | Why dropped | Revivable if |
| --- | --- | --- | --- | --- |
| 3 | **Complaint Autopsy & First-Contact Remedy** | **−Tk 15lakh** | Recovers handling minutes on a cost line that is **21% of upay's real cost base**, and whose own size is UNVERIFIED. No strategic argument a judge will weight. | upay discloses support cost per case — then it becomes a measurable L1 play |
| 7 | **Restock Credit** | **−Tk 41lakh yr 1** | Underwriting a credit line is **outside a PSP's licence** — a regulatory question unanswerable in 24h. Interest income (Tk 24lakh on Tk 2cr at 12%) never covers the 9.33% funding cost (Tk 19lakh) plus default (Tk 6lakh) plus ops (Tk 40lakh). | UCB Fintech holds a lending licence and the parent underwrites |
| 10 | **Willingness-to-Pay Compiler** | **≈ Tk 0** | Requires raising fees on a player whose competitor **cut prices in July 2026 [SOURCED]** and whose ARPU is Tk 89/yr. The optimisation is right; the direction of travel is against it. | upay's realised take-rate is found materially *below* its posted ladder — that is idea #11, which is kept |
| 17 | **Conversion-Priced Agent Tiers** | **+Tk 2lakh** | Ceiling is hard: revenue per agent is **Tk 2,813/yr on the registered base [derived]**. Tier re-pricing moves a rounding error, and giving up commission to move a rounding error is a bad trade. | active agent count is confirmed far below 154k, so per-agent yield rises materially |
| 18 | **Agent Rescue Fund** | **−Tk 1.2cr** | **Negative in all three scenarios**, with a hard ceiling: cost per rescue (Tk 8,000–18,000) must fall below recovered revenue per agent (Tk 2,100 at 20% of an active agent's Tk 10,830). Even restoring an agent to *full* activity (Tk 10,830) fails against the base cost of Tk 12,000. **Break-even requires a free rescue.** | a rescue is genuinely near-zero marginal cost (an SMS plus a rate rebate) — then it is a retention tool, not a funded fund |
| 19 | **Counter Attach Engine** | **+Tk 15lakh** | NBA on a crowded shape against a strong deterministic rival ("always offer DPS"), for **3.5% of revenue**. The differentiating joint framing is not enough on its own. | attach rate is shown to exceed the DPS script's rate — measurable in a prototype |
| 21 | **Merchant Fee-Elasticity Guard** | **+Tk 1lakh** | Protects MDR on a QR line whose **entire** modelled gross is Tk 2.2 crore. There is not enough margin at risk to price. | upay's QR share of value is far above the 5% assumed |
| 23 | **Failed-QR Recovery** | **+Tk 3lakh** | Recovered value lands on the same Tk 2.2 crore QR line; 2% recovery is **Tk 43,000**. Below the noise floor of any support-cost saving. | — genuinely dead at this scale |

**Pattern in the drops:** six of eight sit on the merchant/agent lines where upay's volume is two to
three orders of magnitude below what the idea files assumed, and in **#18 and #23** the ceiling is set by
a hard sourced denominator (Tk 2,813/agent/yr; Tk 2.2cr of QR volume) that no assumption can lift. Two
(#7, #10) are questions of licence and competitive direction, not arithmetic.

**Consequence: Lever 6 (agent productivity) is eliminated entirely.** All three of its ideas (#17
Conversion-Priced Agent Tiers, #18 Agent Rescue Fund, #19 Counter Attach Engine) fail on the same root
cause — **revenue per agent is Tk 2,813/yr on the registered base, and Tk 10,830/yr if only 40,000
agents are actually active.** No commission-tier scheme, rescue fund or attach engine moves a number that
small by enough to matter. The one L6 idea that survives is **#2 Float Pre-Positioning**, filed under L1
because its mechanism is cost-to-serve, and its base case is the best-evidenced number in this document.

---

## 5. What actually moves, if the P&L does not

The honest summary: **at Tk 43.32 crore of revenue, upay's P&L is dominated by its Tk 85 crore loss, and
no product idea in this list is going to change that.** The largest base case on the list — #22 at
Tk 2.5 crore — is **5.8% of revenue and 2.9% of the loss**, and it rests on three stacked assumptions.

What the ideas *do* move is measurable and worth building:

| What moves | Ideas | The number a judge should be shown |
| --- | --- | --- |
| **Volume** — cash-out and merchant transactions per active user | #2, #6, #9, #13, #20, #22 | **Transactions per active user per month**, against the sourced industry baseline of 678.63m txns/month **[SOURCED]**. upay's own current figure is UNVERIFIED — establishing it is itself a deliverable. |
| **Retention** — the 90-day active rate | #4, #5, #14, #15, #16 | **Active rate as % of the 8.5m registered base [SOURCED]**, against bKash's 57.3%. At Tk 89 ARPU this lever is capped at ~Tk 43 lakh per 1% relative — but the *users* are real and the CAC is already sunk. |
| **Merchant stickiness** — terminals that stay live | #20, #22, #25 | **Merchants with >30 days of activity** out of 14,519 **[SOURCED]**. A dead terminal is pure cost and is the one merchant metric that matters at this scale. |
| **Cost-to-serve structure** — refusals, float, prefunding | #1, #2, #13 | **Cash-outs completed ÷ cash-outs attempted**, and **float advanced vs recovered**. Both directly measurable in a prototype; both larger in taka than most revenue ideas. |

**The four non-P&L reasons these still deserve a prototype:**

1. **upay's reported figures are internally inconsistent** (§1.3): 154,000 licensed agents against
   revenue implying 0.27 cash-outs per agent per day. A prototype that *sizes the actual network
   productivity* answers a question upay's own public numbers cannot.
2. **The rubric does not score taka.** Problem relevance 20% · AI depth 20% · business impact 20%, where
   "clear, measurable value and plausible economics" is satisfied by a **rate, ratio or count** a
   business judge can hold. *Transactions per user*, *active rate*, *terminals alive* and
   *cash-outs completed ÷ attempted* are all four of those.
3. **AI necessity is judged against a deterministic rule**, not against taka. #12's refusal, #16's
   partner-funded list, #25's healthy-but-on-break terminal are all model-shaped regardless of scale.
4. **Two of the strongest ideas are cost-side and self-funding** (#13 avoids a publicly disclosed cost;
   #5 and #16 have a third party paying). These do not need upay's revenue to be large to be honest.

---

## 6. The two assumptions that move the entire list

Every number in §3 inherits these. If only two things get pinned before the on-site requirement drop,
pin these.

| Rank | Assumption | Current status | Swing across all 25 ideas | How to resolve in 24h |
| --- | --- | --- | --- | --- |
| **1** | **upay revenue base** = Tk 43.32 crore FY2023 | **SOURCED** (S2/TBS) but possibly depressed by one-offs; the loss figure beside it is **conflicted** (annual Tk 85.43cr vs accumulated Tk 300cr headline) | **±2× on every result.** ARPU, cash-out volume, merchant value and float are all derived from it | Retrieve UCB PLC's annual report subsidiary note. One document. If revenue is Tk 80cr+, several drops come back. |
| **2** | **upay's net share of Bangla QR MDR** | **UNVERIFIED**, named by `upay-model.md` §2.1a as one of three figures that must be pinned | Swings **#6** (the best-evidenced large idea) by **±Tk 45 lakh**, **#20** by ±Tk 60 lakh, and decides whether **#21**'s Tk 2.2 crore QR line is worth protecting at all | upay's `/limits-and-charges` page — the same retrieval that resolves the **agent take-rate conflict** (1.400% vs a tiered 0.7%/0.5% schedule) kills two birds. |

Runners-up, in order: the **blended realised take-rate** (ASSUMED 1.0%; drives total transaction value
and therefore every volume denominator) and **upay's active agent count** (ASSUMED 40,000 against 154,000
registered — swings all of L6).

---

## 7. What this document does not do

- Does not resolve the S2 loss-figure conflict. It is flagged in §1.1 and excluded from every calculation.
- Does not re-derive `upay-model.md` §4's Lever-1 and Lever-3 errors; it works around them. The errors
  are still live in `upay-model.md` §4 and `upay-model-calc.py`.
- Does not claim any ASSUMED figure is a fact. Every one is tagged, and the four largest are listed in §6
  with a resolution route.
- Does not put a taka total on any Lever-8 idea beyond the modelled range. The ≈3.1% of MFS value base is
  **UNVERIFIED (secondary source)** and `upay-model.md` §4 Lever 8 says so explicitly.
- Does not revisit Track 01 §0. Nothing here touches fraud, scam, ATO, mule or AML.