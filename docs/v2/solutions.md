# solutions.md — 40 solutions across the 5 selected problems

Generated 3 Oct 2026 against `docs/CONTEXT.md`, `docs/v2/CONTEXT_v2.md`, `docs/v2/problems.md`,
`docs/01-data/inventory.md`. Method: innovate-or-die innovator pass (lenses from
`references/lenses.md`), idea-refine variation lenses. Critic/evaluator/reviser were **not** run,
by instruction. **Nothing here is ranked, filtered, scored or defended.** L1 entries are named and
then rejected on the record — they are in the file so the search space is auditable, not because
they are candidates.

## Lanes

- **Lane A** — a learned model on real public or collected data.
- **Lane B** — a mechanism, system or market product where AI makes a core decision inside a new
  incentive, protocol, workflow, marketplace or network response. Evaluated by transparent
  simulation calibrated to real public numbers.

## Data labels

`REAL` = exists publicly, already in `docs/01-data/inventory.md`.
`COLLECTABLE` = 3 students, consent, under 8h, already scoped in section B of the inventory.
`SIM` = synthetic, generated from the named public numbers in `docs/v2/problems.md` (every
assumption to be documented per the event rules).

## Field legend

name | how it works | what AI decides (the single core decision) | lane | data | the demo moment |
why it is a challenger-brand weapon | the first thing that would make it fail

---

# P2 — Bangla QR has become an unlicensed cash-out rail

## L1. The obvious fix

**Charge cross-operator QR at the cash-out rate, or refuse it.**
Merchant pays ~1.85% instead of ~0.5–0.8%; customers are discouraged; upay stops losing money.

**AI decides:** nothing. This is a tariff lookup.

**Lane:** B (mechanism, but with no model in it — it fails strict test 1).

**Data:** `REAL` — BDQR value growth and MFS cash-out fee structure from the two Financial
Express / TBS sources in `problems.md`.

**Demo:** a spreadsheet slider showing merchant revenue under a 1.85% tariff.

**Challenger weapon:** none that lasts. It taxes the 7.8m retailers who are the only reason QR
matters, and it is exactly the move every incumbent has already priced.

**Why it fails:** it does not answer the problem's actual question. The transaction still carries
no evidence of a sale, so the merchant keeps cashing out; only the price changes, and the merchant
simply charges the customer more. Nothing in this system learns anything, so remove the tariff and
nothing valuable remains.

## L2. An AI feature on an existing screen

**Sale-evidence badge on the QR checkout screen.**
When an upay customer scans a merchant QR, the merchant app shows a live badge — *sale*,
*uncertain*, *withdrawal-pattern* — computed from the merchant's own transaction stream (amount
distribution against their sales cycle, basket realism against their typical basket, counterparty
novelty, roundness, time-of-day, QR-to-personal-wallet routing). A low-confidence sale triggers a
soft prompt, not a decline.

**AI decides:** is this transaction a purchase by a customer at a merchant, or a withdrawal
masquerading as one? One binary, per transaction, on an existing screen.

**Lane:** A.

**Data:** `REAL` skeleton — no public Bangladeshi merchant dataset exists, so this runs on `SIM`
flows calibrated to named public numbers: Tk1.85% cash-out rate, ~1.85% merchant cut on Tk10,000,
BDQR Tk370m→Tk1.1bn monthly, 7.8m retailers. `COLLECTABLE` feature set — ~200 real merchant
payment rounds across campus shops plus 30 shopkeeper interviews on what a normal basket looks
like, which is the part the simulation cannot invent. Feature set is hand-specified, labels are
weak — by CONTEXT_v2 rule 3 that is a fix item, not a kill.

**Demo:** a judge scans a QR on the judge's own phone; the merchant phone shows the badge
flipping from *sale* to *withdrawal-pattern* within one second, with the two numeric reasons named.

**Challenger weapon:** bKash's stated answer is "continuous monitoring". This puts the
interpretation on the merchant's own screen, in Bangla, at the moment of the transaction — and it
is the only place the missing evidence actually exists. upay can ship a merchant app incumbents
whose agent-locked models will not.

**First thing that makes it fail:** merchants read a *withdrawal-pattern* badge as being accused of
laundering, and stop using upay's merchant tool within a week. The badge must be framed as a
pricing input ("your fee this month"), never as a suspicion, or the network self-destructs.

## L3. A mechanism change

**Split the QR fee by evidence, not by rail.** A QR payment that arrives with a sale artefact
(basket match, counterparty history, delivery evidence) settles at merchant-discount. A QR payment
with none settles at the cash-out rate — and the *recipient* pays it, not the sender. Same rail,
same scan, two prices, decided per transaction by the L2 model. The economic effect is that the
unlicensed money-changer, who currently earns ~Tk185 per Tk10,000 for free, is the one who
internalises the cash-out cost.

**AI decides:** which of the two price regimes this transaction falls into.

**Lane:** B.

**Data:** `SIM` only, calibrated to named public numbers: Tk5–8 per Tk1,000 upay loss on
originated QR, ~1.85% merchant cash-out rate, zero IRF, no MDR floor from 1 Oct 2026, BDQR
Tk1.1bn/day. Every rate is from `problems.md`; no new numbers are invented.

**Demo:** two identical Tk500 payments through one QR. One carries the delivery artefact, one
doesn't. Same instant, two different settlement receipts side by side, with the Tk difference
labelled.

**Challenger weapon:** it changes *who pays*, which is the one lever the incumbents cannot copy
without re-opening their own cash-out P&L. It also makes the honest merchant structurally better
off than the exchanger, so the merchant network pulls toward upay rather than away.

**First thing that makes it fail:** cross-operator settlement rules do not let the recipient pay a
different rate from the sender. If BDQR settlement is symmetric and regulator-set, this collapses
into a fee-discount scheme and the evidence layer earns nothing.

## L4. DELETE the problem

**Delete the merchant's ability to move value out of a wallet into cash.**
Make the merchant QR a *receipt terminal only*: value arrives in a merchant balance that can be
spent at other merchants or withdrawn to a business/bank account, but not paid out in cash to a
third party. The cash-out event stops existing on the merchant QR, so the rate that feeds it
stops too. upay loses nothing on the legitimate sale and stops losing Tk5–8 per Tk1,000 on the
rest.

**AI decides:** nothing per transaction; the model only ranks merchants by risk to enforce the
closure rule with.

**Lane:** B.

**Data:** `SIM` on the same named public numbers; `REAL` for the loss figure (Tk5–8 per Tk1,000,
upay's own statement as reported).

**Demo:** a merchant tries to pay out a customer's cash in the app and simply cannot. The button
is not greyed out for policy reasons — the balance has no cash leg.

**Challenger weapon:** the deepest change any incumbent cannot make unilaterally, because it
requires the network's consent. Being the first mover on a rule that *protects* merchant balances
buys upay the merchant relationship outright.

**First thing that makes it fail:** the merchant is the cash-out business. If a merchant's revenue
is mostly the withdrawal cut, closing it does not remove the cash-out — it moves it to the next
counter, and upay has voluntarily gifted the exploiter a new channel to attack.

## L5. Unreasonable idea 1

**Tax the receiver.** Charge the person *receiving* the QR money a small fee when the transaction
lacks sale evidence, symmetric with what every instant-payment scheme already does on withdrawal.
The cost lands on the person extracting cash, not on the customer being converted — the one party
who is not upay's customer.

**AI decides:** whether the receiving side is being used as a cash-out point.

**Lane:** B.

**Data:** `SIM` on named public numbers; the fee must be calibrated so the exfiltrated amount
(Tk185 per Tk10,000, ~1.85%) exceeds the tax by enough to make cash-out unprofitable but not so
much that legitimate P2P refunds are penalised.

**Demo:** the judge's own phone receives a QR payment from a stranger and gets a Bangla line:
*you received Tk10,000. Tk185 of this is being paid to a merchant as a withdrawal charge.*

**Challenger weapon:** it is the only version of this fix where the exploit pays the tax, which
means it does not need merchant cooperation, does not need BDQR agreement, and can be launched by
a challenger unilaterally. Every incumbent response to QR abuse costs merchants money; this costs
exploiters money.

**First thing that makes it fail:** it is politically impossible to explain and legally
indefensible to charge an ordinary person receiving a legitimate gift Tk185. The first regulator
who reads it as an unauthorised levy kills it.

## L5. Unreasonable idea 2

**Merchant compliance bond.**
Every merchant QR stakes a small, refundable bond (or a share of their fee) that is returned only
while their realised cash-out ratio stays under a learned threshold. A merchant who is mostly
selling keeps every taka; a merchant who is mostly laundering forfeits the bond. This uses the
scarcity that is actually binding — not the fee.

**AI decides:** each merchant's realised withdrawal ratio, and therefore bond release.

**Lane:** B.

**Data:** `SIM` calibrated to named public numbers (Tk10,000 QR returning ~Tk9,815 cash — the
merchant keeping a cash-out-sized cut is the actual signature); `COLLECTABLE` — ~30 shopkeepers
on whether they would accept a bond and how much.

**Demo:** the same merchant runs a week of simulated traffic, 90% sales and 10% disguised
withdrawals. The bond meter on screen moves visibly with the ratio.

**Challenger weapon:** incumbents cannot run it because their merchant base is already
compliant-adjacent to the abuse; a challenger with a clean book can make bond compliance a
selling point to the 7.8m retailers who currently have no alternative to bKash's merchant stack.

**First thing that makes it fail:** the bond is functionally a deposit merchants will price into
their prices. Retailers earning BDT5–10 per Tk100 will not absorb even Tk20 of locked float and
will simply stop accepting the QR.

## L6. Import — verified by search

**(a) Brazil Pix: the DICT anti-fraud database + MED special refund + withdrawal feature.**
Verified: the Banco Central do Brasil operates a proxy-directory *and anti-fraud database* (DICT),
fed mandatorily by PSPs, where accounts carrying a fraud mark are barred from transacting; Pix also
serves **92.6% of transactions at ≤R$200**, and the bank itself lists "withdrawal of cash" as a
Pix feature — so withdrawal is designed into the rail rather than policed around it.
([BCB Pix ecosystem presentation](https://cdn.bancentral.gov.do/documents/sistema-de-pagos/informacion-general/documents/PIX-Brasil_Jose_Vicente_Mattos.pdf?v=1750032000154),
[BIS Pix lessons appendix](https://www.bis.org/publ/bisbull52_appendix.pdf))

**Bangladesh-specific twist:** DICT is a *cross-scheme mandatory* database, which Bangladesh cannot
replicate unilaterally — that is why incumbents say "monitoring". upay's version is a
**self-reported-scheme mark**: upay publishes, open, the fraud-marks it has assigned to its own
payees, and lets any upay customer check any upay number before sending. No regulator, no
cross-operator agreement, no BDQR change — the network is only upay's, but the *standard* is
public and portable, so it is the piece any future BDQR rule would have to adopt.

**(b) Philippines QRPh + GCash: enumerate and close, at scale, with names.**
Verified: GCash blocked **3,200 merchants** in March 2026 for abusing QRPh, then reported
**7,000+** merchants blocked since 2025 across gambling, suspicious transactions and QR *masking*
— where a legitimate-looking QR silently redirects to an illegal destination. GCash publicly named
the tactic and pushed BSP for stricter merchant onboarding.
([Philstar 2026-03-17](https://www.philstar.com/business/2026/03/17/2514755/gcash-blocks-3200-merchants-over-gambling-links),
[GMA News 2026-03-17](https://www.gmanetwork.com/news/money/companies/980363/gcash-cicc-merchants-users/story),
[Manila Bulletin 2026-05-13](https://mb.com.ph/2026/05/13/more-than-7000-fraudulent-merchants-kicked-off-gcash-platform))

**Bangladesh-specific twist:** GCash's answer is *blocking*. upay's version is *labelling*: publish
the resolved merchant identity behind every QR at scan time, so the customer, not the platform,
sees that a QR pointing at a bKash personal number is not a merchant. Blocking loses merchants;
labelling loses nothing and is copyable, which means the first mover sets the definition.

---

# P8 — Digital money cannot move upstream, so the shop counter is a dead end

## L1. The obvious fix

**Cut the merchant MDR to zero (or below zero) and subsidise it from the P&L.**
Retailers get a cheaper digital payment, accept more digital, cash-out drops.

**AI decides:** nothing. A subsidy is an accounting entry.

**Lane:** B, but with no model.

**Data:** `REAL` for the rate regime — MDR floor removed and IRF at zero from 1 Oct 2026; `REAL`
for the margin structure (retailer BDT5–10 per Tk100, distributor BDT1–2 per Tk100, 62% reporting
3–7 day settlement delays).

**Demo:** a fee slider on a whiteboard.

**Challenger weapon:** none. This is the move the regulator already made on 1 Oct 2026, so
executives have already seen it and already know it did not fix the counter.

**Why it fails:** the arithmetic in `problems.md` kills it before any AI is involved. A ~1% MDR
consumes half or more of a distributor's entire profit and a merchant on 1–2% margin will never
accept a 1% fee. Zero MDR is still a fee relative to cash, and cash is the settlement guarantee.
Deleting the fee does not delete the reason for cash.

## L2. An AI feature on an existing screen

**Khata reader.**
Photograph the shopkeeper's handwritten credit book. The system reads the Bangla handwriting and
dates, reconstructs who owes what to whom, and turns one line into a digital payment request the
distributor can settle. The khata stops being a reason to carry notes.

**AI decides:** which handwritten line corresponds to which order, and how confident that reading
is; below threshold it asks the shopkeeper, above it it presents the request.

**Lane:** A.

**Data:** `REAL` — NumtaDB handwritten Bengali digits (CC-adjacent, direct download) and
bengaliai-cv19 graphemes for the characters. `COLLECTABLE` — photographed khata pages from campus
shops and family credit books with shopkeeper consent and blurred names, which is the only source
of *layout* (columns, date conventions, running balances) that no public dataset covers. This is
the inventory's explicit "khata pages + NumtaDB digits" combination.

**Demo:** a judge photographs a real consented khata page on their own phone; within seconds a
payment request for one specific line appears, with the recognised Bangla date and amount shown
back for confirmation.

**Challenger weapon:** this is the only artifact in the entire Bangladeshi MFS stack that has no
digital representation. No incumbent has it, and it converts the most trusted record a retailer
owns into an upay-native flow — which is a switching reason, not a feature.

**First thing that makes it fail:** OCR on messy shop handwriting with column drift, mixed
Bangla/English numerals, and no ground truth is the hardest 48-hour build in this document. If the
recognition is wrong on a real page, the demo fails live, and a wrong amount sent to a distributor
is a real trust-ending event.

## L3. A mechanism change

**Delivery-linked escrow for the wholesale leg.**
A distributor releases goods to a retailer against a digitally paid, AI-attested delivery instead of
against a bundle of notes. upay holds the payment until the delivery signal confirms arrival; the
distributor gets digital upstream volume it currently refuses; upay earns a small settlement fee
plus float instead of losing MDR on a round trip.

**AI decides:** has this consignment actually arrived, on the evidence available at the retailer
and the distributor?

**Lane:** B.

**Data:** `SIM` calibrated to named public numbers — distributor margin BDT1–2 per Tk100, the
~1% MDR that consumes it, the ~2% round-trip cost, 62% of merchants facing 3–7 day settlement
delays, 37% avoiding digital because distributors demand cash. `COLLECTABLE` — what actually
constitutes proof of arrival for 20 retailers and 10 distributors, which the simulation cannot
invent and which is the whole feasibility question.

**Demo:** a simulated consignment. Money is paid digitally, held on screen; a delivery event
releases it; the counter shows the distributor's real BDT1–2 margin preserved rather than eaten.

**Challenger weapon:** it attacks the *distributor's* refusal, which is the actual blocker, and it
aligns the party with 10× the margin. Incumbents cannot do it because they would have to persuade
their own distributors to accept a new confirmation standard — a challenger can simply be the one
distributor-side tool in the market.

**First thing that makes it fail:** if "delivery evidence" turns out to be a phone call, there is
no mechanism and it collapses back to the khata problem wearing a market-design hat. The AI has
to find a signal neither party currently generates.

## L4. DELETE the problem

**Skip the retailer entirely.**
Wholesaler sends payment straight to the distributor; the retailer's cash never enters the system,
so there is nothing to cash out and no round trip to pay for. The ~2% disappears because the leg
that caused it is deleted, not discounted.

**AI decides:** which retailer deliveries are being settled — and, from the transaction stream,
whether a given retailer should be paid direct-to-distributor rather than direct-to-agent.

**Lane:** B.

**Data:** `SIM` on the same named public numbers; the whole point of the deletion is that it needs
fewer parameters, not more.

**Demo:** the round-trip cost line on the whiteboard drops to zero because the line is deleted,
and the retailer is handed cash-free what it was previously given cash for.

**Challenger weapon:** every other answer here tries to make the upstream leg cheaper. This makes
it absent. It is the only one that survives a regulator asking "why are you moving a retailer's
money?" — because no retailer money moves.

**First thing that makes it fail:** retailers are the distributor's credit customers. Paying the
distributor directly converts a receivable into a cash sale and destroys the distributor's
working-capital position — which is precisely the BDT1–2 per Tk100 they were surviving on. The
deletion transfers the problem rather than solving it.

## L5. Unreasonable idea 1

**Subsidise the cash-out, openly.**
If the round trip is the problem, stop fighting it: publish a capped, rate-limited, transparent
subsidised cash-out for upay-originated merchant payments — say free withdrawal up to a daily cap
— and take the loss knowingly as an acquisition cost against Tk1.1bn/day of daily QR volume.
Cash-out is not the enemy; unpriced cash-out is.

**AI decides:** who gets the free tier and how much, within a fixed published subsidy budget.

**Lane:** B.

**Data:** `SIM` on named public numbers — cash-out runs at roughly zero gross margin (1.304%
revenue vs ~1.300% cost), so this is explicitly a P&L decision with a computed ceiling, not a
saving. `COLLECTABLE` — willingness to use a branded free-cash-out point, from 20 merchants.

**Demo:** a merchant's daily cash-out is shown free up to a visible cap, then priced — with the
subsidy budget ticking down on screen, so the executive sees the taka.

**Challenger weapon:** it is unfalsifiable in a pitch and fatal in an audit. Every incumbent is
structurally forbidden from it (their cash-out is already at zero margin), so a challenger can
price it as a strategic loss-leader and be believed — or disbelieved, which is the risk.

**First thing that makes it fail:** at 1.1bn taka a day, any cap that merchants respect is either
too small to change behaviour or too large to survive the balance sheet. There is a band where this
works and the pitch cannot prove it is inside it.

## L5. Unreasonable idea 2

**Agent float as a priced public utility.**
Turn agent float into an openly traded, transparently priced capacity — merchants and distributors
bid for guaranteed next-day cash availability, and the price of float is set by demand rather than
by a tariff schedule. The February 2026 96-hour restriction that suspended Dhaka cash-out
altogether becomes, in this world, a shortage with a visible price.

**AI decides:** the next-window float allocation, given bids, observed withdrawal pressure, and
each agent's actual float rather than its declared float.

**Lane:** B.

**Data:** `SIM` calibrated to named public numbers — agents already take ≥Tk6.40 per Tk1,000 of
the cash-out fee, ~2.4m agents depend on it, and human DSR runners already exist as an informal
price-discovery mechanism (which is why `problems.md` scores P9 unsolvedness at only 3).

**Demo:** a bid placed for float, the allocation shown against competing bids, and the resulting
price per taka displayed live.

**Challenger weapon:** it prices an asset incumbents give away for free as a cost line. A
challenger that publishes a float index is publishing a number incumbents cannot match without
admitting their agent economics were unmanaged — and it converts the agent network from a cost
centre into a revenue line, which is exactly what a challenger needs against 2.4m agents.

**First thing that makes it fail:** agents will not bid for something they currently receive as a
guaranteed allocation, and a float auction invites front-running by the agents with the most cash
— which is a small number of agents.

## L6. Import — verified by search

**(a) China Alipay: escrow as the trust product, monetised from float.**
Verified: Alipay's original core was an **escrow system** — the buyer's payment is held by Alipay
until the buyer confirms receipt; the merchant has certainty the money exists before dispatching
and is paid if no complaint is raised within **7 days** of delivery; Alipay's profit came
principally from **cash flow** (buyers pay on order, merchants are paid weekly or monthly), plus
ads. It now serves 500,000+ external merchants.
([HBS Ai Institute case study](https://aiinstitute.hbs.edu/platform-rctom/submission/alipay-wining-the-payments-game-in-china/),
[Stripe Alipay guide](https://stripe.com/en-jp/resources/more/alipay-an-in-depth-guide))

**Bangladesh-specific twist:** drop the 7-day dispute clock — it assumes a consumer who will
complain to a platform. Use the **khata as the dispute instrument** instead: upay holds funds
until the shopkeeper's handwritten book marks the goods received, and the AI reads that mark.
Bangladesh's genuine settlement guarantee is the notebook, not the consumer complaint, so the
escrow clock should be set by when the notebook is updated. And take the profit the way Alipay
did — from float, because BDT1–2 per Tk100 of distributor margin on 17.4tn of trade is enough to
fund float without touching the merchant's fee at all.

**(b) Brazil Pix: dynamic QR with an embedded invoice reference, for B2B specifically.**
Verified: Pix distinguishes static and **dynamic QR codes for B2B**, and Stripe's technical guidance
is explicit that because Pix is a push payment with instant confirmation, businesses use dynamic
or structured payment requests with **embedded invoice references to automate reconciliation** —
which is what converts a push payment into a matching-able one.
([Stripe Pix payments](https://docs.stripe.com/payments/pix?locale=en-GB),
[Matera Pix whitepaper](https://20392958.fs1.hubspotusercontent-na1.net/hubfs/20392958/Whitepaper%20-%20US/matera-pix-by-the-numbers-q4-2024.pdf))

**Bangladesh-specific twist:** Bangla QR's dynamic variant exists but is used as a *payment request
from the merchant*, which still says nothing about which delivery it settles. upay's dynamic QR
embeds the **consignment** — the SKU count, the distributor, the expected arrival window — so the
payment and the goods are one object. That is the missing evidence, and it costs nothing to add to
a QR that already supports dynamic payloads. The reconciliation saving is the pitch; the consignment
link is the product.

---

# P7 — The MFS wallet is the disbursement rail for illegal lenders

## L1. The obvious fix

**Blocklist the apps and detect their disbursements.**
BFIU has named 31; upay flags incoming transfers from known mule patterns and freezes.

**AI decides:** at best, whether a counterparty is on a list.

**Lane:** A (crowded) or B (rule).

**Data:** `REAL` — IEEE-CIS fraud labels and Elliptic graph are available but both are card and
crypto, not MFS send-flow; PaySim is synthetic and fails strict test 2 by the inventory's own
assessment. There is no real Bangladeshi loan-app dataset.

**Demo:** a blocklist matching demo.

**Challenger weapon:** none. `problems.md` records that fraud (Track 01) is the most crowded lane
at this hackathon and that detection is a losing frame.

**Why it fails:** 31 named against thousands live. The apps are unregistrable, so BFIU can only
publish names, and the money lands on bKash and Nagad numbers — not upay's. Blocking upay's rail
does nothing except push disbursement to a wallet that will not block. It also fails the strict
ideation test: remove the model and you still have a list.

## L2. An AI feature on an existing screen

**The intercept.** In the send-money screen, when a customer's recipient is a number that has also
received from known high-arrears lending patterns, upay shows one Bangla line with the reason: *you
borrowed Tk24,000 and are being asked for Tk81,000. Here is what upay would charge.* No block, no
warning lecture — a price.

**AI decides:** whether this send is an instalment payment to an unlicensed lender, and therefore
whether to show the alternative at all.

**Lane:** A.

**Data:** `COLLECTABLE` — the inventory's highest-uniqueness item: real scam SMS, screenshots and
call stories from our own and relatives' phones, consented and redacted; nothing public contains
this. `REAL` as the classifier seed — BanFakeNews-2.0 (Apache-2.0) and SentNoB for labelled
Bangla text, BLUGE-bengali-ner for entity extraction. The test set must stay real (inventory's
explicit SLR37 rule: synthetic data for training, real for testing).

**Demo:** a judge types a real number that is on a live loan-app arrears list (obtained with
consent, redacted) and sees the price comparison appear in Bangla before they can confirm.

**Challenger weapon:** it does not compete with bKash on detection, it competes by being the only
app that shows the *true cost of the alternative*. The harassment and the Tk81,000 figure come
from Prothom Alo's own victim interviews — using the victims' own arithmetic is something no
blocklist product can do.

**First thing that makes it fail:** showing a price is not enough. A borrower who needs Tk24,000 in
twenty minutes takes it anyway, and upay has now built a payday-loan marketing surface.

## L3. A mechanism change

**Credit passport.**
Make upay's ledger the repayment record these borrowers have never had, and make that record
*portable and visible to the borrower* — a score built only from what upay can lawfully observe,
which the borrower can show any licensed lender. Then offer a small, human-approved, capped line to
people the illegal apps target, priced off that passport. The apps lose the one thing they cannot
fake: a repayment history their victims cannot produce.

**AI decides:** the risk tier shown to the borrower and the offered limit — explicitly as a
recommendation to a human underwriter, never as an autonomous approval.

**Lane:** B.

**Data:** `REAL` — Global Findex 2025 for the BD demand-side baseline (who holds accounts vs who
borrows); `COLLECTABLE` — interaction logs from a clickable prototype, which is the only source
that captures how a real person actually stalls at a money decision. `SIM` for the repayment
elasticity, calibrated to the Tk24,000 → Tk81,000 arrears figure.

**Demo:** a consented volunteer's real (redacted) upay-style spending pattern produces a passport
with named contributing signals, and a deliberately empty passport is shown next to it — showing
that the illegal app's "score" is not a score.

**Challenger weapon:** it changes who decides. The illegal app decides eligibility from data the
borrower gave up under duress; upay decides from the borrower's own ledger and shows the reasoning
back. That is a claim bKash cannot make without adopting it, and it is the argument Track 03
(Financial Independence) rewards.

**First thing that makes it fail:** Bangladesh Bank rules and the event's own Responsible AI
minimums forbid autonomous approve/deny of consequential financial decisions, so the AI can only
recommend — and a human-in-the-loop credit desk does not exist inside a 48-hour demo. The moment
the product needs a real underwriter it stops being a product and becomes a policy proposal.

## L4. DELETE the problem

**Quarantine balance.**
An incoming transfer from an unregistered or unidentifiable disbursement lands in a locked
sub-balance that can be **spent at merchants but never cashed out**, until it is either matched to
a licensed lender's repayment schedule or released as the customer's own funds after a window.
The victim of an illegal loan cannot be drained into handing over cash to the operator, and the
operator's incentive to keep a MFS wallet open on a victim's phone disappears.

**AI decides:** whether this incoming balance is a licensed credit repayment or an unregistered
disbursement.

**Lane:** B.

**Data:** `SIM` on named public numbers (BFIU's 31 named apps; Tk24,000 → Tk81,000 in one week);
the mechanism needs no behavioural data, only the inbound flow.

**Demo:** an inbound Tk24,000 arrives; the balance shows as spendable-at-merchants only, with a
countdown and a "release" button that unlocks once it is explained.

**Challenger weapon:** it removes the harm without touching the app, without a blocklist, and
without blocking a customer. Every incumbent response is a block, and blocks push users into worse
products. This is the only answer in this section that leaves the user with more control than they
had.

**First thing that makes it fail:** quarantining an inbound transfer is an account restriction.
The moment it hits a legitimate transfer — a family member remitting, a business payment — upay has
frozen a real customer's money and taken on exactly the regulator relationship P6/P7 warns about.

## L5. Unreasonable idea 1

**Buy the apps out.**
The apps are unregistrable, unsupervised and want legitimacy more than they want to exist. Pay
them to shut down, publish their victim ledger, and fund victim settlement in cash. Cost is
bounded and known; the alternative is an unbounded enforcement cost against an unregistrable target
where CID and DB Dhaka report receiving no cases at all.

**AI decides:** nothing at runtime. This is an acquisition, and the model later prices the same
victim population.

**Lane:** B.

**Data:** `REAL` — Prothom Alo's five victim interviews and the absence of police complaints;
`SIM` for the settlement cost against the named ~Tk9,000 average fraud loss and the
Tk24,000 → Tk81,000 case.

**Demo:** a settlement calculation showing what full victim reimbursement costs per acquired app,
against what enforcement has cost to date.

**Challenger weapon:** no incumbent can do this — bKash cannot be seen buying its competitors'
victims. A challenger can, publicly, and the PR value of "we paid the victims" is worth more than
the cost, especially against a regulator that has failed to act.

**First thing that makes it fail:** it is not a hackathon project, it is a negotiation, and it pays
criminals with victim money in the first scene a judge watches. The honest version — publish the
cost model, show the mechanism, state that the deal is out of scope — is the only buildable form.

## L5. Unreasonable idea 2

**Publish the hundi price list for loans.**
Run upay's own transaction stream through a model that estimates the *effective annualised cost* of
an unlicensed loan from observed disbursement-to-arrears behaviour, and publish it as a public list,
like a consumer price comparison. TK24,000 → Tk81,000 in a week becomes a published number that
every newsroom in the country can repeat.

**AI decides:** the implied cost of borrowing, per app, per week, from flows only — no app
cooperation, no contact-list access.

**Lane:** A (model) inside a B (market/social) mechanism.

**Data:** `SIM` flows calibrated to named public numbers (500,000+ Play installs on one app;
Tk24,000 → Tk81,000 in one week); `REAL` framing — BFIU's 31 named apps, and the precedent that
TIB publishes similar national figures.

**Demo:** a live counter that fills in implied APR as the judge types a disbursement and an
arrears figure, then a link to the public page.

**Challenger weapon:** upay becomes the institution that named the price of a criminal product. The
executive number — *the average victim pays X% — and it is on our website, not theirs* — is a
single sentence a judge repeats to a colleague.

**First thing that makes it fail:** publishing named implied rates against identifiable apps is a
defamation claim with a legal department attached, and estimating APR from aggregate flows is
statistically fragile enough that one named wrong number destroys the credibility of the whole
list.

## L6. Import — verified by search

**(a) Kenya M-Pesa: Fuliza and M-Shwari — credit priced off the wallet's own behaviour, repaid
same-day by traders.**
Verified: Safaricom/NCBA's **Fuliza** overdraft inside M-Pesa serves **33.4m users** with
**KES 2.9tn (~$22.4bn) lifetime disbursal**, and approvals are driven by a credit score computed
from **M-Pesa, M-Kesho and bank activity over the previous 6 months**; M-Shwari serves 32m users.
Critically for our use, the IMF records that the leading digital lender's loan volume **spikes
between 3 and 5 a.m.**, when small traders buy stock and **repay the same day**.
([IMF Kenya digital transformation](https://www.imf.org/-/media/files/news/seminars/2018/fintech-ssa-2018/mr-nyaoga-chairmans-presentationrevised-jul-5-2018digital-transformation.pdf),
[NBER M-Pesa paper](https://www.nber.org/system/files/working_papers/w17129/revisions/w17129.rev0.pdf),
[NCBA digital lending 2024](https://bhluemountain.com/2025/05/27/kenyas-ncba-disbursed-over-7-7-billion-in-digital-loans-in-2024))

**Bangladesh-specific twist:** Kenya's small-trader credit cycle is an **inventory** cycle — stock
in at dawn, sold out by night, repaid same day. Bangladesh's equivalent is the same, which means the
line should be drawn against *observed stock-purchase transactions* in the wallet, not against a
declared business purpose, and repaid against *observed sales* rather than a calendar date. The
twist is the repayment trigger: our version ties repayment to the merchant-side inflow the shop
already generates, so a trader's line closes itself when the stock sells — which means the lender
never experiences the collection problem that makes these apps brutal.

**(b) India UPI Credit Line — a pre-sanctioned line as a funding account, with withdrawal
prohibited.**
Verified: RBI's 4 Sep 2023 circular and NPCI's 20 Sep 2023 operating circular made a **pre-sanctioned
credit line usable as a UPI funding account**, linked by mobile number to any UPI app with a
**dedicated PIN distinct from the account's**, and NPCI required acquirers to enforce that
**"cash withdrawal at merchants shall not be permitted"** on credit-line funds. UPI also raised P2M
limits to ₹10 lakh/day for verified categories from 15 Sep 2025.
([NPCI circular](https://avantiscdnprodstorage.blob.core.windows.net/legalupdatedocs/26578/NPCI_issued_an_Operating_circular_for_Pre-Sanctioned_Credit_Lines_at_Banks_through_UPI_September222023.pdf),
[RBI note via FIDC](https://www.fidcindia.org.in/wp-content/uploads/2025/09/FIDC-DG-RBI_23Sept2025_Allowing-NBFCs-to-Offer-Credit-Lines-on-UPI.pdf),
[NPCI Credit Line on UPI](http://www.npci.org.in/product/upi/credit-line-on-upi),
[PIB 2025-09-17](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/sep/doc2025917639601.pdf))

**Bangladesh-specific twist:** take the PIN separation and the **withdrawal prohibition**, drop the
lender. UPI's rule that credit funds may be spent at merchants but never withdrawn at a merchant
counter is precisely the constraint that stops an under-served borrower from turning a credit line
into cash for an app's fee. So the product is not a loan at all: it is a **spend-only, merchant-
constrained buffer** attached to a repaid-in-full history, with a separate PIN, where the only way
to move the money is to buy stock. It is simultaneously the Track 03 empowerment answer, the answer
to the illegal-app complaint, and — because credit never leaves the merchant network — an
incremental transaction generator. No autonomous approve/deny: the buffer size is a recommendation
to a human.

---

# P3 — Fraud money is unrecoverable because the only thing that works is a lawyer, inside two hours

## L1. The obvious fix

**Auto-reverse suspicious authorised sends within N minutes.**
Recovery inside 1–2 hours is 70–80% versus under 20% after cash-out. Just automate it.

**AI decides:** whether to reverse — i.e. to deny a completed financial transaction.

**Lane:** B, but the decision is prohibited.

**Data:** `REAL` — the TIB figures (58.8% never complain, 38.1% of those who do get resolution,
6.2% know CIPC exists, ~Tk9,000 average loss) and the recovery-rate-within-window figures.

**Demo:** a reversal firing in a sandbox.

**Challenger weapon:** it is the thing every judge wants to see and the thing that disqualifies the
project. The event rules state no autonomous approve/deny of consequential financial decisions, and
P4's source states Bangladesh has no defined emergency procedure allowing a pause while a victim is
manipulated — which is a *policy* absence, not a build absence.

**Why it fails:** a model that errs toward reversing destroys a customer's legitimate transfer; one
that errs toward caution recovers nothing. There is no threshold that escapes that trade-off, which
is why the answer has to move to the pre-transaction moment or to the funding, not to the reversal.

## L2. An AI feature on an existing screen

**One-tap dossier.**
A single "I was scammed" button assembles the evidence pack a lawyer, a bank and a police station
each need, in the ten minutes before the money is unrecoverable: the transaction trail across
accounts, the timing relative to the call, the voice/SMS artefacts, the counterparty's own
history, and which of the four institutional recipients this case belongs to.

**AI decides:** which institution this case goes to, and which three evidence items are still
missing.

**Lane:** B (workflow) with an A component.

**Data:** `COLLECTABLE` — real scam call re-enactments and scam stories from own/relatives' phones
(4–6h, consent, redaction mandatory); `REAL` — SLR37 Bengali TTS for generating scam-call audio for
*training only*, BanFakeNews-2.0 and SentNoB as labelled text seeds; BB ICT security advisories
and circulars for the institutional-routing rules.

**Demo:** a judge taps one button on a fabricated-but-realistic case and watches a complete,
filable, Bangla dossier with named missing evidence appear in under ten seconds.

**Challenger weapon:** it sells to upay's own operations team first. TIB's finding is not that
victims cannot get redress — it is that 58.8% never complain and only 6.2% know the complaint
centre exists. A dossier that is *assembled automatically* changes the denominator without
changing any policy, and upay is the only party with the transaction trail in the first place.

**First thing that makes it fail:** assembling the dossier is the easy half. The hard half is that
cross-institution evidence still takes longer than the money survives, so a faster pack arrives at
a counter that still cannot act. This solution buys minutes, and minutes are what was missing.

## L3. A mechanism change

**Pre-funded recovery pool.**
A standing, per-transaction contribution into a recovery fund, so a victim's claim does not need a
court injunction *before* money moves. Participants pay a fraction; receivers of fraud proceeds are
debited when identified. The bottleneck was never detection — it was that the money had to survive
long enough for a lawyer, so we make the lawyer unnecessary for the common case.

**AI decides:** the triage priority — which case consumes the scarce legal hour, ranked by
recovery probability per taka, with a named reason per case.

**Lane:** B.

**Data:** `SIM` calibrated to named public numbers (~Tk9,000 average loss, 70–80% recovery inside
1–2h versus under 20% after, 58.8% non-reporting, the Tk80,000 voice-scam case where Tk50,000 was
reported blocked and only Tk10,429 remained a month later). Every figure traces to `problems.md`.

**Demo:** twenty queued claims, one legal-hour budget. The model shows the allocation and the taka
recovered, and then the same twenty with a naive FIFO queue for comparison.

**Challenger weapon:** it converts an operational bottleneck into an economic one, which is a
decision upay can make unilaterally. And the recovered-taka-per-legal-hour curve is the single
executive number the pitch needs: *we move recovery from 38% to a number we chose, at a known cost
per taka.*

**First thing that makes it fail:** the pool is a liability that has to be funded by a levy on
every transaction, and a levy on every transaction is a price rise in a market with a
Tk13.95-per-1,000 competitor. The pool's cost per taka recovered has to come in under the margin of
one cash-out transaction, which is a very short distance.

## L4. DELETE the problem

**Not-yet-sent.**
For authorised send-money above a threshold to a first-time or long-dormant recipient, the money
does not leave immediately. It is held, briefly, while upay's model checks the transfer against
what it knows — and released automatically in the clear case. The victim does not need to call,
complain, produce evidence, or win a race. The scam does not complete; nothing needs to be undone.

**AI decides:** release now or hold — one decision, before the transfer settles.

**Lane:** B (a rule with a model at the decision point, and the rule is what does the work).

**Data:** `REAL` — TIB's finding that providers "lack effective mechanisms to detect or prevent
illicit transactions", plus the observation that in the Tk80,000 case the freeze was reported as
done and Tk39,571 was still unaccounted for a month later. The hold must be short, because the same
case shows held funds leaking.

**Demo:** a judge sends to a stranger's number and watches it sit on screen, then release in three
seconds when the model is confident — and a second send to a familiar recipient that never pauses
at all.

**Challenger weapon:** irreversibility is the entire product. Every remedy in this section operates
*after* a loss; this one makes the loss not occur. It is also the cheapest possible thing to build
in 48 hours, which matters because the mechanism is what judges score.

**First thing that makes it fail:** a hold is a service failure from the user's point of view. If
even 2% of legitimate transfers visibly stall, complaints exceed complaints about fraud, and the
whole category gets regulated. It also cannot touch impersonation where the payee is a real,
trusted contact — which is exactly P4's case.

## L5. Unreasonable idea 1

**Insure it, first-party, unconditionally.**
Following Nubank's Protected Pix — verified at R$5,000/year cover for R$6.99/month, four incidents
a year, explicitly covering impersonation, fake slips and robbery — upay simply covers authorised
fraud losses with its own balance sheet, immediately, without proving anything, because the cost of
the alternative (58.8% never complaining, average Tk9,000, 32% of never-users avoiding MFS out of
fear) is far larger than the payout.

**AI decides:** the payout amount and the claim's category — not whether to pay. Every claim is
paid; the model sets the number and the reason.

**Lane:** B.

**Data:** `SIM` on the named public numbers (Tk9,000 average, Tk80,000 upper case, the 32% of
non-users deterred by fear — that last one is the acquisition argument, and it is in `problems.md`).

**Demo:** a claim filed, paid at the agent in cash, no proof required, with the model showing the
taka recovered and the acquisition value it bought.

**Challenger weapon:** it converts a trust problem into a priced product and it is the only answer
here where the customer is made whole without doing anything. Nubank proved a challenger can carry
insurance on top of a payment rail; nobody has done it in Bangladesh.

**First thing that makes it fail:** it is a P&L decision with no ceiling, it is insurance
underwriting that nobody at upay is licensed to do, and in the worst month a fraud wave costs more
than the fee income it was funded from.

## L5. Unreasonable idea 2

**Outbid the mule.**
Run a public, per-taka bounty on fraud proceeds that arrives through a known mule number, sized
*above* the fraud take. The harvested contact list becomes an attack surface against the operator
rather than a weapon against the victim, and the economics flip: at Tk81,000 of arrears collected,
any operator whose mule network leaks one number loses more than it earns.

**AI decides:** the bounty amount per case, sized to exceed the expected recovery from silence.

**Lane:** B.

**Data:** `SIM` calibrated to named public numbers — the Tk24,000 → Tk81,000 arrears case, the
500,000+ install base, BFIU's 31 named apps; `REAL` framing from Prothom Alo's finding that CID and
DB Dhaka received no complaints at all, i.e. the incentive to stay silent is currently total.

**Demo:** a bounty posted against a simulated mule inflow, with the total payout-to-silence ratio
on screen.

**Challenger weapon:** it is the only answer in this section that pays an adversary rather than a
victim, which is exactly what every enforcement regime in this document has failed to do.

**First thing that makes it fail:** it pays criminals to commit a reportable fraud so upay can pay
them for it. No executive will sign this, and the moment it becomes public it is a confession.

## L6. Import — verified by search

**(a) Brazil Pix: MED, DICT fraud marks, and the 60-minute precautionary block.**
Verified: the Banco Central do Brasil built **MED (Mecanismo Especial de Devolução)**, a special
refund mechanism with **tiered direct refunds to the victim (R$200 → R$5,000)** covering scam and
user error; a **precautionary block** giving PSPs up to **60 minutes of extra time** to stop a
transfer; and **DICT**, a centralised anti-fraud database fed mandatorily by PSPs, where
**accounts carrying a fraud mark are barred from transacting**. Pix's reported fraud is 6–7 per
100,000 transactions and **97% of cases are authorised push payments** — the same shape as P3/P4.
([BCB Pix presentation](https://cdn.bancentral.gov.do/documents/sistema-de-pagos/informacion-general/documents/PIX-Brasil_Jose_Vicente_Mattos.pdf?v=1750032000154),
[BIS lessons appendix](https://www.bis.org/publ/bisbull52_appendix.pdf),
[EMMEC/BCB fraud slide](https://www.emmi-benchmarks.eu/globalassets/documents/pdf/emmec/emmec-meetings-documents/presentation-pix-angelo-duarte-central-bank-of-brazil-dec2025.pdf),
[BCB Resolution 493 summary](https://www.demarest.com.br/en/banco-central-publica-resolucao-que-aperecoe-a-procedimentos-do-pix-resolucao-bcb-no-493))

**Bangladesh-specific twist:** Pix's three mechanisms are *all* cross-scheme, and no Bangladeshi
scheme operator can impose them alone. So split them: adopt the **60-minute precautionary block
inside upay's own ledger today** (unilateral, no regulator, no agreement — which is precisely what
`problems.md` says is missing), and ship **the tiered refund schedule as an open standard** for
any future national scheme, published before any operator adopts it. Two of Brazil's three
mechanisms are then ours by default rather than by negotiation. In taka terms the tiers map to
`problems.md`'s figures directly: ~Tk9,000 average loss, Tk80,000 upper case, so a three-tier
schedule at roughly Tk5,000 / Tk20,000 / Tk80,000 is the calibrated version.

**(b) Nubank: Protected Pix — insured first-party cover sold as a subscription.**
Verified: Nubank launched **Pix Protegido** with Chubb — cover up to **R$5,000/year for R$6.99/
month, four incidents a year** — covering transfers to scammers impersonating family members, fake
bank slips, purchases from fake stores where the goods never arrive, theft of phone/card, and
transactions under physical threat. It is explicitly *not* cover for ordinary delivery problems on
legitimate platforms.
([Nubank newsroom 2025-11-04](https://international.nubank.com.br/company/nubank-launches-protected-pix-enhanced-security-against-theft-and-scams))

**Bangladesh-specific twist:** invert the payment model. Nubank's is opt-in and monthly at a
foreign price point; Bangladesh's equivalent is a **pre-funded taka recovery pool** where the
contribution is a fraction of a basis point on the send fee rather than a separate subscription —
nobody in this population will pay a monthly fee for fraud cover they never expect to use. And
payout in **cash at the agent**, not bank credit, because a victim who has been drained to
Tk10,429 and is calling a helpline does not have a usable bank account. The delivery-problem
exclusion Nubank relies on does not transfer: here a legitimate shop that fails to deliver is a
dispute, and a shop that pays out cash for a QR is P2 — the two are entangled and the boundary has
to be drawn explicitly.

---

# P10 — Women hold 42% of the accounts and under 3% of the cash-out points

## L1. The obvious fix

**Recruit and train more women agents.**
Set a target, run a campaign, certify women agents.

**AI decides:** nothing.

**Lane:** B, no model.

**Data:** `REAL` — women hold ~42% of 239.3m MFS accounts while <3% of 1.5m+ MFS agents are women;
BB's 50% female mandate covers only the 16,000 agent-banking outlets; agent gender is "not tracked,
monitored, or linked to compliance or performance indicators"; 1 in 3 women are uncomfortable at
agent points.

**Demo:** a recruitment dashboard.

**Challenger weapon:** none that survives contact with the market. `problems.md` records that
providers already list female-agent recruitment as a **liquidity, footfall and security problem** —
they have run this campaign and it did not work, because the problem is the agent model, not
recruiting.

**Why it fails:** every stage of the agent journey — selection, licensing, training, daily
operation — assumes a male agent, so women read as "unsuitable" when the model itself is the
exclusion. A recruitment target inside that model produces a number on a slide and no agents on a
street.

## L2. An AI feature on an existing screen

**Discretion routing.**
A setting in the send-money screen that routes to an attested female agent point and masks the
amount at the counter, with the fee and the reason shown plainly. The model scores every agent
point on demonstrated discretion behaviour — not on declared gender, which nobody tracks.

**AI decides:** which agent point is discreet enough for this user, right now.

**Lane:** A.

**Data:** `COLLECTABLE` — interaction logs from a clickable prototype using real women participants
(2–4h, consent, no accounts touched) plus 1-in-3-comfort baseline from UNDP in `problems.md`;
`REAL` for OSM Bangladesh (339MB, ODbL: shops, markets, agent-adjacent POIs) for geographic
feasibility. Gender of agents is **not** collected — that is the point and it is also the fairness
risk to state explicitly.

**Demo:** a judge watches the amount mask on a simulated counter screen, and the routing reason
named in Bangla.

**Challenger weapon:** it monetises something incumbents cannot see because they do not track it —
an attribute nobody has instrumented, published by the first party that does. And "discretion" is a
product a bank can sell; "women agents" is a compliance target a bank has to report on.

**First thing that makes it fail:** discretion routing creates de facto gender segregation in the
agent network, which is a fairness outcome an auditor will find immediately, and it will also fail
in the other direction — an agent flagged as discreet for everyone is discreet for no one.

## L3. A mechanism change

**Home-based agent, and the economics that pay for it.**
Remove the shop requirement: a woman becomes an agent from a room with a phone and a documented
identity, taking home deliveries and assisted transactions. Then pay for *what the shop model
cannot do* — assisted and discreet transactions carry a service fee the merchant point does not
charge, because the merchant point's cost is a shop.

**AI decides:** which transactions are assigned to the home-based tier and at what service level,
from demand density and agent capacity — an allocation decision, not an eligibility decision.

**Lane:** B.

**Data:** `REAL` — the 16,000 agent-banking outlets already run under a 50% female mandate (the
regulatory precedent exists, just not in MFS); WorldPop for population and OSM for distance.
`COLLECTABLE` — 20 women agents or aspiring agents on what a home point actually needs (3–4h,
consented interviews). `SIM` for the service-fee economics against the agent's ≥Tk6.40 per Tk1,000
share.

**Demo:** a home point activated in the app, a delivery routed to it, and the service fee credited
to a real taka figure on screen.

**Challenger weapon:** it moves the entry barrier from capital (a shop) to documentation (an ID),
which is the only barrier a woman's time actually includes. And it creates a revenue line incumbents
cannot copy without cannibalising their own merchant network — a rare asymmetry for a challenger.

**First thing that makes it fail:** a home-based point is a one-person business with no float and
no backup, and cash-out float is what makes an agent's income. Take the shop away and take the
income with it.

## L4. DELETE the problem

**Delete the counter visit.**
Most women's counter activity is cash-in, cash-out and small payments to people nearby. If those
three legs become (a) direct merchant payment, (b) a receive-anywhere receive, and (c) direct
transfer to the recipient's wallet, the uncomfortable interaction has nothing left to happen in.

**AI decides:** which transaction would have been a cash-out and can be re-routed to a digital
counterpart that completes without an agent present.

**Lane:** B.

**Data:** `REAL` — the account/agent gender gap, the 1-in-3 discomfort figure, UNDP's economic-power
framing; `COLLECTABLE` — what the counter visits actually are for, from ~20 women participants.

**Demo:** a day of women's counter activity decomposed into its three legs, each re-routed on
screen, with the visits that disappear counted.

**Challenger weapon:** it is the only answer here that needs no new agents, no training, and no
regulator. It removes the exclusion by removing the occasion, which is a claim incumbents cannot
make because their agent commission model requires the visit to happen.

**First thing that makes it fail:** it deletes the demand side and assumes the supply side will
follow. If women still need cash for physical goods, the counter visit survives and we have added
an app screen to an unchanged world.

## L5. Unreasonable idea 1

**Don't count women at all.**
Score every agent on *discretion* — willingness and demonstrated ability to serve a customer who
needs privacy — and pay for it. Nobody is classified, nobody is counted, no gender data is
collected, no target is set, and money still flows toward whoever serves that demand best, which in
this market is disproportionately women.

**AI decides:** the discretion score, and the premium attached to it.

**Lane:** A inside B.

**Data:** `REAL` — agent gender is explicitly **not tracked or monitored** today, which is a data
void this approach walks around rather than fills; `SIM` for the premium economics against agent
commission. No demographic data is collected, so the fairness check becomes a check that no
protected attribute is used at all — which is a cleaner Responsible AI story than any gendered
alternative.

**Demo:** the leaderboard on screen has no gender column, and nobody can tell who is on it.

**Challenger weapon:** it makes BB's unusable 50% mandate unnecessary by achieving the outcome
without the metric, which is the only move available given the mandate covers 16,000 outlets and
not the 1.5m+ MFS agents who actually matter.

**First thing that makes it fail:** discretion scoring is a proxy for something else — likely
location, likely household composition — and a judge who notices will ask whether the proxy is
doing the discriminating we said it wasn't.

## L5. Unreasonable idea 2

**Productise the workaround.**
Women already transact through a father's, husband's or brother's wallet. Make that an explicit,
paid product: a named linked account where the wallet owner sets a per-transaction ceiling and sees
a redacted ledger. The workaround is already the product; we just put a price on it.

**AI decides:** what the linked owner is told, and what the user is told, about each transaction.

**Lane:** B.

**Data:** `COLLECTABLE` — how many of the ~20 women participants already use a family member's
wallet, and what they would need for it to be acceptable. `REAL` for the underlying gap figures.
This is the highest-risk data collection in this document and must be consented and redacted.

**Demo:** a linked wallet with a ceiling set by the owner and a redacted ledger visible to the
user, both on one screen.

**Challenger weapon:** it monetises an existing behaviour instead of trying to change it, which is
the fastest possible route to P10's demand. And it converts the transaction from an invisible act
into a recorded, bounded, consensual one — which is the same infrastructure the fraud dossier in P3
needs.

**First thing that makes it fail:** it institutionalises financial dependence as a product, it
creates a new fraud surface (a linked account is a new authorisation path), and no judge or
regulator is going to hear it as empowerment.

## L6. Import — verified by search

**(a) Wave (Senegal): free cash-in, free cash-out, 1% send — and the agents' revolt that proved the
service is the product.**
Verified: Wave charges **1% to send but deposit and withdrawal are free at any Wave agent**, bills
are free, and has 7.5m+ downloads; for merchants, **the first 20,000 CFA of daily payments is free
then 1%**. In Dec 2022 incumbent agents in Côte d'Ivoire **halted service to Wave over commission
disputes** — expecting it to cripple Wave — and Wave instead had one of its best weeks in three
years, with transactions spiking.
([wave.com/en/business](https://www.wave.com/en/business),
[Wave app listing](https://mwm.ai/es/apps/wave-mobile-money/1523884528),
[Bloomberg 2022-12-24](https://www.bloomberg.com/news/articles/2022-12-24/fintech-aims-to-take-down-telcos-in-senegal-s-fierce-mobile-money-war))

**Bangladesh-specific twist:** the insight is not the price, it is the **exchange-rate between the
provider and its agents**. Bangladesh's agents take ≥Tk6.40 per Tk1,000 of the cash-out fee and
are simultaneously the 2.4m people most damaged by P2. So upay should use a **subsidised service
fee paid to female and home-based points** — visible on the agent's own screen as income earned
from discretion — funded from the float economics of the merchant tier, and let the agent count
rise without asking any agent to take a pay cut. Wave proved agents will fight over commission and
that the provider can win anyway if the customer-facing service is free.

**(b) India UPI: "cash withdrawal at merchants shall not be permitted" as a standing rule.**
Verified via the NPCI operating circular: for pre-sanctioned credit lines, **acquirers are required
to ensure that cash withdrawal at merchants shall not be permitted**, with a dedicated PIN for
credit-line transactions and merchant-category tagging for compliance.
([NPCI circular 20 Sep 2023](https://avantiscdnprodstorage.blob.core.windows.net/legalupdatedocs/26578/NPCI_issued_an_Operating_circular_for_Pre-Sanctioned_Credit_Lines_at_Banks_through_UPI_September222023.pdf))

**Bangladesh-specific twist:** apply the prohibition in reverse and to a different subject. UPI
bans merchant cash-out so that credit cannot be laundered into cash. Bangladesh's equivalent
prohibition, and it is a much bigger lever, is: **a women's wallet balance cannot be cashed out at
a merchant QR.** One rule, published by the operator, simultaneously (a) removes the transaction
the 1-in-3 uncomfortable customers are avoiding, (b) deletes the P2 cash-out event for those
customers specifically, and (c) removes the exposure that makes fraud reporting hard — because an
agent who can see every transaction is the same exposure `problems.md` names as the reason women
use a family member's wallet. Two of the five problems, one prohibition.

---

# Cross-cutting notes

**The five problems are not five problems.** P2, P8, P7 and P3 all resolve through the same missing
artifact: *a transaction that carries evidence of what physically happened.* P2 needs evidence of a
sale, P8 needs evidence of a delivery, P7 needs evidence of a licensed disbursement, P3 needs
evidence of manipulation. Every L4 deletion in this document is the same deletion applied to a
different moment, and every L3 mechanism is the same idea — attach the evidence, and the economics
follow — aimed at a different counterparty.

**Lane B dominates the surprising entries.** Twelve of the forty change a mechanism, an incentive,
a settlement rule or who bears a cost. That is deliberate and consistent with CONTEXT_v2 rule 6.
The AI in each is a real decision — classification, allocation, eligibility ranking, release —
rather than a detector in a disguise.

**Where the verification is thin.** The `SIM` calibration for P3's recovery pool, P8's escrow
economics and P10's service-fee premium are all built on figures that came from `problems.md`
rather than from upay's own ledger. Before any of those numbers are used in a pitch they need
re-verification, and the Tk5–8-per-1,000 upay loss figure is a company statement as reported by
press, not an audited number.