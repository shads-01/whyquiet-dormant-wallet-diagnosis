# Mix-shift thesis — converged build spec

> Follows `docs/v3/CONTEXT_v3.md` §12 rule 2: pick **one** idea. This document converges the
> mix-shift lane (ideas #10, #12, #6, #8 in `docs/v3/ideas-1-2-3-8-upay-model.md`) onto a single
> buildable product and records why the other three were killed.
> Depends on the corrected arithmetic in `upay-model.md` §4 (patched 3 Oct 2026).

---

## 1. Why mix shift, specifically

> **REVISED 3 Oct 2026 after a pricing re-check.** The first version of this section claimed "upay's
> take rate on cash-out is ~43% of bKash's." **That was wrong** — it compared upay's **UCB ATM** rate
> (0.80%) against bKash's **agent** rate (1.85%). Like-for-like, upay's agent rate is **1.40%, about 24%
> below bKash's 1.85%**, not 43% below. The conclusion survives, but it now rests on different and much
> better evidence, set out below. See `upay-model.md` §2.1 for the corrected ladder.

| Fact | Figure | Source |
| --- | --- | --- |
| upay **agent** cash-out charge | **1.40%** (Tk 14/1,000), inclusive of VAT and taxes — *tiered in practice, current rate UNVERIFIED* | https://www.tbsnews.net/companies/ucbs-upay-offers-lowest-cash-out-fee-234661 (Apr 2021) |
| upay **merchant payment, charged to the customer** | **Free** — "B & M Purchase (In-Store Payment) Free" | upay FAQ (COO-signed), https://www.ucb.com.bd/reports/downloads/Upay/upay-faq.pdf |
| Bangla QR **MDR**, paid by the *merchant* | **Minimum 1%** incl. VAT, mandated from 1 Jul 2026 | https://networkbangladesh.com/bangladesh-bank-sets-minimum-1-merchant-fee-for-bangla-qr-transactions-to-boost-digital-payments/ |
| **Interchange Reimbursement Fee** | Set to **zero** by Bangladesh Bank for Bangla QR | https://thefinancialexpress.com.bd/trade/bangla-qr-misuse-raises-concerns-over-mfs-sustainability (15 Sep 2026) |
| **upay's own disclosed cross-operator QR cost** | **"Tk 5 to Tk 8 per Tk 1,000"**, and upay publicly demanded a cost-recovery mechanism instead of a blanket zero IRF | same |
| Cash-in + cash-out as a share of all MFS value | **49.7%** | BB Oct-2025, computed in `upay-model-calc.py` |
| Cost of services | **63.18%** of revenue, agent commission the obvious target — **split UNVERIFIED** | https://en.bonikbarta.com/business/dt2VlJjSIXS99Mic |

**The real argument, which is stronger than the one I first wrote:**

1. **The customer's saving from switching is the entire cash-out charge, not a marginal rate difference.**
   Merchant payment is free to the upay customer; cash-out costs **up to 1.40%**, and upay's own CEO
   described the schedule as tiered *below* the Tk 14 headline with some wallet tiers free
   (https://today.thefinancialexpress.com.bd/trade-market/upay-offers-lowest-cash-out-fees-highest-client-security-1628439154,
   9 Aug 2021). At the Oct-2025 average cash-out ticket of Tk 2,132 that is a customer saving of roughly
   **Tk 11–30 per transaction — a range, not a point.** A substitution bounty therefore has an
   unusually large, honest, customer-side justification, and the brief's guardrail against manipulative
   recommendation is satisfied, because the customer keeps money rather than spends it. The range is the
   thing to design against: the prototype must *segment by wallet tier*, because a primary-wallet
   customer and a salary-wallet customer need different bounties.
2. **upay's revenue is concentrated on the one product that pays agent commission.** Merchant payment
   is free at the customer end, so upay's economics on it are the merchant MDR against whatever
   processing cost it carries — it is not the 1.4% commission line.
3. **upay is currently on the wrong side of a live regulatory dispute.** With IRF zeroed and a 1% MDR
   floor, upay stated publicly on 15 Sep 2026 that it absorbs Tk 5–8 per 1,000 on cross-operator QR
   while earning 1.4% on its own cash-out. A merchant payment that stays **on upay's own rails** avoids
   that cost entirely.
4. So the prize is not revenue per transaction. It is **(a)** the agent commission inside the 63.18%
   cost-of-services base that stops being paid, **(b)** MDR captured on upay's own QR instead of the
   1.4% paid away on cash-out, and **(c)** the IRF cost avoided by keeping the transaction in-house.
   Points 1 and 3 are new and dated; together they make this a *2026* story rather than a
   cost-programme story.

And the official brief hands us the product spec in plain language (Track 03 worked examples,
`CONTEXT_v3.md` §3):

> *"How can I reduce cash-outs?" → where digital alternatives could replace repetitive cash withdrawal*

That is not our framing imposed on a track. That is the brief describing this product.

### The honest caveat this revision creates

Substituting a 1.4% cash-out with a 1% merchant MDR is a **revenue-reducing** trade at the top line.
The case only closes if the saved agent commission plus captured float exceeds the lost 0.4% spread.
**That is unprovable from public sources** — upay's agent commission share, its net merchant QR revenue,
and its current agent cash-out rate are all **UNVERIFIED**. So the prototype's job on the economics side
is to produce a **breakeven band** and to show which side of it the published price ladder plausibly
lands on — not to assert a positive number. This is now the single largest risk to the thesis and is
promoted to §7's first kill criterion.

---

## 2. The product — **Substitution Desk**

An internal-facing tool (and a customer-facing nudge) that decides, per customer and per month, **how
much upay will pay to move a specific recurring cash-out onto a merchant QR payment** — and refuses
to pay for shifts that would have happened anyway.

The mechanism change: **incentive + who-pays**. Today upay hopes a campaign moves behaviour and
cannot tell whether it did. Here upay buys a specific behaviour change, prices the bounty against the
commission it will save, and the model is required to *decline* customers who are already migrating
on their own.

### Economics

Per **displaced** cash-out (one cash-out the customer stops making, one merchant payment they make instead):

```
value_per_displaced_cashout = commission_saved            # agent commission upay stops paying  [UNVERIFIED]
                             + MDR_earned_own_rail        # merchant pays upay the acquiring fee
                             − processing_cost           # upay discloses Tk 5–8/1,000 on cross-operator QR
                             − cashout_fee_lost          # 0.5%–1.4% of ticket, depending on wallet tier

accept_bounty ⟺ predicted_displaced_cashouts × value_per_displaced_cashout  >  total_bounty_paid
bounty_cap_per_displaced_cashout = value_per_displaced_cashout
```

Note the sign structure, because it is the whole risk: `MDR_earned_own_rail` is at most the 1% BB
floor while `cashout_fee_lost` is at least 0.5% and at most 1.4%. In the **worst** case the fee-to-fee
swap is **positive** (1.0% − 0.5%), in the **best** case it is **negative by ~0.40%** (1.0% − 1.4%). The
direction of the top-line trade therefore *depends on which wallet tier the customer sits in*, and the
model must segment on it rather than assume either case. Only in the negative case does the deal depend
on `commission_saved` clearing the gap. Showing both branches is what makes the product honest — a
version that quietly picked the favourable tier would be assuming the answer.

**`commission_saved` is the UNVERIFIED quantity.** Per `upay-model.md` §2.6 we must not quote an agent
commission share. So the prototype does two things:

1. **Sweeps** `commission_saved` across a plausible range and reports the **breakeven** — the
   commission share at which `value_per_displaced_cashout` goes to zero — as a *computed output of the
   sweep*, printed next to the range that was swept. The demo must not hard-code this number; if a
   judge changes the assumed commission share, the breakeven moves and the screen shows it move.
2. **Never prints `R`.** Value is stated as a ratio that does not require knowing upay's undisclosed
   revenue: bounty paid per 1,000 cash-outs displaced, and bounty as a share of the commission saved.

Any specific figure for the breakeven is an **output to be computed on the day from the sweep**, not an
input to be asserted in a deck.

### Secondary line

Frequency. A substituted cash-out usually adds a merchant payment *and* reduces the cash-in that was
funding it, so net transactions per active user is a **measured, possibly negative** outcome. Report
it as measured. If it is negative, say so on the slide — that honesty is worth more than a fake win.

---

## 3. The AI, and the rule it beats

**Task:** estimate a *dose-response curve* `P(≥1 cash-out/month discontinued | bounty = t)` per customer,
and integrate it against the cap above.

**Model:** two-part.
- A propensity model (LightGBM) over features a rule cannot combine: cash-out frequency and ticket
  distribution, **distance to nearest agent** (public OSM, https://www.openstreetmap.org/copyright),
  merchant-category spend already visible on the wallet, cash-in cadence, prior campaign exposure,
  and agent-float reliability in the customer's area.
- A dose-response head that predicts the *increment* per bounty band rather than a yes/no, so the
  tool can find the efficient point and refuse overpayment.

**The rule it beats — stated precisely, because §13 of the brief is the line weak ideas cross.**
The obvious deterministic version is: *"give Tk 50 to every customer with ≥4 cash-outs/month and
distance-to-agent > 2km."* It fails on three counts the prototype will demonstrate live:
1. It pays the **already-migrating** customers, who need no bounty — pure waste.
2. It pays the same Tk 50 to a customer 500m from an agent and one 5km away, when the second is worth
   several times more.
3. It cannot express *diminishing returns*, so it never stops.

**Eval:** because the synthetic generator carries **known ground-truth dose-response for every
customer**, the model is scored against the answer key — not on AUC. Report the **money**: total
bounty spent to achieve a given number of displaced cash-outs, versus the rule, versus the oracle
ceiling. Three numbers, one chart. That chart is the demo.

---

## 4. Synthetic data — the part that must be right

The data rule is permissive (`CONTEXT_v3.md` §4: synthetic / public / self-generated, every assumption
documented, clean held-out set). The generator therefore has to be **honest about its own truth**,
because the whole evaluation rests on it.

Required structure:
- **Customers** with heterogeneous cash-out needs: a commuting worker, a shop owner who needs cash for
  stock, a student, a remittance recipient. Each gets a *latent* substitution elasticity.
- **Ground truth** `θ_customer` and `displaced(bounty)` stored separately from the observable
  features, so the oracle is available for scoring but never for training.
- **Deliberate traps**, each of which a response-model or rule version gets wrong:
  - *already-migrating* segment — shifts with or without any bounty;
  - *negative-uplift* segment — a bounty makes them cash out *more* (the brief's own warning against
    manipulative recommendation applies to our own intervention);
  - *float-inelastic* segment — their agent never runs out, so substitution is impossible regardless of
    bounty, and a naive model reads their cash-out volume as opportunity;
  - *seasonality* — Eid and month-end shift both the cash-out rate and the elasticity.
- **Clean test set** never touched in training, per the brief.
- Calibration: cash-out volume and ticket distribution calibrated to BB Oct-2025 (174.56m cash-outs at
  Tk 2,132 avg; 142.55m cash-ins at Tk 2,898).

**What real upay data would add, and why it is not a blocker:** inter-FS transaction visibility (to
confirm substitution actually happened rather than moving to a competitor), real agent float
reliability, and real merchant-category spend. The prototype calibrates the *shape* of all three from
public structure; only the *magnitudes* are missing.

---

## 5. Build order for 72h, with seams for the requirement drop

`CONTEXT_v3.md` §1 warns that judges hand out new requirements on the day, so every seam is a real
module boundary (also required by official §12: data prep separate from inference, rules separate from
model output).

| Phase | Module | Note |
| --- | --- | --- |
| 1 | `datagen/` — generator + ground truth + held-out split | Pure Python/numpy, no model deps. Reusable if the requirement drop is "change the population". |
| 2 | `models/` — propensity + dose-response heads | Trained on `datagen` output only. Boundary = pickle/ONNX swap. |
| 3 | `pricing/` — the cap, the accept/refuse rule, the breakeven sweep | **Business rule, deterministic, separately testable.** Requirement drop "change the payout policy" lands here, not in a prompt. |
| 4 | `api/` — FastAPI: `/profile`, `/price`, `/allocate`, `/explain` | Every response carries reasons, not just a number (§12 traceability). |
| 5 | `web/` — Substitution Desk console | Judge-tryable surface. |
| 6 | README, live deploy, video, report | `CONTEXT_v3.md` §9. Budget time; these are graded. |

---

## 6. The demo a judge can try

Ninety seconds, on a phone-sized screen. **Framing must be a fixed target, not a fixed budget** — the
obvious way to script this compares the rule and the model at *different* spend levels, which flatters
whichever one spent more. The honest comparison holds the objective fixed and lets cost vary.

The run, against a target of **39,800 displaced cash-outs** from a 100,000-customer synthetic population:

| Pricer | Cost to hit the target | Per 1,000 displaced |
| --- | --- | --- |
| The deterministic rule | **misses it** — Tk 4.86m buys only 36,900 | — |
| **Our dose-response model** | **Tk 2.61m** | **Tk 66** |
| Oracle (knows ground truth) | Tk 2.35m | Tk 59 |

The script:

1. Judge sees the rule miss the target, and sees **where** it misses: Tk 4.86m spent, 2,900 short, and
   the top of the screen lists the customers it paid that bought nothing.
2. One click on **"price with dose-response"** — **Tk 2.61m, target met, 46% cheaper than the rule.**
3. Judge asks the obvious question: "is that just under-spending?" The tool answers with the **oracle**
   row: Tk 2.35m, so we are **11% off the best achievable**, and the remaining gap is displayed as a
   stated limitation rather than hidden.
4. Judge opens one already-migrating customer: **bounty Tk 0**, reason "this customer is migrating on
   their own; paying here buys nothing."
5. Judge opens one negative-uplift customer: **bounty refused**, with the elasticity curve on screen
   showing it bending the wrong way.
6. Judge drags the **assumed agent-commission share**. The breakeven moves live, and the screen shows
   which side of it the assumed value sits — this is the honest version of the economics, and it is
   more persuasive than a confident number would be.

Steps 4 and 5 are the ones that matter. A tool that only ever says yes is a budget spender; a tool that
shows its own refusals is a decision system.

**All figures above are illustrative placeholders for a synthetic population, to be regenerated live by
the build.** They must not be hard-coded, and no figure from this table may appear in the deck as a
result.

---

## 7. Kill criteria — decide these now, not at 4am

- **NEW, and now first: if the breakeven agent-commission share required for substitution to be
  margin-accretive falls outside the range a published price ladder can plausibly support, the bounty
  is unaffordable and the thesis is dead.** Worked example of the arithmetic the prototype must run:
  losing `1.40% − MDR 1.00% = 0.40%` of ticket value at the top line, against `commission_saved −
  bounty`. If `commission_saved` cannot exceed ~0.4% of ticket value plus the bounty, there is no deal.
  This must be shown as a **band with the unknowns visible**, never as a point estimate. If the band
  cannot exclude the bad outcome, kill the idea rather than assume a favourable commission rate.
- If the model cannot beat the rule by **≥25% on money-per-displaced-cash-out**, it is a dashboard
  with a budget attached. Kill it and fall back to the Agent Shift Market (idea #3), which has a cleaner
  structural story and needs no causal identification.
- If honest calibration shows the *customer-side* saving is not ~1.4% of ticket value — i.e. if upay's
  agent cash-out rate is in fact the tiered 0.5–0.7% structure reported by
  https://newisty.com/upay-charge-calculator — the bounty shrinks proportionally and may fall below
  behavioural noise. **Resolve the current agent rate before committing**; see `upay-model.md` §2.1.
- If judges read the intervention as *paying people to use less of the product*, the framing is wrong
  and no amount of model quality saves it. Mitigation: the brief names this use case explicitly, so the
  pitch must quote it in the first 30 seconds — and because merchant payment is free while cash-out
  costs ~1.4%, the tool can show the customer their own ~Tk 30-per-transaction saving, which makes the
  customer a beneficiary of the intervention rather than its object.

## 8. What was killed, and why

- **#12 Campus Closed Loop** — killed on *business impact*. Highest possible relevance (DIU is inside
  Daffodil Group, which upay has an MoU with) but it is Lever 7, which `upay-model.md` §4 rates "small
  in current revenue terms". The AI component (merchant liveness) is also the thinnest of the four. Keep
  it as the **on-site requirement-drop absorber** — if judges say "make it campus-specific", this is the
  module we point at, and that is exactly what it is good at.
- **#6 Autopay Subscriptions** — killed because upay's bill pay is reportedly free of charge
  (**2021** report, above), so the direct revenue is near zero and the L3 frequency gain is unproven in
  direction. Viable only as a *feed* into this product: subscriptions reduce cash-out need, which is
  the substitution Desk's input. Do not build it as a standalone.
- **#8 Restock Credit** — killed on scope. Credit underwriting against a merchant forecast is a
  two-product build (forecast + underwriting) and it touches **Lever 8, whose base is UNVERIFIED**
  (secondary source only). It is the strongest idea we would be wrong to attempt with 72 hours.

---

## 9. Open items a judge may probe — answer before pitching

1. What is upay's actual merchant-side net revenue, and its actual agent commission share?
   **Both UNVERIFIED.** The prototype answers with a sensitivity band and a breakeven, not a number.
2. How do you know a displaced cash-out did not simply move to bKash?
   **Honest answer: you cannot, without inter-FS visibility.** Say this out loud. It is the strongest
   credibility signal available and it costs nothing to admit.
3. What is upay's dormant base and 90-day active rate? **UNVERIFIED** — inherited from
   `upay-model.md` §6.
4. **What is upay's current agent cash-out rate?** Sources conflict: **1.40%** (Tk 14/1,000, inclusive of
   VAT and taxes) from TBS 2021 and two 2026 third-party calculators, versus a tiered **0.7% primary /
   0.5% remittance, disbursement and salary** schedule labelled updated 18 Sep 2026
   (https://newisty.com/upay-charge-calculator). Business Standard's Dec 2022 wording — "Tk14 per Tk 1,000
   in different layers to even free of cost" — is consistent with tiers existing. **UNVERIFIED.**
   **ACTION: retrieve https://www.upaybd.com/limits-and-charges manually and pin this.** Automated
   retrieval of upay's own charges page failed on 3 Oct 2026. Everything in §1 scales off this number.
5. Does upay pay a 1% MDR merchant-side fee, or less? Bangladesh Bank set a **1% minimum inclusive of
   VAT** from 1 Jul 2026, but individual PSP pricing below the floor is **UNVERIFIED** and upay's own
   published MDR is **not public**. This is the other number that decides the thesis.