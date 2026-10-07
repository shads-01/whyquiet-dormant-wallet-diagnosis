# Long list — 25 surviving ideas from 36

> Built 3 Oct 2026 from `docs/v3/ideas-1-2-3-8-upay-model.md` (12), `ideas-4-6-upay-model.md` (12),
> `ideas-5-7-upay-model.md` (12) and `docs/v3/interview.md`. Clusters follow the eight P&L levers in
> `upay-model.md` §4. Evidence keys (S1–S16) are `interview.md`'s source list.
>
> **Arithmetic corrections carried forward, not fixed at source.** L1 is `0.00632 × X × R`
> (Tk 41.5 cr per 1% relative at the bKash anchor), not Tk 66 cr. L3 per-1m-cash-out is
> **Tk 3.94 cr** (bKash agent 1.85%) / **Tk 2.99 cr** (upay agent 1.40%) / **Tk 1.71 cr** (upay UCB ATM
> 0.80%), not Tk 1.85 cr. upay's agent rate is 24% below bKash's, not 43%. The errors remain live in
> `upay-model.md` §4 and `upay-model-calc.py`.
>
> **Track 01 §0 is still unresolved.** Nothing here touches fraud, scam, ATO, mule or AML.
> `interview.md` is *evidence-derived, not first-hand* — three roles, no upay-specific study.

---

## 1. How 36 became 25

36 ideas → 9 duplicate merges (removing 10 near-duplicates) → 26 distinct → 1 dropped on merit → **25**.

**Merge test applied:** same *money term*, not merely the same technique. Four uplift ideas survived as
four because they move four different budgets (customer offers, retention discounts, contact, merchant
fee); three that moved the *same* taka were merged.

Scored on the three requested criteria, in this order:
- **(a) clarity of the taka mechanism** — can a business judge hold the number in their head?
- **(b) fit with interview evidence** — is the pain in `interview.md`, or only in our own reasoning?
- **(c) AI is necessary** — does the official §13 line ("AI adds value beyond a simple deterministic
  rule") hold, or does a threshold beat us?

---

## 2. The 25, by lever

### L1 — Cost-to-serve (63.18% of revenue; agent commission the obvious target)

**1. Agent Shift Market** · T05 · A3 + (seeded) mix-shift doc
Taka: `0.00632 × X × R`, X = share of failed/re-served transactions removed — *measured, not asserted*.
Evidence: S4 (agents decline small withdrawals, unavailable at night), S3 (break-even 3–5 txns/day).
AI: float depth changes intra-day and is invisible in any static roster. **Keep** — the one idea where the
interview pain (agent says no) and the cost line are the same object.

**2. Float Pre-Positioning** · T05 · **A4 + B7 + B12 merged**
Taka: 1m extra *served* cash-outs = Tk 2.99 cr at upay's 1.40% agent rate.
Evidence: S3 (rural 9–10 / urban 13–26 txns/day needed), F B1/B2 (float and settlement shocks).
AI: the funding need is a P90 tail, not a mean — funding to the mean under-funds exactly the busy agents.
**Keep** — merges three float ideas that all priced the same tail quantity; B7's agent-lender market and
B12's intraday nudge are mechanism variants of A4's lender, not separate products.

**3. Complaint Autopsy & First-Contact Remedy** · T06 · **A7 + A11 merged**
Taka: `0.00632 × X × R`, X = complaint-handling minutes removed — measured with a time-and-motion baseline.
Evidence: none in `interview.md` (support complaints were not interviewed).
AI: Bangla/English free text across app, USSD `*268#`, hotline and agent channels does not cluster on
keywords; A11's reconciliation is multi-step. **Keep, flagged** — strongest internal-P&L taka story,
weakest interview evidence. Human approval key retained (§14).

### L2 — Retention / active rate (57.3%; 35m dormant of 82m)

**4. Goal Autopilot** · T03 flagship · **A9 + C2 merged**
Taka: inherits L2 — 1% relative on active rate = +470k users × Tk 1,397 = Tk 66 cr at full ARPU.
Evidence: S6/BSR — one in five garment workers already save monthly; bKash said workers would use more
with more varied transactions. Directly matches the brief's "save Tk 30,000 in six months" spec.
AI: contribution solved on the *worst* month, not the average — payroll on the 28th and remittance on the
5th give different affordable amounts. **Keep** — flagship track, named persona, real evidence, and the
model is the product (C2's DPS-entry was a co-funding variant of the same on-ramp).

**5. Sponsor Payroll Market** · T02/T04 · **A1 + C3 merged**
Taka: `350k activated × Tk 1,397 = Tk 49 cr` gross, Tk 24 cr at 50% ramp; employer funds the bounty.
Evidence: S6 (wages arrive and are immediately cashed out), S2 (upay 8.5m registered / 154k agents).
AI: 90-day-out compound label (activates *and* transacts ≥4×/mo for 3 months) is unobservable at
decision time; changepoint classification separates job-exit from merely-quiet. **Keep** — both originals
flip the *same* who-pays (the employer, not upay marketing); the merged product is strictly more specific.

### L3 — Frequency (+1% per active user = Tk 66 cr at anchor)

**6. Full-Loop Swap Engine** · T02/T04 · **A10 + C7 merged**
Taka: `converted_value × [(MDR_net + merchant_cashout) − displaced 1.40%]`; customer keeps Tk 11–30/txn.
Evidence: S10/S8 (cash-out volume far exceeds merchant payments; 37% of retailers avoid digital because
suppliers want cash), and the brief's own Track 03 worked example "How can I reduce cash-outs?".
AI: the break-even depends on the *merchant's* cash-out behaviour — a joint customer×merchant
counterfactual. **Keep** — this is the already-converged `mix-shift-THESIS.md` build; C7's full-loop
pricing replaces A10's bounty accounting with the correct one.

**7. Restock Credit** · T05/T08 · A8
Taka: stated as a **mix-shift** claim, not a 1% claim — QR is 0.5% of NPSB value, so honest sizing is a
share, not a taka total. Evidence: DIU host campus sits inside the Daffodil education MoU; S8 supply-chain
cash constraint. AI: the product *is* the auditable interval — a rule gives either a useless average or
an unexplainable one. **Keep, flagged** — great AI-necessity story, weakest taka. Needs the merchant-side
number upay has and we do not.

**8. Incremental Offer Fund** · T04 · A2
Taka: discount moved off upay's commercial-expense line onto the merchant's, only where proven
incremental. Evidence: none in `interview.md` (no merchant campaign data); bKash FY2024 commercial
expense Tk 3.99bn is the anchor. AI: uplift is named in the brief as the sharp ML signal; the deliverable
is Qini/AUUC against injected ground truth. **Keep** — the single most on-brief ML technique, and
strongest when paired with #10, which shares it.

**9. Autopay Subscriptions** · T06 · A6
Taka: **near zero direct revenue** (bill pay is free to upay customers, COO-signed FAQ) — value is L3
frequency consolidation plus cheaper-to-prefund balances. Evidence: S11 (utility bills and salary each
> Tk 3,000 cr/month), S12 (utility bills 20.2% of wallet uses). AI: per-customer, seasonal missed-bill
prediction. **Keep, flagged** — `interview.md` explicitly lists autopay as **UNVERIFIED** in Bangladesh;
search before pitching. Mechanism is crisp even though the taka is not.

### L4 — ARPU / take-rate (95.6% of net revenue is commission)

**10. Willingness-to-Pay Compiler** · T04 · B1
Taka: `+Tk 1/1,000 × 1m cash-outs × Tk 2,132 = Tk 21.3 lakh`; headline 1% realised take-rate ≈ Tk 66 cr.
Evidence: price ladder is public and dated — bKash cut to Tk 13.95/1,000 Jul 2026, cross-MFS added
Tk 8.50/1,000 Nov 2025. AI: the whole quantity is counterfactual — no column exists for "volume at a price
never charged". **Keep** — sharpest counterfactual-per-rupee story in the set, with a fairness floor the
tool cannot cross.

**11. Wallet-Tier & Take-Rate Leakage** · T02/T06 · **B2 + B6 merged**
Taka: both priced the *same* divergence — posted tier vs realised tier. `+Tk 1/1,000 recovered on 1m
cash-outs = Tk 21 lakh`; the 1% watermark is the lever. Evidence: upay CEO describes the schedule as
tiered below Tk 14 with some wallet tiers free (2021) — misassignment is documented, magnitude is not.
AI: tier is a joint objective over provenance, float yield and churn probability; a threshold picks one
field. **Keep** — B6 found the leak, B2 prices the fix; together one product.

**12. Retention Uplift Gate** · T04/T02 · **B4 + C6 merged**
Taka: `value_at_risk × P(retain | offer) − offer_cost`, plus avoided destruction of reactivation option
value. Evidence: S6 (fees resisted, cost-sharing unclear), S12 (42.5% use MFS 1–2×/month).
AI: negative uplift is only observable against a control; a contact with ~0 measured response looks
*free* to any rule. **Keep** — merged because both are the same decision ("does this offer *cause* the
retention?") on the same customer file; the off-switch is the retention gate applied to contact.

**13. Cross-Operator Leak Plug** · T06/L07 · **B3 + C10 merged**
Taka: `rerouted_value × Tk 5–8/1,000` = **Tk 11–17 per payment** at the Tk 2,132 average ticket — a
*disclosed cost being avoided*, not a speculative fee being won. Evidence: upay publicly disclosed
absorbing Tk 5–8/1,000 with IRF zeroed (15 Sep 2026); S8 (37% of retailers keep cash).
AI: "always show own merchants first" degrades the list for the 90% with no own alternative nearby.
**Keep** — highest-certainty per-transaction margin in the whole long list, and self-funding.

### L5 — Activation of dormant (35m dormant; 1% = Tk 49 cr / Tk 24 cr ramped)

**14. Dormant-Lead Bazaar** · T02/T05 · C1
Taka: `bounty = P(reactivate) × ARPU × ramp − visit_cost`; portfolio watermark Tk 49 cr / Tk 24 cr.
Evidence: S3 (agents are the ones who know the street), S14 (37.6% active nationally).
AI: the price is a counterfactual expected value, and the *same* dormant user is worth different amounts
to different agents. **Keep** — the marketplace's sellers are upay's own 130k agents, so the
distribution channel already exists.

**15. Silent-Churn Triage** · T06 · C4
Taka: `users_treated × save_rate × ARPU × ramp`. Evidence: S12 (42.5% use 1–2×/month), S1 (37.6% active).
AI: one observed gap (3 weeks of no transactions) is five diseases with five remedies; the signal is the
*shape* of the decline. **Keep** — the label-free one, and the demo's "no attributable cause" refusal is
the credibility.

**16. Remittance-Season Awakening** · T04 · C5
Taka: partner fee share + L5 watermark; partner-fee share is **UNVERIFIED**, so quote the count only.
Evidence: UCB–Incentive Remit real-time Malaysia corridor is a dated, documented partnership.
AI: seasonality is sender-pay-cycle specific, not calendar average; uplift gates the contact.
**Keep** — the purest *who-pays* flip: the party that earns the fee funds the outreach.

### L6 — Agent productivity (+1%/agent ≈ Tk 24 cr across 130k agents)

**17. Conversion-Priced Agent Tiers** · T05 · B8
Taka: `volume_gain(agent) − commission_delta`, paid only when the gain is real; ceiling
Tk 187,571 revenue/agent/yr (bKash benchmark). Evidence: S3, S4 (decline rates differ by agent).
AI: two adjacent agents with identical location, stock and footfall have different reliability, so the
same static tier is wrong for one of them. **Keep** — includes a downgrade the tool is willing to issue.

**18. Agent Rescue Fund** · T05 · B11
Taka: `taka of rescue spend per reactivated agent`. Evidence: S3 (satisfaction collapses under 15–20
txns/day). AI: "no transactions last month" flags an Eid-break agent identically to a failing one.
**Keep** — the *refusal* is the product, which is what keeps it off the banned churn-dashboard list.

**19. Counter Attach Engine** · T05/T04 · B10
Taka: `revenue/agent = Σ product mix`; watermark +1%/agent ≈ Tk 24 cr. Evidence: S3 (multi-provider
agents earn >40% more), Micro DPS / remittance / recharge all attachable.
AI: uplift-gated next-best-action. **Keep, weakest of the 25** — a static "always offer DPS" script is a
strong competitor and NBA is a crowded shape. Beat it on the *joint* (customer ledger × what this agent
can serve right now) or drop it.

### L7 — Merchant volume (QR = 3% of volume, 0.5% of value — mix-shift, not 1%)

**20. Acceptance-Gap Sniper** · T05 · **C8 + B9 merged**
Taka: `predicted_QR_volume × MDR_net + predicted_proceeds_cashout × 8.00` — small today by the lever's
own admission. Evidence: S8 (supplier-side cash), OSM POI geometry; upay's own agent cash-density is
the strongest proprietary input and we do not have it. AI: two shops 50m apart differ 5× in addressable
cash turnover; the surface is continuous, so no cell threshold survives the geometry.
**Keep** — merged with B9 because both optimise placement on the same continuous surface over the same
OSM data; the merchant-side supply is where the mix is heading.

**21. Merchant Fee-Elasticity Guard** · T04/T05 · C11
Taka: `merchants_saved × QR_volume × MDR_net − holiday_cost`, sized against the **Tk 100 crore** BB
subsidy fund as the external benchmark. Evidence: BMPCA lobbying for 0.25%; documented merchant resistance
to the 1% MDR floor. AI: the loudest objectors are not the ones most likely to leave — invisible to any
rule keyed on complaint volume. **Keep** — priced against the live regulatory fight, dated and real.

**22. Settlement-Timing Yield Desk** · T05 · C9
Taka: `held_value × 9.33% × Δdays` — **Tk 2.56 lakh/day at Tk 1bn held**, explicitly small against the
Tk 66 cr anchor. Evidence: float yield is sourced (FY2024 audited); merchant sweep behaviour is not.
AI: liquidity tolerance is heterogeneous — two grocers with identical volume differ on whether T+1 causes
a stockout. **Keep, flagged** — honest small number, compounding merchant-retention margin, and the
refusal (liquidity-tight merchant) is judge-visible.

**23. Failed-QR Recovery** · T06/L07 · C12
Taka: `recovered_value × (MDR_net + merchant_cashout_net)` plus avoided support cost. Evidence: S12 (46%
still prefer cash), S10 (cash-out dominates). AI: the error code is not the cause — a "timeout" is
retryable in one network state and fatal in another. **Keep** — highest-conversion moment in the funnel
(the customer already chose to pay digitally) and the unrecoverable declaration routes to a human.

### L8 — B2B / payroll (base **UNVERIFIED** — report counts and shares only)

**24. Payroll-as-a-Product** · T07 → T03/T05 · A5
Taka: reported as **dwell days after disbursement** and **share of payroll that never touches an agent**.
No taka total (the ≈3.1% base is a secondary source). Evidence: Agrani Distribution MoU and foodpanda
riders are documented upay partners; S6 (wages used almost only for cash-out).
AI: hour-by-hour wallet trajectory across a payroll cycle sized inside the trust account — a constrained
schedule, not a forecast that ends in a number. **Keep** — the only idea where the float line and the
commission line reinforce rather than trade off.

**25. Campus Closed Loop** · T03/T05 · A12
Taka: **share of on-campus spend that stays inside the upay loop** and **merchants per campus with >30 days
of activity**. No taka. Evidence: DIU (the host) sits inside the same Daffodil Group as upay's education
MoU; UCSI agreement covers campus QR, tuition, scholarships. The RFID student ID is **planned, not live** —
do not claim otherwise. AI: liveness is not "no transactions" — a canteen quiet for 11 days is dying, a
bookshop quiet for 11 days is on break. **Keep** — the relevance-credibility story is unmatched, and DIU
judges know the campus.

---

## 3. Merge and drop ledger — every one of the 36 accounted for

| # | Source | Fate | One-line reason |
| --- | --- | --- | --- |
| A1 | Sponsor Market | **merged → #5** | Same who-pays as C3 (employer-funded dormant salary wallet); C3 is the sharper version with a named changepoint. |
| A2 | Incremental Offer Fund | **keep #8** | Uplift named in the brief; the discount moves off upay's commercial line onto the merchant's. |
| A3 | Agent Shift Market | **keep #1** | Interview pain (S4: agents decline small amounts) and the cost line are the same object. |
| A4 | Float Pre-Positioning | **keep #2** | P90 liquidity forecast; the only idea attacking L1 through a mechanism the model itself flags. |
| A5 | Payroll-as-a-Product | **keep #24** | Only idea where float and commission reinforce; Agrani/foodpanda partners are documented. |
| A6 | Autopay Subscriptions | **keep #9** | Near-zero direct revenue but the brief names bills; **flagged** — autopilot is UNVERIFIED in BD. |
| A7 | Complaint Autopsy | **merged → #3** | Same product surface and same taka as A11 (16268 handling minutes); A11's remedy is the stronger half. |
| A8 | Restock Credit | **keep #7** | Best AI-necessity story in merchant-land; **flagged** — taka is a mix-shift claim, not a 1% claim. |
| A9 | Goal Autopilot | **keep #4** | Flagship track, the brief's named persona, and real evidence (S6: one in five already save). |
| A10 | Cash-Out Substitution Bounty | **merged → #6** | Same taka as C7 but with worse accounting; C7 prices the full loop including the merchant's cash-out. |
| A11 | Hotline Auto-Remedy | **merged → #3** | Same 16268 cost line as A7; the reconciliation engine is the harder AI and the auto-remedy is its output. |
| A12 | Campus Closed Loop | **keep #25** | Unmatched relevance credibility — the host institution sits inside the same group as upay's education MoU. |
| B1 | Willingness-to-Pay Compiler | **keep #10** | Sharpest counterfactual-per-rupee story; the quantity is one no spreadsheet column can hold. |
| B2 | Wallet-Tier Router | **merged → #11** | Prices the same tier-vs-realised divergence B6 detects; forward-optimising beat retrospective audit. |
| B3 | Net-Rail Router | **merged → #13** | Same Tk 5–8/1,000 cross-operator cost C10 avoids; C10's leak-funded incentive is the sharper mechanism. |
| B4 | Price-Churn Shield | **merged → #12** | Same decision as C6 — "does this offer *cause* the retention?" — on the same customer file. |
| B5 | Biller-Side Monetization Desk | **DROP** | Weakest AI necessity in the set: ranking three weighted terms is a spreadsheet job, and no biller economics appear in `interview.md`. |
| B6 | Realised-Take-Rate Leakage Engine | **merged → #11** | Finds the divergence B2 prices the fix for; an audit that reports taka is close to a dashboard. |
| B7 | Agent Float Futures | **merged → #2** | Same P90 shortfall quantity as A4, with a lender-market variant; upay-as-lender is the buildable one. |
| B8 | Conversion-Priced Agent Tiers | **keep #17** | Marginal agent-specific pricing beats a static geography band; the tool issues downgrades too. |
| B9 | Agent Coverage Optimizer | **merged → #20** | Same continuous-surface placement problem as C8 over the same OSM data; merchant supply is where the mix is headed. |
| B10 | Counter Attach Engine | **keep #19, weakest** | Uplift-gated NBA on a crowded shape; survives only on the joint customer×agent-now framing. |
| B11 | Agent Rescue Fund | **keep #18** | Separates seasonal leave from real failure; the refusal to fund is the product. |
| B12 | Flow Balancer | **merged → #2** | Intraday cash-in nudges are the incentive lever inside A4's pre-funding decision, not a separate product. |
| C1 | Dormant-Lead Bazaar | **keep #14** | Sellers are upay's own 130k agents, so the channel exists; the price is a per-agent counterfactual. |
| C2 | Dust-to-DPS | **merged → #4** | Same Track 03 savings on-ramp as A9; NRB co-funding is a who-pays variant of the same conversion. |
| C3 | Payroll Ghosts | **merged → #5** | Same employer-funded dormant-wallet bounty as A1, with the sharper changepoint classifier. |
| C4 | Silent-Churn Triage | **keep #15** | Label-free cause attribution; the "no attributable cause" refusal is judge-visible credibility. |
| C5 | Remittance-Season Awakening | **keep #16** | Purest who-pays flip — the remittance partner that earns the fee funds the list. |
| C6 | Contact-Fatigue Off-Switch | **merged → #12** | Negative uplift is only observable against a control; it is B4's gate applied to contact. |
| C7 | Full-Loop Swap Engine | **keep #6** | Prices the merchant's own cash-out, which is the number the break-even actually turns on. |
| C8 | Acceptance-Gap Sniper | **keep #20** | Ranks prospects by predicted yield, so field commission stops paying for raw quota. |
| C9 | Settlement-Timing Yield Desk | **keep #22, flagged** | Honest small number (Tk 2.56 lakh/day) but a compounding margin line; merchant tolerance is model work. |
| C10 | Cross-Operator Leak Plug | **keep #13** | Highest-certainty per-transaction margin in the list and self-funding from the disclosed leak. |
| C11 | Merchant Fee-Elasticity Guard | **keep #21** | Sized against the Tk 100 cr BB subsidy fund — the loudest objectors are not the ones who leave. |
| C12 | Failed-QR Recovery | **keep #23** | Highest-conversion moment in the funnel; the unrecoverable case routes to a human. |

---

## 4. Where the interview evidence actually constrains the list

`interview.md` is evidence-derived, not first-hand, and it is **not** neutral across the three roles.
The asymmetry matters for selection:

| Interview pain | Source | Ideas it carries |
| --- | --- | --- |
| Agents decline small withdrawals; not available at night | S4, S3 | #1, #2, #17 |
| Agent float and settlement shocks; low volume | S3, F B1/B2 | #2, #17, #18 |
| Merchant fees cut into a distributor's Tk 1–2 per Tk 100 margin | S8, S10 | #20, #21, #23 |
| Digital balance cannot pay a supplier — 37% of retailers avoid digital | S8 | #6, #20 |
| Cash-out fee resisted; wage used almost only for cash-out | S6, S7 | #4, #6, #12, #24 |
| Wallets used 1–2×/month; 62.4% inactive | S12, S1 | #13, #14, #15, #25 |
| Remittance is structurally important | S7, UCB–Incentive Remit | #16 |

**Evidence gaps that should lower confidence on specific ideas:**

- **No agent monthly costs** (rent, float financing, runners) — S-marked "not found". Weakens #2, #17, #18.
- **No 2026 agent income, shopkeeper or upay-user data at all.** Every upay-specific quantity in this list
  is UNVERIFIED and inherits the bKash anchor. Do not print `R`.
- **Autopay / recurring-mandate products in Bangladesh: not verified.** #9 needs a search before it is
  pitched.
- **Shopkeeper baki ledger is solved** (baki.bd, S13) — do not propose it.
- **Three ideas carry no interview evidence at all**: #3 (complaints/support), #8 (merchant campaigns),
  #10 (price ladder — sourced from press, not from users). #10 is fine; the other two are the exposure.

---

## 5. What this list does not do

- Does not resolve Track 01 §0. That is still a team decision and nothing here depends on it.
- Does not pick one. `CONTEXT_v3.md` §12 rule 2 stands: three people × 24h cannot hedge, and this is a
  shortlist to choose *from*, not a set to build.
- Does not patch `upay-model.md` §4 or `upay-model-calc.py`. The L1 and L3 arithmetic errors are still
  live there and will mislead the next reader.