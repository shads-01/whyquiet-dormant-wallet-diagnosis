# Finalists, second five — the rest of the survivors of `redteam.md`

> Written 3 Oct 2026. **Second half of the ten ideas that survived `redteam.md` §2.** Same scaffolding as
> `finalists.md` — the guideline PDF §10 nine-step logic chain, the §10 problem-statement format
> (*"For [specific user], [specific problem] causes [measurable consequence]"*), the three judge
> artefacts, the 48-hour plan with a pre-committed hour-12 kill switch, and one hostile Q&A.
>
> **Read this before the build plans.** These five are the *lower-ranked* half. Three consequences, stated
> plainly rather than buried:
>
> 1. **F6 (#5) is redundant with F2 (#24).** Both are payroll-domiciled; F2 has strictly better
>    economics (lowest break-even bar of any revenue idea in the repo). If you build one, build F2.
> 2. **F7, F9 and F10 all have negative or near-zero base cases** in `economics.md` §3. They are not
>    here because they are good. They are here because they are the only remaining ways to reach the
>    merchant line, and the merchant line is where the mix is heading.
> 3. **F8's whole case is a binary** — whether over-billing exists at all. The honest demo may be *"we
>    found none."* That is a good responsible-AI artefact and a weak business case, in that order.
>
> If you are choosing one idea to build, go to `finalists.md`. This file exists so that the choice was
> made against all ten survivors rather than against the five we liked first.

---

## Scoreboard against the first five

| Rank | Idea | Rel | Biz | Orig | Total | First-five rank |
| --- | --- | --- | --- | --- | --- | --- |
| **F6** | #5 Sponsor Payroll Market | 4 | 3 | 4 | **11** | — |
| **F7** | #8 Incremental Offer Fund | 3 | 3 | 4 | **10** | — |
| **F8** | #11 Wallet-Tier & Take-Rate Leakage | 4 | 3 | 4 | **11** | — |
| **F9** | #20 Acceptance-Gap Sniper | 4 | 2 | 4 | **10** | — |
| **F10** | #25 Campus Closed Loop | 5 | 2 | 3 | **10** | — |

For reference, the first five were #15 (15), #24 (14), #6 (13), #13 (12), #12 (12). The gap from 12 to 11
is the gap between a shortlist and a longlist.

---

## F6 — Sponsor Payroll Market

**Track 02/04.** The only idea in the whole repo where a **third party pays the acquisition cost**. That is
a structural fact, not a number, and it is why this idea survives a year-one loss.

### Official one-page logic chain

| Step | Answer |
| --- | --- |
| **1. User** | upay's campaign budget owner; the **employer's HR or payroll manager** (the actual buyer and the funder); the dormant worker whose wallet is reactivated by a funded bounty. |
| **2. Problem** | upay's dormant base is large and cheap to reach in theory, but at **Tk 89 ARPU** self-funded acquisition cannot clear a bounty — `economics.md` §3 #14 showed the bounty must stay below **Tk 44**, a token gesture. So upay cannot buy these customers. **The employer already has them, already knows who they are, and has a budget for exactly this.** |
| **3. Why now** | S6: electronic wages are preferred by workers, yet wages are used **almost only for cash-out**. Agrani Distribution and foodpanda riders are documented upay partners (`CONTEXT_v3.md` §10). Dormancy is severe nationally — **37.6% of 237m registered MFS accounts were active** at Dec 2024 (S1). Nobody has solved the who-pays problem for dormancy. |
| **4. Solution** | A **marketplace**, not a campaign. upay offers employers a ranked recovery service on *their own* payroll file; the employer funds a bounty per verified activation out of its own acquisition budget, not upay's marketing budget. upay is paid a servicing fee and earns the ongoing transactions. |
| **5. AI role** | Two parts. (a) A **90-day-out compound label** — activates *and* transacts ≥4×/month for 3 months — which is **unobservable at decision time**, which is the entire reason this is a model rather than a filter. (b) A **changepoint classifier** that separates *job exit* from *merely quiet*, so the bounty is never paid for someone who has left the company and cannot be recovered. |
| **6. Impact + target** | **Dormant wallets recovered per employer per year**, target **≥45 at base** — but the number that matters is **break-even: 60 employers in year one**, or 4,400 recovered wallets to clear year-two servicing costs. Secondary: year-2 margin per recovered cohort. |
| **7. Data** | Synthetic employer payroll files plus wallet behaviour. Deliberately include: employees who changed jobs within the employer (changepoint positives), seasonal absent workers, and mass-layoff cohorts. Ground truth to `truth/`, held-out employers reserved — **hold out whole employers**, not random employees, or you leak. |
| **8. Validation** | (a) Changepoint classifier vs the rule baseline **"any wallet quiet for 90 days"** — macro-F1 on held-out employers, with the cost metric being *bounties paid to unrecoverable exits*. (b) Money on upay's own P&L: `recovered × ARPU × ramp − recoveries × servicing cost`. (c) **Year 1 and year 2 reported separately, and both reported.** A year-one loss with a stated path to year two is honest; a year-one loss presented as a year-two win is not. |
| **9. Scale** | Real data adds real payroll files (upay already processes them), real employer churn, and real job-exit labels from eKYC. Module seams: the changepoint model and the bounty policy are separate, so a requirement drop of "change the bounty structure" lands in the policy module. **Employee wage data has a clean lawful basis** — Personal Data Protection Ordinance 2025 §5(3)(e), employment/labour rights — because the employer is the controller for its own payroll file. |

### Problem statement (official format)

> For upay's campaign budget owner, having a dormant base it cannot afford to re-acquire at an ARPU of Tk 89
> per year causes every self-funded activation incentive to be unpayable, so 3.63 million dormant wallets
> stay unreachable even though the employer who employs those same people already knows who they are and
> has a budget to reach them.

### The three things a judge remembers

- **One sentence:** *"We cannot afford to win these customers. The employer can — and they pay."*
- **One taka number:** **Year 1 −Tk 16 lakh, year 2 +Tk 10 lakh** — with the honest footnote that the **aggressive** case is *lower* than base (+Tk 7 lakh vs +Tk 10 lakh), because servicing cost scales with the cohort while the revenue does not. That inversion is the most interesting number in the set.
- **One demo moment:** the judge opens an employer cohort and the tool separates the wallets into **"recoverable — bounty recommended"**, **"job exit — do not pay, this person left the company"**, and **"seasonal — hold"**. Then it shows the employer's cost per *paying* recovery against the naive cost per *attempted* recovery.

### 48-hour build plan

| Hours | P1 — data & model | P2 — API & rules | P3 — web, demo, deliverables |
| --- | --- | --- | --- |
| **0–2** | Scaffold; `datagen/` employer payroll + wallet files | Scaffold; `/cohort /price /activate /explain` | Scaffold; demo URL; README skeleton |
| **2–4** | ⚡ **GATE 0, business not technical:** write the one-page question to a real employer contact — *does your payroll file contain upay wallets that are dormant?* A non-answer is a kill before hour 12 | **Deterministic baseline** — "every 90-day-quiet wallet in the file gets the bounty" — behind the same interface | Cohort table + baseline output. Working demo at hour 4 |
| **4–8** | Changepoint classifier; 90-day-out compound label; **employer-level** held-out split | Bounty policy as a deterministic module; employer-funded accounting (bounty is *their* cost, shown separately) | Employer view and upay view side by side |
| **8–12** | Cost-weighted scoring (bounties paid to unrecoverable exits) | `/explain` returns the changepoint evidence, not just a class | "Do not pay" rows are visible, not hidden |
| **12** | 🛑 **KILL SWITCH — below** | | |
| **12–20** | Year-1 and year-2 P&L reported as two separate columns | Employer self-serve view (the buyer sees their own money) | The two-year P&L with the aggressive-case inversion shown |
| **20–24** | ✅ **Pre-evaluation-ready.** Freeze v1 | OpenAPI docs | **README + live deploy up. Report drafted** |
| **24–36** | Employer-type variant (factory vs platform vs delivery) | | Video demo |
| **36–42** | Bounty-price sensitivity sweep | | |
| **42–48** | Bug fixes only | | README/report/video final; rehearse all three |

**🛑 Hour-12 kill switch — two gates, and gate 0 may already have ended this.**
**Gate 0 (hours 0–4, business):** at least one plausible employer path exists. If nobody will even test
the premise, stop here — this idea is a sales motion before it is a model.
**Gate 1 (hour 12, AI vs rule):** continue **only if** the changepoint classifier beats "90 days quiet"
on **bounties paid to unrecoverable job exits**, at equal recovery count. If the classifier does not
reduce wasted bounties, the model is decoration and the whole who-pays thesis collapses into "send a
bounty" → **fall back to F7**, which reuses the same uplift machinery and has a cleaner falsifiable claim.

### Judge's hardest question, and the honest answer

> *"Your year one is negative and your aggressive case is worse than your base case. That's a business that
> gets worse as it succeeds. Why is this a product at all?"*

**Honest answer:** "It does get worse as it succeeds, and I'd rather show you that than hide it — the
reason is that servicing cost scales with the cohort while the revenue per user doesn't, and upay's ARPU
is Tk 89 against bKash's Tk 1,397. At that ARPU the ceiling is structural. What survives the ceiling is
the **who-pays flip**: the bounty is the employer's money, so upay's only spend is servicing, and the
breakeven is 60 employers. I'm not claiming this makes upay's P&L. I'm claiming it's the only mechanism on
the list where upay's acquisition cost is someone else's budget line — and that's the thing worth
piloting, because at our ARPU no self-funded version can work." *(All employer counts, workers per employer,
recoveries per employer and servicing costs are `ASSUMED`. The partner names are SOURCED; their sizes are not.)*

---

## F7 — Incremental Offer Fund

**Track 04 Growth & Campaign Intelligence.** The technique is the brief's own named sharp signal. The
*mechanism* — merchants co-funding customer offers — has no evidence behind it at all, and the prototype's
real job is to try to kill it.

### Official one-page logic chain

| Step | Answer |
| --- | --- |
| **1. User** | upay's campaign budget owner; the **merchant** who would part-fund a customer discount; the customer receiving the offer. |
| **2. Problem** | upay runs offer campaigns and **cannot tell whether any of them caused a transaction**. The discount is paid from upay's commercial-expense line, so an offer to a customer who would have transacted anyway is invisible waste — and the brief's own critique applies: *"This customer will transact" is weaker than "this customer is likely to transact because of the offer."* |
| **3. Why now** | Uplift modeling is **named in the official brief** as the sharp ML signal, and most teams will build response prediction and miss it. bKash's FY2024 commercial expense was **Tk 3.99bn** [SOURCED] — the category is large enough that even a small efficiency gain matters, and large enough that mismeasurement has been expensive for years. |
| **4. Solution** | A fund that pays discounts **only where the offer is proven incremental**, and moves the co-funding onto the **merchant** rather than upay: a merchant benefits from the transaction, so a share of the discount belongs to them. Offers to customers who would transact anyway are declined. |
| **5. AI role** | **Uplift / Qini estimation** on treatment-control labelled campaigns — explicitly not response prediction. Two outputs matter: the **incremental** set to fund, and the **negative-uplift** set to refuse. The deliverable is **Qini and AUUC against injected ground truth**, which is what makes it scorable without upay data. |
| **6. Impact + target** | **Share of the offer budget provably non-incremental. Target ≥12%** for the build to pay for itself (`economics.md` §3 #8 break-even), against an assumed 30% base. Secondary: incremental cash-outs unlocked, target ~18,000. |
| **7. Data** | Synthetic campaigns with treatment-control labels — sanctioned explicitly by brief §11. Inject: an **always-takers** segment (responds regardless), a **never-takers** segment, a **negative-uplift** segment (the offer makes them transact less), and a merchant-co-funding response distribution that includes a **majority of merchants who refuse**. Ground truth to `truth/`; held-out campaigns reserved. |
| **8. Validation** | Qini coefficient and AUUC against injected truth — the headline. Then money: `budget × non_incremental% × merchant_share + incremental_txns × U1 − build`. Rule baseline: **"offer to the top decile by response propensity"** — it will look excellent on redemptions and fund a segment whose incremental lift is near zero. Report both. Sensitivity: the conservative case is **negative**, so the conservative case is the headline. |
| **9. Scale** | Real data requires a randomised holdout across campaigns — the same honest ask as the first five's F5, and the same point: **it is a decision, not a data problem.** Architecture keeps the fund allocation as a deterministic module outside the model, so a policy change lands in code. Add the consent and do-not-contact surface before any offer goes to a named customer. |

### Problem statement (official format)

> For upay's campaign budget owner, having offers sent without any way to know whether they caused the
> transaction causes an estimated 30% of the discount budget to be spent on customers who were going to
> transact regardless, so the commercial-expense line cannot be justified incrementally and the merchant,
> who actually benefits from the transaction, contributes nothing to it.

### The three things a judge remembers

- **One sentence:** *"We only pay for the transaction the offer actually caused — and we ask the shopkeeper to fund it, because it's their sale."*
- **One taka number:** **Tk 47 lakh base, and the conservative case is −Tk 50 lakh.** Say both, in that order, on the slide. Never print **Tk 5 crore** as upay's budget — it is an assumption, and bKash's Tk 3.99bn is the only sourced figure in the neighbourhood.
- **One demo moment:** the judge opens a merchant co-funding simulation and sets merchant cooperation to **0%**. The tool does not break — it **reports that the mechanism is gone** and falls back to "discount funded by upay only, which halves the case to Tk 48 lakh at best." Then it asks the real question out loud: *we do not know whether upay merchants will co-fund. This prototype is designed to find out.*

### 48-hour build plan

| Hours | P1 — data & model | P2 — API & rules | P3 — web, demo, deliverables |
| --- | --- | --- | --- |
| **0–2** | Scaffold; `datagen/` campaigns with treatment/control and injected lift | Scaffold; `/uplift /allocate /merchant-fund /explain` | Scaffold; demo URL; README skeleton |
| **2–6** | Generator incl. always-takers, never-takers, **negative-uplift**, and a **merchant-refusal-majority** distribution | **Deterministic baseline** — "offer to the top decile by response propensity" | Allocation table + baseline. Working demo at hour 6 |
| **6–8** | **HOUR-6 GATE:** held-out campaigns exist; injected lift unreachable from campaign features | Baseline end-to-end; redemption metric computed *alongside* money | Demo script v1 shows baseline winning on redemptions |
| **8–12** | Two-model uplift estimator; Qini + AUUC; merchant co-funding response model | Fund allocation as a deterministic module, unit-tested | UI shows uplift + funding split, not a redemption score |
| **12** | 🛑 **KILL SWITCH — below** | | |
| **12–20** | Money report at merchant-share 0% / 25% / 50% | `/explain` returns lift and drivers; zero-cooperation path is a first-class response | The 0% co-operation demo moment |
| **20–24** | ✅ **Pre-evaluation-ready.** Freeze v1 | OpenAPI docs | **README + live deploy up. Report drafted** |
| **24–36** | Second synthetic market with weak response signal | | Video demo |
| **36–42** | Conservative-case-first reporting wired through every view | | |
| **42–48** | Bug fixes only | | README/report/video final; rehearse all three |

**🛑 Hour-12 kill switch.** Continue **only if** (1) the uplift model recovers the **Qini coefficient**
against injected truth materially better than the propensity-decile baseline, and (2) it identifies the
**negative-uplift** segment instead of ranking it as a top target. If (2) fails, the fund would actively
damage customers while showing rising redemptions → drop. If Qini recovery is weak but the money report is
positive, ship it as a **budget-hygiene** tool and delete the causal claim from the deck. **Do not present
merchant co-funding as a mechanism. Present it as the hypothesis the prototype exists to falsify** — that
framing is both more honest and more persuasive than a fake success.

### Judge's hardest question, and the honest answer

> *"Merchant co-funding has literally zero evidence anywhere in your own documents. You invented it. You
> are building a product on an assumption you made up."*

**Honest answer:** "Yes, and that is stated in my own economics file: the merchant co-funding share is
`ASSUMED` with *no evidence at all* that upay merchants will co-fund. I did not invent it to be lazy — I
invented it because it is the only way the discount moves off upay's commercial line, and that is the
mechanism the brief's uplift framing is pointing at. But I have deliberately built the prototype so it can
**fail**: set merchant cooperation to zero and the tool reports the mechanism is gone and the case halves.
So the honest pitch is that the uplift model is the deliverable and the co-funding is the hypothesis. If
the pilot says merchants won't co-fund, I have still built the thing that proves which offers were
incremental — and that is worth more than the co-funding ever was." *(Offer budget Tk 5 crore, the 30%
non-incremental share, the 25% merchant share and the 18,000 incremental cash-outs are all `ASSUMED`.
Only bKash's FY2024 commercial expense of Tk 3.99bn is SOURCED.)*

---

## F8 — Wallet-Tier & Take-Rate Leakage, repositioned as a compliance self-audit

**Track 02/06.** Red-teaming made this idea **stronger**, not weaker: it is no longer a revenue-recovery
tool, it is a **regulator-facing self-audit** that runs before Bangladesh Bank runs it for them.

### Official one-page logic chain

| Step | Answer |
| --- | --- |
| **1. User** | upay's finance/compliance function; the **retail agent** who must display the correct rate to the customer; the customer billed at the wrong tier. |
| **2. Problem** | upay's cash-out schedule is **tiered in practice** — the CEO has described rates as *"less than Tk 14 … in different layers and in cases free of cost"* [SOURCED, 2021] — and some wallet tiers are free. Every transaction must be billed at the right tier for the right wallet. Nothing checks that systematically. |
| **3. Why now** | **Bangladesh MFS Regulations 2022, §9.0 *Schedule of Charges*** requires MFS providers to set rates in a "competitive, non-collusive" manner, to keep BB's Payment Systems Department "fully apprised of **all rate settings and rate revisions**", and to "ensure **prominent display of the rates of charges in all their retail agent outlets**". That is a live, named obligation on exactly the thing this tool checks. |
| **4. Solution** | A **continuous self-audit**, not a remediation project. Every transaction is re-derived from the posted schedule and the wallet's actual tier and compared to what was billed. The output is a dated attestation: how many transactions were checked, how many diverged, by how much, and what was done about each. |
| **5. AI role** | A **joint tier assignment** over three things a threshold cannot combine: the wallet's **provenance** (salary / remittance / disbursement, which is what determines eligibility for the free or reduced tiers and is visible in upay's own wallet inflow display), **float yield behaviour** (a wallet whose balance behaves like a float account is being treated as one), and **churn probability**. A rule picks one field and gets the tier wrong on mixed wallets. |
| **6. Impact + target** | **Transactions billed above the correct tier, as a share of transactions checked. Break-even is 0.21%** — but the honest metric is not the taka. It is **coverage**: share of cash-out transactions re-derived every day, target **100%**, and the count of divergences found, reported whether it is zero or large. |
| **7. Data** | Synthetic wallets with **mixed provenance** — salary, remittance, disbursement, mixed, none — each assigned a correct tier and a billed tier with an injected error rate. Ground-truth correct tier to `truth/`. The **zero-error population must be present and large**, because a prototype that only ever finds leakage teaches the model nothing about the benign case. Held-out split. |
| **8. Validation** | **Precision on the flagged set, measured against the injected truth** — an audit that flags correct bills is worse than no audit, because it destroys trust in the rate card. Then money: `cash_out_revenue × billed_over_tier% × recoverable − audit_cost`. Rule baseline: **reconcile invoices against the published rate card** — a spreadsheet, and a genuinely strong rival that a judge will propose. The model must beat it on **mixed-provenance wallets specifically**, not overall. |
| **9. Scale** | Real data adds the actual rate-card version history and the actual provenance tags — both of which upay holds and we do not, and both of which are the entire difficulty. Architecture: the rate card is a **data-prep input, not code**, so a rate revision (which BB must be notified of anyway) is a data drop. **Compliance-first framing:** this is the one idea in the repo where the deliverable is a document an auditor would accept. |

### Problem statement (official format)

> For upay's compliance function, having a tiered cash-out schedule that varies by wallet type with no
> systematic re-derivation of what each transaction should have been billed causes any billing divergence
> to be found only by chance, so upay cannot tell its PSD that its rates are applied as published, and a
> customer billed above the posted tier has no way to know.

### The three things a judge remembers

- **One sentence:** *"Bangladesh Bank requires the rate to be displayed at every agent outlet. This is the tool that proves we display the right one."*
- **One taka number:** **Tk 1 lakh base** — and the interesting part is that the **aggressive case is Tk 2.0 crore while the base is roughly zero**, because the entire case rests on whether over-billing exists at all. If it does not, the tool's value is the attestation, not the recovery.
- **One demo moment:** the judge opens a **mixed-provenance** wallet — a salary wallet that also receives remittances. The rate-card reconciliation clears it. The model does not, and shows which field drove the assignment. Then the judge asks **"what if you're wrong?"** and the tool shows its own precision on the injected truth, including the false-positive rate, before it will flag a single real transaction.

### 48-hour build plan

| Hours | P1 — data & model | P2 — API & rules | P3 — web, demo, deliverables |
| --- | --- | --- | --- |
| **0–2** | Scaffold; `datagen/` wallets with provenance, correct tier, billed tier, injected error rate | Scaffold; `/reconcile /explain /attest` | Scaffold; demo URL; README skeleton |
| **2–6** | Generator incl. a **large zero-error population** and mixed-provenance wallets | **Strong deterministic rival** — reconcile against the published rate card — as the default path | Wallet screen + rate-card reconciliation. Working demo at hour 6 |
| **6–8** | **HOUR-6 GATE:** held-out split exists; error rate is a parameter so 0% is one run | Rate card loaded as **data**, versioned, not hard-coded | Demo script v1 shows the spreadsheet catching most of it |
| **8–12** | Joint tier model over provenance + float behaviour + churn | `/attest` endpoint producing a **dated coverage statement** | UI shows the mixed-provenance disagreement |
| **12** | 🛑 **KILL SWITCH — below** | | |
| **12–20** | Precision / false-positive rate on injected truth; money at error rates 0.1% / 0.3% / 0.8% | Attestation PDF/JSON export | The "show me your false-positive rate" screen |
| **20–24** | ✅ **Pre-evaluation-ready.** Freeze v1 | OpenAPI docs | **README + live deploy up. Report drafted** |
| **24–36** | Rate-revision history as a time series (a revision drop-in demo) | | Video demo |
| **36–42** | Agent-outlet display compliance view | | |
| **42–48** | Bug fixes only | | README/report/video final; rehearse all three |

**🛑 Hour-12 kill switch — the unusual one, because the honest result may be "nothing found."**
Two gates. **Gate A (precision):** the model's precision on flagged transactions must be high enough that
an auditor would accept the flag list. An audit that cries wolf is worse than no audit. **Gate B (the
business gate):** the prototype must demonstrate that **coverage and attestation have value independent of
finding leakage** — because if the injected truth is clean and the tool reports clean, the business case
is zero. Concretely: the hour-12 report must show the tool correctly processing **100% of transactions
daily at near-zero false-positive rate**, and that must be presentable as the deliverable.
If Gate A fails, tighten the model or stop — a low-precision audit does not ship.
If Gate B fails, this idea has no business case and should be presented, if at all, **as a responsible-AI
exercise, not as a commercial product.** Do not manufacture leakage to make the demo look good; the brief
bans accuracy-score-as-the-product and a fabricated finding is worse.

### Judge's hardest question, and the honest answer

> *"What if you find nothing? Then you have built an expensive spreadsheet and the business case is zero."*

**Honest answer:** "Then the business case is zero, and I will say that on the slide rather than hope
nobody asks. What we would have is a **dated, reproducible attestation** — every cash-out transaction
re-derived from the posted schedule, zero divergences above tolerance — which is precisely the thing
MFS Regs 9.0 obliges upay to be able to tell its Payment Systems Department. That has real value and it is
not measurable in taka. And the tool is the reusable instrument: it is the same reconciliation re-run
after every rate revision, which BB requires upay to notify anyway. I would rather ship an audit that
returns a clean result than invent a leak to justify it — a fabricated finding would be the worst thing in
this entire document." *(The 0.3% over-tier rate, the 60% recoverable fraction and the Tk 20 lakh audit cost
are all `ASSUMED`. What is SOURCED is that tiers exist and vary, per the CEO's 2021 description — which
proves nothing about whether they are applied correctly.)*

---

## F9 — Acceptance-Gap Sniper

**Track 05 Merchant & Agent Intelligence.** Negative year one, thin steady state — and red-teaming found
the argument that rescues it: **merchant acquisition is a mandated control, not an optimisation.**

### Official one-page logic chain

| Step | Answer |
| --- | --- |
| **1. User** | upay's **field acquisition team** (the user, and the one paying the field cost); the merchant being approached; the district officer deciding where the quarter's effort goes. |
| **2. Problem** | Field acquisition is commissioned per **raw signup quota**, so a field officer is paid the same for a shop in a dense market as for one on an empty arterial road. upay has **14,519 merchants** [SOURCED, FY2023] and pays to add more, without knowing which additions will ever transact. |
| **3. Why now** | **Bangladesh Bank's *Guidelines for Merchant Acquiring and Escrow Services, 2023* (PSD Circular No. 10, 26 Sep 2023)** apply to banks, MFS, PSPs and PSOs and require merchant **onboarding policies, documentation, document verification, risk assessment, risk management, refunds, merchant activity monitoring, and dispute resolution**. Merchant acquisition is therefore a **compliance-required control with a documented process**, and upay's field budget is being spent on it today without measuring yield. |
| **4. Solution** | Rank **prospects** — not locations — by predicted first-year net yield, and stop paying commission on raw quota. A field officer's day is allocated to the prospects most likely to become live terminals, and the commission follows **verified activation**, not form-signing. |
| **5. AI role** | **Continuous-surface placement.** Addressable cash turnover varies smoothly across a city, so two shops 50 m apart can differ five-fold in what they could plausibly turn over, and **no grid-cell threshold survives the geometry**. The model scores a point (lat/long, category, surrounding footfall proxies from OSM) for predicted QR value, subject to the mandated risk-assessment gate. |
| **6. Impact + target** | **Verified-live merchants per field visit, and year-2 net MDR per merchant acquired.** Break-even is **667 merchants per year**, or a **field cost below Tk 12,000 at 1,200 merchants**. Report year 1 and year 2 separately — year 1 is **negative at base (−Tk 23 lakh)**. |
| **7. Data** | Synthetic merchants with categories, locations, footfall proxies and a first-year activation hazard. Deliberately include: **the same shop category with a 5× spread in addressable turnover at identical density**, so a cell-threshold baseline visibly fails. Ground truth first-year QR value to `truth/`. Held-out city split — hold out a whole city, not random shops. |
| **8. Validation** | Net MDR per field visit at **equal visit count** for model vs the cell-threshold baseline. Then the money: `merchants × (QR value × MDR × net share − field cost)`, at net shares 30% / 50% / 70%. Rule baseline: **"send the team to the top-N grid cells by existing merchant density"** — which is what a district officer does today and which the geometry defeats. |
| **9. Scale** | Real data adds upay's **own agent cash-density map**, which is the strongest proprietary input available and which we do not have — it is the honest reason a pilot matters. Architecture: the **mandated risk-assessment gate is a deterministic module in front of the model**, never inside it (brief §12), so compliance never depends on a prediction. |

### Problem statement (official format)

> For upay's field acquisition team, having commission paid per raw signup quota causes a district officer
> to earn the same for a shop that will never transact as for one that will, so 1,200 merchants a year
> carry a field cost above the net MDR at every conservative setting and upay cannot tell which
> acquisitions were worth making.

### The three things a judge remembers

- **One sentence:** *"Stop paying for signatures. Start paying for shops that are still alive in year two."*
- **One taka number:** **Year 1 −Tk 23 lakh, year 2 +Tk 48 lakh** — and the honest detail is that **field cost of Tk 8,000 sits above the Tk 12,000 net MDR line at conservative net shares**, so the payback depends entirely on upay's net share of MDR, which is `UNVERIFIED`.
- **One demo moment:** the judge picks two shops on the map, **50 metres apart, same category**. The tool shows a 5× difference in predicted addressable cash turnover and says why. Then the judge asks what happens if a merchant fails the mandated risk assessment — and the answer is that **the model is never consulted**, because the compliance gate sits in front of it.

### 48-hour build plan

| Hours | P1 — data & model | P2 — API & rules | P3 — web, demo, deliverables |
| --- | --- | --- | --- |
| **0–2** | Scaffold; `datagen/` merchants + OSM fetch for one city, cached with attribution | Scaffold; `/rank /visit /activate /explain` | Scaffold; demo URL; README skeleton |
| **2–6** | Synthetic merchants incl. the **5×-at-50 m** construction; **city-level** held-out split | **Deterministic baseline** — "top-N grid cells by merchant density" | City map with scored prospects. Working demo at hour 6 |
| **6–8** | **HOUR-6 GATE:** held-out city exists; OSM cache committed **with licence attribution** | Baseline end-to-end at equal visit count | Demo script v1 shows the grid baseline failing |
| **8–12** | Yield surface model; activation-hazard head | **Mandated risk-assessment gate in front of the model**, deterministic and unit-tested | Map + 50 m comparison view |
| **12** | 🛑 **KILL SWITCH — below** | | |
| **12–20** | Money at net shares 30/50/70; year-1 and year-2 columns | Commission on **verified activation**, not signup | The "gate runs first" screen |
| **20–24** | ✅ **Pre-evaluation-ready.** Freeze v1 | OpenAPI docs | **README + live deploy up. Report drafted** |
| **24–36** | Second city; agent cash-density as a **documented proxy layer** | | Video demo |
| **36–42** | Merchant activity monitoring view (also an R11 control) | | |
| **42–48** | Bug fixes only | | README/report/video final; rehearse all three |

**🛑 Hour-12 kill switch.** Continue **only if** the yield-surface model beats the grid-cell baseline on
**net MDR per field visit at equal visit count**, on a **held-out city**. If the grid baseline wins, the
geometry claim is wrong and the idea collapses to a density map. Note the second gate is a blocker, not a
score: **OSM data is under the Open Database Licence, which carries attribution and share-alike obligations
for derived databases.** Confirm intended use and record the attribution string before hour 24. **Verify
this — do not assert it.**

### Judge's hardest question, and the honest answer

> *"Your field cost per merchant is higher than your net merchant fee at every conservative setting. Nothing
> here is profitable. Why is it worth building?"*

**Honest answer:** "In year one, and at conservative settings, it isn't — I'll show you −Tk 23 lakh rather
than hide it. Two things make it worth building anyway, and neither is the payback. First, **Bangladesh
Bank's 2023 merchant-acquiring guidelines make merchant onboarding, risk assessment and activity monitoring
a mandatory control** — so upay is already spending this money on a compliance-required function and can
only choose to spend it badly or well. Second, merchant QR is where the mix is heading, and this is the
only tool in the set that touches it. The honest framing is compliance-first and ROI-second, and I would
rather present a negative year one with a mandated control behind it than a positive year one built on a
number I invented." *(Merchants per year, field cost per merchant, QR value per merchant and net MDR share
are all `ASSUMED`; the 14,519 merchant count is SOURCED.)*

---

## F10 — Campus Closed Loop

**Track 03/05.** Highest relevance available in the repo — **DIU hosts this hackathon and sits inside the
same Daffodil Group that upay signed an education MoU with** — and the weakest base case on the list
(negative). It is here because relevance is 20% of the rubric and a credibility asset cannot be bought
with taka.

### Official one-page logic chain

| Step | Answer |
| --- | --- |
| **1. User** | upay's campus partnerships team; the **campus merchant** whose terminal is about to go dark; the university's finance office. The student is a beneficiary, never the data subject — see step 5. |
| **2. Problem** | A dead QR terminal is **pure cost**: a merchant installed it, paid for the device and the MDR flow, and now earns nothing. The naive liveness rule is *"no transactions for N days = dead."* On a campus that rule is wrong constantly — **a canteen quiet for 11 days is dying, a bookshop quiet for 11 days is on break.** |
| **3. Why now** | upay signed a strategic MoU with the **Daffodil Group** to advance digital payments across the education ecosystem, and a separate agreement with **UCSI University** covering campus-wide QR merchant payments, tuition fees, scholarships and an RFID smart student ID. The host institution of this hackathon, **DIU, sits inside that same group.** Merchant activity monitoring is also a mandated control under BB's 2023 merchant-acquiring guidelines. |
| **4. Solution** | A **merchant liveness monitor** scoped to campus terminals, with a category-conditioned model that separates **seasonal closure** from **real decline** from **category-driven demand shift**, and a three-way action: *intervene / schedule a check-in / leave alone*. **The refusal — leave a healthy-but-on-break terminal alone — is the product.** |
| **5. AI role** | **Category-conditioned liveness decomposition.** Liveness is not one signal; it is demand shape relative to what that category's own calendar predicts (exam weeks, semester breaks, Ramadan, exam-result day). Model the *residual* against the category's expected curve, not against zero. **Hard constraint: merchant-side data only.** No student-level model, no student-level targeting, no campus-wide spend profile — see the compliance note below. |
| **6. Impact + target** | **Merchants with >30 days of activity, out of 14,519** [SOURCED] — the one merchant metric that matters at this scale. Target: **terminals saved from going dark per campus, base 8**; break-even is **2.3 campuses live**. Report as a count of terminals kept alive, never as a taka total. |
| **7. Data** | Synthetic campus merchants with **category-specific calendars**: canteen, bookshop, stationery, hostel kiosk, printing, pharmacy, transport. Deliberately include a canteen on semester break and a bookshop on exam week, both of which a zero-transaction rule would condemn. Ground truth "was this terminal actually dying" to `truth/`. Held-out campus split. |
| **8. Validation** | Precision on the **intervene** set against injected truth, and — the metric that matters — **false-intervention rate on the seasonal cohort**. A liveness model that pings healthy merchants is the merchant-churn model everyone already has, and it will lose the room. Rule baseline: **"no transactions in 11 days = dead."** Report both, and show the baseline's false-intervention count. |
| **9. Scale** | Real data adds actual campus merchant lists (upay has them under the MoUs), real category calendars from a partner university, and real dormancy definitions. **The merchant is the data subject and an adult, which is what makes this design lawful.** Architecture: merchant-liveness scoring is a module that a requirement drop of "make it campus-specific" simply points at — which is why `mix-shift-THESIS.md` §8 kept this idea as the on-site requirement-drop absorber. |

### ⚠ Mandatory compliance constraint — read before building

**Personal Data Protection Ordinance, 2025 (Ordinance No. 61 of 2025) §9(3)**: a data controller shall not
conduct activities such as *"tracking, monitoring, **profiling** or targeted advertising of a specific
child using his/her behaviour or other data."* §9(4) holds parental or guardian consent valid only until
the child reaches 18. A campus population contains a material share of students under 18.

Therefore: **the model is merchant-side only.** The merchant is the data subject, is an adult, and merchant
liveness is the actual idea. No student-level behaviour model. No student-level targeting. No campus-wide
spend profile. This is not a preference — it is a prohibition, and the negative should be stated on the
slide: *"we deliberately did not model the students."*

**Also: do not claim the UCSI RFID student ID is live. It is planned, not live.**

### Problem statement (official format)

> For a campus merchant at upay who installed a QR terminal and pays MDR on every transaction, having
> "no transactions for 11 days" as the only liveness rule causes healthy terminals to be written off as
> dead during every semester break and exam week, so upay churns the merchants it spent its acquisition
> budget winning.

### The three things a judge remembers

- **One sentence:** *"A canteen quiet for eleven days is dying. A bookshop quiet for eleven days is on break."*
- **One taka number:** **Base case −Tk 0.6 lakh; even the aggressive case is Tk 14 lakh.** Present it as **8 terminals kept alive per campus**, and let the relevance argument — not the number — carry the pitch. This is the one finalist where that trade is correct.
- **One demo moment:** the judge opens the campus map and clicks a terminal flagged **"quiet for 11 days."** The tool shows the category's expected curve, the actual, and the verdict: **"on break — do not intervene."** Then it shows the same 11-day gap on a canteen terminal and the verdict flips to **"intervene."** Same signal, opposite action, and the reason is the category.

### 48-hour build plan

| Hours | P1 — data & model | P2 — API & rules | P3 — web, demo, deliverables |
| --- | --- | --- | --- |
| **0–2** | Scaffold; `datagen/` campus merchants with **category calendars** | Scaffold; `/terminal /diagnose /intervene /explain` | Scaffold; demo URL; README skeleton |
| **2–6** | Canteen/bookshop/stationery/hostel/printing/pharmacy/transport; semester-break and exam-week cohorts; ground truth to `truth/` | **Deterministic baseline** — "no transactions in 11 days = dead" | Campus map + terminal list. Working demo at hour 6 |
| **6–8** | **HOUR-6 GATE:** held-out campus exists; seasonal cohorts present and labelled | Baseline end-to-end **with the false-intervention count computed** | Demo script v1 shows the baseline condemning a bookshop |
| **8–12** | Category-conditioned residual model; three-way action head | **`merchant-side-only` guard as an enforced schema constraint**, not a convention | Map + the two-terminal comparison |
| **12** | 🛑 **KILL SWITCH — below** | | |
| **12–20** | Precision on intervene; **false-intervention rate on the seasonal cohort**; terminal-keep-alive count | Compliance guard tested; no customer/student field exists in the schema | The 11-day bookshop vs canteen moment |
| **20–24** | ✅ **Pre-evaluation-ready.** Freeze v1 | OpenAPI docs | **README + live deploy up. Report drafted** |
| **24–36** | Second campus; Ramadan and exam-result-day calendars | | Video demo |
| **36–42** | Merchant activity-monitoring view (also an R11 control) | | |
| **42–48** | Bug fixes only | | README/report/video final; rehearse all three |

**🛑 Hour-12 kill switch.** Continue **only if** the model **materially reduces false interventions on the
seasonal cohort** relative to the 11-day rule, at equal or better precision on the intervene set. If the
category conditioning does not work, this is a merchant-churn model — a well-known global shape with no
entry — and **drop**. A second, non-negotiable gate: the **merchant-side-only compliance guard must be
enforced in the schema by hour 12**, not documented in the README. If a student-level field has crept into
the data model, the project is in breach of PDPO §9(3) and must be fixed before anything else ships.
**Fallback: F1**, which shares the synthetic-generator spine and needs no campus-specific data.

### Judge's hardest question, and the honest answer

> *"The host institution's students are partly under 18, and the data protection ordinance bans profiling
> children. Isn't your own flagship demo the thing you just described is illegal?"*

**Honest answer:** "It would be, if we modelled students — so we don't, and that was a design decision
forced by the law rather than a preference. The data subject in our system is the **merchant**: an adult
business with a QR terminal, whose liveness is a question about its own revenue. There is no student-level
behaviour model, no student-level targeting and no campus-wide spend profile anywhere in the system, and
that constraint is enforced in the data schema rather than promised in the README. The negative is on the
slide on purpose — *we deliberately did not model the students* — because a campus product that quietly
profiled a million teenagers would be the fastest way to lose a Bangladesh Bank compliance officer, and
also because the merchant-side question is the one that actually decides upay's cost." *(Campuses live,
terminals per campus, terminals saved and cost per campus are all `ASSUMED`. The Daffodil MoU, the UCSI
agreement and the 14,519 merchant count are SOURCED. The RFID student ID is planned, not live.)*

---

## Cross-cutting note

If you are choosing between the two files, `finalists.md` is the shortlist and this file is the longlist.
The honest summary of the whole twenty-five-idea exercise, after red-teaming, is in `economics.md` §5:
**at Tk 43.32 crore of revenue, no idea in this repo changes upay's P&L materially, and the best cases are
the best-evidenced ones.** That is not a reason to build nothing. It is a reason to build the thing whose
number you can defend, on the track whose metric is a rate rather than a rupee, and to say out loud which
of your inputs are assumptions.
