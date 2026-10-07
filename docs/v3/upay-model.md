# upay business & unit-economics model

> Companion to `CONTEXT_v3.md`. Facts sourced externally; **everything unsourced is marked UNVERIFIED**.
> Derivation arithmetic is reproducible: `python docs/v3/upay-model-calc.py` (all assertions pass).
> Research date: 3 Oct 2026.

---

## 0. The load-bearing caveat

**upay's own financials are not public.** UCB Fintech Company Limited is a private subsidiary; no revenue
line-item, transaction volume, active-user count, or agent count beyond marketing copy has been disclosed.
UCB PLC's consolidated annual report would carry it as a subsidiary, but I did not retrieve that
document — **everything about upay's income statement is therefore UNVERIFIED.**

What *is* available, and what this document is built from:

1. **bKash Limited's audited financial statements** — the only Bangladeshi MFS with published,
   KPMG-audited line-item accounts. Every BD MFS operates under the same Bangladesh Bank MFS
   regulations and therefore the same revenue architecture, so bKash is a legitimate *structural*
   template for how upay earns.
2. **Bangladesh Bank Payment Systems Reports** — official industry totals.
3. **Published price points and partner announcements** from upay/UCB/bKash/Nagad.

**How to read the taka figures:** the primary unit here is **"1% of revenue"**. Because upay's revenue
is undisclosed, expressing value as a percentage of revenue lets any reader substitute a real upay
number later. bKash FY2025 revenue of **Tk 65.65 billion** is used as the calibration anchor, where
**1% = Tk 66 crore**. That anchor is stated every time, and is never presented as upay's size.

---

## 1. How an MFS makes money — the revenue architecture

### 1.1 The only audited breakdown available (bKash FY2024)

Source: bKash Limited, audited financial statements for the year ended 31 December 2024, Note 24 —
https://www.legacy.bracbank.com/financialstatement/bkash-limited-audited-financial-statements-december-31-2024.pdf

| Revenue line | FY2024 (Tk) | % of gross | % of net revenue |
| --- | --- | --- | --- |
| Commission income | 47,348,509,688 | 82.64% | 93.61% |
| Airtime commission | 1,163,864,848 | 2.03% | 2.30% |
| Return on trust cum settlement accounts | 8,780,951,978 | 15.33% | 17.36% |
| **Gross revenue** | **57,293,326,514** | 100% | — |
| VAT | (6,711,270,107) | — | — |
| **Revenue (net)** | **50,582,056,407** | — | 100% |

bKash's own definition of commission income, quoted from the same note:

> "Commission income includes service charge earned from cash out/e-money settlement, Person to Person
> (P2P) balance transfer, bill payment by customer and commission earned from banks against inward
> remittance, nano loan and savings deposits."

**Three structural facts fall out of this, and they matter more than any single product:**

- **Commission is ~83% of gross revenue.** Transaction service charges dominate.
- **Float is ~15% and is a rate trade, not a product.** Return on customer trust balances was 17.4% of
  net revenue in FY2024, earned on an end-2024 trust balance of Tk 94.07bn — an implied yield of
  **9.33%**. That is a policy-rate-sensitive income line. It scales with *average float*, not with
  engagement, and it is invisible to a customer-facing dashboard.
- **Airtime is 2%** — a commodity pass-through, and the only line with a low-margin, high-volume shape.

### 1.2 bKash P&L shape (the cost side matters as much as the revenue side)

| Metric | FY2024 | FY2025 |
| --- | --- | --- |
| Revenue (net) | Tk 50.58bn | Tk 65.65bn |
| Cost of services | Tk 32.70bn (**64.64%**) | Tk 41.48bn (**63.18%**) |
| Gross profit | Tk 17.88bn (35.36%) | Tk 24.18bn (36.82%) |
| Operating + commercial expenses | Tk 14.47bn | Tk 17.10bn |
| Net profit | Tk 3.16bn (**6.24%**) | Tk 6.61bn (**10.07%**) |

Sources: FY2024 as above; FY2025 from https://en.bonikbarta.com/business/dt2VlJjSIXS99Mic (citing bKash's
financial statements). FY2025 audited statements with line-item note — **not retrieved, UNVERIFIED**.

**Cost of services is ~63% of revenue and is dominated by agent commission.** The same audited notes
confirm the mechanism: *"Deferred commission represents commission paid to agents for performing cash in
transactions for which revenue will be generated in the next financial period(s)."* The exact
commission-vs-other split inside cost of services is **UNVERIFIED**.

**Consequence: an MFS gross-margin business is really an agent-economics business.** The operator keeps
a spread of roughly 1–2% of transaction value and pays most of it away. That is why take-rate
compression (bKash cutting cash-out from Tk 18.50 to Tk 13.95 per thousand in July 2026) is an
existential lever, not a pricing tweak.

### 1.3 upay's revenue lines — status

| Line | upay offers it? | upay's share of revenue |
| --- | --- | --- |
| Cash-out | Yes — https://www.upaybd.com/products/Cash-Out | **UNVERIFIED** |
| P2P / Send Money | Yes — https://www.upaybd.com/ | **UNVERIFIED** |
| Merchant payment (QR) | Yes — https://www.upaybd.com/products/make-payment | **UNVERIFIED** |
| Bill pay | Yes; reportedly free of charge — https://today.thefinancialexpress.com.bd/trade-market/upay-offers-lowest-cash-out-fees-highest-client-security-1628439154 | **UNVERIFIED** |
| Airtime recharge | Yes — https://play.google.com/store/apps/details?id=bd.com.upay.customer | **UNVERIFIED** |
| Float / trust-account return | Presumed, as a licensed PSP — **UNVERIFIED** | **UNVERIFIED** |
| Inward remittance, salary disbursement, government disbursement, Micro DPS, prepaid card | Yes, per partner announcements §3 | **UNVERIFIED** |

If upay charges no bill-pay fee (per the 2021 Financial Express report), then unlike bKash it has **no
bill-pay commission line to defend**, and its mix is more concentrated in cash-out, P2P and float than
bKash's. This is an inference from a five-year-old article — **UNVERIFIED**.

**Do not put a upay revenue number in a deck.** If a judge asks, the honest answer is that upay does not
disclose it and here is the audited template from the one BD MFS that does.

---

## 2. Unit economics

### 2.1 Published price points — the take-rate ladder

All taka per Tk 1,000 withdrawn/transferred:

| Provider / channel | Tk per 1,000 | % | Source |
| --- | --- | --- | --- |
| bKash, standard agent | 18.50 | 1.850% | https://www.bkash.com/en/products-services/cashout |
| bKash, designated "Priyo Agent" (up to Tk 50k/month) | 13.95 | 1.395% | https://www.thedailystar.net/business/organisation-news/news/bkash-reduces-cash-out-charge-tk-1395-4222326 |
| bKash, ATM | 14.90 | 1.490% | https://www.bkash.com/en/products-services/cashout |
| Nagad | ~12.00 (derived from its stated Tk 6.50/1,000 saving vs others) | ~1.200% | https://www.bssnews.net/business/391553 |
| **upay, agent (headline / ceiling)** | **14.00 (1.400%)**, inclusive of VAT and taxes — but **tiered below this**, and some wallet tiers are free | 1.400% ceiling | https://www.tbsnews.net/companies/ucbs-upay-offers-lowest-cash-out-fee-234661 (Apr 2021, "1.4% or Tk14 per Tk1,000 from agent points, which is inclusive of VAT and taxes"); upay CEO in interview: "charges of different wallets are **less than Tk 14** per Tk 1,000 in different layers and in cases it is free of cost", across primary / salary / remittance / disbursement wallets — https://today.thefinancialexpress.com.bd/trade-market/upay-offers-lowest-cash-out-fees-highest-client-security-1628439154 (9 Aug 2021) |
| **upay, UCB ATM** | **8.00 (0.80%)** | 0.800% | https://today.thefinancialexpress.com.bd/trade-market/upay-offers-lowest-cash-out-fees-highest-client-security-1628439154 (2021); UCB schedule of charges May 2026 still states 0.8% of withdrawal amount for the upay co-branded prepaid card: https://www.ucb.com.bd/reports/schedule-of-charges/ucb-plc-conventional-soc-may2026.pdf |
| Cross-MFS transfer (interoperability, from Nov 2025) | 8.50 | 0.850% | https://www.thedailystar.net/supplements/mobile-financial-services |

This ladder is the whole competitive story in one table: **the spread between the cheapest and dearest
cash-out in the market is roughly 1.2x**, and the cheapest operators are not the biggest.

**CORRECTION (3 Oct 2026) — the upay *agent* row was missing, and its absence caused a downstream
error.** For five years this table listed only upay's **ATM** rate (0.80%) while listing **bKash's agent**
rate (1.850%). Comparing the two is an apples-to-oranges error: it made upay look ~43% cheaper than
bKash on cash-out when the like-for-like agent comparison is **1.400% vs 1.850%, i.e. upay is ~24%
cheaper**. Anyone who cited "upay's cash-out take rate is 0.80%" as upay's customer-facing rate — as
`docs/v3/ideas-1-2-3-8-upay-model.md` and `docs/v3/mix-shift-THESIS.md` §1 originally did — was wrong.
**Do not compare upay's ATM rate to any competitor's agent rate.**

**upay's own published charge list does not resolve the agent rate today.** Two third-party sources
disagree and neither is authoritative: 1.400% (Tk14/1,000) from
https://cashoutcalc.tech/ and https://www.tbsnews.net/companies/ucbs-upay-offers-lowest-cash-out-fee-234661,
versus a tiered schedule (agent cash-out 0.7% primary / 0.5% remittance, disbursement and salary;
UCB ATM free up to Tk 25,000/month) from https://newisty.com/upay-charge-calculator, labelled updated
18 Sep 2026. A tiered structure is consistent with the Business Standard wording above ("Tk14 … in
different layers to even free of cost") and with upay's documented **multi-wallet** design (primary /
salary / remittance / disbursement). **Current upay agent cash-out rate: UNVERIFIED.** upay's own
`/limits-and-charges` page could not be retrieved during this check — **retrieve it manually and
re-pin this row before any external use.**

### 2.1a What the customer pays, and what upay earns on the merchant side

Three sourced facts materially change any mix-shift argument, because they invert the naive assumption
that merchant payment is a lower-margin version of cash-out:

| Fact | Value | Source |
| --- | --- | --- |
| **Merchant payment to the customer** | **Free.** "B & M Purchase (In-Store Payment) Free", "Online Purchase Free" | upay FAQ (COO-signed), https://www.ucb.com.bd/reports/downloads/Upay/upay-faq.pdf · https://www.ucb.com.bd/reports/downloads/Upay/Upay_FAQ.pdf |
| Wallet-to-wallet transfer, bill pay, mobile recharge, ATM withdrawal | All **Free** | same |
| **Bangla QR MDR (paid by the merchant)** | **Minimum 1% inclusive of VAT**, mandated from 1 July 2026; supersedes parts of a Feb 2026 order. Previously a 1.15% ceiling | https://networkbangladesh.com/bangladesh-bank-sets-minimum-1-merchant-fee-for-bangla-qr-transactions-to-boost-digital-payments/ (2 Jul 2026) · https://online-d11.thedailystar.net/business/economy/news/bangla-qr-adoption-faces-resistance-over-merchant-fees-4236621 |
| **Interchange Reimbursement Fee (IRF)** | Set to **zero** by Bangladesh Bank for Bangla QR | https://thefinancialexpress.com.bd/trade/bangla-qr-misuse-raises-concerns-over-mfs-sustainability (15 Sep 2026) |
| **upay's own disclosed cost** | "Upay said it incurs a cost of around **Tk 5 to Tk 8 per Tk 1,000** when its customers use Bangla QR to pay through another operator" — and upay publicly called for a cost-recovery mechanism instead of a blanket zero IRF | same |
| Merchant cash-out of Bangla QR proceeds | upay **8.00**/1,000 · Rocket 9.00 · bKash 11.50 per 1,000 | https://www.ink.bd/1848/bangla-qr-payment-charges (10 Jul 2026) — third-party, **UNVERIFIED** |
| Policy pressure on MDR | BB created a **Tk 100 crore** fund to subsidise small-merchant charges; BMPCA demanding a cut to 0.25% | Daily Star (above) · https://thefinancialexpress.com.bd/trade/scrap-bangla-qr-service-charge-to-build-cashless-bangladesh-bmpca (12 Jul 2026) |

**Two structural consequences, both material:**

1. **Merchant payment is free to the customer while cash-out costs upay customers up to 1.4%.** The customer's
   own saving from substituting a cash-out with a merchant payment is therefore not a marginal rate
   difference — it is up to the *whole* cash-out charge. Because upay's rate is **tiered below the
   Tk 14 headline and some wallet tiers are free**, the saving is a **range, roughly Tk 11–30 per
   transaction** at the Tk 2,132 average cash-out ticket (0.5%–1.4%). The upper bound is what a
   primary-wallet customer sees; the lower bound is the salary/disbursement-wallet case. upay also
   confirms "All types of bill payments are free of charge" (same source), which is why `upay-model.md`
   §1.3 treats bill pay as having no commission line to defend.
2. **upay is on the wrong side of a live regulatory dispute.** With IRF zeroed and a 1% MDR floor,
   upay has publicly said it absorbs Tk 5–8 per 1,000 on cross-operator QR while collecting a 1.4%
   cash-out fee on its own cash-out line. This is dated within three weeks of hackathon registration
   closing and is the freshest publicly documented upay pricing position available.

**What remains UNVERIFIED:** upay's actual net revenue per merchant QR transaction, its agent commission
share, and its current agent cash-out rate. A mix-shift business case can be *bounded* but not *closed*
until those three are pinned.

### 2.2 ARPU and active rate

| Metric | Value | Derivation |
| --- | --- | --- |
| bKash revenue per active user, FY2025 | **Tk 1,397/year = Tk 116/month** | Tk 65.65bn ÷ 47m active |
| bKash active users | 47m (transacted in prior 90 days) | https://en.bonikbarta.com/business/dt2VlJjSIXS99Mic |
| bKash registered customers | 82m | same |
| **Active rate** | **57.3%** | 47m ÷ 82m |
| Dormant registered base | **35m** | 82m − 47m |
| bKash e-money outstanding, end-2025 | Tk 110.04bn | same |

**Caveat — "active user" is not a standardised definition.** The Daily Star separately reports bKash
claiming 4.20 crore (42m) active and Nagad claiming 2.82 crore — a different figure on a different
definition/date (https://www.thedailystar.net/business/news/tk-6000cr-moves-daily-not-every-wallet-winning-4220811).
Bangladesh Bank reports *accounts*, not actives, and its account series is internally inconsistent across
press coverage (239.3m in Jan 2025 vs 145.6m in June 2025 vs 141.4m male+female in Oct 2025) — **treat
all active-user and account-count comparisons as UNVERIFIED.**

### 2.3 Transaction economics (Bangladesh Bank, October 2025)

Source: https://today.thefinancialexpress.com.bd/public/trade-market/mfs-transactions-maintain-rising-trend-in-oct-25-1767372858

| Product | Volume | Value | Avg ticket | % of value |
| --- | --- | --- | --- | --- |
| P2P transfer | 134.26m | Tk 476.93bn | Tk 3,552 | 30.2% |
| Cash-in | 142.55m | Tk 413.17bn | Tk 2,898 | 26.2% |
| Cash-out | 174.56m | Tk 372.23bn | Tk 2,132 | 23.6% |
| **Total** | **678.63m** | **Tk 1.58trn** | **Tk 2,328** | 100% |

FY2024 baseline: ~7.3bn transactions, Tk 17,383bn value, avg ticket **Tk 2,381**
(https://www.bb.org.bd/pub/annual/psdreport/paymentreport_dec2024.pdf).

**The headline structural fact: cash-in plus cash-out is 49.7% of all MFS value.** Roughly half of
everything moving through Bangladesh's wallets is moving between cash and digital, not between people
or between businesses. Cash-out is also the **highest-volume, lowest-ticket** product — 174.56m
transactions averaging Tk 2,132.

### 2.4 Cost per transaction

**Cannot be derived honestly.** It requires the operator's own transaction count, and neither upay's nor
bKash's total payment volume is disclosed in the statements retrieved. bKash's cost of services
(Tk 41.48bn FY2025) divided by *industry* transactions would be meaningless, since that denominator
includes Nagad, Rocket and upay.

What **is** derivable:

- **Revenue per cash-out** at the bKash standard rate: Tk 18.50 per Tk 1,000, so **Tk 18.50 per cash-out of
  Tk 1,000** and **Tk 39.4 per cash-out at the Oct-2025 average ticket of Tk 2,132** — i.e. Tk 18.5m per
  1m cash-outs at Tk 1,000 each, or Tk 39.4m per 1m at the actual average ticket. **CORRECTION (3 Oct 2026):**
  this bullet previously listed only the Tk 1,000 figure as if it were "per 1 million cash-outs", which is
  the origin of the Tk 1.85 crore error in §4 Lever 3.
- **Cost of services per Tk 1,000 of cash-out value**: if agent commission were the bulk of a
  Tk 32.70bn cost base spread over an unknown volume, the operator's retained spread per Tk 1,000 is
  **UNVERIFIED**.

### 2.5 CAC — genuinely unknown

**No MFS in Bangladesh publishes CAC.** No primary source found for bKash, Nagad or upay. **UNVERIFIED.**

Two indirect anchors, offered as *framing* rather than as figures:

- bKash's FY2024 "commercial expenses" line was **Tk 3,996,902,095** against 82m registered customers
  (audited statements above). If treated as all customer-acquisition spend, that is ~**Tk 49 per
  registered customer lifetime** — implausibly low as a true blended CAC, which suggests this line is
  mostly brand/retained marketing, not acquisition. This is **interpretation, not a CAC figure.**
- bKash's growth to 82m registered customers against 47m actives implies heavy top-of-funnel spend and
  heavy leakage — the acquisition problem in this market is *activation*, not signup. That is a
  structural read of the 57.3% active rate, not a CAC number.

### 2.6 Agent commission share

**UNVERIFIED.** No disclosed split between agent commission and other cost of services.

Bounded inference: customer pays Tk 18.50 per Tk 1,000 at a standard bKash agent (1.85%). An agent
keeping float and serving walk-in cash must retain the majority; the operator's gross margin of 36.8%
(FY2025) after paying agents implies the operator retains well under half of 1.85%. **Do not quote an
agent share.** Quote the customer-facing price ladder instead, which is sourced.

---

## 3. Assets upay has that bKash and Nagad lack or underuse

Grouped by *why it might matter*. Each row is sourced; the strategic reading is flagged as analysis.

### 3.1 Parent-bank balance sheet and reach

| Asset | Detail | Source |
| --- | --- | --- |
| Parent bank branch network | **236 UCB branches** | https://www.ucb.com.bd/banking/retail-banking/upay-ucb-card |
| Parent agent-banking network | **64 districts, 273 upazilas**; account opening, deposits/withdrawals, transfers, Palli Biddut, remittance | https://www.ucb.com.bd/banking/agent-banking/business-network |
| Bank licence + PSL standing | upay is the MFS brand of UCB Fintech, subsidiary of UCB PLC, Bangladesh Bank licensed since early 2021 | https://www.upaybd.com/who-we-are |

**Analysis:** bKash is a *subsidiary* of BRAC Bank but a standalone PSP with its own P&L and 5,616
employees (https://platform.tracxn.com/a/d/company/5318f947e4b0f7e165ed6f08/bkash). upay is smaller
(~324 employees, https://platform.tracxn.com/a/d/company/59a99b4fe4b0414cfd07a974/upay) but sits
*inside* a 236-branch, 273-upazila bank. The parent network is a distribution asset for services a
standalone PSP cannot easily offer — savings, credit, remittance, SME.

### 3.2 Campus and education — the most distinctive asset

| Asset | Detail | Source |
| --- | --- | --- |
| Daffodil Group MoU | upay payment acceptance integrated across Daffodil's "education and corporate ecosystem" | https://www.ucb.com.bd/news-and-events/press-release/upay-and-daffodil-group-sign-strategic-partnership-mou-to-advance-digital-payments |
| UCSI University | campus-wide QR merchant payments, **tuition fee payment**, **scholarship disbursement**, planned **RFID smart student ID** | https://www.ucb.com.bd/news-and-events/press-release/upay-and-ucsi-university-bangladesh-sign-agreement-to-build-a-cashless-smart-campus |

**Analysis:** this is a closed, addressable, high-density environment — students, parents, canteens,
bookshops, tuition flows, scholarship disbursement, and a card identity layer. bKash and Nagad have
disbursement scale (Nagad distributes government allowances to 7.9m beneficiaries,
https://www.tbsnews.net/economy/corporates/nagad-marks-new-milestone-digital-finance-record-transactions-1275141)
but no documented campus-identity-plus-payments-plus-tuition stack. **Also note: DIU, which is hosting
this hackathon, sits inside Daffodil Group — the same group upay signed an MoU with.**

### 3.3 B2B / distribution / gig

| Asset | Detail | Source |
| --- | --- | --- |
| **Agrani Distribution** | Strategic partner of upay; MoU to expand upay's nationwide B2B operations | https://www.agranidistribution.com/news |
| **foodpanda** | Digital cash-collection solution for foodpanda riders nationwide; rider-centric migration journey | https://www.ucb.com.bd/news-and-events/press-release/upay-foodpanda-partnership-to-simplify-transactions-1 |

**Analysis:** Agrani Distribution gives upay a physical nationwide B2B route-to-market that is not a
consumer app — an FMCG distribution network is a shelf, a sales force and a reconciliation problem in
one. foodpanda gives upay gig-worker accounts at national scale. Both are B2B/payroll-adjacent volume
that bKash and Nagad serve only through generic corporate-sales motions.

### 3.4 Product features

| Feature | Detail | Source |
| --- | --- | --- |
| Wallet with **inflow provenance** — wallet shows where money came from: salary, disbursement, remittance | upay's app listing claims this as a first-in-Bangladesh capability | https://play.google.com/store/apps/details?id=bd.com.upay.customer |
| Real-time remittance from Malaysia (FELDA Mobile / Incentive Remit) direct into upay wallet; "first ever real time remittance distribution channel in Bangladesh" | UCB release | https://www.ucb.com.bd/news-and-events/press-release/ucb-and-incentive-remit-launched-real-time-remittance-service-in-bangladesh |
| NRB Bank tie-up: Add Money, bank↔wallet transfer, **Micro DPS**, remittance, credit-card bill pay | signed 22 Jul 2026 | https://www.tbsnews.net/economy/corporates/upay-nrb-bank-partner-expand-digital-financial-services-1494556 |
| UCB–upay co-branded prepaid card, dual-currency EMV, loadable at any of 130,000+ agents, usable globally | load limit Tk 36 lakh/yr; travel quota US$12,000/yr | https://www.ucb.com.bd/banking/retail-banking/upay-ucb-card |
| USSD `*268#` alongside app; app usable with **no internet charge on Grameenphone** | 2021 reports | https://today.thefinancialexpress.com.bd/trade-market/upay-offers-lowest-cash-out-fees-highest-client-security-1628439154 |
| Bangla + English app; traffic-fine, Indian-visa and Titas-gas bill payment | | https://play.google.com/store/apps/details?id=bd.com.upay.customer |

### 3.5 Honest limits of this section

- **upay merchant count: UNVERIFIED.** No public figure. bKash has 350,000+ agents; upay has 130,000+
  (agent count sourced, merchant count is not).
- **upay market share: UNVERIFIED.** One aggregator puts upay inside an "others 30.3%" bucket as of
  Dec 2022 (https://directory.exports.bd/remittance) — too coarse and too old to use.
- The **RFID smart-student-ID** project is "planned" per the UCB release. Do not claim it is live.
- The Grameenphone zero-rating and low cash-out fee are **2021 claims** and may be stale.

---

## 4. Eight P&L levers, ranked

**Unit convention.** For any lever that scales revenue or cost proportionally, **1% movement = 1% of
revenue**. At the bKash FY2025 calibration anchor of Tk 65.65bn revenue, that is **Tk 66 crore**. For
upay, substitute: **1% movement = 0.01 × upay revenue**, which is undisclosed — so read every taka
figure below as *"per 1% of upay's revenue, assuming upay's revenue is R"*, and Tk 66 crore is the
worked example at bKash's R.

Ranking is by **(credibility of the baseline × how large 1% is × how hard it is to move)**.

| # | Lever | Baseline (sourced) | 1% movement | Taka worth | Confidence |
| --- | --- | --- | --- | --- | --- |
| 1 | **Cost-to-serve** | Cost of services = **63.18%** of revenue (bKash FY25) | 1% relative cut in cost-to-serve | **Tk 41.5 cr** at anchor *(= 0.632% of revenue)* | High on size, low on mechanism |
| 2 | **Retention / active rate** | **57.3%** 90-day active rate; 35m dormant of 82m | +1% relative on active rate = +0.57pp = +470k users | **Tk 66 cr** at full ARPU (Tk 1,397/yr) | High — two sourced inputs |
| 3 | **Frequency** | 678.63m txns/month industry; avg ticket Tk 2,328 | +1% txns per active user | **Tk 66 cr**; per 1m extra cash-outs = **Tk 3.94 cr** (bKash 1.85%) / **Tk 2.99 cr** (upay agent 1.40%) / **Tk 1.71 cr** (upay UCB ATM 0.80%) | High |
| 4 | **ARPU / take-rate** | Take-rate ladder Tk 8.00–18.50 per 1,000 | +1% realised take-rate | **Tk 66 cr**; +Tk 1 per 1,000 on 1m cash-outs of Tk 2,132 = **Tk 21 lakh** | Medium — price is competitive |
| 5 | **Activation of dormant users** | **35m** dormant (bKash) | 1% of dormant = 350k users | **Tk 49 cr** at full ARPU; **Tk 24 cr** at 50% ARPU ramp | Medium-high |
| 6 | **Agent productivity** | bKash: 350k agents, **Tk 187,571 revenue/agent/yr**; industry 174.56m cash-outs/mo | +1% cash-outs per agent | **Tk 3.94 cr** per 1m extra cash-outs at bKash's 1.85% agent rate (**Tk 2.99 cr** at upay's 1.40% agent rate); at 130k upay agents, +Tk 1,876/agent ≈ **Tk 24 cr** | Medium |
| 7 | **Merchant volume** | QR = **3% of NPSB volume, 0.5% of value**; Bangla QR ~1m merchants (BB 2025); **min MDR 1% incl. VAT from 1 Jul 2026; IRF zeroed** — see §2.1a | +1% merchant volume | Small in *current* revenue terms — this is a **mix-shift** lever, not a 1% lever. **Upgraded 3 Oct 2026:** the economics changed materially — merchant payment is free to the customer and earns a merchant-side MDR against a disclosed Tk 5–8/1,000 cross-operator cost, so the question is no longer "is QR monetised" but "does upay's own-rail QR net more than the 1.40% cash-out line it would displace" | Low on 1% value, high on strategic value |
| 8 | **B2B / payroll volume** | Salary disbursement ≈3.1% of MFS value; government payment ≈1.2% (Jan 2025, **secondary source**) | +1% of B2B volume | **UNVERIFIED** — no reliable base value | Low |

### Derivations, stated

**Lever 1 — cost-to-serve.** Tk 41.48bn cost of services ÷ Tk 65.65bn revenue = 63.18%. A 1% relative
reduction = Tk 414.8m ≈ **Tk 41.5 crore**, of which the agent commission pool is the obvious target. The
*size* is well sourced; *how* to cut it is not, because the commission split is UNVERIFIED.
**CORRECTION (3 Oct 2026):** this previously read "≈ Tk 66 crore". That conflated a 1% *relative* cut in a
line worth 63.18% of revenue with 1% *of* revenue. The correct general form is `0.00632 × X × R`, where `X`
is the fractional relative reduction in cost-to-serve. `Tk 66 crore` remains correct only as 1% of revenue
itself.

**Lever 2 — retention.** Active rate 47m ÷ 82m = 57.3%. A 1% relative lift → 57.87%, i.e. +0.573pp of
82m = 469,860 users. × Tk 1,397 ARPU = Tk 656m = **Tk 66 crore**. Note this is the cleanest lever in the
table because both inputs are sourced — and because it is nearly pure upside: those users are already
acquired and already cost CAC.

**Lever 3 — frequency.** Oct-2025 industry: 678.63m transactions. +1% = 6.79m more transactions/month
= 81.4m/year. At the cash-out price point (Tk 18.50 per Tk 1,000, avg ticket Tk 2,132) each
transaction carries ~Tk 39.4 of gross revenue at full take-rate (Tk 2,132 ticket × Tk 18.50/1,000), but the
blended figure across P2P (revenue share undisclosed) and merchant is lower — so **Tk 66 crore is the
revenue-scaling estimate and the Tk 3.94 cr/million-cash-out figure is the cash-out-only floor.**
**CORRECTION (3 Oct 2026):** the floor was previously stated as Tk 1.85 cr, computed as
`18.50 × 1,000,000` — i.e. assuming every cash-out is exactly Tk 1,000. At the Oct-2025 average cash-out
ticket of Tk 2,132 the figure is **2.13× higher: Tk 3.94 cr** at bKash's 1.85% agent rate, **Tk 2.99 cr**
at upay's 1.40% agent rate, or **Tk 1.71 cr** at upay's UCB **ATM** rate of 0.80%. `upay-model-calc.py`
now asserts all three.

**SECOND CORRECTION (3 Oct 2026) — an earlier draft of this note contained a false claim and it has been
removed.** It stated "upay's published take rate is roughly 43% of bKash's, therefore winning more cash-out
volume is a structurally weaker lever for upay." **That was wrong.** It divided upay's **UCB ATM** rate
(0.80%) by bKash's **agent** rate (1.85%) — different channels. See §2.1: the take-rate ladder carried no
upay *agent* row at all, which is what allowed the error. Like-for-like, upay's agent rate of 1.40% is
about **24%** below bKash's 1.85%, not 43% below. The mix-shift argument survives on other grounds —
see §2.1a, where the real argument is that merchant payment is **free to the customer** while cash-out is
not, and that upay publicly disclosed carrying Tk 5–8 per 1,000 on cross-operator QR — but the
"upay is worse at cash-out volume" claim is withdrawn.

**Lever 4 — ARPU.** Take-rate is the most contested number in the market (bKash cut it in July 2026;
cross-MFS interoperability added an Tk 8.50/1,000 transfer charge from Nov 2025). Direction of travel is
*downward*, which makes this lever strategically urgent even though its arithmetic is simple. +Tk 1 per
Tk 1,000 across 1m cash-outs averaging Tk 2,132 = Tk 2.13m per million transactions ≈ **Tk 21 lakh**.

**Lever 5 — activation.** 35m dormant × 1% = 350,000 users × Tk 1,397 = **Tk 49 crore**. Discounted to
50% ARPU because reactivated users do not immediately transact like mature ones: **Tk 24 crore**. Both
figures assume upay's dormant base scales the same as bKash's — **UNVERIFIED for upay.**

**Lever 6 — agent productivity.** Tk 65.65bn ÷ 350,000 agents = Tk 187,571 revenue per agent per year.
A 1% productivity lift = Tk 1,876 more per agent. Applied to upay's 130,000 agents: Tk 244m =
**Tk 24 crore**. Per-transmission check: 1m extra cash-outs at the Oct-2025 average ticket of Tk 2,132 =
Tk 39.4m = **Tk 3.94 crore** gross at bKash's 1.85% agent rate (**Tk 2.99 crore** at upay's 1.40%
agent rate; Tk 1.71 crore at upay's 0.80% UCB ATM rate), before
the agent's own cut.

**Lever 7 — merchant volume.** Bangladesh Bank's 2025 report shows QR at **3% of NPSB volume and 0.5%
of value** — merchant acceptance is a rounding error in *value* terms even after ~1m Bangla QR
merchants were onboarded. So merchant volume is not where 1% is worth much *today*. It is where the
mix is headed, and it is the only lever that converts cash-out volume into higher-frequency, lower-value
volume. Treat the 1% taka value as small and the strategic value as large.

**Lever 8 — B2B/payroll.** Salary disbursement and government payment appear in secondary aggregations
as ~3.1% and ~1.2% of MFS value (https://directory.exports.bd/remittance) — **secondary source, treat as
UNVERIFIED.** The primary Bangladesh Bank monthly breakdowns I retrieved do not itemise these. No reliable
base value, so no honest taka figure. Structurally this is upay's most under-exploited lane given
Agrani Distribution, foodpanda, and the campus tuition/scholarship agreements — but that is a
strategic read, not a quantified one.

---

## 5. What this document deliberately does not do

- **No product ideas.** Out of scope by instruction.
- **No upay revenue estimate.** Not disclosed, and a fabricated figure is the one thing that would
  discredit the whole submission with a technical judge.
- **No CAC, no agent commission share, no cost-per-transaction for upay.** Unsourced; marked UNVERIFIED
  rather than estimated.
- **No upay customer, merchant, or market-share figure.** Does not exist in public sources.

## 6. Open items a judge may probe — get answers before pitching

1. What is upay's actual transaction volume and active-user count? *(Currently UNVERIFIED — this is the
   weakest point in the submission and should be acknowledged as such.)*
2. What is the split of cost of services between agent commission and everything else?
3. What share of upay's revenue is float/trust-account return, and how rate-sensitive is it? For bKash
   this was 17.4% of net revenue at a 9.33% implied yield — if upay is similar, a 100bp policy-rate move
   is a material P&L event.
4. What is upay's dormant base, and what is its 90-day active rate?
5. Does upay earn anything on bill pay, or is it genuinely free?