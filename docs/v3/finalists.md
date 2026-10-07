# Finalists — top 5 by relevance × business impact × originality

> Written 3 Oct 2026. Universe: the **10 survivors of `redteam.md` §2**. The 7 kills in `redteam.md` §1
> are not reconsidered. Official scaffolding is taken from the guideline PDF §10 (*Student Idea
> Development Framework*) — the nine-step logic chain and the problem-statement format are quoted from it,
> not invented:
>
> > **Recommended problem statement format:** *"For [specific user], [specific problem] causes [measurable
> > consequence]"*
>
> Taka figures are from `economics.md` §3 and carry that document's tags. Anything I add beyond it is
> marked. **Every taka number below is an annual impact on upay's P&L at a base case, not a claim about
> actual results.**

---

## 0. Scoring, and one timing caveat

Scores 1–5. Business impact is scored on **how well a business judge can hold the number and how little
it rests on assumption** — not on the size of the number.

| Rank | Idea | Rel | Biz | Orig | Total | Track |
| --- | --- | --- | --- | --- | --- | --- |
| **F1** | **#15 Silent-Churn Triage** | 5 | 5 | 5 | **15** | 06 / 02 |
| **F2** | **#24 Payroll-as-a-Product** | 5 | 4 | 5 | **14** | 07 → 03 / 05 |
| **F3** | **#6 Full-Loop Swap Engine** | 5 | 4 | 4 | **13** | 02 / 04 |
| **F4** | **#13 Cross-Operator Leak Plug** | 4 | 3 | 5 | **12** | 06 / 07 |
| **F5** | **#12 Retention Uplift Gate** | 4 | 4 | 4 | **12** | 04 / 02 |

**Why the three highest-relevance ideas in the repo are not here.** `#25 Campus Closed Loop` has the highest
relevance score available — DIU hosts the hackathon and sits inside the same Daffodil Group as upay's
education MoU — but it scores **5 / 2 / 3**. Its base case is negative and its largest aggressive number
is Tk 14 lakh. `#20 Acceptance-Gap Sniper` is **4 / 2 / 4** for the same reason: field cost sits above net
MDR at every conservative setting. `#5 Sponsor Payroll Market` is **4 / 3 / 4** and is excluded as
**redundant with F2** — same payroll domicile, strictly worse economics (F2's break-even is the lowest of
any revenue idea in the set). `#11 Wallet-Tier & Take-Rate Leakage` is **4 / 3 / 4** after red-teaming
raised its relevance via MFS Regs 9.0, and misses the cut on one specific risk: its entire case resolves
to a binary — whether over-billing exists at all — and the honest demo may well be *"we found none."*
That is a good 5% story and a bad 20% business-impact story.

**Timing caveat, stated once.** `CONTEXT_v3.md` §1 records ~24 hours left of the 72-hour initial window
when those docs were written. A 48-hour plan therefore overruns it. I have built the 48 hours you asked
for and structured it against the **real** phase shape in `CONTEXT_v3.md` §1 — 0–12 build, 12–24
**pre-evaluation-ready**, 24–48 depth plus the §9 deliverables — so the first 24 hours stand alone if the
window is 24 and not 48.

**Team:** 3 (max per hackathon rules §2). P1 data/models · P2 API + business rules · P3 web + demo +
deliverables. Every member must be able to demo and explain the design — that is a hard constraint from
`docs/CONTEXT.md`, and P3 does not own the code, only the surface.

---

## F1 — Silent-Churn Triage (Cause Desk)

**Track 06 Operations & Service Intelligence.** The strongest of the set on all three axes: the problem is
the largest number in the repo, the mechanism is the only label-free one, and the refusal is the product.

### Official one-page logic chain

| Step | Answer |
| --- | --- |
| **1. User** | upay's dormant-wallet operations team (primary); the dormant customer (secondary). Persona: a garment worker whose wallet is active on payday and silent for eleven weeks afterwards. |
| **2. Problem** | upay has exactly one signal for dormancy — three weeks without a transaction — and that gap is **five different diseases with five different remedies**: job exit, migration, a solved problem, a fee shock, a supply-side failure. Today upay either treats all five identically or treats none. |
| **3. Why now** | 237m registered MFS accounts at Dec 2024 with only **37.6% active** (S1, TIB/BB); **42.5% of users transact once or twice a month** (S12, 2018 survey of 442 users). upay's own base is 8.5m registered, modelled at 3.63m dormant (`economics.md` §1.2). Crucially, **the label does not exist** — cause of dormancy is not a column in any ledger, so this cannot be bought off the shelf. |
| **4. Solution** | **Cause Desk** — an internal console that reads a dormant wallet's entire transaction *shape* since acquisition, attributes a cause where one is attributable, maps cause → remedy, prices the remedy, and **refuses** where no cause is attributable. |
| **5. AI role** | **Label-free multi-cause classification of the decline shape.** The generator knows the true cause; the model never sees that label. Output is a posterior over cause families plus the feature contributions that drove it (SHAP-style, per brief §14 explainability). |
| **6. Impact + target** | **Recovered dormant wallets as a share of the triaged base. Target ≥1.9%** on a 35% triaged base (≈24,000 users, 0.66% of the dormant base) — the stated break-even. Secondaries: cause-attribution accuracy (target ≥50%) and **share refused as "no attributable cause"** — the credibility metric, not a performance metric. |
| **7. Data** | Synthetic only (brief §11). Customers, transactions with types, devices/locations/timestamps/channels, cases. Ground-truth cause written to a **separate file never read by training**. Deliberate traps: job-exit, holiday-quiet, solved-once, fee-shock, supply-blocked. Clean held-out split, never trained on. |
| **8. Validation** | Offline: macro-F1 over five cause families on held-out synthetic. **Then money, not accuracy:** `users_recovered × ARPU × ramp − triage_cost`, for rule vs model vs oracle. The rule baseline is **"3 weeks silent → reactivation message to everyone."** Report the cases **where the rule was right** — a model that never loses to a threshold is not believable. |
| **9. Scale** | Real upay data would add three things we lack: inter-FS visibility (to see whether a "recovered" wallet just moved to bKash), campaign-response ground truth, and eKYC-verified identity for employer/travel causes. Module seams are data-prep / inference / business-rule separated per brief §12, so a warehouse drop swaps the generator and nothing else. |

### Problem statement (official format)

> For upay's dormant-wallet operations team, having only one signal for dormancy — three weeks without a
> transaction — causes the same blanket reactivation message to be sent to five different underlying
> problems, so an entire Tk 2.1 crore modelled recovery rests on a 4% recovery rate that no evidence
> supports in either direction.

### The three things a judge remembers

- **One sentence:** *"A wallet going quiet is five diseases, and upay only has one thermometer."*
- **One taka number:** **Tk 2.1 crore base case — 4.8% of upay's FY2023 revenue — from diagnosing 1.27 million triaged wallets for Tk 18 lakh.** It is the only idea in the set that reaches a large fraction of the dormant base cheaply.
- **One demo moment:** the judge asks to see a wallet the tool *refuses* to act on. The screen shows 22 features, none of which discriminate, and the verdict: **"No attributable cause. I will not spend your money here."**

### 48-hour build plan

| Hours | P1 — data & model | P2 — API & rules | P3 — web, demo, deliverables |
| --- | --- | --- | --- |
| **0–2** | Scaffold repo; `datagen/` skeleton; write the 5 cause families and their observable fingerprints | Repo scaffold; FastAPI skeleton with `/profile /triage /explain /refuse` stubs | Repo scaffold; wire a "judge can try this" URL; README skeleton with all §9 headings |
| **2–6** | **Generator complete**: population with heterogeneous pay cycles, ground-truth cause written to `truth/` (never imported by training), traps, held-out split | Deterministic **rule baseline** — "3 weeks silent → message everyone" — behind the same interface as the model | Triage list UI against the rule baseline. Working demo by hour 6, even though the model does not exist yet |
| **6–8** | **HOUR-6 GATE:** generator produces held-out ground truth and the calibration sanity-check passes | Rule baseline end-to-end; money calculator wired to `economics.md` U3 | Demo script v1 written against the *rule* |
| **8–12** | Model: shape features → 5-family classifier; calibration on held-out | `/explain` returns SHAP contributions, not just a label (brief §12 traceability) | Console shows decline shape + contributions |
| **12** | 🛑 **KILL SWITCH — see below** | | |
| **12–20** | Multi-seed runs; money report vs rule vs oracle; sensitivity on the 4% recovery assumption | Refusal path as a first-class API response, not an exception | Refusal screen — the money shot. Commit history continuous |
| **20–24** | ✅ **Pre-evaluation-ready.** Freeze v1. Tag release | OpenAPI docs; every response carries reasons | **README + live deploy up. Project report drafted** |
| **24–36** | Fairness check across relevant groups (brief §14); adversarial cases: what if the wallet is quiet *because* the model is wrong | Idempotent `/triage`; logging so the demo is reproducible | Video demo script and recording; requirement-drop absorber documented |
| **36–42** | Second population variant so a requirement drop is "change the population" | | |
| **42–48** | Bug fixes only; no new features | | README/report/video final; deploy; rehearse all three members |

**🛑 Hour-12 kill switch — go/no-go, decided by the pre-committed test, not by how the day felt.**
Continue **only if both** hold: (1) the classifier beats the deterministic rule on **macro-F1 over the five
cause families on held-out data**, and (2) the **money** report shows model ≥ **25% better money per
recovered wallet** than the rule. If (1) fails but (2) passes, we have mis-attributed causes and a
recoverable product → cut to two cause families and re-run. If (2) fails, the idea is a dashboard with a
budget attached (`brief` §13) → **fall back to F3**, which shares this generator's skeleton and can be
live in 12 hours.

### Judge's hardest question, and the honest answer

> *"Your entire recovery number is a 4% recovery rate on an unknown base. What stops this being a report
> generator that flatters itself?"*

**Honest answer:** "Two things, and one admission. The admission: I have no evidence for 4% in either
direction — `economics.md` says so explicitly — so the tool prints it as an assumption and shows what
happens at 1% and at 8%. The first real check is that the five causes are **distinguishable from the
observable shape**, and if they aren't, the model can't work and we find that out on day one rather than
in front of a judge. The second is the refusal: about half of what we triage, we expect to decline, and
that is the honest output of a diagnostic tool. If the number of refusals is zero, I would not trust the
model." *(Triage rate is `ASSUMED` at 35% and recovery at 4% per `economics.md` §3 #15; neither is
sourced. Do not print them as facts.)*

---

## F2 — Payroll-as-a-Product (Cycle Map)

**Track 07 Open Innovation, filed against 03/05.** The only idea in the repo where the float line and the
commission line **reinforce instead of trading off**, and the lowest break-even bar of any revenue idea.

### Official one-page logic chain

| Step | Answer |
| --- | --- |
| **1. User** | upay's B2B/payroll product team; the employer's payroll manager; the worker who is waiting for the money to last the week. |
| **2. Problem** | Payroll arrives as **one credit and drains within hours**. upay earns a single disbursement fee and holds a balance for about a day and a half that nobody plans around. Neither upay nor the employer can say *when* the money will be gone, so neither can act on it. |
| **3. Why now** | S6: electronic wages are preferred by workers, yet wages are used **almost only for cash-out**. Agrani Distribution and foodpanda riders are documented upay partners (`CONTEXT_v3.md` §10, `long-list.md` #24). B2P salary disbursement is an authorised MFS service (MFS Regs 2022). And `economics.md` §1.3 shows the agent network is under-utilised — the binding constraint is **demand timing, not float supply**. |
| **4. Solution** | **Cycle Map** — ingests a disbursement file, reconstructs the hour-by-hour wallet trajectory of the whole cohort across one pay cycle, and publishes a **constrained schedule**: the balance at each hour, and the action when it breaches. Explicitly **no liquidity guarantee** (MFS Regs 2022 Reg. 7.5(i): no loan against the Trust Fund). |
| **5. AI role** | Not a forecast that ends in a number — a **constrained trajectory solver** bounded by the trust-account balance, driven by a learned **hourly cash-out propensity** conditioned on hour-of-cycle, days-since-payday and worker type; plus a breach-point classifier (*does this cohort breach at hour 31?*). The learning is the propensity curve; the schedule is the optimisation. |
| **6. Impact + target** | **Share of payroll that never touches an agent**, and **dwell days after disbursement**. Target: dwell 1.5 → 2.5 days on a pilot cohort. Break-even is **Tk 12 crore of annual payroll, or 340 workers** — the lowest bar of any revenue idea in the set, because no agent commission is paid away. |
| **7. Data** | Synthetic payroll files. Partner *names* are documented; their *sizes* are not — so cohorts are synthetic. Ground-truth hourly trajectories in `truth/`, held-out cohorts reserved. Worker types: factory line worker, delivery rider, office clerk, migrant worker. |
| **8. Validation** | Oracle-trajectory error in hours; breach-point precision/recall; then `payroll_value × fee + balance × yield`. The rule baseline is **"everyone cashes out on payday morning"** — it misses the day-2 and day-3 residual completely, which *is* the demo. Sensitivity: strip float out and the case is a Tk 35 lakh disbursement-fee story with an assumed 0.35% fee. Say that. |
| **9. Scale** | Real data adds actual disbursement files (upay already holds them), real hourly cash-out curves, and worker-type clustering. **Employee wage data has a clean lawful basis** — Personal Data Protection Ordinance 2025 §5(3)(e), "implementation of legal rights relating to employment, labor rights or social security" — which makes this the safest data story of the five finalists. |

### Problem statement (official format)

> For an employer's payroll manager at upay, having wages arrive as a single lump that drains within hours
> causes upay to earn one disbursement fee on a balance it cannot plan around, so Tk 100 crore of annual
> payroll volume would be worth only Tk 39 lakh — under one percent of revenue — and the employer is
> never told the money has already gone.

### The three things a judge remembers

- **One sentence:** *"Payday is not one event. It is thirty-six hours, and we can tell you which hour each worker runs dry."*
- **One taka number:** **Tk 39 lakh base — but the break-even is only 340 workers**, the lowest of any revenue idea, because there is no agent commission to pay away.
- **One demo moment:** the judge drags the disbursement date forward one day. The hour-by-hour balance ribbon re-shapes; **two cohorts breach at different hours**; the tool names the hour and the breach size, then says: *"This is a forecast, not a guarantee — we will not promise your workers float."*

### 48-hour build plan

| Hours | P1 — data & model | P2 — API & rules | P3 — web, demo, deliverables |
| --- | --- | --- | --- |
| **0–2** | Scaffold; `datagen/` payroll-file generator | Scaffold; FastAPI with `/cohort /trajectory /breach /explain` | Scaffold; demo URL; README skeleton |
| **2–6** | Generator: disbursement files, worker types, hourly cash-out with a **latent per-worker-type propensity**; ground truth to `truth/` | **Deterministic baseline** — "everyone cashes out on payday morning" — behind the same interface | Cohort table + a static trajectory ribbon. Working demo at hour 6 |
| **6–8** | **HOUR-6 GATE:** held-out cohorts exist; oracle reconstruction error < 1 hour | Baseline end-to-end; breach arithmetic wired | Demo script v1 against the *rule* |
| **8–12** | Learn hourly propensity; breach-point classifier; solver bounded by trust balance | `/explain` returns the hour and the driver, not just a number | Ribbon UI driven by the real model |
| **12** | 🛑 **KILL SWITCH — below** | | |
| **12–20** | Money report; ablation — float stripped vs float included | **No-guarantee clause surfaced in every API response**; breach → recommended action | The "we will not promise float" line on screen |
| **20–24** | ✅ **Pre-evaluation-ready.** Freeze v1 | OpenAPI docs | **README + live deploy up. Report drafted** |
| **24–36** | Cohort with an Eid-shifted cycle (requirement-drop absorber) | | Video demo |
| **36–42** | Employer-side view: the same data as the payroll manager sees it | | |
| **42–48** | Bug fixes only | | README/report/video final; rehearse all three |

**🛑 Hour-12 kill switch.** This is the finalist with the **weakest AI-necessity story**, so the gate must
attack exactly that. Continue **only if** the learned hourly propensity beats the deterministic
"cash-out on payday morning" curve on **hourly trajectory error on held-out cohorts** *and* the breach
classifier materially outperforms "assume 48 hours for everyone". If the deterministic curve wins, the
idea is an optimiser with no learning in it and fails `brief` §13 → **fall back to F1**. If the propensity
wins but the breach classifier does not, keep the trajectory map and drop the breach product.

### Judge's hardest question, and the honest answer

> *"Isn't hour-by-hour wallet trajectory modelling just a simulation where you wrote the answer? What
> actually breaks when real workers show up?"*

**Honest answer:** "Partly, and I'll say which part. The solver is a simulation — that is just arithmetic
over a balance. The only learned component is **the hourly cash-out propensity curve**, and that is the
only thing that would need re-estimating on real data. We can prove it is load-bearing: we deliberately
perturb the propensity by two hours and the breach predictions move to exactly the cohorts you'd expect.
What I cannot claim is that real workers follow our curve. S6 tells us wages are used almost only for
cash-out — that gives us the **shape**, not the **timing**, and timing is the entire product. If real
timing is bimodal (all at 11am on payday, or all at 7pm after work), this collapses into a schedule, and
that is the first thing we would test in a pilot." *(Trajectory and dwell figures are `ASSUMED`; the ≈3.1%
payroll base is `UNVERIFIED`, secondary source only.)*

---

## F3 — Full-Loop Swap Engine (Substitution Desk)

**Track 02/04.** The only idea in the repo whose base case clears Tk 1 crore, and the one the brief hands
us a product spec for in plain language. This is the build `mix-shift-THESIS.md` already converged.

### Official one-page logic chain

| Step | Answer |
| --- | --- |
| **1. User** | upay's campaign budget owner (primary); the upay customer who pays a cash-out fee every time they need physical money (secondary — and the beneficiary). |
| **2. Problem** | Merchant payment is **free** to the upay customer; cash-out costs **up to 1.40%** (Tk 14/1,000, tiered in practice, current rate UNVERIFIED). So the customer's saving from switching is the whole cash-out charge — roughly **Tk 11–30 per transaction**. But upay cannot tell which customers would move on their own, so a substitution incentive pays the already-migrating and overpays the rest. |
| **3. Why now** | A **live, dated regulatory dispute.** Bangladesh Bank set the Interchange Reimbursement Fee to **zero** for Bangla QR, and upay publicly disclosed absorbing **Tk 5–8 per Tk 1,000** on cross-operator QR while demanding a cost-recovery mechanism instead of a blanket zero (Financial Express, 15 Sep 2026 — three weeks before registration closed). The brief's Track 03 names the product itself: *"How can I reduce cash-outs?"* |
| **4. Solution** | **Substitution Desk** — per customer per month, how much upay will pay to move a *specific recurring* cash-out onto a merchant QR payment; priced against the commission it will save; and **declining** customers already migrating on their own. |
| **5. AI role** | Two-part. (a) **Propensity model** (LightGBM) over features no rule can combine: cash-out frequency and ticket distribution, **distance to nearest agent** (public OSM), merchant-category spend already visible on the wallet, cash-in cadence, prior campaign exposure, area agent-float reliability. (b) **Dose-response head** predicting the **increment per bounty band**, not a yes/no — so the tool finds the efficient point and refuses overpayment. Scored against **injected ground-truth dose-response**, not against AUC. |
| **6. Impact + target** | **Bounty paid per 1,000 cash-outs displaced.** Two targets: beat the deterministic rule by **≥25% on money-per-displaced-cash-out**, and land within **11% of the oracle ceiling** at a *fixed objective* (39,800 displaced cash-outs from a 100,000-customer synthetic population). |
| **7. Data** | Synthetic, with `θ_customer` and `displaced(bounty)` written to `truth/` and never imported by training. **Four deliberate traps**, each of which a response-model or rule gets wrong: *already-migrating* (shifts with no bounty), *negative-uplift* (a bounty makes them cash out **more**), *float-inelastic* (their agent never runs out, so substitution is impossible and a naive model reads their volume as opportunity), and Eid/month-end seasonality. Calibrated to BB Oct-2025: 174.56m cash-outs at Tk 2,132 average, 142.55m cash-ins at Tk 2,898. Clean held-out set. |
| **8. Validation** | **Money, not accuracy.** Cost to hit a fixed displacement target — rule vs model vs oracle, one chart, and that chart is the demo. Framing must hold the objective fixed and let cost vary; comparing at different spend levels flatters whoever spent more. Then the **breakeven sweep**: drag the assumed agent-commission share and the breakeven moves live. Never print upay's undisclosed revenue base — value is a ratio. |
| **9. Scale** | Real upay data would add inter-FS transaction visibility (to confirm substitution did not simply move to bKash), real agent-float reliability, and real merchant-category spend. The prototype calibrates the *shape* of all three from public structure; only the *magnitudes* are missing. Modules: `datagen/` → `models/` → `pricing/` (deterministic, separately testable) → `api/` → `web/`, so a requirement drop of "change the payout policy" lands in `pricing/`, not in a prompt. |

### Problem statement (official format)

> For upay's campaign budget owner, having no way to distinguish customers who would stop cashing out on
> their own from customers who need an incentive causes substitution discounts to be paid to wallets that
> were already migrating, so the spend cannot be proven incremental and the Tk 5–8 per Tk 1,000
> cross-operator cost stays on the P&L.

### The three things a judge remembers

- **One sentence:** *"We pay people to stop cashing out — and we refuse to pay the ones who already stopped."*
- **One taka number:** **Tk 90 lakh base at 1% of cash-out value converted — the only idea in the set that clears Tk 1 crore in its base case**, because it monetises *cost* (saved agent commission + avoided IRF) rather than volume.
- **One demo moment:** the judge drags the **assumed agent-commission share** slider. The breakeven band moves live and the screen shows which side of it the assumption sits. Then one click on *price with dose-response*: target met, **46% cheaper than the rule**, with the oracle row visible proving we are 11% off the best achievable.

### 48-hour build plan

| Hours | P1 — data & model | P2 — API & rules | P3 — web, demo, deliverables |
| --- | --- | --- | --- |
| **0–2** | Scaffold; `datagen/` from `mix-shift-THESIS.md` §4 verbatim | Scaffold; `/profile /price /allocate /explain` | Scaffold; demo URL; README skeleton |
| **2–6** | Generator + ground truth + **all four traps** + held-out split; calibration check against BB Oct-2025 | **Deterministic rule** — "pay Tk 50 to everyone with ≥4 cash-outs/month and >2 km to an agent" — behind the same interface | Allocation table + rule output. Working demo at hour 6 |
| **6–8** | **HOUR-6 GATE:** held-out set exists; ground truth is genuinely unreachable from training inputs | Rule end-to-end; the pricing cap implemented as a **deterministic, separately testable** module | Demo script v1 against the *rule* |
| **8–12** | Propensity model, then dose-response head; score against injected truth | `pricing/` accept/refuse rule + **breakeven sweep** | UI shows bounty + reason per customer |
| **12** | 🛑 **KILL SWITCH — below** | | |
| **12–20** | Money chart: rule vs model vs oracle at a fixed objective | `/explain` returns the dose-response curve, not a scalar | **The breakeven slider** — the honesty artefact |
| **20–24** | ✅ **Pre-evaluation-ready.** Freeze v1 | OpenAPI docs; `pricing/` unit tests | **README + live deploy up. Report drafted** |
| **24–36** | Fairness: performance across the negative-uplift and float-inelastic segments | Refusal is a typed API response, never an exception | Video demo; refusal screens (bounty Tk 0 / refused) |
| **36–42** | Second population (a merchant-dense district) as requirement-drop absorber | | |
| **42–48** | Bug fixes only | | README/report/video final; rehearse all three |

**🛑 Hour-12 kill switch.** Two independent tests, both pre-committed in `mix-shift-THESIS.md` §7.
Continue **only if** (1) the model beats the rule by **≥25% on money-per-displaced-cash-out** at a fixed
objective, and (2) the **breakeven agent-commission share falls inside the range a published price ladder
can plausibly support**. If (1) fails, it is a dashboard with a budget attached → drop. If (1) passes and
(2) fails, the bounty is unaffordable and the thesis is dead — in that case **pivot the same generator to
F5**, since both are dose-response-on-injected-truth problems and F5's payoff does not depend on the
commission share. **Do not assume the favourable branch of the sign structure to get under the bar.**

### Judge's hardest question, and the honest answer

> *"Replacing a 1.4% cash-out with a 1% merchant fee reduces your top line. In the worst case you're
> 0.4% of ticket value worse off before any commission is counted. Why is this worth doing?"*

**Honest answer:** "On fees alone, in the best case it costs us about 0.4% of ticket value — that's real and
I won't dress it up. It pays only if the agent commission we stop paying plus the cross-operator cost we
avoid clears that gap. upay's commission share is not public, so **I cannot tell you the answer**, and
anyone who quotes you a confident number here is guessing. What the tool does instead is compute the
breakeven and show whether the plausible range clears it. If it doesn't, the honest output is *don't run
this campaign* — which is a decision our current process cannot make at all, because right now we cannot
tell an incremental campaign from a self-selecting one." *(upay's net share of merchant QR MDR is
`UNVERIFIED` and is the top sensitivity in `economics.md` §3 #6; it swings the base case by ±Tk 45 lakh.)*

---

## F4 — Cross-Operator Leak Plug (Own-Rail Router)

**Track 06/07.** The smallest taka of the five and the highest certainty per transaction — it avoids a cost
upay has **publicly disclosed** rather than winning a speculative fee. And it carries the sharpest
fairness constraint, which is the responsible-AI story.

### Official one-page logic chain

| Step | Answer |
| --- | --- |
| **1. User** | the upay customer standing at a merchant choosing who to pay; upay's payments product team. |
| **2. Problem** | upay absorbs **Tk 5–8 per Tk 1,000** on cross-operator QR — publicly disclosed on 15 Sep 2026. The obvious fix, *"show our own merchants first,"* **degrades the list for the large majority of customers who have no upay merchant within reach** (our estimate, not a sourced figure — `long-list.md` #13 puts it at 90%; nothing measures it). We have a fix that is right for a minority and harmful for everyone else. |
| **3. Why now** | The IRF was set to **zero** and upay publicly demanded a cost-recovery mechanism instead of a blanket zero — a live dispute, dated three weeks before registration closed. Meanwhile the interoperability question is open: BB launched its interoperable platform on **1 Nov 2025** without bKash (which cited security concerns) or Nagad (not approved), the Governor publicly conceded it *"did not work well for lack of participation,"* and a Gates Foundation instant-payment platform is announced for **July 2027**. The leak exists because interoperability is incomplete — which means it may close by regulation. |
| **4. Solution** | A **constrained re-ranking** of the merchant list. Own-rail preference applies only where a comparable own-rail option exists within a radius budget. Where none exists, the customer's own choice is preserved and **the tool abstains**. |
| **5. AI role** | Two estimates composed into a constrained objective, not a classifier: (a) `P(own-rail option exists within radius)` from merchant geography and OSM POI data, (b) `P(accepts own-rail when shown)` from customer behaviour. The **abstention threshold is the fairness constraint**, and it is what no threshold-based rule can express. |
| **6. Impact + target** | **Cross-operator QR value rerouted to own rails, as a share of cross-operator value**, plus **cost avoided in Tk per 1,000**. Target: rerouting **2.7%** of cross-operator QR value (≈Tk 1.5 crore) covers the build. Hard secondary target: **degradation on the no-own-rail population must be zero by construction.** |
| **7. Data** | Synthetic transactions plus OSM POI geometry for merchants and agents. The population must deliberately include a long tail of customers with **no upay merchant within any reasonable radius** — without that population the fairness claim is unfalsifiable. |
| **8. Validation** | Money: Tk per 1,000 avoided, at the sourced Tk 5–8. Fairness: the abstention rate and the measured list-change on the no-alternative cohort, which must be **exactly zero**. Rule baseline: *"always show own merchants first"* — it wins on money and fails the fairness constraint, and we report both. **The IRF-restored scenario must be in the model and on the slide**, not in a footnote. |
| **9. Scale** | Real data adds upay's actual merchant and agent locations — its own **agent cash-density map is the strongest proprietary input and we do not have it** — plus NPSB National Payment Data (BB PSD Circular No. 13, 20 Nov 2025) and live cross-operator volumes. Interoperability status is a **policy input, not a constant**, so the deployment shape is a model parameter, not a rewrite. |

### Problem statement (official format)

> For an upay customer paying a QR merchant, having no way to move a payment onto upay's own rails without
> hiding the merchants they can actually reach causes upay to absorb Tk 5–8 per Tk 1,000 on every
> cross-operator QR it does not intercept, so a fix aimed only at customers who have an own-rail option
> makes the experience worse for everyone who does not.

### The three things a judge remembers

- **One sentence:** *"We would rather lose a sale than hide a shop that isn't there."*
- **One taka number:** **Tk 18 lakh base — the smallest of the five, and self-funding by construction**, because the avoided cost *is* the incentive budget. High certainty per transaction: it avoids a disclosed cost, it does not win a speculative fee.
- **One demo moment:** the judge searches for a customer in a district with no upay merchant. The tool reports **"No own-rail option within 2 km — abstaining; the customer's list is unchanged."** Then the judge drags the IRF slider to a *restored* state and the value goes to zero, and the tool says so out loud before the judge has to ask.

### 48-hour build plan

| Hours | P1 — data & model | P2 — API & rules | P3 — web, demo, deliverables |
| --- | --- | --- | --- |
| **0–2** | Scaffold; synthetic merchant/agent/customer geography + transactions | Scaffold; `/options /route /explain /abstain` | Scaffold; demo URL; README skeleton |
| **2–6** | OSM POI fetch for one district, cached to disk; population incl. the **no-own-rail long tail** | **Deterministic baseline** — "always show own merchants first" — plus the fairness measurement harness | Merchant list UI, baseline behaviour. Working demo at hour 6 |
| **6–8** | **HOUR-6 GATE:** the no-own-rail cohort exists and is measurable; OSM cache committed with attribution | Baseline end-to-end **with the fairness metric already computed** | Demo script v1 shows baseline winning on money and failing fairness |
| **8–12** | Existence model + acceptance model + constrained re-ranker | Abstention as a first-class decision, logged | Abstention is visible in the UI as a state, not a silence |
| **12** | 🛑 **KILL SWITCH — below** | | |
| **12–20** | Money report at sourced Tk 5–8; **IRF-restored scenario** | `explain` returns why it intervened *or why it abstained* | The two demo moments above |
| **20–24** | ✅ **Pre-evaluation-ready.** Freeze v1 | OpenAPI docs | **README + live deploy up. Report drafted** |
| **24–36** | Multi-district run; robustness at 1 km / 2 km / 5 km radius | | Video demo |
| **36–42** | Add upay agent cash-density as a *proxy* density layer (documented as a proxy) | | |
| **42–48** | Bug fixes only | | README/report/video final; rehearse all three |

**🛑 Hour-12 kill switch.** Continue **only if both**: (1) the constrained router beats "always show own
merchants first" on **money per 1,000 rerouted** at equal intervention rate, and (2) **measured list
degradation on the no-own-rail cohort is exactly zero**. If (2) fails, the fairness claim is false and the
project is actively harmful → drop regardless of (1). If (1) fails while (2) holds, we have built a safe
intervention that does not pay → **fall back to F5**, whose gate machinery (uplift on injected truth) is
the same shape and whose payoff does not depend on a per-transaction saving.

**Compliance check before hour 24 (not a gate, a blocker):** OSM data is under the Open Database Licence,
which carries attribution and share-alike obligations for derived databases. Confirm the intended use
before shipping anything derived, and record the attribution string in the README either way.
**Verify this — do not assert it.** (`redteam.md` §2 #20 flagged the same item.)

### Judge's hardest question, and the honest answer

> *"Bangladesh Bank zeroed the IRF to push adoption. bKash refused interoperability and BB's Governor has
> already admitted it failed. If bKash joins, your cost disappears and so does your product. Why would
> anyone build on a subsidy that is designed to be withdrawn?"*

**Honest answer:** "The premise is right and it is the biggest risk to this project, so it is in the model
rather than around it — drag the IRF slider to a restored state and the tool reports zero value. That is
not a weakness I am hiding; it is the honest description of the business. What survives either way is the
**decision rule**, not the saving: the abstention constraint is what makes own-rail preference safe, and
that constraint is required for any future routing change, whether or not this particular leak exists.
I also want to be plain about the ranking — this is the smallest taka of the five finalists, at Tk 18
lakh. I picked it because it is the only one where the money is a cost upay has already put in public,
rather than a number I assumed." *(Merchant QR value and cross-operator share are `ASSUMED` at 5% and 25%
per `economics.md` §3 #13; the Tk 5–8/1,000 cost itself is SOURCED.)*

---

## F5 — Retention Uplift Gate

**Track 04/02.** Uplift modeling is the brief's own named sharp signal, and the refusal — *do not discount
the customer who was already loyal, and stop contacting the one you would have scared off* — is a
judge-visible product rather than a metric.

### Official one-page logic chain

| Step | Answer |
| --- | --- |
| **1. User** | upay's retention campaign owner (primary); the at-risk customer who has already been contacted three times this quarter (secondary). |
| **2. Problem** | A discount sent to a customer who was going to stay anyway is pure waste. A contact to a customer the contact would **deter** is negative value that nonetheless looks like success on response rate. Neither is visible without a control group, and upay does not run one. |
| **3. Why now** | **42.5% of users transact once or twice a month** (S12); cash-out fees are resisted and cost-sharing rules are unclear (S6/UNDP). And the brief names the technique itself: *"This customer will transact" is weaker than "this customer is likely to transact because of the offer."* Most teams will build response prediction and miss this. |
| **4. Solution** | A **gate on the retention budget**. Per customer: an estimate of whether the offer *causes* retention, a value-at-risk figure, and a decision — **fund, or refuse**. The same gate applied to outbound contact is the off-switch, so one model governs both budgets. |
| **5. AI role** | **Uplift / Qini estimation** (two-model or causal forest), explicitly *not* response prediction. A **negative-uplift segment is a first-class output**, not an error case. The deliverable is **Qini coefficient and AUUC against injected ground truth**, which is why the prototype can be scored honestly without upay data. |
| **6. Impact + target** | **Share of retention discount spend proven non-incremental. Target ≥29%** (the stated break-even). Second target: **the count of customers the model refuses to contact** — reported as a success metric, not a suppression. |
| **7. Data** | Synthetic campaigns with **treatment/control labels** — explicitly sanctioned by brief §11, which lists "campaigns/offers/treatment-control labels" among sanctioned synthetic domains. Ground-truth incremental effect written to `truth/`. Held-out campaigns reserved. Must include a negative-uplift cohort and a contact-fatigue cohort. |
| **8. Validation** | **Qini coefficient and AUUC against injected ground truth** — the headline, because it is the metric response prediction cannot fake. Then money: `value_at_risk × P(retain \| offer) − offer_cost`. Rule baseline: **"discount everyone flagged as at-risk"** — it will look excellent on response rate and will destroy value on the negative-uplift segment. Report both curves. Sensitivity: the Tk 2 crore budget is entirely assumed, so present the conservative case. |
| **9. Scale** | Real data requires a **randomised holdout**, which is the honest ask — and is itself the strongest argument for the project, because the holdout is a decision rather than a data problem. Architecture keeps the gate as a **deterministic business rule outside the model**, so a policy change lands in code, never in a prompt (brief §12). Add consent state and a do-not-contact flag per Personal Data Protection Ordinance 2025 §5 before any contact goes out. |

### Problem statement (official format)

> For upay's retention budget owner, having discounts sent without any way to know whether they *caused*
> the retention causes an estimated 35% of a Tk 2 crore discount budget to be spent on customers who would
> have stayed anyway, so Tk 1.1 crore of modelled value rests on a spend figure nobody has and on a
> contact channel that may itself be deterring the customers it targets.

### The three things a judge remembers

- **One sentence:** *"We refuse to discount the customer who was already loyal — and we stop contacting the one we would have scared off."*
- **One taka number:** **Tk 1.1 crore base at 2.5% of revenue — from a Tk 2 crore budget that is itself an assumption.** Present **Tk 20 lakh**, the conservative case, as the honest headline.
- **One demo moment:** the top row of the segment list is a customer with a **negative** estimated uplift. The contact button is greyed out and the reason reads: *"This customer's response to past contacts is negative; contacting them destroys retention. We are not sending it."* Then the judge drags the discount budget down and watches the model **stop discounting the already-loyal first**.

### 48-hour build plan

| Hours | P1 — data & model | P2 — API & rules | P3 — web, demo, deliverables |
| --- | --- | --- | --- |
| **0–2** | Scaffold; `datagen/` campaigns with treatment/control and injected ground truth | Scaffold; `/gate /allocate /explain /suppress` | Scaffold; demo URL; README skeleton |
| **2–6** | Generator: heterogeneous response types incl. **negative-uplift** and contact-fatigue cohorts; ground truth to `truth/` | **Deterministic baseline** — "discount everyone flagged at-risk" — plus the **do-not-contact** flag | Segment table + baseline allocation. Working demo at hour 6 |
| **6–8** | **HOUR-6 GATE:** held-out campaigns exist; injected truth is unreachable from campaign features | Baseline end-to-end; response-rate metric computed *alongside* money so the trap is visible | Demo script v1 shows the baseline winning on response rate |
| **8–12** | Two-model uplift estimator; Qini + AUUC; negative-uplift posterior | **Gate as a deterministic module** (fund / refuse / suppress-contact), separately unit-tested | UI shows uplift + confidence, not a response score |
| **12** | 🛑 **KILL SWITCH — below** | | |
| **12–20** | Money report; budget sweep; fairness across groups (brief §14) | `/explain` returns the uplift estimate and its drivers | The refusal/suppression screens |
| **20–24** | ✅ **Pre-evaluation-ready.** Freeze v1 | OpenAPI docs; gate unit tests | **README + live deploy up. Report drafted** |
| **24–36** | Qini curve on a second synthetic market with weaker response signal | | Video demo |
| **36–42** | Consent + do-not-contact states threaded end to end | | |
| **42–48** | Bug fixes only | | README/report/video final; rehearse all three |

**🛑 Hour-12 kill switch.** Continue **only if** (1) the uplift model recovers the **Qini coefficient**
against injected ground truth materially better than a response model on the same features, and (2) it
**identifies the negative-uplift cohort** rather than ranking those customers as the best targets. If (2)
fails, the project will actively harm customers while looking successful on response rate → drop. If the
Qini recovery is weak but the money report is positive, keep the gate as a *budget* instrument and drop
the causal claim from the deck entirely — do not present uplift you cannot demonstrate.

### Judge's hardest question, and the honest answer

> *"Your entire uplift estimate depends on a randomised control group that upay doesn't run. Without one,
> this is response prediction with a confident label."*

**Honest answer:** "Without a holdout, yes — and I'd be misleading you if I said otherwise. What I can show
today is that the *method* is correct on data where I injected the truth: the Qini curve recovers the
increment rather than the response, and it surfaces the negative-uplift segment that a response model
would have ranked as our best target. The real requirement isn't data, it's a decision — upay has to agree
to hold out some customers and some contacts for a period. That is a business decision, not a technical
one, and it is the only thing standing between this prototype and a real answer. The second thing I would
say is that the refusal is worth building even if the uplift number never gets validated, because right
now we have no mechanism at all for noticing that a campaign is doing harm." *(The Tk 2 crore retention
budget, the 35% non-incremental share and the 29% break-even are all `ASSUMED` per `economics.md` §3 #12.)*

---

## 6. Cross-cutting notes for all five

1. **One hour, reused everywhere: the consent and compliance block.** Personal Data Protection Ordinance
   2025 puts the **burden of proof on the controller** (§5). One README section and one screen covering
   lawful basis, consent surface, do-not-contact, and which BB instrument each decision touches answers the
   5% Responsible AI and 5% Security criteria together. It is the cheapest differentiation available,
   because our competitors' decks will not have it.
2. **Charge display.** MFS Regs 2022 §9.0 requires prominent display of charges at retail agent outlets.
   Any bounty, discount or fee shown in a prototype should say where a customer would see it displayed.
3. **Never print upay's undisclosed revenue base.** Value is stated as a rate, a ratio or a count.
4. **Every finalist has a pre-committed kill switch at hour 12 and a named fallback** — F1→F3, F2→F1,
   F3→F5, F4→F5, F5→(drop). That is deliberate: the fallback is chosen so it reuses the generator or the
   gate machinery already built, so switching costs hours, not days.
5. **The generator is the shared asset.** All five build `datagen/` first with ground truth in a file
   training never imports. That is the single decision that makes the hour-12 fallbacks cheap and makes the
   on-site requirement drop absorbable.
6. **One unresolved item, `CONTEXT_v3.md` §0.** None of these five touches fraud, scam, ATO or mule. If
   the team decides Track 01 is in scope after all, this list does not change — but the compliance load
   shifts to BFIU/AML obligations and the responsible-AI section has to be rebuilt.
