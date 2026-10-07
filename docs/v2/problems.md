# problems.md — PROBLEM SELECTION (not solutions)

Compiled 3 Oct 2026. Sources read: `docs/CONTEXT.md`, `docs/v2/CONTEXT_v2.md`,
`docs/02-ideas/01-candidates.md` (PART A pain table + PART B assumption audit only —
no candidate solutions were read), `docs/v2/field-notes.md`.

**No solution is proposed in this file.** This file ranks problems. A separate step
turns a problem into a product.

Contested numbers from earlier rounds are re-checked below; two did not survive.

---

## Scoring method

Six axes, 1–5 each, max 30. Scores are argued, not derived.

| Axis | 1 | 3 | 5 |
|---|---|---|---|
| **S** Severity (taka / harm per incident) | nuisance | four figures | seven figures or livelihood-destroying |
| **F** Frequency (how many people, how often) | rare | thousands | national, daily |
| **M** Money flow upay could touch | indirect | fee-side | first-party P&L or the growth engine |
| **U** Unsolvedness | working product exists in BD, URL shown | partial fix, being worked on | no working product; documented structural gap, URL shown |
| **A** Act-alone (5 = upay ships without regulator/bank; 1 = blocked) | needs BFIU/police/court | needs BB policy or a bank partner | upay's own ledger, app, agent network |
| **L** Challenger leverage (can this take users from bKash/Nagad?) | incumbents already own it | contested | incumbents' own model actively blocks them from solving it |

Selection preference, per the brief: high **M**, structurally unsolved (**U**),
attackable from upay's side (**A**). Crowd risk noted where relevant.

---

## PART 1 — Consolidated pain register, scored

Field-note pains (A1–A5, B1–B2, C1–C3) and PART A pains (A1–A20) were merged where
they describe the same failure. Nine PART A entries with no field-note corroboration
and no money-flow path were kept as single entries so nothing is silently dropped.

| ID | Problem | S | F | M | U | A | L | Σ | Evidence note |
|---|---|---|---|---|---|---|---|---|---|
| **P1** | Cash-out is too expensive | 3 | 5 | 4 | **2** | 5 | **1** | 20 | bKash already cut it to Tk13.95/1,000 via two "Priyo Agents" up to Tk50,000/month (Jul 2026) — a working product, so U=2 and L=1: [tbsnews.net/economy/corporates/bkash-lowers-cash-out-charge-monthly-withdrawals-1486291](https://www.tbsnews.net/economy/corporates/bkash-lowers-cash-out-charge-monthly-withdrawals-1486291). MFS cash-out also runs at ~0 gross margin (1.304% revenue vs ~1.300% cost). |
| **P2** | Bangla QR has become an unlicensed cash-out rail | 4 | 5 | 5 | 5 | 5 | 5 | **29** | upay states it loses **Tk5–8 per Tk1,000** whenever its customer pays another operator's QR; a Tk10,000 merchant QR returns ~Tk9,815 cash, the merchant keeping a cash-out-sized cut; BDQR daily value went Tk370m (Jul) → Tk1.1bn (Aug) with no test of genuineness: [thefinancialexpress.com.bd/trade/bangla-qr-misuse-raises-concerns-over-mfs-sustainability](https://thefinancialexpress.com.bd/trade/bangla-qr-misuse-raises-concerns-over-mfs-sustainability), [tbsnews.net/bangladesh/how-abuse-bangla-qr-threatens-countrys-mfs-ecosystem-1538591](https://www.tbsnews.net/bangladesh/how-abuse-bangla-qr-threatens-countrys-mfs-ecosystem-1538591) |
| **P3** | Fraud victims get slow or no redress | 5 | 4 | 4 | 5 | 3 | 4 | **25** | TIB: providers "lack effective mechanisms to detect or prevent illicit transactions"; 58.8% of victim users never complain, only 38.1% of those who do get resolution, 6.2% know CIPC exists; avg loss ~Tk9,000: [thedailystar.net/business/news/mfs-enabling-money-transfers-also-abuses-3904931](https://www.thedailystar.net/business/news/mfs-enabling-money-transfers-also-abuses-3904931). Practical recovery requires a lawyer and an ex-parte court injunction inside 1–2 hours. |
| **P4** | Impersonation fraud is an *authorised* payment with zero recourse | 5 | 3 | 4 | 5 | 2 | 3 | 22 | "Bangladesh has no dedicated reimbursement scheme for this form of fraud and no clearly defined emergency procedures allowing authorities to pause a suspicious transfer while a victim is being manipulated"; no forensic standard for AI audio exists in the Evidence Act or Cyber Security Act 2026: [campaign.thedailystar.net/voice-cloning-fraud](https://campaign.thedailystar.net/voice-cloning-fraud/). Tk80,000 case; provider told the family Tk50,000 was blocked, one month later only Tk10,429 remained. |
| **P5** | Criminals social-engineer the provider's own care desk | 5 | 3 | 3 | 4 | 4 | 3 | 22 | Bagerhat: cloned fingerprints → replacement SIMs → call care desk with prepared security-question answers → Tk2.5 lakh taken from two businessmen: [tbsnews.net/bangladesh/crime/9-arrested-bagerhat-over-sim-cloning-mobile-banking-fraud-1557496](https://tbsnews.net/bangladesh/crime/9-arrested-bagerhat-over-sim-cloning-mobile-banking-fraud-1557496). Security questions are the weak asset; upay owns that recovery flow. |
| **P6** | Accounts frozen at scale with no clear unfreezing | 4 | 5 | 3 | 4 | 2 | 3 | 21 | 55,000 frozen/suspended (Jun 2026) plus 14,000 more (Aug 2026); BFIU Circular 5 of 19 Aug 2026 now orders providers to report *linked* accounts, widening collateral freeze: [tbsnews.net/bangladesh/bfiu-freezes-55000-mfs-accounts-over-gambling-hundi-allegations-khosru-1471416](https://www.tbsnews.net/bangladesh/bfiu-freezes-55000-mfs-accounts-over-gambling-hundi-allegations-khosru-1471416), [tbsnews.net/economy/bfiu-orders-banks-report-linked-accounts-when-any-account-frozen-1519801](https://www.tbsnews.net/economy/bfiu-orders-banks-report-linked-accounts-when-any-account-frozen-1519801). BFIU owns the freeze, so A=2. |
| **P7** | Fake loan apps use the MFS wallet as their disbursement and harvesting rail | 4 | 4 | 4 | 5 | 4 | 5 | **26** | BFIU named 31 unauthorised apps (Aug 2026); "Quick Loan" has 500,000+ Play installs; a victim took Tk24,000 and was shown Tk81,000 of arrears in one week, then had his contacts called; Prothom Alo spoke to five victims and "CID and detective branch of Dhaka Metropolitan Police claim they have received no complaints or cases": [en.prothomalo.com/bangladesh/crime-and-law/vje45fpc6p](https://en.prothomalo.com/bangladesh/crime-and-law/vje45fpc6p), [tbsnews.net/bangladesh/bfiu-warns-against-borrowing-unauthorised-apps-online-platforms-1526606](https://www.tbsnews.net/bangladesh/bfiu-warns-against-borrowing-unauthorised-apps-online-platforms-1526606). Funds land on bKash/Nagad numbers. India had shut 3,718 such apps by June 2026; Bangladesh has no equivalent. |
| **P8** | Digital money cannot move upstream, so retailers cash out to restock | 4 | 5 | 5 | 5 | 3 | 5 | **27** | 7.8m small/medium retailers; wholesale+retail = BDT 17.4tn (2025); only ~10% of flows beyond the counter stay digital; 37% of retailers avoid digital *because distributors demand cash*; distributor margin is BDT1–2 per Tk100, so a ~1% MDR consumes half or more; 62% of merchants reported 3–7 day settlement delays. MicroSave states it unsolved: [microsave.net/2026/05/14/why-bangladeshs-supply-chains-still-run-on-cash-despite-digitization](https://www.microsave.net/2026/05/14/why-bangladeshs-supply-chains-still-run-on-cash-despite-digitization/) |
| **P9** | Agent income is shrinking and float shocks bite | 3 | 5 | 4 | 3 | 3 | 2 | 20 | Agent/distributor/operator take ≥Tk6.40 per Tk1,000 of the cash-out fee, ~2.4m agents depend on it; Feb 2026's 96-hour restriction suspended cash-out entirely in Dhaka and activists went unpaid. Partly fixed: BB allowed weekend/holiday distributor cash up to Tk50 lakh/day in 2022, and human runners (DSRs) exist — hence U=3. |
| **P10** | Women hold the accounts but are locked out of the channel | 3 | 4 | 3 | 4 | 5 | 4 | **23** | Women hold ~42% of 239.3m MFS accounts but **<3% of MFS agents are women**, while BB's 50% female mandate applies only to the 16,000 agent-banking outlets, not the 1.5m+ MFS agents; agent gender is "not tracked, monitored, or linked to compliance or performance indicators"; discomfort at agent points affects 1 in 3 women: [tbsnews.net/thoughts/policy-paradox-heart-bangladeshs-digital-finance-story-1313211](https://www.tbsnews.net/thoughts/policy-paradox-heart-bangladeshs-digital-finance-story-1313211), [microsave.net/2026/01/12/women-must-power-the-digital-economy](https://www.microsave.net/2026/01/12/women-must-power-the-digital-economy/), [undp.org/bangladesh/blog/digital-wages-can-unlock-womens-economic-power-bangladesh](https://www.undp.org/bangladesh/blog/digital-wages-can-unlock-womens-economic-power-bangladesh) |
| **P11** | Hundi drains the formal remittance channel | 5 | 3 | 5 | 4 | 3 | 4 | 23 | Hundi is estimated at nearly half of remittance inflows; ~$16bn average annual illicit outflow 2009–2023; remittance ≈ 6% of GDP; **upay agents were named** in CID findings alongside bKash/Nagad/Rocket. BFIU's method is a fixed parameter list (after-midnight transactions, cash-in-only or cash-out-only accounts, four transactions in a minute, Tk3 crore agent accounts) — a threshold list, and it suspended only 230 accounts: [tbsnews.net/bangladesh/bfiu-suspends-cash-out-from-230-mfs-accounts-over-hundi-transactions-533286](https://www.tbsnews.net/bangladesh/bfiu-suspends-cash-out-from-230-mfs-accounts-over-hundi-transactions-533286). Crucially, hundi demand fell 60–70% when the rate gap closed to Tk1–2 — it is a *price* problem, not a detection problem: [tbsnews.net/economy/falling-hundi-demand-dollar-rate-secret-behind-aug-sep-remittance-boost-962051](https://www.tbsnews.net/economy/falling-hundi-demand-dollar-rate-secret-behind-aug-sep-remittance-boost-962051) |
| **P12** | Online gambling funds itself through wallets | 4 | 4 | 3 | 2 | 2 | 2 | 17 | Already being answered by law and force: Cyber Security Act 2026 §20 makes online gambling a punishable offence; BB directed providers on 28 May 2026 to surveil merchants and customers. 55,000 accounts frozen is enforcement, not a product. Squeezed lane. |
| **P13** | E-commerce refunds lock up when a seller vanishes | 4 | 3 | 3 | 3 | 2 | 3 | 18 | Tk214 crore sat in gateways in 2021, Tk166 crore frozen at a single gateway on police request; the High Court asked why the authorities' inaction should not be declared illegal. Needs gateways and courts, so A=2. Source is 2021 — current state unverified. |
| **P14** | Deepfake social content harvests MFS numbers at scale | 3 | 4 | 3 | 4 | 3 | 3 | 20 | 52 deepfake videos and 31 pages pushing "Family Card" cash offers, harvesting bKash/Nagad numbers in comments; one reel reached 310,000 views; the numbers feed downstream account fraud: [thedailystar.net/news-0/news/follow-share-comment-get-scammed-deepfakes-push-fake-family-card-offers-facebook-4125551](https://www.thedailystar.net/news-0/news/follow-share-comment-get-scammed-deepfakes-push-fake-family-card-offers-facebook-4125551). Harm is real but indirect and mostly not in upay's ledger. |
| **P15** | The interface excludes by dialect and literacy | 3 | 4 | 3 | 3 | 5 | 4 | 22 | ~57% of the population sits outside the formal system; poor financial/digital literacy plus missing data are named as the main barriers for garment workers; incumbent voice services are menu-based IVR. Cheap to act on alone (A=5) but low money flow (M=3). |
| **P16** | KYC funnel confuses and drops people | 2 | 4 | 2 | 3 | 4 | 2 | 17 | BB e-KYC rules are a real constraint and not attackable, but assist *within* the funnel is free. Low harm per incident, so S=2. |

### Rejected on the allowed kill reasons (CONTEXT_v2 rule 3)

- **Already solved in Bangladesh, URL shown:** P1 cash-out price level — bKash's Priyo Agent
  tier already delivers Tk13.95/1,000. Merchant MDR pressure is also partly relieved
  from 1 Oct 2026 (no 1% floor MDR, zero IRF, instant settlement), though note that this
  same policy is what creates P2. Small consumer credit is also live
  (bKash + City Bank, ~Tk1,500 crore disbursed), so credit-adjacent ideas must not be
  sold as unserved. Wrong-number sends have a shipped fix (bKash confirmation prompt).
- **Blocked by a named regulator:** P12 online gambling (Cyber Security Act 2026 §20);
  the freeze half of P6 (BFIU orders, not provider discretion).
- **No plausible 48-hour path:** the cross-border corridor half of P11.

---

## PART 2 — The five selected problems

Selected on M + U + A. Σ order: P2 (29), P8 (27), P7 (26), P3 (25), P10 (23).
P4, P11 and P15 also scored 22–23 and are documented above with reasons for exclusion.

---

### P2. The cash-out event has moved onto the QR rail, and nobody can tell a sale from a withdrawal

**Who suffers.** Everyone, in three places at once. upay pays **Tk5–8 per Tk1,000** on
every transaction it originates into another operator's QR, from its own P&L. The
~2.4m agents lose the cash-out commission that funds them, at a moment when IRF has
gone to zero and MDR's floor has been removed — cash-out already runs at roughly zero
gross margin. And the merchant is now an unlicensed money changer, keeping ~Tk185 per
Tk10,000, which is exactly the cash-out rate, while inflating the national
transaction statistics that everyone plans against.

**Cost.** Not one incident but a rate on every QR payment: 0.5–0.8% of originated
volume for upay, ~1.85% of cashed value for the merchant, and 2.4m agents' livelihoods
exposed. Daily BDQR value tripled from Tk370m to Tk1.1bn in one month.

**Why it persists.** Every party is individually rational and collectively destroying
the network. Zero IRF means the originator cannot recover cost, so the cheapest
response is to refuse the transaction; instead the cost is exported to cash. bKash's
answer is "continuous monitoring"; there is no product anywhere that distinguishes a
genuine sale from a disguised cash-out, because the transaction looks identical.

**The assumption that may be wrong.** Everyone assumes the cash-out *fee* is the
problem. It isn't. The fee is a price signal, and prices move — bKash cut it 25% in a
year. The real artefact is that the transaction carries no evidence of a sale at all.
Assume instead that the missing thing is not price but *proof*, and the fee stops
being the fight.

---

### P8. Digital money cannot move upstream, so the shop counter is a dead end

**Who suffers.** The 7.8m small and medium retailers, and above them every distributor
whose margin the fee consumes. Retailers earn BDT5–10 per Tk100; distributors earn
BDT1–2 per Tk100. A ~1% MDR takes half or more of a distributor's entire profit, so
even if the money *could* move, the economics would still say no.

**Cost.** Not a fee but a dead end. A retailer paid digitally must cash out — paying
MDR *and* an agent fee — because the wholesaler demands cash and will not release goods
against an order-matched digital confirmation. That round trip costs roughly 2% of
turnover on a 1–2% margin. It is also the reason the cash-out problem exists at all:
every upstream payment that goes digital removes one cash-out.

**Why it persists.** The rails were built for P2B, not B2B. Bangladesh digitised the
counter perfectly and left the supply chain behind, so the only instrument that gives
a distributor instant, undeniable, order-linked confirmation of payment is a bundle of
notes. Cash is not a payment method here; it is the settlement guarantee. 37% of
retailers avoid digital payments *specifically* because their suppliers demand cash.

**The assumption that may be wrong.** Everyone assumes retailers need cheaper digital
payments. They don't — a merchant on 1% margins will never accept a 1% fee. They need
the thing cash uniquely provides: certainty that the money arrived against *this
delivery*. Price is the wrong lever; settlement evidence is the product.

---

### P7. The MFS wallet is the disbursement rail for illegal lenders, and there is no trusted alternative

**Who suffers.** People with a real, urgent, small borrowing need and no formal credit
history — the exact population MFS was meant to reach. They install an app, grant it
their contacts, photos and message history, receive a small sum, and are then
contact-listed people are called and threatened. One victim took Tk24,000 and was
shown Tk81,000 of arrears within a week.

**Cost.** A multiple of the principal — Tk24,000 borrowed, Tk81,000 demanded — plus
harassment of an entire phone book. BFIU has named 31 apps; "Quick Loan" alone has
500,000+ Play installs. Prothom Alo spoke to five victims and CID/DB Dhaka reported
receiving **no complaints or cases at all**.

**Why it persists.** The apps are unregistrable, so BFIU can only publish names, while
the money is disbursued straight to bKash and Nagad numbers — meaning the MFS is
already the rail and already has the transaction record. Nobody built the other half:
the trusted signal. A licensed provider has exactly what these borrowers lack, a real
repayment history, and has never used it to offer them anything.

**The assumption that may be wrong.** Everyone assumes the problem is *detecting* loan
apps. Detection is a losing frame — 31 named, thousands live, and it is the most
crowded lane at this hackathon. The unclaimed half is that these borrowers are not
criminals, they are the under-served, and a challenger holding their repayment history
can compete on trust rather than on a blocklist.

---

### P3. Fraud money is unrecoverable because the only thing that works is a lawyer, inside two hours

**Who suffers.** Roughly 1 in 10 MFS users, and 17% of agents — whose average loss is
over Tk18,000. Then the wider base: about 32% of people who have never used MFS avoid
it out of fear, which is a cost to upay's acquisition that appears in no fraud report.

**Cost.** Average victim loss ~Tk9,000, ranging to Tk83,000. But the real cost is the
clock. Once the money is cashed out, recovery is under 20% and usually needs an ex-parte
court injunction. Inside one to two hours it is 70–80%. TIB found 58.8% of victim users
never complained at all and only 6.2% knew the regulator's complaint centre existed —
the system has lost the victim before it loses the money.

**Why it persists.** Because the transaction was authorised. The victim approved it,
so every rule treats it as legitimate, and the only instrument that can stop it is a
provider's discretionary freeze plus a court's order. Providers "lack effective
mechanisms"; hotlines are reported ineffective. Meanwhile, when upay *did* act in the
Tk80,000 voice-scam case, the family was told Tk50,000 was blocked — and one month
later only Tk10,429 remained, with Tk39,571 unaccounted for.

**The assumption that may be wrong.** Everyone assumes the problem is detection speed.
Detection is not the bottleneck — the victim already knows within minutes. The
bottleneck is that assembling evidence across BB, BFIU, police and four providers takes
longer than the money survives, so nobody bothers. Assume the product is the *dossier*,
not the alarm.

---

### P10. Women hold 42% of the accounts and under 3% of the cash-out points

**Who suffers.** Roughly half of 239.3m registered accounts, and every user who is
discomforted at a male-run agent counter — one in three women by UNDP's account. Women
who transact anyway do so through a father's, husband's or brother's wallet, or through
an agent who sees every transaction, which is the same exposure that makes fraud
reporting hard in the first place.

**Cost.** Not yet priced, and that is the finding. Women hold about 42% of accounts
while under 3% of the 1.5m+ MFS agents are women. The state's only gender mandate — 50%
female agent-banking representatives — applies to the 16,000 agent-banking outlets and
not to the channel that handles the overwhelming majority of cash-in, cash-out, remittance
and government payments. Nothing is lost because it is counted; it is lost because
agent gender is not tracked, monitored, or tied to any compliance or performance
indicator, so the gap is invisible to the people who could close it.

**Why it persists.** The agent model was designed around male-owned shops, mobility and
documentation. Every stage of the journey — selection, licensing, training, daily
operation — assumes a male agent, so women read as "unsuitable" when the model itself is
the exclusion. Providers list female-agent recruitment as a liquidity, footfall and
security problem. It is a channel-design problem wearing a risk-assessment costume.

**The assumption that may be wrong.** Everyone assumes this is an *account ownership*
and *literacy* problem — get women a wallet, teach them to use it. The data says the
women already have the wallets; they are locked out of the counter. Fix the producer
side and the demand side has somewhere to go.

---

## PART 3 — Gaps, and what would change the ranking

- **No interviews have been conducted.** Everything above is secondary-source. Source
  counts are not people-counts. Eight conversations would still be worth more than
  twenty more searches.
- **Two figures from earlier rounds did not survive checking.** The "Tk58 crore stuck in
  e-commerce refunds" figure could not be verified; the sourced number is Tk214 crore in
  2021 and may since have moved. And the "Tk387 minimum fee on a Tk30,000 cash-out" is
  now above bKash's headline rate of Tk13.95/1,000 — the fee problem is shrinking, not
  growing, which is precisely why P2 replaced P1.
- **P4 vs P3.** P4 (impersonation, zero recourse) may be the larger social problem, but
  the money answer requires a reimbursement policy and BFIU, so A=2. It stays a
  supporting problem, not a lead one.
- **What would flip P11 into the top five:** evidence that upay can move the
  *receiving-side* price, since the rate gap is what drives hundi, not detection.
- **What would kill P8:** if a licensed B2B settlement product ships before the
  hackathon. Nothing of the kind appears in any source read; MicroSave calls it unsolved.