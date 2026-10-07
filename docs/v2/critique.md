# critique.md — skeptical judge pass over `docs/v2/solutions.md`

Written 3 Oct 2026. Inputs read: `docs/CONTEXT.md`, `docs/v2/CONTEXT_v2.md`,
`docs/v2/solutions.md`, plus web checks. **Every claim in `solutions.md` was treated as
untrusted data.** I did not read `docs/v2/problems.md` or `docs/01-data/inventory.md`, so every
number `solutions.md` inherits from them is second-hand and marked UNVERIFIED below.

## Judge's standing (per CONTEXT_v2 rule 3)

I may kill a solution **only** for:
- (a) already solved in Bangladesh, with a URL to a working product;
- (b) blocked by a named law or regulator;
- (c) nobody would use it, with named evidence.

Small samples, weak labels, simulation-only evidence, difficulty, and "an LLM could do this"
are **FIX ITEMS**, recorded as fix items.

---

## 0. External verification performed

### Confirmed by search (used as evidence below)

| Fact | Source |
|---|---|
| **MFS platforms may not lend from their own funds.** "MFS platforms will not engage in any lending from their own funds, but will be free to act as agents of BB licensed banks and financial institutions in disbursing loans and in accepting repayments on behalf of the principals concerned." | BB *Regulatory Guidelines for Mobile Financial Services in Bangladesh* (rev. Jul 2015), cl. 6.6 — https://www.bb.org.bd/aboutus/draftguinotification/guideline/mfs_final_v9.pdf ; superseded in form by *Bangladesh Mobile Financial Services (MFS) Regulations, 2018*, https://www.bb.org.bd/mediaroom/circulars/psd/jul302018psdl04e.pdf |
| **PSS Act 2024 criminalises unauthorised lending.** "Without approval of Bangladesh Bank, any type of investment taking, lending, deposit or financial transaction through online or offline is prohibited." Penalty: up to 5 years' imprisonment or Tk50 lakh or both. | *Payment and Settlement Systems Act, 2024* (passed 4 Jul 2024) — summarised by BB Payment Systems Report Jun 2024, https://www.bb.org.bd/pub/annual/psdreport/paymentreport_jun2024.pdf ; and TBS 6 May 2024, https://www.tbsnews.net/bangladesh/law-order/payment-and-settlement-system-bill-protect-customers-interest-placed-js-844836 |
| **PSS Act 2024 settlement finality.** "Any settlement executed in accordance with established procedures is regarded as **final, irrevocable, and without dispute**." | BB Payment Systems Report 2025, https://www.bb.org.bd/pub/annual/psdreport/paymentreport_dec2025.pdf |
| **Bangladesh Bank already mandates removing the cash leg from Bangla QR.** "If any merchant is found using Bangla QR for cash-out activities instead of payments, the facility must be cancelled immediately." Acquiring institutions "are required to actively monitor transaction patterns and prevent misuse, such as artificial transaction splitting or **unauthorised cash-outs**." | BB circular, 1–3 Apr 2026, mandatory Bangla QR adoption — https://www.thedailystar.net/business/news/banks-mfs-providers-asked-adopt-bangla-qr-june-or-face-penalties-4141576 |
| **IRF set to zero and the 1% MDR floor repealed, effective 1 Oct 2026.** | https://www.thedailystar.net/business/economy/news/bb-waives-merchant-fees-boost-bangla-qr-adoption-4244786 |
| **Customer charges require central-bank prior approval.** "Any customer charges will require prior approval from the central bank"; TSA shortfall penalty is the lower of SLF (11.50%) or Tk30 lakh; directors/CEO/treasury personally liable. | BB draft *Payment System Operator (PSO) Regulation, 2025* — https://www.bb.org.bd/aboutus/draftguinotification/guideline/PSO_Regulation.pdf ; BSS 7 Nov 2025, https://www.bssnews.net/business/329457 |
| **IDRA is the sole regulator of the insurance sector in Bangladesh**; insurance business requires registration and certification by IDRA under the Insurance Act 2010 / IDRA Act 2010. | BB Financial Institutions Division — https://www.bb.org.bd/en/index.php/financialactivity/insurance |
| **Digital khata for Bangladeshi shopkeepers already ships as paid products**: Halkhata (offline-first POS + customer credit, ৳500–৳4,000/mo, https://halkhata.bd/), Dokan Khata (https://dokankhata.com/), BD Khata (https://bdkhata.com/), DebtX (https://debtx.netlify.app/). All are **typed** ledgers, none reads the existing paper book. | as linked |
| **bKash already has a self-service complaint channel** (Self Complaint / e-CMS, launched 19 Jan 2026), a 16247 helpline, a live-chat complaint cell, and "continuous awareness campaigns … collaborating with BFIU". | https://www.tbsnews.net/economy/corporates/bkash-introduces-self-complaint-system-faster-service-1338251 ; https://www.bkash.com/en/customer-service/avoid-fraud |
| **bKash scale**: 350,000+ agents, 900,000 merchants, 83m+ customers (Apr 2026). | https://www.bkash.com/en/about |
| **Merchant credit off transaction history already ships in Bangladesh**: bKash + BRAC Bank merchant loan pilot. | https://www.tbsnews.net/bangladesh/bkash-deploys-largest-bangla-qr-network-nationwide-accelerate-cashless-payment-1495011 |
| **BB has authorised end-to-end digital bank lending (e-loan, ≤Tk50,000, 11 May 2026) and "e-Payment Credit" (6 Sep 2026, ≤Tk10,000, settlement of digital payment obligations only, data stored in Bangladesh).** | https://www.tbsnews.net/economy/banking/bb-allows-banks-offer-e-loans-tk50000-one-year-tenure-1436401 ; https://www.bb.org.bd/mediaroom/circulars/psd/jun082026psd08e.pdf (index date 06 Sep 2026: https://www.bb.org.bd/mediaroom/circulars/brpd/sep062026brpd-117e.pdf) |

### Explicitly UNVERIFIED (carried from `solutions.md`, not re-checked by me)

Pix 92.6%-at-≤R$200 and DICT's mandatory cross-scheme nature; GCash's "3,200 merchants blocked Mar 2026" and
"7,000+ since 2025"; Pix MED tiered refund R$200→R$5,000 and the 60-minute precautionary block; Pix's 6–7
per 100,000 fraud and 97% authorised-push shape; Alipay's 7-day dispute clock and 500,000+ external merchants;
Nubank Pix Protegido at R$5,000/yr for R$6.99/mo; M-Pesa Fuliza 33.4m users / KES2.9tn and IMF's 3–5am
trader-repayment finding; NPCI's ₹10 lakh/day P2M limit; Wave's free cash-in/out and the Dec 2022 agent revolt.
Also unverified because I did not read them: every figure `solutions.md` cites from `problems.md` and
`docs/01-data/inventory.md` — the ~1.85% cash-out rate, Tk5–8 per Tk1,000 upay loss, BDQR Tk370m→Tk1.1bn,
7.8m retailers, 2.4m agents, ≥Tk6.40 per Tk1,000 agent share, retailer BDT5–10 per Tk100, 62% facing 3–7
day settlement delays, Tk24,000→Tk81,000, ~Tk9,000 average fraud loss, 58.8% non-reporting, 38.1% resolution,
6.2% CIPC awareness, women at 42% of 239.3m accounts and <3% of 1.5m+ agents, the 1-in-3 discomfort figure,
and the 2.4m/1.5m+ agent and account counts.

### Structural problems found in `solutions.md` itself (not solution-level, fix at file level)

1. **P10 L2 and P10 L5.1 are the same AI decision.** Both score agent *discretion* behaviour and pay for it.
   L5.1 is L2 with the routing dropped. That is 1 solution listed twice, which inflates the apparent count.
2. **P2 L6(b) is a softer version of something BB has already mandated.** The 1 Apr 2026 circular orders the QR
   facility cancelled for merchants doing cash-out. `solutions.md` pitches *labelling* the same merchant at scan
   time instead. The difference (label vs cancel) is real and is GCash's lesson, but the pitch must not imply
   the absence of a rule — the judge will have read the circular.
3. **Inherited `SIM` calibration is one layer from an unread source.** The file's own closing note admits the
   recovery-pool, escrow and service-fee economics all trace to `problems.md`, not a ledger. Anything in the
   top 12 that leans on a taka number must carry a stated derivation in the pitch, not a citation.

---

# 1. Verdict on every solution

Format: **VERDICT** — reason or fix list.

## P2 — Bangla QR has become an unlicensed cash-out rail

**P2 L1 — Charge cross-operator QR at the cash-out rate, or refuse it. — KILL (b).**
The fee schedule is set by the regulator, not the operator. BB sets the IRF, set it to zero from 1 Oct 2026,
and repealed the 1% MDR floor in the same instrument; the PSO Regulation 2025 requires central-bank prior
approval for customer charges. An individual MFS setting a differentiated cross-operator tariff unilaterally
is a charge without approval. https://www.thedailystar.net/business/economy/news/bb-waives-merchant-fees-boost-bangla-qr-adoption-4244786
and https://www.bb.org.bd/aboutus/draftguinotification/guideline/PSO_Regulation.pdf

**P2 L2 — Sale-evidence badge on the QR checkout screen. — SURVIVE.**
- FIX-1. The badge must be framed as a **pricing input, never a suspicion**. `solutions.md` already says this; it
  must be in the UI copy, in the Bangla, in the demo, and in the fairness section.
- FIX-2. Replace the hand-specified feature set with one collected signal that no simulation can invent: 200 real
  merchant payment rounds across campus shops where the shopkeeper states the true basket after each payment.
  That turns weak labels into 200 weak labels *plus* 200 verified ones, which is enough for a demo and honest
  enough for a pitch.
- FIX-3. Report the confusion matrix per merchant-size band, not one accuracy number. The fairness criterion
  already mandates a group check; merchant size is the group that matters.
- FIX-4. The honest answer to "why not just cancel these merchants?" is that BB's circular already orders
  cancellation and it has not stopped the flow — say that out loud before the judge does.

**P2 L3 — Split the QR fee by evidence, not by rail. — SURVIVE, heavily conditioned.**
- FIX-1. The stated failure mode (recipient cannot pay a different rate) is a **settlement-rule** question, and
  PSS Act 2024 makes settlement "final, irrevocable, and without dispute". Resolve it before building: get the
  BDQR/NPSB rule in writing. If the rate is symmetric, this collapses to a discount and the evidence layer earns
  nothing — which is what `solutions.md` itself says.
- FIX-2. BB approval is required for any customer charge. Frame the *default* rate as the published schedule and
  the evidence-linked rate as a promotional campaign, which the 1 Jul 2026 MDR circular expressly contemplates
  ("Acquiring institutions … may still run promotional campaigns … even if that means offering rates below the
  new floor"). That is a legal footing, not a workaround. https://www.thedailystar.net/business/news/merchants-pay-least-1-fee-bangla-qr-transactions-4213416
- FIX-3. It is the P2 idea that actually changes **who pays**. Say that sentence in the pitch; nothing else in P2 does.

**P2 L4 — Delete the merchant's ability to move value out into cash. — KILL (a)+(b).**
Already solved in Bangladesh, by the regulator, in force. BB's April 2026 circular: "If any merchant is found
using Bangla QR for cash-out activities instead of payments, the facility must be cancelled immediately."
The "receipt terminal only" merchant is the regulator's prescribed state, not our invention. A pitch that asks
for it is asking for something already law. https://www.thedialystar.net/business/news/banks-mfs-providers-asked-adopt-bangla-qr-june-or-face-penalties-4141576
(see `RESCUE R1`)

**P2 L5.1 — Tax the receiver. — KILL (b).**
A unilateral fee on a person receiving a transfer is a customer charge. The PSO Regulation 2025 requires prior
central-bank approval for customer charges, and the PSS Act 2024 attaches up to 5 years / Tk50 lakh to
unauthorised transactions. The file's own objection — "legally indefensible to charge an ordinary person
receiving a legitimate gift Tk185" — is the same objection, raised by the file, not by me.
https://www.bb.org.bd/aboutus/draftguinotification/guideline/PSO_Regulation.pdf
(see `RESCUE R2`)

**P2 L5.2 — Merchant compliance bond. — SURVIVE.**
- FIX-1. A bond is a levy on merchants; it needs the same BB-approval footing as FIX-2 above, or it must be
  structured as a refundable float deposit against which fees are settled (which the PSO Regulation's Trust and
  Settlement Account regime already contemplates).
- FIX-2. The 30-shopkeeper interview must ask one question only: *at what monthly locked amount do you stop
  accepting upay QR?* That produces a real number, and a real number is the whole answer.
- FIX-3. Simulation is fine here (Lane B) but the loss signature — Tk10,000 in, ~Tk9,815 out — must be
  demonstrated on the 200 collected merchant rounds, not asserted.

**P2 L6(a) — Self-reported-scheme fraud mark (Pix DICT analogue). — SURVIVE.**
- FIX-1. A "check any upay number before sending" service is the cheapest high-wow item in the whole file and
  the easiest to build in 48h. Keep it.
- FIX-2. Legal footing must be stated: upay marks *its own* payees, publishes only what it assigned itself, and
  exposes it to its own customers. No cross-scheme data, no regulator.
- FIX-3. Do not claim fraud is recovered by marking — mark rate is an input to detection, not recovery. Say so.

**P2 L6(b) — Label the resolved merchant identity behind every QR at scan time (GCash analogue). — SURVIVE.**
- FIX-1. It is currently the highest-relevance idea in P2 and it must be positioned as *labelling versus
  blocking*, against GCash's 7,000+ merchant removals. State the trade: blocking loses merchants, labelling
  loses nothing.
- FIX-2. Disclose that BB's April 2026 circular already orders cancellation for cash-out merchants, and that the
  gap is not the rule but the resolution of *which number a QR actually points at* in the customer's hand.
  That reframing is both true and much stronger.
- FIX-3. Demo must include a QR that resolves to a personal wallet, because that is the moment judges understand.

## P8 — Digital money cannot move upstream

**P8 L1 — Cut merchant MDR to zero and subsidise. — SURVIVE as a stated non-answer.**
- FIX-1. It is a tariff lookup and fails CONTEXT's strict test 1. Keep it only as the 15-second strawman the
  executive already believes in, then kill it on stage with the arithmetic. Never list it as a candidate.

**P8 L2 — Khata reader (handwritten Bangla OCR → payment request). — SURVIVE.**
- FIX-1. **Differentiation is mandatory and must be spoken first.** Halkhata, Dokan Khata, BD Khata and DebtX all
  sell a digital khata to Bangladeshi shopkeepers today. The only thing none of them do is read the paper book
  the shop already has — Halkhata's own FAQ says you import an Excel/CSV and "anything you leave behind stays in
  the old book". That sentence is the whole pitch.
- FIX-2. Confidence gating is the product, not a safety feature. Below threshold, ask the shopkeeper; above it,
  propose the request. Show both paths in the demo.
- FIX-3. A wrong amount sent to a distributor is a real-world trust-ending event. Default to *propose, never
  auto-send*, and say that on stage.
- FIX-4. Held-out test set = khata pages from shops the team did not build the model on, photographed by a
  third party. Judges' own pages, if they consent, are the live demo.

**P8 L3 — Delivery-linked escrow for the wholesale leg. — SURVIVE.**
- FIX-1. The whole idea lives or dies on "what is proof of arrival". Collect it: 20 retailers and 10
  distributors, one question — *what do you already produce, without being asked, that proves goods arrived?*
  If the answer is "a phone call", say so on stage and pivot to `R4` rather than pretending.
- FIX-2. Holding customer funds while goods are in transit is taking a deposit. Confirm the trust/settlement
  treatment under the PSS Act 2024 / PSO Regulation 2025 TSA regime before the demo, and name it in the pitch.
- FIX-3. Merge with P8 L6(b): the consignment embedded in the dynamic QR is the evidence, the khata mark is the
  release trigger, escrow is the settlement. Three entries, one product. Pick one and say so.

**P8 L4 — Skip the retailer entirely (pay the distributor direct). — SURVIVE.**
- FIX-1. `solutions.md` already names the fatal flaw and it is fatal to the *economics*, not the idea: paying a
  distributor direct converts the retailer's receivable into a cash sale and destroys the distributor's
  working capital — the exact BDT1–2 per Tk100 they survive on. The pitch must confront this in sentence one.
- FIX-2. Rescue direction: only the *sub-distributor-to-retailer* leg can be deleted without touching the
  distributor's receivable. Say that on stage; it converts the objection into the demonstration of thought.

**P8 L5.1 — Subsidise the cash-out, openly. — KILL (c).**
Named evidence: upay's cash-out already runs at ~zero gross margin (the file's own figures: 1.304% revenue vs
~1.300% cost), so there is no economic room for a subsidy — and the customer's alternative is not upay. bKash
operates 350,000+ agents and 900,000 merchants with 83m+ customers and free cash-out at every one of them
(https://www.bkash.com/en/about). A merchant asked to prefer an upay agent for *free* cash-out when a bKash agent
is a five-minute walk away will not. Nobody uses it.
(see `RESCUE R5`)

**P8 L5.2 — Agent float as a priced public utility. — SURVIVE.**
- FIX-1. The best original idea in the file and the least defended. Two named-evidence facts carry it, both
  UNVERIFIED and both load-bearing: agents take ≥Tk6.40 per Tk1,000, and human DSR runners already exist as an
  informal price-discovery mechanism. **Verify both before the pitch.** If agents already bid informally for float,
  the pitch is "formalise the market DSRs already run", which is a *better* story — not "invent a market".
- FIX-2. Front-running by high-cash agents is the real risk and it is a mechanism risk, not a difficulty risk.
  Mitigate with per-agent float caps and a disclosed allocation rule.
- FIX-3. The February 2026 96-hour election restriction (BB capped P2P at Tk1,000 and suspended IBFT outright,
  https://www.bssnews.net/news/358990) is the single best scene-setting fact in the file. A float index prices
  exactly the thing that circular rationed by decree. Lead with it.

**P8 L6(a) — Alipay-style escrow monetised from float, with the khata as the dispute instrument. — SURVIVE.**
- FIX-1. Drop the 7-day dispute clock and keep the khata mark. That is the whole novelty and it is a genuinely
  Bangladeshi instrument, not a transplanted one.
- FIX-2. "Take the profit from float" is the part a CFO will not accept from students. Either show the float
  arithmetic with named rates or drop the claim. Do not assert it.
- FIX-3. This is the same product as P8 L3 + P8 L6(b). One pitch, three imported references.

**P8 L6(b) — Dynamic QR with the consignment embedded (Pix B2B analogue). — SURVIVE.**
- FIX-1. It costs almost nothing: Bangla QR already supports dynamic payloads, so the consignment object is a
  payload field, not a new rail. Say that — it makes the 48-hour feasibility obvious to the judges.
- FIX-2. The reconciliation saving is the pitch; the consignment link is the product. `solutions.md` gets this
  right and it should be repeated verbatim in the exec summary.

## P7 — The MFS wallet is the disbursement rail for illegal lenders

**P7 L1 — Blocklist the apps and detect their disbursements. — SURVIVE as a stated non-answer.**
- FIX-1. Keep it as the strawman. "31 named against thousands live, and the money lands on bKash and Nagad
  numbers, not ours" is a two-line demolition and it sets up the winner.

**P7 L2 — The intercept (show the true price of the alternative). — SURVIVE.**
- FIX-1. The file's own failure note is the pitch's hardest question and it must be answered, not buried: a
  borrower who needs Tk24,000 in twenty minutes takes it anyway. The honest answer is that the intercept is not
  aimed at the borrower — it is aimed at the *moment the number is typed*, and its real job is to change what the
  borrower believes the loan costs.
- FIX-2. Compliance guard, stated up front: this is a price disclosure, not a credit decision, and no approve/deny
  of lending occurs anywhere in the product. That keeps it inside the event's Responsible AI minimums and outside
  the PSS Act lending prohibition.
- FIX-3. Test set must be real scam messages from consented phones (SLR37: synthetic for training, real for
  testing). Do not demo on a message the team wrote.

**P7 L3 — Credit passport. — KILL (b), as written. RESCUED as `R3`.**
The product's payoff is "offer a small, capped line to people the illegal apps target". That is lending, and it
is prohibited twice over: BB's MFS guidelines state "MFS platforms will not engage in any lending from their own
funds" (cl. 6.6, MFS Guidelines rev. Jul 2015 / MFS Regulations 2018), and the PSS Act 2024 prohibits "any type of
investment taking, lending, deposit or financial transaction" without BB approval, punishable by up to 5 years or
Tk50 lakh. A MFS *may* act as agent for a BB-licensed bank — which is exactly the rescue.
https://www.bb.org.bd/aboutus/draftguinotification/guideline/mfs_final_v9.pdf

**P7 L4 — Quarantine balance (spendable at merchants, never cashable out). — SURVIVE.**
- FIX-1. The file names the risk correctly: this is an account restriction, and the first false positive freezes a
  real customer's remittance. Fix it structurally — auto-release on a timer with no human in the loop, and the
  customer's own money released by default.
- FIX-2. Frame the rule as a published spend constraint, exactly as NPCI's credit-line circular does ("cash
  withdrawal at merchants shall not be permitted"), and cite it. Bangladesh has the same instrument; nobody here
  has applied it to inbound balances.
- FIX-3. It changes who bears a cost — the operator, not the victim — which is what makes it Track 03 and not
  Track 01. Say that in the first 30 seconds.

**P7 L5.1 — Buy the apps out. — SURVIVE, in one buildable form only.**
- FIX-1. The only buildable form is the **cost model plus a lawful takedown playbook**: publish what full victim
  reimbursement would cost per app against what enforcement has cost to date, and show the CID/DB Dhaka
  non-reporting figure as the denominator. That is a document, not a negotiation, and it is honest.
- FIX-2. Never pay a criminal in the first scene a judge watches. If the deck mentions acquisition at all, it is
  one line at the end, after the model.
- FIX-3. The UNVERIFIED `~Tk9,000 average loss` and the victim counts must be re-verified before they carry a
  taka number.

**P7 L5.2 — Publish the hundi/lending price list. — SURVIVE.**
- FIX-1. **Defamation is a fix, not a kill.** Publish implied cost *bands* by app archetype — "apps charging 2–4×
  per week" — with no named app. The newsroom number survives; the lawsuit does not.
- FIX-2. Present the headline honestly as a per-week multiple, not an APR. `2.375× in seven days` is defensible
  from the documented case; "12,383% APR" invites a statistics judge and is arithmetically silly.
- FIX-3. It needs a real, repeatable estimator from flows. Build it, show it on a held-out week, and let it
  estimate *unseen* apps — that is the AI-depth answer to "why is this a model and not a lookup".

**P7 L6(a) — Fuliza/M-Shwari trader cycle (rescued version `R7`). — KILL (b) as written.**
The credit line is the same prohibited lending as P7 L3.
https://www.bb.org.bd/aboutus/draftguinotification/guideline/mfs_final_v9.pdf
(see `RESCUE R7`)

**P7 L6(b) — UPI Credit Line analogue: a spend-only, merchant-constrained buffer. — KILL (b).**
It is a credit line. "A spend-only, merchant-constrained buffer attached to a repaid-in-full history" is a loan
with a spend restriction. Blocked by MFS cl. 6.6 and by the PSS Act 2024 lending prohibition. The withdrawal
prohibition is a genuinely clever import and is preserved in the rescue.
(see `RESCUE R7`)

## P3 — Fraud money is unrecoverable because the only thing that works is a lawyer, inside two hours

**P3 L1 — Auto-reverse suspicious authorised sends within N minutes. — KILL (b).**
PSS Act 2024: a settlement executed under established procedures is "final, irrevocable, and without dispute".
Reversing a completed authorised send is denying a settled transaction, and the event's own Responsible AI
minimums prohibit autonomous approve/deny of consequential financial decisions. https://www.bb.org.bd/pub/annual/psdreport/paymentreport_dec2025.pdf
The file reaches the same conclusion independently. Keep as strawman.

**P3 L2 — One-tap dossier. — SURVIVE.**
- FIX-1. **bKash already has a complaint channel** (Self Complaint / e-CMS since 19 Jan 2026, 16247, live chat).
  The pitch must not claim no complaint channel exists. The claim is narrower and true: *the assembled evidence
  pack does not exist.* Say that precisely.
  https://www.tbsnews.net/economy/corporates/bkash-introduces-self-complaint-system-faster-service-1338251
- FIX-2. The number is the denominator TIB actually complains about: 58.8% never complain and only 6.2% know CIPC
  exists. The dossier's job is to change the denominator, not the process.
- FIX-3. Sell it internally first — upay's own ops team is the first customer, and an internal buyer is the most
  credible thing a student team can put in a slide.

**P3 L3 — Pre-funded recovery pool, with AI triage of the legal hour. — KILL (b).**
Two independent problems. (i) A standing per-transaction contribution is a levy on every transaction, which
requires central-bank approval of the charge. (ii) Debiting a receiver's settled account to fund a victim, and
reversing settled funds, runs straight into PSS Act 2024 settlement finality ("final, irrevocable, and without
dispute"). https://www.bb.org.bd/aboutus/draftguinotification/guideline/PSO_Regulation.pdf
(see `RESCUE R6`)

**P3 L4 — Not-yet-sent (hold above threshold to a first-time recipient, release when clear). — SURVIVE. Top of file.**
- FIX-1. This is the only P3 idea that changes **when irreversibility happens**, and that is a mechanism change
  in the strict sense of CONTEXT_v2 rule 6.
- FIX-2. Pre-execution is legally different from P3 L1 and the distinction must be stated on stage, precisely:
  no settled transaction is reversed; nothing is denied; the money simply has not left. That single sentence
  defuses the PSS Act finality objection and the autonomous-deny objection at the same time.
- FIX-3. The service-failure risk is real and the number to publish is the false-hold rate on the 200+ consented
  real transfers. Any number above a few percent and the pitch is dead — so measure it before the demo, not after.
- FIX-4. It cannot touch impersonation where the payee is a real trusted contact. Say so. A judge will find it
  anyway; finding it yourself is worth more than the point you lose.
- FIX-5. It is also the cheapest thing to build in 48 hours, which matters because the mechanism is what is scored.

**P3 L5.1 — Insure it, first-party, unconditionally. — KILL (b).**
"IDRA is the sole regulator of insurance sector in Bangladesh" and insurance business requires IDRA registration
and certification under the Insurance Act 2010 / IDRA Act 2010. An MFS underwriting fraud cover is unlicensed
insurance, and it is also a levy on every transaction to fund the pool.
https://www.bb.org.bd/en/index.php/financialactivity/insurance
(see `RESCUE R8`)

**P3 L5.2 — Outbid the mule. — KILL (b).**
A per-taka bounty paid on fraud proceeds that arrive through a known mule number is consideration paid for the
commission of a reportable offence, and paying unlawful lenders/operators is an unauthorised financial operation
under the PSS Act 2024 (up to 5 years or Tk50 lakh). **UNVERIFIED:** I did not locate the specific
Money Laundering Prevention Act 2017 section that would make this watertight — do not cite one in the deck until
it is confirmed. The kill does not depend on it.
https://www.tbsnews.net/bangladesh/law-order/payment-and-settlement-system-bill-protect-customers-interest-placed-js-844836

**P3 L6(a) — Pix MED + 60-minute precautionary block. — SURVIVE. Top of file.**
- FIX-1. Split it explicitly, because only half is ours: the **60-minute precautionary hold inside upay's own
  ledger is unilateral and shippable now**; the tiered refund schedule is an *open standard published for
  adoption*, which is a thought-leadership play, not a product. Never present the second half as something upay
  will operate.
- FIX-2. "60 minutes" is UNVERIFIED in my pass. Verify before the pitch; the demo does not depend on the exact
  number, the pitch does.
- FIX-3. The taka mapping — three tiers at roughly Tk5,000 / Tk20,000 / Tk80,000 against a ~Tk9,000 average and
  an Tk80,000 upper case — is the most executive-ready number in the file. Derive it on stage.

**P3 L6(b) — Nubank Pix Protegido analogue. — KILL (b) as written; its payout mechanism is `RESCUE R8`.**
Opt-in subscription cover is insurance (IDRA Act 2010). The file's own "Bangladesh twist" — a pre-funded taka
recovery pool funded by a fraction of a basis point on the send fee — is the P3 L3 levy, killed above.

## P10 — Women hold 42% of accounts and under 3% of cash-out points

**P10 L1 — Recruit and train more women agents. — SURVIVE as a stated non-answer.**
- FIX-1. Use it as the strawman. "Providers already list female-agent recruitment as a liquidity, footfall and
  security problem and it did not work" is the setup for the whole section.

**P10 L2 / P10 L5.1 — Discretion routing / don't count women at all. — SURVIVE (merged, per finding 0.1).**
- FIX-1. **Merge them.** They are the same AI decision; a judge who notices loses the team's credibility for the
  rest of the pitch. One idea: score agents on demonstrated discretion, pay for it, collect no gender data.
- FIX-2. The proxy objection is the strongest single objection to this idea and it must be pre-empted, not
  conceded: score *observed behaviour* (amount-masking opt-in rate, question-asking refusal rate, repeat-customer
  return rate) and publish the correlation with agent location and neighbourhood income as a **disclosure**, so
  the auditor's finding is already in our deck.
- FIX-3. The fairness check becomes elegant and must be stated: *the check is that no protected attribute is
  collected or used at all.* That is a stronger Responsible AI answer than any gendered alternative in the file.
- FIX-4. It makes BB's unusable 50% female mandate unnecessary by hitting the outcome without the metric. That
  sentence is the exec hook.

**P10 L3 — Home-based agent, and the economics that pay for it. — SURVIVE.**
- FIX-1. The file names the fatal flaw: remove the shop and you remove the float, and float is the income. The
  fix is to change the entry barrier *without* removing float — a home point that holds no float takes only
  receive/transfer/assisted-service volume and refers cash-out to a nearby shop point. Say that; it turns a fatal
  flaw into a designed constraint.
- FIX-2. The regulatory precedent is real and citable: 16,000 agent-banking outlets already run under a 50% female
  mandate. The argument is that the mandate exists for banking outlets and not for the 1.5m+ MFS agents that
  matter (UNVERIFIED count).
- FIX-3. It changes **who pays** (assisted service carries a fee the shop point does not charge, because a shop
  is not required). Mechanism change.

**P10 L4 — Delete the counter visit. — SURVIVE.**
- FIX-1. Strongest claim in the section and the least defended: it needs no new agents, no training, no regulator.
  Incumbents cannot say it because their agent commission model requires the visit to happen. Lead the section
  with that.
- FIX-2. It deletes demand and assumes supply follows — the file says so. Collect the demand decomposition from
  the 20 women participants *before* the demo so the routing is data-shaped, not opinion-shaped.
- FIX-3. It must not be confused with R11 (prohibiting merchant cash-out for women's balances). They are two
  different deletions; if both are pitched, pick one.

**P10 L5.2 — Productise the workaround (named linked wallet). — SURVIVE.**
- FIX-1. The file's own objection is correct and is the whole problem: it institutionalises dependence and creates
  a new authorisation path. Do not pitch it as empowerment; pitch it as **consent, bounded and visible** — the
  same infrastructure the P3 dossier needs. That framing is honest and Track 03-legible.
- FIX-2. Consent collection here is the highest-risk in the file. Do not ask a participant to disclose that she
  uses her brother's wallet in front of the team. Anonymous form, no names, no accounts touched.
- FIX-3. A linked account is a new authorisation path and therefore a new fraud surface — state the control
  (per-transaction ceiling, owner-set, owner-visible ledger) in the security section.

**P10 L6(a) — Wave: subsidised service fee paid to female and home-based points. — SURVIVE.**
- FIX-1. The insight is right and it is not the price, it is the exchange rate between provider and agents.
  Bangladesh's agents take ≥Tk6.40 per Tk1,000 (UNVERIFIED, load-bearing) and are simultaneously the 2.4m people
  most damaged by P2. Verify the number before the pitch.
- FIX-2. Fund it from the merchant tier's float economics — and if that arithmetic cannot be shown with named
  rates, say "the subsidy is a P&L decision we are not asking you to approve today" rather than asserting a
  funding source.

**P10 L6(b) — A women's wallet balance cannot be cashed out at a merchant QR. — SURVIVE. Top of file.**
- FIX-1. One rule, published by the operator, that simultaneously removes the transaction 1-in-3 uncomfortable
  customers are avoiding, deletes the P2 cash-out event for exactly those customers, and removes the "agent sees
  every transaction" exposure that pushes women to a family member's wallet. **Two problems, one prohibition.**
  That is the strongest single sentence in `solutions.md` and it should be the opening line of the pitch.
- FIX-2. Cite the instrument that makes it legitimate: NPCI required acquirers to enforce "cash withdrawal at
  merchants shall not be permitted" for pre-sanctioned credit lines. Bangladesh has the same tool; nobody here has
  applied it to a protected cohort. The pitch is the application, not the invention.
- FIX-3. It changes a settlement rule. That is a mechanism change in the strict sense.
- FIX-4. Fairness inversion: it must be stated as a *restriction added for the customer's protection*, and the
  upside (privacy) must be shown alongside the downside (less cash access) so it does not read as paternalism.

---

# 2. Rescue pass

Seven solutions were killed. Four have a version that avoids the kill reason. Three do not, and I say so.

**R1 — RESCUED from P2 L4 (receipt-only merchant).**
BB has already ordered the cash leg cancelled for merchants abusing QR, so the deletion is law, not invention.
> **Rescue:** stop asking for the deletion and start *enforcing it visibly*. upay publishes, at scan time, which
> of its own merchant points have been de-registered under the April 2026 circular, and pays the model to decide
> *which* points get de-registered. The AI decision becomes enforcement targeting instead of a policy we were
> going to invent.

**R2 — RESCUED from P2 L5.1 (tax the receiver).**
The blocker is that a unilateral fee on a recipient needs BB approval.
> **Rescue:** no fee on the recipient at all. Instead the **sender** pays a published, promo-framed QR fee that
> varies by evidence — which the MDR circular expressly permits as a promotional campaign below the floor — and
> the *default* is the full rate. The recipient is never charged; the exploiter still pays more than the honest
> merchant.

**R3 — RESCUED from P7 L3 (credit passport).**
The blocker is that MFS may not lend from its own funds, but may act as agent for a BB-licensed bank.
> **Rescue:** the passport is the product and the bank is the principal. upay builds the repayment record from
> its own ledger, shows it to the borrower, and *sells the record* to a BB-licensed NBFC or bank as an agent —
> exactly what MFS cl. 6.6 permits and what bKash+BRAC Bank already do with merchant credit. No autonomous
> decision: the passport is evidence, a human approves.

**R5 — NOT RESCUED from P8 L5.1 (subsidise the cash-out).**
No version survives. Upay's cash-out runs at ~zero gross margin (1.304% vs ~1.300%), so there is no room to
subsidise, and bKash's 350,000+ agents give the merchant free cash-out everywhere. Do not revive.

**R6 — RESCUED from P3 L3 (pre-funded recovery pool).**
The blockers are the transaction levy and settlement finality.
> **Rescue:** the fund is contributed **ex ante by upay alone out of a fixed disclosed budget**, not as a levy on
> transactions — no charge, no approval needed. And it never touches a settled account: it pays only claims that
> are still inside the 60-minute precautionary window, which `R10` already creates. Finality is respected because
> nothing settled is ever reversed.

**R7 — RESCUED from P7 L6(a) and P7 L6(b) (trader credit line / spend-only buffer).**
The blocker is lending by an MFS.
> **Rescue:** keep the two genuinely novel mechanics and drop the credit. upay detects the **inventory cycle**
> (stock-in at dawn, stock-out by night, repaid from the merchant's own inflow) and pays for it as a
> *repayment-verification and savings-for-stock* product — no lending, no line, no balance. If a BB-licensed
> partner later wants to lend against the detected cycle, upay is already the detection layer. Separately, keep
> the **withdrawal prohibition** as a rule on any such balance: spend-only at merchants, never cashable out.

**R8 — RESCUED from P3 L5.1 and P3 L6(b) (first-party insurance).**
The blocker is that only an IDRA-licensed entity may do insurance.
> **Rescue:** **unconditional goodwill reimbursement from upay's own balance** — no premium, no cover schedule,
> no policy terms, no risk classification, therefore not a contract of insurance. Every claim is paid, the model
> sets only the *category and the amount*, and the framing on stage is "we pay you back because you are our
> customer", not "you bought cover". Payout in cash at the agent, because a victim down to Tk10,429 has no usable
> bank account.

**R9 — NOT RESCUED (P3 L1), NOT RESCUED (P3 L5.2).** Both are structurally prohibited; P3 L1 is superseded by
P3 L4 and P3 L5.2 has no lawful form.

**Summary: 4 rescued (R1, R2, R3, R6, R7, R8 — six, of which two are the same mechanism),
2 not rescuable (R5, R9), 7 original solutions killed.**

---

# 3. Top 12 by UPSIDE = relevance x impact x originality (1–5 each)

Scores are my judgement. Evidence line is one line and names the thing that sets the score.

### 1. P10 L6(b) — A women's wallet balance cannot be cashed out at a merchant QR
relevance **5** · impact **5** · originality **5**
One published rule removes the uncomfortable transaction, deletes the P2 cash-out event for that cohort, and
removes the "agent sees everything" exposure — two problems, one prohibition, in a country where BB's April 2026
circular proves the regulator already acts on merchant cash-out and NPCI proves the instrument exists.

### 2. P7 L3R — Credit passport (rescued: no lending, sold as evidence to a licensed bank)
relevance **5** · impact **5** · originality **4**
It attacks the one thing the illegal apps cannot fake — a repayment history their victims cannot produce — and
the rescue puts it exactly inside MFS cl. 6.6's permitted agency role. Track 03's argument in one screen.

### 3. P3 L4 — Not-yet-sent (hold above threshold to a first-time recipient)
relevance **5** · impact **5** · originality **3**
Every other P3 remedy operates after a loss; this makes the loss not occur, and it is the cheapest thing in the
file to build in 48 hours. Originality 3 only because Pix's 60-minute precautionary block is a known import.

### 4. P2 L6(b) — Label the resolved identity behind every QR at scan time
relevance **5** · impact **5** · originality **5**
GCash blocked 7,000+ merchants; this loses no merchant and sets the definition instead, and the only thing
missing in Bangladesh is resolving *which number the QR points at* in the customer's hand.

### 5. P8 L3 + L6(a) + L6(b) merged — Consignment-embedded dynamic QR, khata-marked escrow release
relevance **4** · impact **5** · originality **4**
Bangla QR already supports dynamic payloads, so the consignment costs a field, not a rail; the khata is the one
Bangladesh settlement instrument no one has put on a network; it attacks the distributor's refusal, not the fee.

### 6. P8 L5.2 — Agent float priced as a public utility (float index)
relevance **4** · impact **4** · originality **5**
The February 2026 96-hour election circular rationed cash-out by decree; a float index prices exactly what that
decree rationed. Nobody has published one, and incumbents cannot without admitting their agent economics were
unmanaged.

### 7. P7 L5.2 — Publish the implied cost of an unlicensed loan, in bands, no names
relevance **5** · impact **4** · originality **5**
*2.375× in seven days* is a number every newsroom in the country can repeat and it is computable from flows with
no app cooperation — the only P7 idea that produces a public good rather than a feature.

### 8. P2 L2 — Sale-evidence badge on the merchant's own screen
relevance **5** · impact **4** · originality **3**
It puts the interpretation where the missing evidence actually exists, in Bangla, at the moment of the
transaction — and bKash's own public answer is "continuous monitoring", which does not.

### 9. P10 L2/L5.1 merged — Score every agent on discretion, collect no gender data
relevance **4** · impact **4** · originality **5**
It hits the outcome BB's 50% mandate was aimed at while making the metric unnecessary, and "no protected
attribute collected at all" is a cleaner Responsible AI story than anything else in the file.

### 10. P7 L6(a)R — Inventory-cycle detection: stock in at dawn, repaid from the shop's own sales
relevance **4** · impact **4** · originality **4**
No lending survives; the *detection* does, and it is the only item in the file that closes a credit line itself
when the stock sells — the one property that makes informal-lender repayment brutal.

### 11. P8 L2 — Khata reader (handwritten Bangla → payment request)
relevance **4** · impact **4** · originality **4**
The khata is the only artifact in the Bangladeshi MFS stack with no digital representation, and the four existing
products (Halkhata, Dokan Khata, BD Khata, DebtX) are all typed ledgers — none reads the paper book the shop
already has, and Halkhata's own FAQ says so.

### 12. P3 L2 — One-tap scam dossier
relevance **5** · impact **4** · originality **3**
TIB's real finding is not that victims lack redress but that 58.8% never complain and 6.2% know CIPC exists; a
dossier assembled in ten minutes changes the denominator without changing policy, and upay is the only party
holding the transaction trail.

**Next four, in order:** P2 L3 (evidence-split fee — highest mechanism-change in P2, but blocked on a settlement-
symmetry fact we do not yet have); P10 L3 (home-based agent without float); P10 L6(a) (Wave-style agent service-
fee premium); P3 L6(a) (Pix precautionary block + tiered refund standard, split into shippable half and
thought-leadership half).

---

# 4. Pitch test for the top 12

Format: **the sentence a judge repeats** · **the taka number** *(how I would compute it)* · **the live demo moment**.

**1 — Women's balance, no merchant cash-out.**
*Sentence:* "One rule — a woman's wallet cannot be cashed out at a merchant QR — deletes the transaction one in
three women avoid, closes the cash-out fraud rail for exactly the people who use it, and takes away the reason
she uses her brother's wallet."
*Taka:* the women's share of merchant cash-out legs. **Compute:** in the 20-participant study, record every
cash-out leg and the average cash-out ticket; multiply women's share × average ticket × 1.85% (the cash-out rate)
× upay's active women's base × 12. This is the cash-out volume that becomes a direct merchant payment. It is a
*conservative* number — the privacy benefit is not in it at all.
*Demo:* a judge opens the app as a woman, scans a merchant QR, and the cash-out option is simply absent with one
Bangla line naming the rule; then switches to a male profile and watches it appear.

**2 — Credit passport.**
*Sentence:* "The loan apps decide eligibility from data the victim gave up under duress; we build the one
repayment record they can never produce, and we show our reasoning to the borrower."
*Taka:* **Tk57,000 per borrower per week** — the documented Tk24,000 → Tk81,000 case. **Compute:** 81,000 − 24,000
= 57,000, which is 2.375× principal in seven days. Then compute upay's own priced alternative on the same seven
days at a 30-day capped rate of 1.0%: 24,000 × 1.0% × (7/30) ≈ Tk560. The gap, **Tk56,440**, is what the pitch is
about. State the annualised simple figure (~1,240%) only if the judge asks.
*Demo:* a consented volunteer's redacted real spending pattern produces a passport with each contributing signal
named; next to it, an empty passport for a victim of one of the apps, showing the app's "score" is not a score.

**3 — Not-yet-sent.**
*Sentence:* "Every remedy here runs after the money is gone; ours moves the moment irreversibility happens."
*Taka:* **Tk9,000 → Tk6,750** per stopped transfer. **Compute:** average loss Tk9,000 × (75% recovery inside 1–2h
− 19% after) = Tk5,040 retained on average; scale by the number of hold-eligible first-time-recipient transfers
per month, measured in week 1 on the 200+ consented real transfers. Publish the **false-hold rate** as the second
number — the whole idea depends on it being under a few percent.
*Demo:* a judge sends to a stranger's number and watches the money sit, then release in three seconds with the two
named reasons; then sends to a familiar number and watches it never pause at all.

**4 — QR identity label.**
*Sentence:* "bKash's answer to QR abuse is to delete seven thousand merchants; ours is to tell the customer, at
scan time, which number the QR actually points at — so we lose nobody and the first mover writes the definition."
*Taka:* **Tk185 per Tk10,000**, then the annual figure. **Compute:** Tk185 is the 1.85% cash-out take on Tk10,000
that an unlicensed cash-out currently earns for free. Annual: 5–8 taka per Tk1,000 lost on upay-originated QR ×
the share of upay QR volume that the label model classifies as disguised cash-out (measured on the 200 collected
merchant rounds, not assumed) × upay's annual QR volume. **State both the direct cash saved and the merchant
count saved.**
*Demo:* a judge scans a QR that resolves to a personal bKash number and the screen shows the payee type before
they confirm; then scans a real merchant QR and it resolves to a trade name.

**5 — Consignment QR + khata escrow.**
*Sentence:* "The payment and the goods become one object: the consignment is inside the QR, the khata marks the
arrival, and the money moves when the notebook says it moved."
*Taka:* **Tk1.50 per Tk100 of wholesale** — the distributor's own margin, preserved rather than eaten. **Compute:**
BDT1–2 per Tk100 (UNVERIFIED) → use the midpoint Tk1.50; multiply by the wholesale volume that becomes digitally
settled because the distributor no longer refuses digital. Sensitivity table at Tk1 and Tk2. Also compute the
float income on the held balance at the agent's own cash-out share (≥Tk6.40 per Tk1,000, UNVERIFIED).
*Demo:* a consignment is paid digitally and held on screen; a photograph of the shopkeeper's own khata line,
dated today, releases it; the counter shows the Tk difference against the cash it replaced.

**6 — Float index.**
*Sentence:* "In February the central bank rationed cash-out by decree for 96 hours; we price the thing that
decree rationed, and publish the index every morning."
*Taka:* the published float index, **TkX per Tk1,000 per day**. **Compute:** take one day's aggregate cash-out
volume, divide by the agents' declared float for that day, and multiply by the commission agents actually earned
(≥Tk6.40 per Tk1,000, UNVERIFIED — verify). The index is the clearing price a merchant would pay for guaranteed
next-day cash. Second number: **2.4m agents** currently receiving float as a free allocation with no published
price.
*Demo:* a bid for float is placed live, the allocation is shown against competing bids, and the resulting price
per taka is displayed.

**7 — Implied cost of an unlicensed loan.**
*Sentence:* "We are the institution that puts a price on a criminal product — and we publish it in bands, not
names, so no newsroom can be sued and every borrower can check."
*Taka:* **2.375× in seven days**, i.e. ~**1,240% simple annualised**. **Compute:** (81,000 / 24,000 − 1) ×
(365 / 7) = 2.375 × 52.14 ≈ 123.8×. Present the multiple as the headline and the annualisation as the footnote.
The headline number becomes the *median* implied cost across apps, estimated from flows on a held-out week.
*Demo:* the judge types a disbursement and an arrears figure and the implied cost fills in live, then the app is
placed in an anonymous band on the public page.

**8 — Sale-evidence badge.**
*Sentence:* "The evidence of whether a QR payment was a sale or a withdrawal exists on one screen — the
merchant's own — and no incumbent's agent-locked model will put it there."
*Taka:* **Tk100 per merchant per month** of MDR saved at a 1% floor on Tk10,000 of monthly volume, plus the
carrier number: 5–8 taka per Tk1,000 × share classified as disguised cash-out × annual QR volume. **Compute:**
MDR 1% × Tk10,000 = Tk100/month per merchant; multiply by merchants onboarded and by 12. Then add the avoided
loss figure. Show it as a per-merchant number *first*, because that is the one a merchant cares about.
*Demo:* a judge scans a QR on their own phone and the merchant's phone shows the badge flipping from *sale* to
*withdrawal-pattern* within a second, with the two numeric reasons named in Bangla.

**9 — Discretion scoring, no gender data.**
*Sentence:* "Bangladesh Bank has a 50% female-agent mandate covering 16,000 banking outlets and not the 1.5 million
agents who actually matter; we hit the outcome by paying for discretion and never collecting gender at all."
*Taka:* the **discretion premium needed to make a home-based point viable**: a shop point earns BDT5–10 per Tk100
(UNVERIFIED), so the premium must beat **Tk5–10 per Tk1,000** or nobody signs up. **Compute:** set the premium at
the point where a home point's expected monthly income exceeds the shop point's, using the collected 20-interview
willingness-to-switch data. Publish the threshold on stage — it is the honest number and it is checkable.
*Demo:* the leaderboard on screen has no gender column, and a judge cannot tell who is on it; the routing reason
appears in Bangla on a simulated counter.

**10 — Inventory-cycle detection.**
*Sentence:* "We watch the shop buy stock at dawn and sell it by night, and we call the loan repaid when the stock
sells — so the lender never has to chase anyone."
*Taka:* **Tk54,000 per borrower per week** avoided. **Compute:** documented illegal cost Tk57,000 per week
(2.375× on Tk24,000); the same revolving Tk24,000 at a 30-day capped 1.0% costs about Tk560 over seven days;
difference ≈ Tk56,440. Round down and use **Tk54,000** conservatively. Say explicitly that no line of credit is
being offered — only the detection.
*Demo:* a consented trader's redacted month of transactions shows stock-in clustered before dawn and stock-out
through the day, and the repayment event fires on a sale rather than on a calendar date.

**11 — Khata reader.**
*Sentence:* "Four companies already sell Bangladeshi shopkeepers a digital khata; not one of them can read the
notebook the shop already has — that is the only artefact in this entire stack with no digital form."
*Taka:* the **cost of slow collection**. **Compute:** average daily outstanding credit per shop, from the 20
collected shop books × 30 days × a capital rate. Use the agent cash-out share (≥Tk6.40 per Tk1,000, UNVERIFIED) as
the opportunity cost: Tk2,000 average daily outstanding × ~1,640 taka/year ≈ **Tk3,280 per shop per year** of
financing cost the shop is carrying for free. That is the value of knowing who owes what, today.
*Demo:* a judge photographs a real consented khata page on their own phone and, within seconds, one specific line
comes back as a payment request with the recognised Bangla date and amount shown for confirmation — and a
low-confidence page asks the shopkeeper instead of guessing.

**12 — One-tap dossier.**
*Sentence:* "58.8% of fraud victims never complain and only 6.2% know the complaint centre exists; we build the
evidence pack in the ten minutes before the money is unrecoverable, so the counter can finally act."
*Taka:* **taka recovered per legal hour**. **Compute:** take 20 synthetic-but-calibrated claims at the ~Tk9,000
average, run them through the model's triage and through naive FIFO, and report recovered taka ÷ legal hours for
each. The delta is the number. Second number: the unrecorded base — 58.8% × Tk9,000 × (number of annual fraud
victims) is what is currently invisible to upay's own risk team.
*Demo:* a judge taps one button on a realistic case and watches a complete, filable, Bangla dossier appear in under
ten seconds with the three missing evidence items named.

---

# 5. Which of the top 12 change a mechanism

Per CONTEXT_v2 rule 6, at least half must change an incentive, settlement, protocol, who pays, or who decides.

**Mechanism-changing (9 of 12):**
1. **QR identity label** — changes *who decides*: the customer, not the platform, at scan time.
4. **Women's balance, no merchant cash-out** — changes a *settlement rule*, unilaterally published.
5. **Consignment QR + khata escrow** — changes *settlement* and makes payment and goods one object.
6. **Float index** — changes an *incentive*: float goes from a free allocation to a priced, traded capacity.
7. **Implied-cost index** — changes *who names a price*: creates a public good that did not exist.
8. **Sale-evidence badge** — changes *what the fee is a function of*: from rail to evidence.
9. **Discretion scoring** — changes *where the money goes*: payment for an unmeasured service, with no
   protected attribute collected.
10. **Inventory-cycle detection** — changes *what closes a credit obligation*: a sale, not a date.
3. **Not-yet-sent** — changes *when irreversibility occurs*: before settlement rather than after.
2. **Credit passport** — changes *who decides eligibility*: the borrower's own ledger, shown back to them.

**Not mechanism-changing (3 of 12):** 11 khata reader (a model on an existing screen), 12 one-tap dossier
(a workflow on an existing screen), and — if counted — 8 sale-evidence badge, which sits on the boundary and is
counted as mechanism only because the fee basis moves.

**9 of 12, comfortably above the required half.**

---

# 6. Residual risks I could not resolve

1. **The whole taka layer is one document deep.** `solutions.md` calibrates its `SIM` numbers to
   `docs/v2/problems.md`, which I did not read. Every taka figure above is a *derivation from an unverified
   input*. Before any of these numbers is spoken, someone must read `problems.md` and check at least the loss
   rate, the cash-out rate and the agent share against a source.
2. **The Pix/GCash/Nubank/M-Pesa/Wave/NPCI imports in `solutions.md` are unverified.** The demo does not depend on
   them, but a judge will ask "where does this come from" and "is this number right".
3. **The settlement-symmetry fact for P2 L3 is unknown**, and it decides whether P2's best mechanism idea exists.
   Get it in writing from BDQR/NPSB before building.
4. **The float figures (≥Tk6.40 per Tk1,000, 2.4m agents) are load-bearing for #6 and appear nowhere else.** If
   they are wrong, #6's index has no reference price.
5. **Nothing here has been tested against upay's actual integration surface.** The pitch promises an API; nobody
   has confirmed one exists.