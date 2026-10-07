# 12 product ideas — levers 5, 7

> Generated against `docs/v3/CONTEXT_v3.md` (rubric, tracks, data rule, banned themes) and
> `docs/v3/upay-model.md` §4 (lever baselines). Levers requested: **5 activation of dormant users**
> and **7 merchant volume**.
> `analogs.md` **does not exist** in this repo — re-searched on 3 Oct 2026 (`*analog*` across the full
> tree, no match). Nothing here was cross-checked against it. Same finding as `ideas-4-6-upay-model.md`.
>
> This batch does **not** re-cover `ideas-1-2-3-8-upay-model.md` (levers 1,2,3,8), `ideas-4-6-upay-model.md`
> (levers 4,6) or `mix-shift-THESIS.md`. Four prior ideas sit adjacent to ones below; the differentiation
> is stated inline on each: #1 vs *Sponsor Market*, #4 vs *Complaint Autopsy*, #7 vs *Cash-Out Substitution
> Bounty* and *Incremental Offer Fund*, #8 vs *Agent Coverage Optimizer*.

---

## 0. Lever arithmetic, stated

- **L5.** Dormant base **35m** (bKash: 82m registered − 47m 90-day active = **57.3% active rate**);
  `1% of dormant = 350k users × Tk 1,397 ARPU = Tk 49 crore`, **Tk 24 crore at a 50% ARPU ramp**. For
  upay the dormant base itself is **UNVERIFIED** — quote the mechanism, not a upay user count.
  (`upay-model.md` §2.2, §4 Lever 5.)
- **L7.** QR = **3% of NPSB volume, 0.5% of value**; ~1m Bangla QR merchants; **MDR minimum 1% incl. VAT
  from 1 Jul 2026**, **IRF zeroed**, upay publicly discloses **Tk 5–8/1,000** cost on cross-operator QR;
  merchant payment is **free to the customer**. Per `upay-model.md` §4 this is a **mix-shift** lever, not
  a 1% lever: the real question is *does upay's own-rail QR net more than the 1.40% agent cash-out line it
  displaces*. Full-loop gross per Tk 1,000: MDR ≤ Tk 10 (1% incl. VAT — upay's net share of it UNVERIFIED)
  + merchant cash-out of QR proceeds **Tk 8.00** (third-party, UNVERIFIED — https://www.ink.bd/1848/bangla-qr-payment-charges)
  = **Tk 10–18** vs **Tk 14** displaced (upay agent 1.40%). The swap is net-positive for only part of the
  base — finding which part is the model's job, and most ideas below do exactly that.

**Lever formulae used below.**
L5 = `Δrevenue = reactivated_users × ARPU × ramp` (anchor: 350k × Tk 1,397 = Tk 49 cr; × 0.5 ramp = Tk 24 cr).
L7 = `Δnet = rerouted_value × (own_loop_net − displaced_take_rate)` and `Δfloat = settled_value × 9.33% × Δdays`.

---

## 1. The 12 ideas

Each is one paragraph. `TRACK:` is the official track (`CONTEXT_v3.md` §3). `LEVER:` is `upay-model.md` §4.
`MECH:` names the mechanism changed — **incentive / who-pays / workflow / marketplace / pricing**.

### 1. Dormant-Lead Bazaar — agents claim reactivation leads priced by a model

**TRACK:** 02 (also 05) · **LEVER:** 5 (activation) · **MECH: marketplace + incentive.** **User:** the
upay agent who personally knows which households on her street stopped using their wallet, and upay's
activation lead with a 35m-class dormant base (bKash-calibrated; upay's own base UNVERIFIED) and no way
to spend reactivation money efficiently. The job: *turn dormant users near each agent into priced,
claimable leads the agent can work on foot.* Differentiation from *Sponsor Market* (`ideas-1-2-3-8` #1):
there the reactivator was an external third party who benefits; here the marketplace's sellers are upay's
own **130,000+ agents** (https://www.ucb.com.bd/banking/retail-banking/upay-ucb-card) paid a priced bounty
on a verified first transaction, and the AI's product is the *price*, not the match. **Money (L5):** the
line that moves is engagement → commission; the actionable unit is `bounty = P(reactivate) × ARPU × ramp −
visit_cost`, and the portfolio watermark is 350k activations = **Tk 49 cr** (Tk 24 cr at 50% ramp). **AI:**
lead pricing — predict each dormant user's activation probability and expected 90-day ARPU from residual
ledger shape, distance, and dormancy cause. A rule cannot do it because the price is a **counterfactual
expected value**: a flat "Tk 50 per reactivation" overpays hopeless leads and underpays the ones a
specific agent can actually reach, and a spreadsheet cannot express that the same dormant user is worth
different amounts to different agents. **Data:** **synthetic with injected ground truth** (known true
activation propensity per user, an agent-proximity layer from OpenStreetMap — https://www.openstreetmap.org/copyright);
real upay data would add real dormancy durations and actual agent-visit conversion. **48-hour demo:** the
judge sees two adjacent dormants priced ৳180 and ৳0, watches the bazaar **refuse to list** the hopeless
lead, claims a lead as an agent, logs the visit, and sees the bounty pay out only on the verified first
transaction.

### 2. Dust-to-DPS — a dormant residual balance becomes a savings account's first installment

**TRACK:** 03 (flagship) · **LEVER:** 5 (activation) · **MECH: who-pays + product workflow.** **User:**
the dormant customer with ৳150–800 stranded in the wallet — too little to care about, too real to ignore —
and upay's deposit-growth owner holding the **NRB Bank Micro DPS tie-up** signed 22 Jul 2026
(https://www.tbsnews.net/economy/corporates/upay-nrb-bank-partner-expand-digital-financial-services-1494556).
The job: *convert a dead balance into a live savings relationship with one consented tap.* The mechanism
change: **NRB and upay co-fund the first installment** — the entity that earns the deposit pays for the
conversion, not the customer. **Money (L5, honest both sides):** `value = reactivation_ARPU + deposit_funding_value
− float_yield_given_up`; the wallet residual moving into DPS **reduces trust-account float** (9.33% implied
yield, FY2024 audited — https://www.legacy.bracbank.com/financialstatement/bkash-limited-audited-financial-statements-december-31-2024.pdf)
and **replaces it with deposit funding** for the parent group; the file states that trade openly rather
than hiding it, because a technical judge will find it. Reactivation watermark: Tk 49 cr / Tk 24 cr (L5).
**AI:** predict acceptance propensity *and* the auto-debit amount the customer will sustain without
defaulting — a joint optimisation over balance size, inflow seasonality and stated goals. A rule cannot do
it because "offer DPS to everyone with >৳100" produces defaults and resentment; the sustainable amount is
a per-customer counterfactual no spreadsheet computes. Guardrail (Track 03): empowered, transparent, no
hidden fee — the tool shows the customer the math in Bangla before any debit. **Data:** **synthetic** with
an injected cohort whose sustainable debit differs from their nominal balance; real upay data would add
actual DPS repayment behaviour. **48-hour demo:** the judge plays a dormant customer, accepts the offer,
and watches the residual convert to a DPS plan with the sustainable amount the model chose — then tries
to force an unsustainable amount and sees the tool cap it with its reason shown.

### 3. Payroll Ghosts — find the salary wallets that died when the job did

**TRACK:** 02 (also 04) · **LEVER:** 5 (activation) · **MECH: incentive + who-pays.** **User:** the
operations lead at a foodpanda-style employer or Agrani Distribution depot whose riders churn monthly —
**foodpanda rider collections** and **Agrani B2B** are documented upay partners
(https://www.ucb.com.bd/news-and-events/press-release/upay-foodpanda-partnership-to-simplify-transactions-1 ·
https://www.agranidistribution.com/news) — and upay's disbursement owner, whose payroll wallet goes dark
the week the rider quits and stays dark forever. The job: *separate "left the job" dormancy from "still
employed, just quiet" dormancy, and re-enrol the leavers at their next employer.* The mechanism change:
**the incoming employer's HR desk gets a re-enrolment bounty**, paid by upay's payroll team out of the
disbursement volume it wins — who pays flips from upay marketing to a B2B sales motion. **Money (L5 + L8
adjacency):** each recovered payroll wallet returns salary-inflow engagement — `Δrevenue = recovered_wallets ×
ARPU × ramp` (Tk 49 cr / Tk 24 cr watermarks) plus the disbursement float and disbursement take the
employer brings; salary disbursement ≈3.1% of MFS value is a **secondary, UNVERIFIED** base
(https://directory.exports.bd/remittance). **AI:** classify inflow-cadence break-point: a salary wallet
that stops on a predictable payday boundary with a preceding resignation-shaped ledger is a *job exit*; one
that thins gradually is not. A rule cannot do it because the two shapes overlap heavily at monthly
granularity and the cost of misclassification is a wasted HR visit; the break-point is a changepoint-
detection problem, not a threshold. **Data:** **synthetic payroll ledgers** with injected
resignation/bench/quiet archetypes; real upay data would add true employer-mapping and re-enrolment
outcomes. **48-hour demo:** the judge views 50 "stopped" payroll wallets and watches the model tag the
ghosts, export a re-enrolment list to a mock HR desk, and leave the merely-quiet riders alone — with the
misclassification cost of the naive rule displayed next to it.

### 4. Silent-Churn Triage — diagnose dormancy from the ledger, with no complaint on record

**TRACK:** 06 Operations & Service Intelligence · **LEVER:** 5 (activation) · **MECH: workflow.** **User:**
upay's service-operations owner, who inherits dormancy as an undifferentiated pile: these customers never
complained, they just stopped — so the complaint pipeline (`Complaint Autopsy`, `ideas-1-2-3-8` #7) has
**nothing to work from**. The job: *infer the cause of each exit from the last active weeks' ledger shape
alone, and route each cause to the executed remedy that fits it.* **Money (L5):** every pre-emptively
saved user is a reactivation avoided-forever: `saved = users_treated × save_rate × ARPU × ramp`; watermarks
Tk 49 cr / Tk 24 cr. **AI:** label-free cause attribution — cluster the terminal ledger into fee-shock,
failed-transaction, agent-dry-up, fee-comparison exit, and genuine lifecycle exit. A rule cannot do it
because the **same observed gap** (no transactions for 3 weeks) is five different diseases with five
different remedies, and the distinguishing signal is the *shape of the decline*, not any single field;
unsupervised structure discovery is exactly what a spreadsheet lacks. Responsible-AI framing: every cause
is a hypothesis shown with its supporting transactions, and no remedy executes without human approval —
this is diagnosis support, not automated denial. **Data:** **synthetic with injected cause archetypes and
a deliberately causeless cohort** the tool must refuse to label; real upay data would add whether the
inferred causes predict real recovery. **48-hour demo:** the judge drops a synthetic dying user into the
queue, reads the named cause with its evidence transactions, sees the assigned remedy land in a mock
support queue — and sees the tool output "no attributable cause" for one user it correctly declines to
guess about.

### 5. Remittance-Season Awakening — sell the ranked list to the partner who earns the fee

**TRACK:** 04 Growth & Campaign Intelligence · **LEVER:** 5 (activation) · **MECH: who-pays.** **User:**
the dormant ex-remittance receiver whose last wallet activity was a Malaysia transfer, and upay's
partnership owner for the **UCB–Incentive Remit real-time Malaysia corridor**
(https://www.ucb.com.bd/news-and-events/press-release/ucb-and-incentive-remit-launched-real-time-remittance-service-in-bangladesh)
who cannot currently tell the partner *which* lapsed receivers to spend re-engagement money on. The job:
*predict which dormant receivers will receive an inflow this season, rank them, and sell the ranked list
to the remittance partner — the party that earns the fee pays for the list.* That is the mechanism change:
**the partner, not upay's marketing budget, funds outreach.** **Money (L5 + remittance line):**
`Δrevenue = reactivated × ARPU × ramp + partner_fee_share × predicted_inflow_value`; partner-fee share is
**UNVERIFIED**, so the file quotes only the L5 watermarks (Tk 49 cr / Tk 24 cr) as sized. **AI:** a
seasonal inflow-arrival model per receiver (corridor, sender cadence, Eid/harvest calendar) crossed with
an **uplift** estimate — contact only where the touch changes the receiver's wallet choice at the next
transfer. A rule cannot do it because "all Malaysia-corridor dormants" is most of the list and the
seasonality is receiver-specific (sender pay cycles, not calendar averages); a spreadsheet has no arrival
distribution. **Data:** **synthetic with a real Eid calendar and injected sender-cadence truth**; real
upay data would add actual corridor timing. **48-hour demo:** the judge drags "weeks to Eid" and watches
the ranked list reshuffle live, sees the uplift model **suppress contacts** on receivers the touch would
not move, and sees the invoice line the partner would pay for the list.

### 6. Contact-Fatigue Off-Switch — the list of dormant users you must never contact

**TRACK:** 04 (offer fatigue is a named Track 04 direction) · **LEVER:** 5 (activation) · **MECH:
workflow (lifecycle orchestration).** **User:** upay's lifecycle-marketing owner running reactivation SMS
and push at dormant-base scale, whose current tooling measures *response rate* and therefore cannot see
the customers whom contact actively pushes further away — the ones who mute, ignore, and eventually
abandon. The job: *decide not only who to contact and in what sequence, but who to leave alone
permanently.* **Money (L5, negative space):** the value is avoided destruction of reactivation option
value — `preserved = |negative_uplift_population| × ARPU × ramp`; against a Tk 49 cr (Tk 24 cr at ramp)
portfolio, silently poisoning even 5% of it is a Tk 1–2.5 cr quarterly loss no dashboard ever shows,
because the harm lands as *absence*. **AI:** negative-uplift estimation with a Qini/AUUC read next to a
plain response-model AUROC so the judge sees the exact divergence. A rule cannot do it because a contact
with ~0 measured response looks *free* to any rule and any spreadsheet — only a causal model can observe
that for this segment the counterfactual no-contact outcome was better. This is also the Responsible-AI
story (official §14): fairness and non-manipulation enforced as an executed suppression list, not a
paragraph. **Data:** **synthetic with injected negative-uplift segment** and a "response model gets it
wrong on purpose" decoy cohort; real upay data would require randomised holdouts — stated as the
integration requirement. **48-hour demo:** the judge compares the response model's target list against
the off-switch's, sees the overlapping customers the response model wants to spam and the off-switch
forbids, and toggles the off-switch off to watch the modelled dormant-base retention curve bend down.

### 7. Full-Loop Swap Engine — intercept the cash-out only where QR actually nets more

**TRACK:** 02 (also 04) · **LEVER:** 7 (merchant volume) · **MECH: incentive.** **User:** the salaried
upay customer who cashes out Tk 3,000 every payday at the agent downstairs — paying up to **1.40%** —
when a upay-QR grocery two doors away would take the same money for free, and upay's mix-shift owner who
must not burn margin subsidising swaps that lose money. The job: *per customer, rank which cash-out
occasions to convert to upay-QR, priced on the full loop.* Differentiation from *Cash-Out Substitution
Bounty* (`ideas-1-2-3-8` #10): that idea paid a customer bounty; this is a **placement-and-ranking
product with no bounty**, and it prices the loop the bounty version ignored — the merchant's own cash-out
of QR proceeds. **Money (L7):** `Δnet = converted_value × [(MDR_net + merchant_cashout_rate) − displaced_take_rate]`;
per Tk 1,000: own-loop **Tk 10–18** (MDR ≤ Tk 10 net of VAT content, upay's share UNVERIFIED; merchant
proceeds cash-out Tk 8.00, third-party UNVERIFIED — https://www.ink.bd/1848/bangla-qr-payment-charges) vs
**Tk 14** displaced — so the swap is net-positive only above a break-even mix, which is exactly the
per-customer quantity the model computes. The customer's own saving is the **Tk 11–30 per transaction**
range from `upay-model.md` §2.1a. **AI:** predict each customer's recurring cash-out occasions and match
them against a nearby upay-QR acceptance surface, then accept the swap only where the full-loop net is
positive. A rule cannot do it because "push QR everywhere" destroys margin on the sub-break-even half of
the base, and the break-even depends on the merchant's own cash-out behaviour — a joint, customer×merchant
counterfactual. **Data:** **synthetic transaction panels + OSM merchant geometry**; real upay data would
add actual merchant cash-out behaviour, the number the whole break-even turns on. **48-hour demo:** the
judge opens one customer's month, sees which three cash-outs the engine would intercept and the full-loop
taka per interception, then picks a customer with no nearby upay-QR merchant and watches the engine
**decline to nudge** — and shows the customer-side fee saving in Bangla.

### 8. Acceptance-Gap Sniper — onboard merchants where cash density is proven and QR is absent

**TRACK:** 05 Merchant & Agent Intelligence · **LEVER:** 7 (merchant volume) · **MECH: network design +
incentive.** **User:** upay's merchant-acquisition field lead with an onboarding quota and no map —
Bangla QR has ~1m merchants but is still **0.5% of NPSB value** (`upay-model.md` §4 Lever 7), so the
constraint is not merchants signed, it's *merchants placed where cash actually changes hands*. The job:
*rank un-onboarded storefronts inside cash-dense, QR-empty cells, and pay field agents for predicted —
not raw — onboarding yield.* Similar *shape* to *Agent Coverage Optimizer* (`ideas-4-6` #9) but a
different supply: that placed upay's own agents; this ranks third-party merchant prospects whose economics
are MDR + proceeds cash-out, and the mechanism change is **field commission tied to model-predicted
yield**, so gaming the quota stops paying. **Money (L7):** `prospect_value_year = predicted_QR_volume ×
MDR_net + predicted_proceeds_cashout × 8.00`; absolute taka is small today by the lever's own admission —
the strategic claim is mix direction, stated as such. **AI:** a demand surface (footfall proxies, POI
density, agent-adjacent cash-in patterns from OSM — https://www.openstreetmap.org/copyright) crossed with
per-prospect conversion propensity. A rule cannot do it because two shops 50m apart can differ 5× in
addressable cash turnover and the surface is continuous — there is no cell-based threshold that survives
contact with the geometry. **Data:** **public (OSM) + synthetic spend surface with injected hotspots**;
real upay data would replace the proxy with actual agent-network cash density — the single strongest
proprietary input upay owns for this. **48-hour demo:** the judge clicks a market cell, sees the cash
density heat, the three ranked prospects with their predicted annual taka, and the optimizer **declining**
a fourth prospect because an existing upay merchant already captures that demand.

### 9. Settlement-Timing Yield Desk — pay merchants to let upay hold the balance one more day

**TRACK:** 05 (also 07) · **LEVER:** 7 (merchant volume, float line) · **MECH: who-pays + pricing.**
**User:** the merchant collecting QR proceeds who currently sweeps to cash daily — at upay's
**Tk 8.00/1,000** merchant cash-out rate (third-party, UNVERIFIED — https://www.ink.bd/1848/bangla-qr-payment-charges),
sweeping is itself a cost — and upay's treasury owner, whose **float earns a 9.33% implied yield**
(bKash FY2024 audited — https://www.legacy.bracbank.com/financialstatement/bkash-limited-audited-financial-statements-december-31-2024.pdf).
The job: *price each merchant a transparent T+1 settlement option — upay holds the day's proceeds and
shares part of the float yield back.* The mechanism change: **who earns the settlement window** flips from
nobody (instant sweep) to a negotiated split. **Money (L7/float):** `Δfloat_income = held_value × 9.33% ×
Δdays`; at Tk 1bn of QR settlement held one extra day ≈ **Tk 2.56 lakh/day** — small against the Tk 66 cr
anchor, so this is pitched honestly as a per-merchant compounding margin line, not a headline. **AI:**
predict which merchants can tolerate T+1 without losing sales to cash-stockouts (ledger liquidity buffer,
weekday pattern, inventory turnover proxies) and what compensation clears. A rule cannot do it because
liquidity sensitivity is heterogeneous and invisible: two grocers with identical volume differ in whether
a one-day delay causes a stockout, and a flat offer either overpays the tolerant or churns the tight. **Data:**
**synthetic merchant ledgers with injected stockout events**; real upay data would add actual sweep
behaviour and stockout-correlated refunds. **48-hour demo:** the judge toggles a merchant between instant
and T+1 and watches upay's float ledger and the merchant's yield share recompute; then opens a
liquidity-tight merchant the desk **refuses to move** — with the predicted stockout that refusal avoids.

### 10. Cross-Operator Leak Plug — stop paying Tk 5–8 per 1,000 to your competitors' merchants

**TRACK:** 06 Operations & Service Intelligence (also 02) · **LEVER:** 7 (merchant volume) · **MECH:
incentive + ranking.** **User:** the upay customer standing at a competitor's QR sticker because it is
the nearest shop — and upay's finance owner who publicly disclosed absorbing **Tk 5–8 per Tk 1,000** on
exactly those transactions with **IRF zeroed** (https://thefinancialexpress.com.bd/trade/bangla-qr-misuse-raises-concerns-over-mfs-sustainability,
15 Sep 2026). The job: *predict which upay customers will pay cross-operator QR in the next seven days
and reorder their in-app "nearby" merchant list so a comparable upay-QR option surfaces first — funded
from the leak itself.* The mechanism change: **the avoided leak is the reward budget** — savings finance
small merchant-side or customer-side incentives, so the programme is self-funding rather than a marketing
line. **Money (L7):** `saved = rerouted_value × Tk 5–8/1,000`; at the Tk 2,132 average ticket that is
**Tk 11–17 per rerouted payment** — the highest-certain-margin per-transaction figure in this lever,
because it is a disclosed cost being avoided, not a speculative fee being won. **AI:** ranking under a
budget — predict cross-operator payment propensity per customer, match against the upay-QR acceptance
surface, and rank the in-app list so the nudge fires only where a genuine alternative exists. A rule
cannot do it because "always show upay merchants first" degrades the list for the 90% with no upay
alternative nearby (and destroys trust in the feature), and propensity varies by payday, corridor and
merchant category. **Data:** **synthetic payment panels + OSM merchant layer**; real upay data would add
actual cross-operator interchange records — the ledger that makes the leak precisely countable. **48-hour
demo:** the judge plays a customer payment at a competitor QR, sees the app surface a comparable upay
merchant, watches the leak-savings ledger tick over in taka, and then tests the honesty case: a payment
with **no upay alternative** gets a clean, unmanipulated list.

### 11. Merchant Fee-Elasticity Guard — targeted fee relief where it causes acceptance to survive

**TRACK:** 04 Growth & Campaign Intelligence (also 05) · **LEVER:** 7 (merchant volume) · **MECH: pricing
+ incentive.** **User:** the small merchant publicly resisting Bangla QR fees — merchant resistance to the
**minimum 1% MDR** is documented, the BMPCA is lobbying for **0.25%**, and Bangladesh Bank has created a
**Tk 100 crore** subsidy fund (https://online-d11.thedailystar.net/business/economy/news/bangla-qr-adoption-faces-resistance-over-merchant-fees-4236621 ·
https://thefinancialexpress.com.bd/trade/scrap-bangla-qr-service-charge-to-build-cashless-bangladesh-bmpca ·
https://www.thefinancialexpress.com.bd/trade/bangla-qr-misuse-raises-concerns-over-mfs-sustainability) —
and upay's merchant-pricing owner who must keep acceptance alive without blanket fee holidays. The job:
*give fee relief only to the merchants who would actually drop QR without it, and let the inelastic
merchants keep paying.* Differentiation from *Incremental Offer Fund* (`ideas-1-2-3-8` #2): that funded
transaction offers to customers; this prices **the merchant-side fee itself**, the object of the live
regulatory fight. **Money (L7):** `retained_MDR = merchants_saved × predicted_QR_volume × MDR_net −
holiday_cost`; sized against the Tk 100 cr subsidy pool as the external benchmark for what fee relief
costs the industry. **AI:** fee-elasticity estimation per merchant plus an **uplift** gate — the holiday
must *cause* the acceptance to survive. A rule cannot do it because the merchants who complain loudest are
not the ones most likely to leave, and blanket relief hands margin to merchants who would have accepted QR
at 1% anyway — a distinction invisible to any rule keyed on complaint volume or size. **Data:** **synthetic
merchant panel with injected true elasticities including a loud-but-loyal decoy segment**; real upay data
would add observed acceptance drops around the Jul 2026 MDR floor. **48-hour demo:** the judge raises the
fee slider; the guard exempts exactly the elastic cohort, keeps charging the loud-but-loyal decoys, and
shows the holiday-spend vs retained-MDR curve with the uplift model's refusal to fund a non-incremental
merchant.

### 12. Failed-QR Recovery — a failed payment is a recoverable event, not a lost customer

**TRACK:** 06 Operations & Service Intelligence · **LEVER:** 7 (merchant volume) · **MECH: workflow.**
**User:** the customer whose QR payment fails at the counter and who — in the awkward silence — opens a
competitor app instead, and upay's support owner who eats the resulting ticket volume. The job: *at the
moment of failure, decide the one recovery action most likely to complete the payment — instant retry,
add-money-then-retry, alternate rail — or declare it unrecoverable and route to a human.* **Money (L7 +
06 adjacency):** `recovered_value × (MDR_net + merchant_cashout_net)` per saved transaction plus avoided
support cost; every recovered payment is merchant volume the mix-shift thesis needs, at the highest
conversion moment there is — the customer already decided to pay digitally. **AI:** failure-cause
prediction from the failure signature (timeout vs insufficient balance in source vs connectivity vs
merchant-side), where the same surfaced error code maps to different optimal remedies. A rule cannot do it
because the error code is not the cause — a "timeout" is retryable in one network state and fatal in
another, and retrying a dead payment actively sours the customer; the mapping is probabilistic and
state-dependent. Responsible-AI framing: no payment is auto-executed without the customer's explicit tap,
and the unrecoverable declaration always routes to a human — no consequential automated denial. **Data:**
**synthetic failure logs with injected cause-remedy ground truth and a clean held-out set** (official §11
test discipline); real upay data would add real failure distributions across networks. **48-hour demo:**
the judge injects three failures; one is recovered by retry, one by an add-money prompt, and the third is
**declared unrecoverable** with the reason shown and a hand-off to support — the refusals are the
credibility.

---

## 2. Compliance check against the brief

| Requirement | Status |
| --- | --- |
| ≥5 ideas change a mechanism, not add a model to a screen | **12 of 12** carry a `MECH:` tag. The sharpest: #1 *marketplace (priced leads)*, #2 *who-pays (deposit funds the offer)*, #3 *who-pays (employer bounty)*, #5 *who-pays (partner buys the list)*, #7 *incentive (self-funding swap)*, #8 *network design + incentive (predicted-yield commission)*, #9 *who-pays (settlement-window split)*, #10 *incentive (leak-funded)*, #11 *pricing (targeted fee relief)* |
| ≥4 in Tracks 02, 04, 05 or 06 | **11 of 12** — #1 (02/05), #3 (02/04), #4 (06), #5 (04), #6 (04), #7 (02/04), #8 (05), #9 (05/07), #10 (06/02), #11 (04/05), #12 (06). #2 is Track 03 (flagship), deliberately kept |
| Not a generic chatbot | no open-ended chat surface; every idea terminates in a price, a ranked list, a settled contract, an executed remedy, or a refused action |
| Not a generic dashboard | each ends in an executed decision; the engines that must say "no" (#1 unlisted lead, #2 capped debit, #4 no-cause-found, #6 do-not-contact, #7 declined nudge, #8 declined prospect, #9 refused T+1, #11 non-incremental holiday, #12 unrecoverable) are the product |
| Not accuracy-as-product | every model output is priced in taka of reactivation, float, avoided leak, retained MDR or recovered payment; #1, #4, #5, #6, #11, #12 are scored against injected ground truth, not AUC |
| Track 01 conflict (`CONTEXT_v3.md` §0) | **avoided entirely** — no fraud, scam, account-takeover, mule or AML idea anywhere |
| Other banned themes | no phishing, spoofing, deepfake, OCR of paper documents, Bangla ASR, generic churn dashboard (#6 is an *action* product that suppresses contact, not a churn dashboard) |
| "AI beats a deterministic rule" (official §13) | each idea names the specific rule that fails and why; #1, #4, #6, #7, #10, #11, #12 show the model overruling that rule on a live case |
| Responsible AI / fairness (official §14) | #2 caps the debit and shows the math; #4 diagnoses with human-approved remedies; #6 is itself a non-manipulation product; #7 shows the customer their saving in Bangla; #12 keeps every execution customer-tapped with human fallback; no idea autonomously approves/denies a consequential financial decision |
| Evidence discipline | every external figure reuses a URL already verified in `upay-model.md` / `CONTEXT_v3.md`, is derived from them, or is marked **UNVERIFIED** |
| No `R` printed as a number | upay revenue and user counts never stated; dormant base and taka figures quoted with the bKash anchor named and upay applicability flagged UNVERIFIED |

## 3. What I did not do

- **No Track 01 idea.** `CONTEXT_v3.md` §0 remains unresolved; that is a team decision, not mine to make.
- **No `analogs.md` cross-check.** The file does not exist in this repo (re-verified 3 Oct 2026).
- **No taka figure resting on a UNVERIFIED upay quantity.** upay's dormant base, its merchant count, its
  current agent cash-out rate, its net share of MDR, and merchant cash-out at Tk 8.00 are all flagged
  inline; the L7 break-even in idea #7 is stated as a range, not a point.
- **No edit to `upay-model.md` or `upay-model-calc.py`.** The corrections recorded in the previous two
  idea files remain live in the source model.
- **No re-cover of levers 1, 2, 3, 4, 6, 8.** Adjacencies to prior ideas (#1↔Sponsor Market, #4↔Complaint
  Autopsy, #7↔Cash-Out Substitution Bounty, #7↔Incremental Offer Fund, #8↔Agent Coverage Optimizer) are
  differentiated inline rather than hidden.
