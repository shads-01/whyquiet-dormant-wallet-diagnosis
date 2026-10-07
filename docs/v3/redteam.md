# Red team — upay executive + Bangladesh Bank compliance officer

> Written 3 Oct 2026. Scope: the **17 ideas still standing** after `economics.md` §3 (the 8 drops in
> `economics.md` §4 are not re-litigated here). Method: three kill grounds only, per instruction —
> **(K1) already solved in Bangladesh, with URL · (K2) blocked by a named law or regulator, cited ·
> (K3) nobody would use it, with named evidence.** Everything else is a FIX, not a kill.
>
> **Result: 7 killed, 10 fixed.** Three of the seven kills are regulator blocks, not judgement calls.
> The most important finding is that `economics.md`'s single best-evidenced number — #2, Tk 52 lakh —
> sits on a mechanism that **Bangladesh MFS Regulations, 2022 Reg. 7.7 prohibits by name.**

---

## 0. The instrument list

Every citation below is a live Bangladesh Bank or Parliament instrument. This is ammunition we did not
previously have: **the 25-idea long list contains zero regulatory citations** (grep for `Settlement System|
MFS Regulations|Trust Fund|Escrow` across `docs/v3/*.md` returns nothing). Three ideas collide with named
prohibitions.

| # | Instrument | Operative text we rely on | Source |
| --- | --- | --- | --- |
| R1 | **Bangladesh Mobile Financial Services (MFS) Regulations, 2022**, Reg. 7.7 | "MFS providers are **strictly prohibited** to engage in **taking deposit and lending from their own funds**." | https://www.bb.org.bd/aboutus/regulationguideline/psd/mfs_regulations_2022.pdf |
| R2 | Same, Reg. 7.5(i) | E-money balances must be ≤ real cash in trust-cum-settlement accounts plus G-securities. "**No loan is permissible against the Trust Fund** and/or any other instruments that are derived from the Trust Fund." | same |
| R3 | Same, Reg. 9.0 *Schedule of Charges* | Rates "set in a **competitive, non-collusive** manner"; keep BB's PSD "fully apprised of all rate settings and rate revisions"; ensure "**prominent display of the rates of charges in all their retail agent outlets**". | same |
| R4 | Same, Reg. 5.2 | Where MFS acts as **authorised agent** of a bank/FI/MFI, "the regulatory compliance of deposit taking, lending and other financial services … **will rest with the principal(s)**". | same |
| R5 | Same, permitted-services clause | B2P **salary disbursement** is an authorised MFS service. | same |
| R6 | **Payment and Settlement System Act, 2024** (passed 4 Jul 2024), s.4(2) | No person, institution or company shall operate a payment system or provide any payment services **without a BB licence**. Penalty up to **5 years' imprisonment or Tk 5 million, or both**; cognizable, non-bailable, non-compoundable. | https://www.bb.org.bd/pub/annual/psdreport/paymentreport_jun2024.pdf · https://www.vdb-loi.com/bd_publications/bangladesh-enacts-payment-and-settlement-system-act-2024-strengthening-financial-security-and-consumer-protection/ |
| R7 | **Guidelines for Trust Fund Management in Payment and Settlement Services** (BB PSD Circular No. 06, 6 May 2021), §6.2 | A PSO providing merchant acquiring "holds merchants' sale proceeds **on trust for an agreed-upon time before settlement**. Therefore, the money reflects a **liability of the PSO to its actual owner i.e. the merchants**." | https://www.bb.org.bd/mediaroom/circulars/psd/may062021psd06.pdf |
| R8 | Same, §11.1 | The Trust Cum Settlement Account may be used for "collecting, disbursing, holding, settling, fee realization and/or **investing** the Trust Fund". So investing customer money is **permitted**. | same |
| R9 | **BB PSD Circular No. 14, 24 Nov 2025** — instant settlement of Bangla QR, effective **15 Dec 2025** | Payments **under Tk 10 lakh credited instantly**; **small and marginal businesses under individual retail accounts must be settled instantly**. | https://www.tbsnews.net/economy/instant-transfer-bangla-qr-payments-15-dec-1293956 · https://www.bssnews.net/business/335351 |
| R10 | **Draft PSO Regulation, 2025** (BB PSD, 4 Nov 2025), §126 | A PSO may hold/delay a portion of merchant payables **only** as a chargeback-proportional safeguard. "**Apart from this, any undue delay in merchant settlement is prohibited.**" §11: settlement ≤ 5 business days absent BB-directed escrow. §33: max T+1. §12: cash settlement with merchants not permissible. | https://www.bb.org.bd/aboutus/draftguinotification/guideline/PSO_Regulation.pdf |
| R11 | **Guidelines for Merchant Acquiring and Escrow Services, 2023** (BB PSD Circular No. 10, 26 Sep 2023) | Applies to banks, MFS, PSPs, PSOs. Mandatory functions include merchant **risk assessment, risk management, refunds, merchant activity monitoring, dispute resolution**. | https://apparelresources.com/business-news/retail/bangladesh-launches-new-guidelines-bat-for-e-commerce-sector/ · index at https://thebankingcircular.com/circulars/channel-banking/digital-banking/act-and-guidelines/ |
| R12 | **Personal Data Protection Ordinance, 2025** (Ordinance No. 61 of 2025, gazetted 16 Nov 2025) | §5 consent must be freely given, specific, unambiguous, revocable; **burden of proof on the controller**. **§36**: any person who, without necessary consent or legal basis, processes or transfers personal data "for malicious purposes **or with the intention of gaining profit**" → up to **5 years' imprisonment or Tk 10 lakh fine**. §5(3)(e) lawful ground without consent: "implementation of legal rights relating to **employment, labor rights or social security**". **§9(3)**: a controller shall not "track, monitor, **profile** or targeted advertise" a **specific child** using its behaviour or data. | https://www.dpo-india.com/Resources/Privacy_Regulations_in_Asia_Pacific_Countries/Bangladesh-Personal-Data-Protection-Ordinance,2025(Ordinance.No.61-2025).pdf |
| R13 | **Deposit Protection Ordinance, 2025** (Ordinance No. 64 of 2025) | Deposit-protection regime for banks and FIs; touch-points flagged for the trust-fund work. | https://www.bb.org.bd/en/index.php/mediaroom/circular |
| R14 | BB MFS transaction limits, re-fixed 27 Mar 2025 | Daily cash-in Tk 50,000 · daily cash-out Tk 30,000 · monthly cash-in Tk 3 lakh · monthly cash-out Tk 2 lakh · max balance Tk 5 lakh · **no limit on transaction numbers**. | https://www.tbsnews.net/economy/mfs-transaction-limit-refixed-daily-maximum-cash-tk50000-cash-out-tk30000-1103256 |

**Note on `docs/CONTEXT.md` and older rounds:** the ban on fraud/scam/ATO/mule is **self-imposed**. The
official brief lists Track 01 as fraud/scam/ATO/mule intelligence. That conflict (`CONTEXT_v3.md` §0) is
still open. This document does not resolve it, and nothing in the 17 depends on it. If it is ever
resolved in favour of Track 01, the compliance load shifts to BFIU/AML obligations, not to this
instrument list.

---

## 1. Kills

### KILL 1 — #2 Float Pre-Positioning, *lender variant* — **K2, regulator, high confidence**

**What we proposed.** Advance cash or e-float to an agent who will run short, charge an advance fee, eat
default risk. `economics.md` §3 #2 prices the base case at **+Tk 52 lakh** and calls it
"the best-evidenced number in this document", resting on S3 (agents are volume-constrained at 9–26
transactions/day). `long-list.md` §2 merges B7 into it and names the mechanism: "**upay-as-lender is the
buildable one**".

**Why it is blocked.** Three independent clauses, any one of which is fatal:

1. **R1 — MFS Regs 2022 Reg. 7.7, verbatim:** "MFS providers are strictly prohibited to engage in taking
   deposit and lending from their own funds." Advancing cash to an agent at a fee *is* lending from
   own funds. There is no safe reading of it.
2. **R2 — Reg. 7.5(i):** "No loan is permissible against the Trust Fund." If the advance is funded from
   the trust-cum-settlement account — the only place a PSP's idle cash sits — the trust fund cannot be
   encumbered for it. So the lender variant is blocked *and* has no lawful funding source.
3. **R6 — PSSA 2024 s.4(2):** the same activity carried on under an adjacent label is unlicensed payment
   activity, punishable by up to 5 years and/or Tk 5 million, non-compoundable.

The "advance fee 1.0–2.5%" is also a return on money the provider is holding, which reads as deposit
taking under Reg. 7.7's first limb.

**What this costs us.** The best-evidenced idea on the list, and the only one whose base case rests on
something `interview.md` actually evidences. The *arithmetic* survives; the *mechanism* does not.

**RESCUE — keep the forecast, drop the loan.** upay never lends. Reg. 5.2 (R4) expressly contemplates
the opposite: MFS providers may act as **authorised agent** of a BB-licensed bank or FI, and regulatory
compliance then "will rest with the principal". upay is a subsidiary of **UCB PLC, a scheduled
commercial bank**. So the product becomes **"Float Risk Radar, licensed to UCB"**:

- upay sells the **P90 intraday liquidity forecast** to UCB PLC as principal.
- **UCB PLC**, in its own name and on its own licence, extends the working-capital line to the agent.
- upay earns a **licence + routing fee** for the forecast and the origination. It never holds the
  receivable, never charges the advance fee, never touches the trust fund.
- The agent is a **borrower of the bank**, not a customer of upay's credit book. Nothing in Reg. 7.7 is
  engaged, and the bank's own credit discipline replaces the `default%` assumption that
  `economics.md` flags as the #2 sensitivity.

The demo is unchanged and the AI-necessity story is *stronger*, because a model that a bank will
underwrite on is a more credible artefact than a model that predicts a lending decision nobody may make.
Judge it on **cash-outs completed ÷ cash-outs attempted** and on agents funded — a ratio and a count,
which is what the rubric rewards.

---

### KILL 2 — #9 Autopay Subscriptions — **K1, already solved, high confidence**

**Already in production in Bangladesh, free to the customer:**

- **bKash Auto Pay** covers Send Money, Pay Bill and Mobile Recharge on a set date, with app + SMS
  notification, customer-initiated only ("AutoPay can only be enabled by the customer after accepting the
  terms and conditions"), free of any additional charge, and cancel/restart at will.
  https://www.bkash.com/en/page/autopay · https://www.bkash.com/en/products-services/auto-pay
- It extends to insurance premiums on a dedicated product page: https://www.bkash.com/en/products-services/auto-pay
- It is a **standard bank integration**: Standard Chartered Bangladesh implemented a third-party Auto
  Bills Pay system (auto-debit, DPDC/DESCO/TITAS/WASA, retry logic, dual control).
  https://asdbd.com/products/auto-bills-pay-system/
- Tokenised recurring authorisation is documented as the recommended bKash mode for ISP billing:
  https://docs.ispbills.com/docs/en/settings/payment_gateways/

`interview.md` §"Not verified" flagged autopay in Bangladesh as **UNVERIFIED** and told us to search
before pitching. We did not. It is solved, it is free, and it is shipped by the competitor whose DPS
product already has 4.3m accounts (see KILL 3).

There is no version of this idea where a judge scores "we built autopay" as differentiated.

**RESCUE — autopay is not the product; the bill calendar is the input.** The AI was never the standing
order. It was "per-customer, **seasonal missed-bill prediction**". The standing order is a commodity we
buy from bKash's feature set; what we cannot buy is the **forward schedule of a customer's committed
cash demand** — every bill amount, every due date, every auto-debit, normalised against paydays and
Eid.

Rebuild as **"Commitment Calendar"**: a read-only model, no payments product at all, that produces, per
customer, `expected cash-out demand over the next 30/60/90 days, with its variance`. It has exactly two
consumers, both already in the long list:

- **#2/#1** — the agent float forecast (when will demand spike, and at which agents).
- **#6** — the substitution desk (a customer with a Tk 3,000 gas bill on the 8th is *not* a
  cash-out-reduction prospect on the 28th).

If bKash's own autopay succeeds, this data exists only inside bKash. That is the point: it is the asset.

---

### KILL 3 — #4 Goal Autopilot — **K1, already solved as a product, medium-high confidence**

`economics.md` already flagged this: **+Tk 12 lakh base, 0.28% of revenue, and "the whole idea never
reaches break-even on its own"**. The correctness of that arithmetic is not in dispute. What is in
dispute is whether there is a product left after the incumbent ships it. There is not.

**bKash's savings stack, live today:**

| Element | Evidence |
| --- | --- |
| Monthly DPS, Tk 500 → **Tk 20,000**, tenors 6/12/24/36/48 months | https://www.bkash.com/products-services/savings/monthly-dps |
| **A purpose/goal field** — "Savings-er upokh nichun to **sebingsho bojogri**" (select the purpose of opening the savings) | same |
| Explicit goal framing in bKash's own words: "designed for individuals looking to **accumulate a significant sum within a short period to meet specific goals**" | https://www.tbsnews.net/economy/corporates/bkash-partners-dhaka-bank-idlc-offer-monthly-tk-20000-dps-1172011 |
| **Weekly** savings Tk 250–5,000 — "introduced in the bKash App for the first time in the country", aimed at "daily wage-based professionals" | https://www.tbsnews.net/economy/corporates/weekly-savings-option-tk250-5000-added-bkash-app-855056 |
| Fixed Deposit from Tk 10,000, 6/12 months | https://www.bkash.com/products-services/savings/fdr |
| **4.3m+ DPS accounts opened via the app since 2021**; ~2m accounts by May 2024; about one-third women | the two TBS articles above |
| **bKash waives the applicable cash-out fee** on DPS maturity | https://www.bkash.com/products-services/savings/monthly-dps |
| Six banks/NBFIs already integrated, incl. IDLC Finance, Dhaka Bank, City Bank, Mutual Trust, BRAC, Eastern | bKash savings pages + IDLC launch |

So the instrument, the goal field, the low entry ticket, the auto-debit, the partner-bank stack, the
free cash-out at maturity, and the scale are all shipped. And per that last row we cannot out-subsidy
it: `economics.md` puts **upay ARPU at Tk 89/yr** against bKash's Tk 1,397/yr. A fee-waived product
competed by a 16× revenue-per-user incumbent is not a market we enter.

**RESCUE — do not build a savings account. Build the affordability solver, and licence it out.**
The one thing missing from every bKash flow above: the instalment is chosen from a **fixed grid**
(Tk 500/1,000/2,000/2,500/3,000/5,000/10,000/20,000). The customer is asked what they can pay, not told.
Nobody in Bangladesh ships the inverse. So:

- **Product = `FeasibilitySolver`**, not a wallet feature. Given a pay cycle (wages on the 28th per S6,
  remittance on the 5th per S7), an existing commitment calendar (KILL 2's output) and a target
  ("Tk 30,000 in six months" — the brief's own words, `CONTEXT_v3.md` §3), it returns the **affordable
  monthly contribution computed on the customer's worst month, not their average**, plus the trade-offs.
- **Revenue is a B2B licence to the partner bank/FI**, exactly the structure bKash uses with IDLC and
  Dhaka Bank. upay is already an agent of banks for deposit-taking under R4. The model is the product;
  upay does not hold the deposit and takes no credit risk.
- The demo never touches a savings balance: it is a **planner + a chart**, and the AI-necessity test
  (§13 of the brief) is against the grid, which is exactly a simple deterministic rule — and exactly the
  line the brief says weak ideas cross badly.

---

### KILL 4 — #22 Settlement-Timing Yield Desk — **K2, regulator, very high confidence**

`economics.md` §3 #22 carries the **largest base case on the whole list, Tk 2.5 crore, 5.8% of revenue**,
and the same section calls it "the most assumption-stacked number in this document". It is also the
clearest regulatory kill in the set, and the reason is dated within nine months.

**Why it is blocked.** The product is: merchant leaves QR proceeds on the books for an extra day; upay
shares the float yield with them.

1. **R9 — BB PSD Circular No. 14 of 24 Nov 2025, in force 15 Dec 2025:** payments under **Tk 10 lakh
   must be credited instantly**, and **instant settlement is specifically mandated for small and
   marginal businesses under individual retail accounts** — which is precisely the "two grocers with
   identical volume" segment `economics.md` #22 models. The regulator has not left this merchant
   segment discretion; it has taken the discretion away and given it a deadline that has already passed.
2. **R10 — Draft PSO Regulation 2025 §126:** deliberate delay in merchant settlement is permitted
   **only** as a chargeback-proportional safeguard, "in accordance with the trend of chargeback amounts
   it usually receives on that specific merchant". "**Apart from this, any undue delay in merchant
   settlement is prohibited.**" Paying a merchant to wait is not a chargeback safeguard. §33 caps
   settlement at T+1 and requires monthly reporting to PSD for anything beyond it.
3. **R7 — Trust Fund Guidelines §6.2:** merchants' sale proceeds are a **liability of the provider to the
   merchant**, held on trust. Paying a yield on a trust liability is not remuneration the provider is
   licensed to pay; combined with R1 (Reg. 7.7 deposit-taking) and R6 (PSSA 2024 s.4(2)), the "merchant
   share of the yield" line — `ASSUMED` at 35–60% in `economics.md` — is the exact taka that creates the
   breach.

Three assumptions stacked in `economics.md`; we never checked whether the mechanism is legal. It is not.

**RESCUE — keep the heterogeneity model, invert who gets paid.** The one genuinely good thing in #22 is
the observation: *"liquidity tolerance is heterogeneous — two grocers with identical volume differ on
whether T+1 causes a stockout."* That observation survives; the yield-share does not.

Rebuild as **"Stockout Risk, funded by the bank"**:

- The model predicts, per merchant, **P(stockout before next settlement)** from volume, category,
  restock cycle and settlement timing. Heterogeneous tolerance is the whole point, so the AI-necessity
  argument is untouched.
- **upay pays nothing.** A merchant flagged as liquidity-tight is routed into the **same licensed
  principal channel as KILL 1's rescue**: UCB PLC, as authorised agent principal under R4, offers a
  working-capital line or an invoice-discount product (see §5, the BB factoring pilot) against that
  merchant's verified QR receipts.
- The merchant liveness and risk-assessment surface is not a nice-to-have — **"merchant activity
  monitoring" is a mandated control under R11** (BB PSD Circular No. 10 of 26 Sep 2023), alongside
  risk assessment, refunds and dispute resolution. So the model is regulatory infrastructure, and the
  refusal ("this merchant is liquidity-tight and does not qualify") is a compliance output.

The taka becomes third-party-funded and the regulatory exposure goes to zero. Given R9 has already
compressed settlement to instant for the target segment, the honest base case is small — say that out
loud and lead with the control, not a number.

---

### KILL 5 — #16 Remittance-Season Awakening, *the who-pays flip as framed* — **K2, data law, medium-high confidence**

**What we proposed.** The purest who-pays flip on the list: the remittance partner that earns the fee
funds the outreach, by buying a ranked list of its own lapsed receivers from upay. `economics.md` §3 #16
already stripped the partner list fee out of every case and downgraded it to "upside" — it now prices
**+Tk 37 lakh** on upay's own P&L. The whole reason to keep it was the who-pays mechanism, and that is
the part that is blocked.

**Why it is blocked.** The Malaysia-corridor receivers are **upay wallet holders**. Their wallet number,
balance history, dormancy length and transaction pattern are personal data upay holds. Selling or handing
a ranked list of them to a separate legal entity — BPMI / Incentive Remit, the UCB remittance partner
(`CONTEXT_v3.md` §10) — is processing and transferring personal data to a third party **for profit**.
Under **R12, Personal Data Protection Ordinance 2025 §36**, any person who does so "without the necessary
consent or legal basis … **with the intention of gaining profit**" faces **up to 5 years' imprisonment or
a Tk 10 lakh fine**. §5 puts the **burden of proof on the controller** — upay, not the partner — and
requires consent to be specific, unambiguous and revocable, with the purpose, retention period, transfer
and withdrawal procedure disclosed. "We bought a marketing list" is not a lawful basis.

We also cannot lean on the remittance partner's own consent: the partner never had these customers'
data, so it cannot have obtained consent to receive it.

**RESCUE — sell the model, never the list.** Same product, same counterparty, zero personal data moved:

- upay provides a **seasonality-and-uplift scorer** that the remittance partner runs **inside its own
  consented base**, against the partner's own lapsed-receiver records. upay's IP is the model; the
  partner's data never leaves the partner.
- Where upay's own customers must be involved, upay contacts them **itself**, under its own consent,
  and the partner funds the *campaign budget*, not a per-lead bounty on identified people.
- upay's revenue becomes a **model licence fee plus a corridor performance fee**, which is exactly the
  `UNVERIFIED` partner-fee line `economics.md` already excluded. We have now converted that
  UNVERIFIED into a compliant form — a licence for software is a far easier sell to a remittance partner
  than a customer database, and it is a sale the partner can sign without a DPO conversation.

The seasonality claim (`interview.md` S7: sender pay-cycle specific, not calendar average) is
unaffected and remains the AI content.

---

### KILL 6 — #14 Dormant-Lead Bazaar — **K2, data law, high confidence**

**What we proposed.** 154,000 franchise agents each get a ranked list of dormant upay customers near
them, priced by expected value, and pay a bounty per verified activation. `economics.md` §3 #14 prices
it at **+Tk 16 lakh** base and then delivers the kill itself: *"the bounty must stay below **Tk 44**
(ARPU × ramp) — i.e. a token gesture, not a real incentive. At a Tk 250 bounty no achievable activation
rate rescues it."* The aggressive case is **−Tk 1.6 crore**.

**Why it is blocked.** Two separate failures, and the compliance one is decisive regardless of the
arithmetic.

1. **Arithmetic (not a permitted kill ground, recorded for completeness):** the idea cannot clear a
   bounty floor of Tk 44 against a per-agent value of Tk 2,813/yr on the registered base.
2. **R12, PDPO 2025 §36 — this is the kill ground.** Distributing a ranked list containing wallet numbers,
   names and contact details to 154,000 independent franchise agents is a third-party transfer of
   personal data for profit, without a lawful basis and with the burden of proof on upay. On the
   arithmetic above, upay would be paying agents a token amount for a list worth nothing to them — the
   §36 "**malicious purposes or with the intention of gaining profit**" language is squarely in play for
   the list product even where the bounty is nominal. **Agents are not employees** of upay, so no
   employer-law lawful basis under §5(3)(e) exists.

**RESCUE — the agent gets a number, never a name.** Invert who pulls the record:

- The agent dashboard shows **only an aggregate count** for their catchment — "18 dormant upay wallets
  live within 1 km of you" — with no name, no number, no transaction detail. Aggregates are not personal
  data.
- The dormant customer, on their **own next app open or transaction**, sees "an upay agent near you
  will top up your wallet" and taps to claim. The record resolves **server-side at the moment of the
  customer's own action**, and the reward is a **token the customer already owns** (a free small
  merchant payment, a recharge coupon). Nothing is transferred to the agent.
- upay's acquisition cost collapses from a paid bounty to the CAC it already spends, which is the only
  way this works at Tk 89 ARPU — and `economics.md` §3 #14 already reached that conclusion for the
  **employer-funded** sibling (#5), which is why #5 survives and #14 does not.

Kill the bazaar; keep the funnel. The honest statement to a judge is the one `economics.md` already
wrote: **at Tk 89 ARPU, self-funded acquisition must be free.**

---

### KILL 7 — #1 Agent Shift Market — **K3, nobody would use it, medium confidence**

**The lowest-confidence kill in this document, and I want that on the record.** `interview.md` is
evidence-derived, not first-hand (S3 is BCG multi-country 2019, not upay agents). If any kill here is
wrong, it is this one.

**Why nobody would use it.** The product asks a customer standing at an agent counter with cash in hand
to walk to a different agent. Two independent reasons it fails:

1. **The user of the product is paid to be harmed by it.** S3 (https://www.bcg.com/publications/2019/how-mobile-money-agents-can-expand-financial-inclusion):
   agents doing fewer than **15–20 transactions a day report significantly lower satisfaction**; provider
   break-even is 3–5/day; agents need 9–10/day rural and 13–26/day urban. Agent volume is *the* binding
   pain. Every cash-out this product reroutes away from agent A is commission agent A does not earn
   (`economics.md` U1 = **Tk 29,850 per 1,000 cash-outs**). We are asking the party with the documented
   volume problem to hand volume to a competitor. No agent incentive design fixes that.
2. **There is no evidence the customer would walk.** S4 (Hazra) evidences the complaint as *"agents often
   decline small withdrawals, and an agent is not always available when needed"* — a **supply** failure,
   not a **discovery** failure. The customer is not looking for a better agent; the agent is not there.
   Nothing in `interview.md` supports walk-away behaviour.

And `economics.md` §3 #1 already prices the base case at **−Tk 20 lakh** (Tk 10.0 lakh of recovered
cash-outs against a Tk 30 lakh cost), with a break-even that requires the market to clear **36%** of
all refusals.

**RESCUE — prevent the refusal, don't route around it.** Keep the float model from KILL 1's rescue,
keep the refusal pain from S4, and remove the inter-agent competition entirely:

**"Float-Aware Refusal Prevention."** The P90 intraday forecast tells *this* agent, in advance and on
their own dashboard, "based on your current float and expected 17:00 demand you will run short by about
Tk 4,000; hold this much or route your own cash-in here." The agent never has to refuse, so no customer
is asked to walk, and **no agent is asked to help a competitor**.

- The AI-necessity claim is unchanged and is the strongest in the set: float depth moves intra-day and is
  invisible in any static roster, and S4/S3 describe the mechanism directly.
- The metric is the one `economics.md` §5 already names as judge-holdable: **cash-outs completed ÷
  cash-outs attempted**. A rate, not a dashboard of scores.
- upay earns the forecast licence from UCB (KILL 1's channel), and — this is the elegant part — the
  intraday cash-in nudge that B12 was merged into #2 is now the **incentive lever inside the same
  forecast**, so `long-list.md`'s merge decision turns out to have been right even though the lender
  half of it was illegal.

---

## 2. FIX list — the 10 that survive

Not killed. Not because they are good — most are weak — but because none of the three kill grounds
applies. Each gets the minimum fix required to survive a hostile question.

| # | Idea | Base taka (`economics.md`) | The fix, and the question it must survive |
| --- | --- | --- | --- |
| **#5** | Sponsor Payroll Market | −16L yr1, +10L yr2 | **The dormant wallets must exist in the employer's own payroll file** — currently UNVERIFIED, and `economics.md` notes year-1 is negative and the aggressive case is *lower* than base. **Fix:** stop claiming dormant-user activation. Reframe as **"Payroll Cycle Calendar"** — employer-funded, and the deliverable is the employer-side commitment schedule (R5 permits B2P salary disbursement; R12 §5(3)(e) gives a lawful basis without consent for "employment, labor rights or social security"). **Kill criterion:** if you cannot get one named employer to say the dormant-wallet figure is non-zero, drop it. |
| **#6** | Full-Loop Swap Engine | **+90L — best P&L** | Best idea on the list and the one already converged in `mix-shift-THESIS.md`. **Four fixes.** (1) **Top-line direction:** substituting 1.4% cash-out for 1% MDR is **revenue-reducing at the top line**; the case closes only on saved commission plus avoided IRF, and upay's net MDR share is UNVERIFIED. Print the breakeven band with the unknowns visible, never a point. (2) **R3:** the bounty is a promotional discount — document it as a promotion and keep PSD apprised. (3) **R12 §5:** the customer nudge needs specific, revocable consent, and a do-not-contact switch; the negative-uplift segment must be a hard refusal, which `mix-shift-THESIS.md` §4 already traps. (4) **R14:** state the BB transaction limits alongside the synthetic population so no judge assumes unbounded volume. **Kill criterion (already written, keep it):** if the breakeven commission share falls outside what a published price ladder can support, kill it — do not assume the favourable branch. |
| **#8** | Incremental Offer Fund | +47L (cons −50L) | The technique is the brief's own named sharp ML signal — that is worth real marks. **Fixes.** (1) **Merchant co-funding has zero evidence**; `economics.md` says so. Frame as a **hypothesis the prototype tests**, never a mechanism you assert. (2) **R3:** merchant-funded discounts sit next to the merchant MDR floor; keep them clearly outside the posted charge schedule. (3) **R12 §5:** targeting requires consent; the negative-uplift segment must be refusable. (4) The budget is ASSUMED and bKash cut cash-out to Tk 13.95/1,000 in Jul 2026, so the conservative case is the honest headline. |
| **#11** | Wallet-Tier & Take-Rate Leakage | −3L base, +2.0cr aggr | **This idea gets stronger under red-teaming, and the compliance officer is the reason.** **R3** requires MFS providers to "ensure **prominent display of the rates of charges in all their retail agent outlets**" and to keep PSD "fully apprised of all rate settings and rate revisions". A customer billed above their posted wallet tier is therefore **not only a revenue leak — it is a live breach of a named regulation**, with a regulator that has already fixed the transaction limits by circular (R14). **Reposition from "recover revenue" to "regulatory self-audit before BB finds it".** That fixes the negative base case: the value is compliance and the taka is a liability to be quantified, not income to be booked. **The demo survives unchanged and is the most honest one on the list** — you show a judge the leakage, or you show them there is none. |
| **#12** | Retention Uplift Gate | +1.1cr base | Largest *revenue* case on the list and it rests on a discount budget nobody has sized. **Fixes.** (1) **R3:** any retention discount is a posted rate; non-collusive, PSD apprised. (2) **R12 §5:** the contact needs consent and an explicit **do-not-contact** state, and the negative-uplift segment is the Responsible-AI centrepiece — if contact deters customers, a response-rate model destroys value while looking successful. (3) **Do not present the base taka** (`economics.md`'s own instruction); present the conservative case. The refusal — *do not discount the already-loyal* — is the product. |
| **#13** | Cross-Operator Leak Plug | +18L | Highest certainty per transaction, and the **highest policy-reversal risk in the document.** The Tk 5–8/1,000 cross-operator cost exists because bKash **refused to join BB's interoperable platform at its 1 Nov 2025 launch** (security concerns; Nagad was not approved), and BB's Governor publicly conceded "interoperable payment did not work well for lack of participation" — while announcing a **Gates Foundation instant payment platform targeted for July 2027**. https://www.tbsnews.net/economy/instant-transfer-bangla-qr-payments-15-dec-1293956 · https://publisher.tbsnews.net/economy/banking/interoperable-payment-did-not-work-well-lack-of-participation-governor-1293496 · https://en.wikipedia.org/wiki/Bangla_QR **If bKash joins, the leak closes by regulation and this product has nothing left to fix.** **Fix:** build it, but put an **IRF-restored scenario in the model and on the slide** — "value = 0 if interoperability lands" — and state the dependency out loud. A judge who thinks of that first and hears it from you wins the round. Also: the reroutable-50% assumption depends on an upay-QR merchant existing nearby, and S8's 37% supplier-cash figure suggests that layer is thin. |
| **#15** | Silent-Churn Triage | **+2.1cr — best risk profile** | One of the three strongest, and it survives cleanly. **Fixes.** (1) **R12 §5:** outreach to a large dormant base needs consent proof and revocability; use upay's own first-party channel only, never a third party. (2) The `recovery rate` assumption (4%) is what separates −Tk 22 lakh from +Tk 2.1 crore and **nothing supports it in either direction** — so the tool must be able to say "no attributable cause", which is the demo. (3) A correctly diagnosed **exit you cannot remedy is a free-text report**, not a product; score only causes with a mapped remedy. Judge it on the refusal, never on the taka. |
| **#20** | Acceptance-Gap Sniper | −23L yr1, +48L yr2 | **The regulatory hook is better than the payback, and the payback loses.** **R11** (BB PSD Circular No. 10, 26 Sep 2023) makes **merchant onboarding — documentation, verification, risk assessment, risk management, refunds, activity monitoring, dispute resolution** — a mandatory control for any MFS/PSP/PSO doing merchant acquiring. A ranked acceptance-gap tool is **the compliant way to spend the field team's acquisition budget**, not an optimisation. That reframes a negative year 1. **Fixes:** (1) lead with the R11 control, not the payback; (2) field cost (Tk 8,000) is above net MDR at every conservative setting — never lead with ROI; (3) **licence check:** the OSM geometry comes from the Open Database Licence, which carries attribution and share-alike obligations for derived databases. Confirm scope before shipping anything derived. **Verify this — do not assert it.** |
| **#24** | Payroll-as-a-Product | +39L | The only idea where the float line and the commission line reinforce rather than trade off, and it has the lowest break-even bar of any revenue idea (**Tk 12 crore of annual payroll, or 340 workers**). **Fixes.** (1) **R2 is the live risk:** Reg. 7.5(i) — no loan against the Trust Fund. The "hour-by-hour trajectory sized inside the trust account" must be sold as a **forecast with no liquidity guarantee**. Say "we do not guarantee float" on the slide, because a bank that has been told the opposite will not renew. (2) **R12 §5(3)(e)** gives a clean lawful basis for employer-side processing of worker wage data — state it, because that is what makes this the safest data story in the set. (3) **R5** confirms B2P salary disbursement is authorised. (4) `economics.md` says the float component is **10% of the case** — strip it and lead with the disbursement fee. |
| **#25** | Campus Closed Loop | **−0.6L base** | Negative base case and the largest taka on the list is 14 lakh at the aggressive end. It survives on one asset no taka buys: **DIU hosts this hackathon and sits inside the same Daffodil Group upay signed an education MoU with.** **Fix — and this one is mandatory.** **R12 §9(3) prohibits tracking, monitoring, profiling or targeted advertising of a specific child using its behaviour or other data, and §9(4) holds parental consent valid only to age 18.** A campus product that models *individual student* behaviour profiles a large population that is partly children. Therefore: **scope the model to merchant-side data only.** The merchant is the data subject, is an adult, and merchant liveness is the actual idea ("a canteen quiet for 11 days is dying, a bookshop quiet for 11 days is on break"). **No student-level model, no student-level targeting, no campus-wide spend profile.** And **R11** helps again: "merchant activity monitoring" is a mandated control. Do not claim the UCSI RFID student ID is live — `long-list.md` is right that it is planned. |

---

## 3. Cross-cutting fixes

1. **Every idea now needs a consent line in the README.** R12 puts the burden of proof on the
   controller. One short "lawful basis, consent surface, do-not-contact" block, reused, costs an hour
   and answers the 5% Responsible AI criterion and the 5% security criterion at once.
2. **Every customer-facing number needs a prominent-display statement (R3).** If the prototype shows a
   fee, bounty or discount, say where a customer would see it displayed under Reg. 9.0.
3. **Stop printing the trust-fund yield as if it were free money.** R7 says merchant proceeds are a
   liability to the merchant; R8 says investing the trust fund is permitted. Both are true, and together
   they mean the float line is real but it is a **rate trade**, which `upay-model.md` already says.
4. **One more number to pin** alongside `economics.md` §6's top two: **upay's active agent count**. Every
   agent-side idea inherits it, and `economics.md` §1.3 shows 154,000 registered agents against
   revenue implying 0.27 cash-outs per agent per day — a 260× inconsistency. That inconsistency is
   itself a strong finding and is worth a slide.
5. **Do not let the regulator be a surprise in the demo.** Add a compliance page to the console showing
   which regulation each decision touches. For a Bangladesh Bank compliance officer that is the most
   persuasive artefact in the room, and it costs a day.

---

## 4. Errors in our own documents, found while red-teaming

| Where | Error | Correct |
| --- | --- | --- |
| Older rounds / third-party summaries | "Payment and Settlement Systems Act 2018" | **Payment and Settlement System Act, 2024**, passed 4 Jul 2024 (R6). The 2018 and 2022 instruments are the **Bangladesh MFS Regulations**, and **2022 replaced 2018** — `economics.md` §4 drops #7 citing a licence limit that is live in Reg. 7.7 of the 2022 text. |
| `docs/v3/*.md` as a whole | Zero regulatory citations anywhere in the long list | §0 above. Three of seven kills came from instruments we had simply never opened. |
| `mix-shift-THESIS.md` §8 | "killed #12 Campus Closed Loop", "#6 Autopay", "#8 Restock Credit" — **but those numbers are from the pre-merge `ideas-*-upay-model.md` numbering, not `long-list.md`'s.** Campus is **#25**, Autopay is **#9**, Restock Credit is **#7**. Two documents, two numbering schemes, same symbols. | Fix the cross-references before anyone on the team builds the wrong thing. |
| `long-list.md` §2 #2 | "B7's agent-lender market … A4's lender" as the *buildable* variant | Unbuildable. R1. See KILL 1. |

---

## 5. Two things I found that un-kill ideas we already dropped

Not part of the brief, but they are on the way past and the exec should know.

- **#7 Restock Credit** was dropped in `economics.md` §4 because "underwriting a credit line is outside a
  PSP's licence — a regulatory question unanswerable in 24h". It is now answerable. BB has a **pilot
  framework for exactly this**: *Guidelines for Local Factoring/Receivable Financing through Digital
  Platform — Pilot Phase* (ThinkBig Solutions Ltd.), investment cap Tk 20 crore per financier, **T+1**
  settlement, recourse on the approving corporate.
  https://www.bb.org.bd/mediaroom/circulars/psd/jan182022psd01.pdf · https://www.tbsnews.net/economy/banking/micro-enterprises-get-receivable-financing-easily-359239
  Restock credit is **invoice factoring against upay's own verified QR receipts** — the receivable is
  observable, which is what the platform is designed around, and the financier is a bank/NBFI under R4,
  never upay. Still too big for 72 hours, but it is no longer a licence question.
- **Deposit Protection Ordinance, 2025 (Ordinance No. 64 of 2025)** (R13) is the newest instrument in the
  frame and nobody in the team has read it. Check it before touching anything that touches the trust fund.

---

## 6. What I refused to kill, and why

Discipline matters more than the kill count.

- **#6 Full-Loop Swap Engine** has a revenue-reducing top line, a commission share that is UNVERIFIED, and
  a breakeven that might fall outside the plausible range. That is an arithmetic problem with an already
  written kill criterion. It is the best P&L idea on the list. Not mine to kill.
- **#15 Silent-Churn Triage** and **#12 Retention Uplift Gate** are both uplift/causal ideas on a
  `Tk 89 ARPU` base with assumed discount budgets. Weak economics is not one of the three permitted kill
  grounds.
- **#25 Campus Closed Loop** has a **negative base case**. Still not a permitted kill ground, and the
  relevance asset is real and dated.
- **#11 Wallet-Tier Leakage**'s base case is **−Tk 3 lakh**. Red-teaming made it *better*, not worse.
- **Track 01 (§0 of `CONTEXT_v3.md`)** remains unresolved and is not a compliance problem. Fraud, scam,
  ATO and mule intelligence is an **officially listed track direction**; our ban on it is self-imposed.
  Nobody should die on that hill without the team deciding it.

---

## 7. The one-paragraph version for the pitch rehearsal

Seven of seventeen ideas die on contact with the regulator or the incumbent — and the two that carried the
best evidence (#2) and the biggest number (#22) die on **named clauses we had simply never read**:
MFS Regs 2022 Reg. 7.7 forbids upay lending from its own funds, and BB's instant-settlement circular of
Nov 2025 took away the merchant delay that #22 was going to sell. What survives is smaller and better:
models, forecasts and allocation decisions that a licensed bank acts on and upay never funds itself, sold
to UCB PLC or to a partner bank or FI as an agent under Reg. 5.2, with every customer contact carried on
consent and every number presented as a rate, a ratio or a count. The judge-facing line is: **we do not
lend, we do not take deposits, and we do not move anyone's money without telling them — we tell a bank
where the risk is, and it decides.**
