#!/usr/bin/env python3
"""
spikes/economics.py — back-of-envelope business case for the top 6 UPSIDE ideas
from docs/v2/critique.md.

Run:  python spikes/economics.py
Out:  docs/v2/economics.md   (redirect stdout)

RULES OBSERVED
  * Every input is either SOURCED (with a URL in SOURCES) or ASSUMED (in ASSUMPTIONS).
  * Where a figure cannot be sourced, a range is carried and the range is printed.
  * No scenario is floored at zero to look better than the evidence.
  * upay's own money is separated from social value created. They are not the
    same number and conflating them is the main error this script exists to avoid.

BASE YEAR: 2023 — the last year upay published transaction value, revenue and
loss. No upay P&L for 2024 or 2025 was found publicly. Every "current" figure
below is therefore a 2023 figure, and that is a real limitation, not a formality.
"""

from __future__ import annotations

# ---------------------------------------------------------------- SOURCES ----
# Every verified figure used anywhere below. Key = short id, used in NOTES.
SOURCES = {
    "TBS_UPAY_2023": (
        "upay FY2023: revenue Tk43.32cr (+114% yoy), net loss Tk85.43cr "
        "(2022: Tk117.84cr, 2021: Tk110.20cr), accumulated losses Tk313cr, "
        "total transaction value Tk9,826cr (+87%), registered customers 8.5m, "
        "retail agents ~154k, merchants 14,519.",
        "https://www.tbsnews.net/economy/stocks/upays-accumulated-losses-cross-tk300cr-2023-877946",
    ),
    "MARKEDIUM_UPAY_2021": (
        "upay 2021: 3.9m customers, 106k agents, 195 distribution houses, "
        "13.2m transactions, Tk30.7bn volume, revenue Tk174.2m of which "
        "Tk171.6m (98.5%) cash-out & others, gross profit Tk12.7m (7.3%), "
        "operating loss Tk1,138.3m, G&A Tk366.0m, selling & marketing Tk785.0m.",
        "https://markedium.com/a-performance-overview-of-upays-1st-year-in-operation/",
    ),
    "BB_MFS_FEB2025": (
        "BB MFS comparative summary, Feb 2025: 13 providers; 1,856,190 agents; "
        "239.24m registered customers (male 137.88m / female 101.02m); 1.226m "
        "merchant accounts; 671.34m transactions worth Tk164,726.30 crore in the "
        "month; daily average 23.98m transactions worth Tk5,883.08 crore.",
        "https://www.bb.org.bd/en/index.php/financialactivity/mfsdata",
    ),
    "FE_OCT2025": (
        "MFS Oct 2025: 678.63m transactions (+5.30% mom) worth Tk1.58tn (+2.82%). "
        "P2P = 30.13% of transactions, 134.26m txns, Tk476.93bn. Cash-in 26.10% of "
        "value (Tk413.17bn); cash-out 23.51% of value (Tk372.23bn).",
        "https://thefinancialexpress.com.bd/trade/mfs-transactions-maintain-rising-trend-in-oct-25",
    ),
    "TI_BD_MFS_2025": (
        "TIB MFS governance study 2025: 6.3% of personal account holders, 17.0% of "
        "agents, 1.6% of merchants were fraud victims; 3.6% / 8.7% / 1.4% incurred "
        "financial loss. Loss RANGE for personal users Tk300-Tk83,000 (no mean "
        "published); agents Tk200-Tk376,000; merchants Tk53-Tk45,000. 58.8% of "
        "personal users did not complain; of those who did, 38.1% got resolution. "
        "Only 6.2% know BB's CIPC. Only 7.6% of individual victims filed a police GD.",
        "https://www.ti-bangladesh.org/images/2025/report/mfs/Executive-Summary-Mobile-Financial-Services-Sector-En.pdf",
    ),
    "PRI_2022": (
        "PRI survey (7,279 respondents), 2022: 1 in 10 MFS users victimised; "
        "AVERAGE loss Tk9,000 for a user, Tk18,000 for an agent; ~30% of complaining "
        "users get no resolution.",
        "https://www.tbsnews.net/features/panorama/rate-mfs-fraud-victims-higher-among-highly-educated-401222",
    ),
    "FE_QRMISUSE_2026": (
        "upay states it incurs a cost of ~Tk5-8 per Tk1,000 when its customers pay "
        "another operator's Bangla QR; upay calls for a cost-recovery mechanism "
        "instead of blanket zero IRF. Industry: a Tk10,000 merchant-QR payment can "
        "return ~Tk9,815 in cash; normal MFS cash-out charges Tk13-Tk18.50 per Tk1,000. "
        "BB ordered full Bangla QR adoption by 30 Jun 2026; IRF and the 1% MDR floor "
        "were removed effective 1 Oct 2026.",
        "https://thefinancialexpress.com.bd/trade/bangla-qr-misuse-raises-concerns-over-mfs-sustainability",
    ),
    "TBS_QRMISUSE_2026": (
        "Cash-in costs MFS providers ~Tk6.40 per Tk1,000 (a PROVIDER COST, not an "
        "agent commission). Providers recover it from cash-out charges and MDR. "
        "Cash-out capped Tk30,000/day and Tk2 lakh/month; P2P Tk50,000/day, Tk3 lakh/month.",
        "https://www.tbsnews.net/bangladesh/how-abuse-bangla-qr-threatens-countrys-mfs-ecosystem-1538591",
    ),
    "DS_NAGAD_BDQR_2026": (
        "Nagad, 1-29 Aug 2026: 540,760 Bangla QR transactions worth Tk315.18 crore; "
        "Tk38.11 crore (12.1% of value) transacted between 11pm-6am, flagged as unusual. "
        "Nagad wrote to BB on 2 Sep 2026. BB says an inspection has begun.",
        "https://online.thedailystar.net/news/bangladesh/news/suspicious-payments-shadow-bangla-qr-transaction-boom-4272266",
    ),
    "UNB_BDQR_2026": (
        "BB (30 Sep 2026): average daily Bangla QR value rose from ~Tk28 crore in "
        "June to Tk143.54 crore; daily transactions from ~100,000 to ~350,000; "
        "3.9m (39 lakh) merchant points accept Bangla QR.",
        "https://unb.com.bd/category/Business/bangla-qr-transactions-surge-nearly-fivefold-to-tk-14354cr-daily-bb/196633",
    ),
    "DS_AGENTSPLIT_2021": (
        "Cash-out charge split (bKash statement): 77% agents+distributors, 8% MNOs, "
        "14% MFS providers, 1% government tax. At Tk18.50/1,000 that is Tk14.25/1,000 "
        "to the agent+distributor pool.",
        "https://www.thedailystar.net/business/news/mfs-industry-swells-riding-low-income-groups-2087905",
    ),
    "FE_TARIFF_2021": (
        "An agent receives Tk9.0-plus per Tk1,000 transaction while the retail charge "
        "is Tk18; the agent's take is roughly invariant to the retail charge. The "
        "agency model pays 57-80% of each transaction to the agency chain.",
        "https://today.thefinancialexpress.com.bd/views-reviews/rationalising-high-mfs-charges-1612271914",
    ),
    "TBS_AGENTINC_2022": (
        "BBS survey of 218 mobile banking outlets: a marginal mobile-banking point "
        "earns on average Tk16,370 per month in commissions.",
        "https://publisher.tbsnews.net/supplement/mfs-livelihood-resources-millions-549362",
    ),
    "BKASH_CASHOUT": (
        "bKash published rates: Tk18.50 per Tk1,000 at ordinary agents; Tk13.95 per "
        "Tk1,000 at two 'Priyo Agents' up to Tk50,000/month.",
        "https://www.bkash.com/en/products-services/cashout-from-agent",
    ),
    "TBS_WOMEN_2025": (
        "Women hold 42% of 239.3m registered MFS accounts; fewer than 3% of MFS "
        "agents are female; BB's 50% female mandate applies to agent banking "
        "(16,019 agents / 21,248 outlets), not to the 1.5m+ MFS agents.",
        "https://www.tbsnews.net/thoughts/policy-paradox-heart-bangladeshs-digital-finance-story-1313211",
    ),
    "MSC_WOMEN_2026": (
        "MicroSave (Jan 2026): women are 'less than 1%' of MFS agents; 42% of "
        "accounts. NOTE: conflicts with TBS '<3%'. Both are carried as a range.",
        "https://www.microsave.net/2026/01/12/women-must-power-the-digital-economy/",
    ),
    "UNDP_WOMEN_2025": (
        "UNDP (Sep 2025): discomfort at agent points affects one in three women. "
        "Findex 2025: account ownership 43%, digital payment use 34%, women's "
        "account gap 20pp.",
        "https://www.undp.org/bangladesh/blog/digital-wages-can-unlock-womens-economic-power-bangladesh",
    ),
    "BB_AGENTBANK_2025": (
        "BB agent-banking quarterly (Mar 2025): 15,838 agents, 21,023 active "
        "outlets, 24.67m agent-banking accounts, deposit balance Tk42,632 crore, "
        "loans Tk10,467 crore. Female agents were 9.11% of agent-banking agents at "
        "Dec 2024, before the BRPD 50% circular of 8 May 2025.",
        "https://www.bb.org.bd/pub/quaterly/agent_bank_stat/agent_jan-mar2025.pdf",
    ),
    "MSC_SUPPLY_2026": (
        "MicroSave (May 2026): 7.8m small/medium retailers; >9m microentrepreneurs = "
        "~25% of GDP; only ~10% of flows beyond the retail counter stay digital; ~37% "
        "of retailers avoid digital payments BECAUSE suppliers demand cash; retailer "
        "margin BDT5-10 per BDT100 of goods sold; distributor margin BDT1-2 per "
        "BDT100; MDR usually ~1%, which consumes half or more of a distributor's profit.",
        "https://www.microsave.net/2026/05/14/why-bangladeshs-supply-chains-still-run-on-cash-despite-digitization/",
    ),
    "MSC_ROADMAP_2025": (
        "MSC/BB roadmap: 51% of retail traders cite unclear MDR as a reason to avoid "
        "DFS; 45% of restaurant owners and 58% of retail traders see digital payments "
        "as unprofitable because of high MDR and slow settlement.",
        "https://www.microsave.net/2025/09/26/roadmap-to-strengthen-digital-transactions-in-bangladesh-by-2031/",
    ),
    "TBS_BDQR_INCENTIVE": (
        "BB incentive on Bangla QR NPSB transactions up to Tk2,000: acquirer receives "
        "0.10% capped at Tk2; issuer receives 0.20% capped at Tk4. Paid to "
        "institutions, not customers or merchants.",
        "https://www.tbsnews.net/supplement/bangla-qr-gains-ground-risks-remain-1556986",
    ),
    "PROTHOMALO_LOANAPPS_2026": (
        "Prothom Alo (22 Aug 2026): victim Saeed Mia borrowed Tk24,000 total; after "
        "one week the app showed Tk81,000 in arrears; he repaid Tk54,000; his "
        "acquaintances were called and threatened. n=1. Quick Loan: up to Tk300,000 "
        "at 18% interest, 500,000+ Play installs. Sathi Loan: up to Tk150,000 at "
        "18-26% p.a., 100,000+ installs. PA identified 30 such apps.",
        "https://en.prothomalo.com/bangladesh/crime-and-law/vje45fpc6p",
    ),
    "BFIU_31_2026": (
        "BFIU (27-28 Aug 2026) named 31 unauthorised loan apps (Sathi Loan, Quick "
        "Loan, FinCash, Pop Cash, TakaNow ...). Lending without BB approval is "
        "punishable; may also be a predicate offence under the Money Laundering "
        "Prevention Act 2012.",
        "https://www.tbsnews.net/bangladesh/bfiu-warns-against-borrowing-unauthorised-apps-online-platforms-1526606",
    ),
    "TBS_ELECTION_2026": (
        "BB circular 8 Feb 2026: 96-hour restriction 9-12 Feb. P2P capped at Tk1,000 "
        "per transaction, max 10/day (Tk10,000/day ceiling); IBFT suspended; "
        "cash-in and cash-out suspended at agents. Merchant payments and utility "
        "bills continued. Normal caps: cash-in Tk50,000/day, cash-out Tk30,000/day, "
        "P2P Tk50,000/day. Agents reported unpaid and unable to serve customers.",
        "https://www.tbsnews.net/bangladesh-election-2026/national-polls-bb-limits-p2p-mfs-tk1000-transaction-suspends-internet",
    ),
    "MFS_L6_6": (
        "BB MFS Guidelines cl. 6.6: 'MFS platforms will not engage in any lending "
        "from their own funds, but will be free to act as agents of BB licensed "
        "banks and financial institutions in disbursing loans and in accepting "
        "repayments.'",
        "https://www.bb.org.bd/aboutus/draftguinotification/guideline/mfs_final_v9.pdf",
    ),
    "PSO_REG_2025": (
        "BB draft PSO Regulation 2025: 'Any customer charges will require prior "
        "approval from the central bank.' TSA shortfall penalty is the lower of SLF "
        "(11.50%) or Tk30 lakh; directors/CEO/treasury personally liable.",
        "https://www.bb.org.bd/aboutus/draftguinotification/guideline/PSO_Regulation.pdf",
    ),
    "PSS_ACT_FINALITY": (
        "PSS Act 2024: 'Any settlement executed in accordance with established "
        "procedures is regarded as final, irrevocable, and without dispute.'",
        "https://www.bb.org.bd/pub/annual/psdreport/paymentreport_dec2025.pdf",
    ),
}

# ------------------------------------------------------------ ASSUMPTIONS ----
# Every input with no source. Each is a judgement, not a finding.
ASSUMPTIONS = [
    ("A1", "upay's active-customer rate is 35% of registered.",
     "No source splits upay's 8.5m registered into active. upay's own executive said "
     "~35% for the industry in Dec 2022; BB reported 37.6% active for the industry at "
     "Dec 2024. 35% is the conservative end.", "TBS_UPAY_2023, TI_BD_MFS_2025"),
    ("A2", "upay's 2023 figures still describe its scale.",
     "No upay P&L for 2024 or 2025 is public. If upay has grown, every absolute taka "
     "figure here is too low; if not, they are about right.", "TBS_UPAY_2023"),
    ("A3", "upay's blended take rate is 0.441% of transaction value.",
     "Derived: Tk43.32cr revenue / Tk9,826cr volume. This is upay's realised revenue "
     "yield, not a posted rate.", "TBS_UPAY_2023"),
    ("A4", "upay's customer acquisition cost is Tk201 per net customer.",
     "Derived: 2021 selling & marketing Tk785.0m / 3.9m cumulative customers. This is "
     "a crude proxy: Tk785.0m was a FIRST-YEAR LAUNCH budget including brand spend, "
     "and the denominator is cumulative net adds since inception, not 2021 adds. A "
     "mature CAC is very likely lower. Treat as an upper bound, and note it is a "
     "ONE-OFF figure while revenue per customer is ANNUAL - the two must not be "
     "added without saying so.", "MARKEDIUM_UPAY_2021"),
    ("A5", "Average MFS transaction ticket is Tk2,328.",
     "Derived from Oct 2025: Tk1.58tn / 678.63m transactions. Used to convert upay's "
     "transaction VALUE into a transaction COUNT, which upay has never published.",
     "FE_OCT2025"),
    ("A6", "upay's transaction mix matches the industry mix.",
     "30% P2P, 23.5% cash-out by value. upay's own 2021 split was 98.5% revenue from "
     "cash-out & others, so upay is more cash-out-heavy than assumed here. This makes "
     "the P2P-derived numbers for idea 3 an OVERSTATEMENT.", "FE_OCT2025"),
    ("A7", "upay's cross-operator Bangla QR volume is 1% / 4% / 10% of its total "
           "transaction value.",
     "No source. upay publishes no QR split. BDQR is national; upay holds 14,519 of "
     "1.226m merchant accounts (1.2%), so a small share is plausible but the split "
     "between originating and acquiring is unknown.", None),
    ("A8", "The disguised-cash-out share of cross-operator QR is 3% / 8% / 12%.",
     "No source measures this. The only public detection datapoint is Nagad's 12.1% "
     "of BDQR value transacted 11pm-6am, which is an off-hours proxy, not a "
     "cash-out measurement, and is on one provider and 29 days. 12% is used as a "
     "ceiling, not a central estimate.", "DS_NAGAD_BDQR_2026"),
    ("A9", "A visible payee label prevents 25% / 50% / 75% of the disguised cash-outs "
           "it detects.",
     "No source. A label deters; it cannot block. Nothing establishes a deterrence "
     "elasticity in Bangladesh.", None),
    ("A10", "Fraud incidence among sends to a first-time recipient is 2% / 4% / 8%.",
     "No source. TIB gives 6.3% of ALL personal account holders as annual fraud "
     "victims, which is not comparable to a per-transaction rate. This is the single "
     "weakest number in the model.", "TI_BD_MFS_2025"),
    ("A11", "Stopping a transfer before it settles recovers 30pp / 45pp / 60pp more "
            "than recovering after the money is cashed out.",
     "No source. critique.md used '75% inside 1-2h vs 19% after' with no citation; "
     "that pair is dropped. The clock logic is real (TIB and reporting support the "
     "1-2h ex parte injunction), the magnitudes are not.", "TI_BD_MFS_2025"),
    ("A12", "1% / 3% / 7% of upay's P2P sends go to a first-time recipient.",
     "No source. Bangladesh publishes no first-time-recipient rate. This is invented "
     "and is the second-weakest number in the model.", None),
    ("A13", "The share of upay's active women currently transacting through a family "
            "member's wallet is 1% / 3% / 10%.",
     "No source. UNDP's 'one in three' measures DISCOMFORT at agent points, not "
     "wallet-sharing, and wallet-sharing is not measured anywhere public. "
     "Critique.md's pitch test silently treats these as the same number.", "UNDP_WOMEN_2025"),
    ("A14", "A BB-licensed lender pays upay 1% / 2% / 3% of principal originated via "
            "a credit passport.",
     "No Bangladesh rate exists for this; it does not exist as a product. MFS cl. 6.6 "
     "permits the agency role that makes it lawful.", "MFS_L6_6"),
    ("A15", "0.5% / 2% / 5% of upay's active customers have used an unlicensed loan app.",
     "No source. BFIU named 31 apps; Play install counts are cumulative downloads, "
     "not users, and one app alone shows 500,000+. 600k installs across the two named "
     "apps is a floor for the whole market, not for upay's slice.", "BFIU_31_2026"),
    ("A16", "Average loan taken from an unlicensed app is Tk10,000 / Tk24,000 / Tk30,000.",
     "Tk24,000 is n=1 from Prothom Alo. Tk150,000 and Tk300,000 are the advertised "
     "CEILINGS those apps publish, which is not what victims actually take.",
     "PROTHOMALO_LOANAPPS_2026"),
    ("A17", "upay can reach 500 / 2,000 / 6,000 retailers with a consignment-settlement "
            "product.",
     "No source. Bounded above by upay's 14,519 merchants (2023). The Agrani "
     "Distribution B2B partnership announced Aug 2026 discloses no volume. The "
     "aggressive case is a guess.", "TBS_UPAY_2023"),
    ("A18", "Average wholesale purchase per reached retailer is Tk50,000 / Tk120,000 / "
            "Tk250,000 per month.",
     "No source. No Bangladeshi wholesale ticket is published. If a retailer's whole "
     "turnover is BDT5-10 per BDT100 of goods sold, a Tk120,000 monthly purchase "
     "implies a Tk6,000-12,000 monthly retail business, which is plausible but "
     "unverified.", "MSC_SUPPLY_2026"),
    ("A19", "post-1-Oct-2026 MDR on wholesale can be set at 0.25% / 0.50% / 1.00%.",
     "The 1% floor and zero IRF both took effect 1 Oct 2026, so sub-1% MDR is now "
     "permissible. The specific rates are assumptions. Note the irony: MicroSave's "
     "May 2026 blocker for upstream digitisation was that a 1% MDR eats half a "
     "distributor's 1-2% margin. That blocker has been legislated away; settlement "
     "CONFIRMATION is now the only real blocker, which is exactly what idea 5 sells.",
     "FE_QRMISUSE_2026, MSC_SUPPLY_2026"),
    ("A20", "upay agents hold 0.5 / 1 / 2 days of cash-out float.",
     "No source. Derived ceiling instead: upay's float cannot exceed its own cash-out "
     "flow, so the model prices float as a multiple of daily cash-out volume rather "
     "than an invented per-agent balance.", None),
    ("A21", "5% / 15% / 35% of upay's agents would bid for priced float.",
     "No source, and no evidence was found that float is scarce or contested in "
     "Bangladesh. critique.md residual risk #4 flagged exactly this and it remains "
     "UNRESOLVED. problems.md's own U=3 rating for P9 concedes float shocks are "
     "'partly fixed'.", None),
    ("A22", "A float clearing fee of 0.05% / 0.15% / 0.30% per taka per day.",
     "No reference price exists anywhere. Also a legal risk: charging agents for float "
     "is a levy on agents and needs BB prior approval.", "PSO_REG_2025"),
    ("A23", "Annual operating cost of each mechanism, in Tk crore.",
     "No public figure exists for any of these. Engineering + compliance + field ops, "
     "sized by hand. These drive every break-even in this model and are the least "
     "defensible numbers here.", None),
]

# --------------------------------------------------- VERIFIED upay 2023 ------
CR = 10_000_000.0  # 1 crore = 1e7 taka

UPAY = {
    "revenue_cr": 43.32,        # S: TBS_UPAY_2023
    "txn_value_cr": 9826.0,     # S: TBS_UPAY_2023
    "net_loss_cr": 85.43,       # S: TBS_UPAY_2023
    "accum_loss_cr": 313.0,     # S: TBS_UPAY_2023
    "customers": 8_500_000,     # S: TBS_UPAY_2023
    "agents": 154_000,          # S: TBS_UPAY_2023
    "merchants": 14_519,        # S: TBS_UPAY_2023
    "sm_2021_cr": 78.5,          # S: MARKEDIUM_UPAY_2021 (Tk785.0m = Tk78.5cr)
    "ga_2021_cr": 3.66,          # S: MARKEDIUM_UPAY_2021 (Tk366.0m)
    "op_loss_2021_cr": 113.83,   # S: MARKEDIUM_UPAY_2021 (Tk1,138.3m)
    "revenue_2021_cr": 17.42,    # S: MARKEDIUM_UPAY_2021 (Tk174.2m)
    "customers_2021": 3_900_000,  # S: MARKEDIUM_UPAY_2021
}

INDUSTRY = {
    "accounts": 239_240_000,     # S: BB_MFS_FEB2025
    "female_accounts": 101_020_000,  # S: BB_MFS_FEB2025
    "agents": 1_856_190,         # S: BB_MFS_FEB2025
    "merchants": 1_226_000,      # S: BB_MFS_FEB2025
    "monthly_value_cr": 164_726.30,  # S: BB_MFS_FEB2025
    "p2p_share_txn": 0.3013,     # S: FE_OCT2025
    "cashout_share_value": 0.2351,   # S: FE_OCT2025
    "avg_ticket": 2328.0,        # S: FE_OCT2025 + A5
}

# Derived once, used everywhere.
TAKE_RATE = UPAY["revenue_cr"] / UPAY["txn_value_cr"]        # A3
UPAY_ACTIVE = UPAY["customers"] * 0.35                        # A1
WOMEN_ACTIVE = UPAY_ACTIVE * (INDUSTRY["female_accounts"] / INDUSTRY["accounts"])
REV_PER_CUSTOMER = UPAY["revenue_cr"] * CR / UPAY["customers"]
CAC = UPAY["sm_2021_cr"] * CR / UPAY["customers_2021"]        # A4
UPAY_TXN_COUNT = UPAY["txn_value_cr"] * CR / INDUSTRY["avg_ticket"]   # A5
UPAY_CASHOUT_VALUE_CR = UPAY["txn_value_cr"] * INDUSTRY["cashout_share_value"]  # A6
UPAY_P2P_COUNT = UPAY_TXN_COUNT * INDUSTRY["p2p_share_txn"]   # A6

SCEN = ("conservative", "base", "aggressive")
SI = {"conservative": 0, "base": 1, "aggressive": 2}


def band(lo: float, base: float, hi: float) -> tuple:
    return (lo, base, hi)


# ============================================================== IDEAS ========
# Each idea: who pays, per-unit economics, annual upay P&L in Tk crore,
# social value in Tk crore (kept separate), break-even, two key assumptions.

IDEAS = {}


# --- 1. Women's wallet balance cannot be cashed out at a merchant QR --------
def idea_1():
    share = band(0.01, 0.03, 0.10)          # A13
    cac_weight = band(0.0, 0.5, 1.0)        # A4 applied to the retained customer
    value_per = [REV_PER_CUSTOMER + cac_weight[i] * CAC for i in range(3)]
    upay_cr = [WOMEN_ACTIVE * share[i] * value_per[i] / CR for i in range(3)]
    revenue_only_cr = [WOMEN_ACTIVE * share[i] * REV_PER_CUSTOMER / CR for i in range(3)]
    op = 0.05                                # A23
    be_share = op * CR / (WOMEN_ACTIVE * value_per[SI["base"]])
    IDEAS["1. Women's balance: no merchant cash-out"] = dict(
        who_pays="Nobody pays for the rule. It is a settlement constraint upay "
                 "publishes unilaterally. upay forgoes nothing it books today (a "
                 "disguised cash-out earns upay no MDR and, cross-operator, costs it "
                 "Tk5-8/1,000).",
        mechanism="Changes a settlement rule: a named cohort's balance cannot be "
                  "cashed at a merchant QR.",
        unit=f"per shifted active woman: Tk{REV_PER_CUSTOMER:,.0f}/yr revenue "
             f"retained + up to Tk{CAC:,.0f} one-off CAC avoided",
        unit_social="privacy and dignity; not priced anywhere",
        upay_cr=upay_cr,
        social_cr=[0.0, 0.0, 0.0],
        revenue_only_cr=revenue_only_cr,
        opex=(op, op, op),
    op_cr=op,
        breakeven=f"{be_share*100:.3f}% of active women shifted "
                  f"(~{be_share*WOMEN_ACTIVE:,.0f} users). Near zero, because the "
                  f"rule costs almost nothing.",
        keys=["A13 wallet-sharing rate (unsourced)",
              "A4 Tk201 CAC proxy (2021 launch budget, not a marginal CAC)"],
        verdict="Cheap and real, but NOT a taka story. Revenue-only view is "
                f"Tk{revenue_only_cr[0]:.2f}-{revenue_only_cr[2]:.2f}cr. The "
                "headline number is acquisition-cost avoidance, and that number "
                "rests on a launch-budget proxy. Judge pitch should NOT use a "
                "taka figure for this idea; use the retention one.",
    )


# --- 2. Credit passport: repayment record sold as agency evidence -----------
def idea_2():
    borrower_share = band(0.005, 0.02, 0.05)   # A15
    fee = band(0.01, 0.02, 0.03)               # A14
    loan = band(10_000, 24_000, 30_000)        # A16
    per = [fee[i] * loan[i] for i in range(3)]
    eligible = [UPAY_ACTIVE * borrower_share[i] for i in range(3)]
    upay_cr = [eligible[i] * per[i] / CR for i in range(3)]
    social = [eligible[i] * (81_000 - 24_000) / CR for i in range(3)]  # Tk57,000 gap, n=1
    op = 1.5                                    # A23
    be = op * CR / per[SI["base"]]
    IDEAS["2. Credit passport (agency sale of record)"] = dict(
        who_pays="A BB-licensed bank or NBFC pays, on loans originated through the "
                 "passport. upay is the agent, not the lender - the role BB MFS "
                 "Guidelines cl. 6.6 explicitly permits.",
        mechanism="Changes who decides eligibility: the borrower's own repayment "
                  "ledger, shown back to them and sold as evidence.",
        unit=f"per borrower originated: Tk{per[0]:,.0f} / Tk{per[1]:,.0f} / "
             f"Tk{per[2]:,.0f} (1/2/3% of a Tk10k/24k/30k loan)",
        unit_social=f"per borrower: Tk{81_000-24_000:,} of avoided arrears "
                    "(n=1, Prothom Alo)",
        upay_cr=upay_cr,
        social_cr=social,
        opex=(op, op, op),
    op_cr=op,
        breakeven=f"{be:,.0f} borrowers/yr = {be/UPAY_ACTIVE*100:.3f}% of upay's "
                  f"active base",
        keys=["A15 share of active customers who used an unlicensed app (unsourced)",
              "A14 agency fee rate (no such product exists, so no market rate)"],
        verdict=f"Base case Tk{upay_cr[1]:.2f}cr = {upay_cr[1]/UPAY['revenue_cr']*100:.0f}% "
                f"of upay revenue, against a social pool ~13x larger. The economics "
                "are small; the compliance exposure is the real risk, not the upside.",
    )


# --- 3. Not-yet-sent: hold above threshold to a first-time recipient --------
def idea_3():
    incidence = band(0.02, 0.04, 0.08)        # A10
    delta = band(0.30, 0.45, 0.60)            # A11
    first_time = band(0.01, 0.03, 0.07)       # A12
    per = [9000.0 * incidence[i] * delta[i] for i in range(3)]
    held = [UPAY_P2P_COUNT * first_time[i] for i in range(3)]
    victim_cr = [held[i] * per[i] / CR for i in range(3)]
    goodwill = band(0.5, 1.5, 4.0)            # A23 - upay's own budget, a pure COST
    upay_cr = [0.0, 0.0, 0.0]               # upay recovers nothing; the victim does
    be = goodwill[SI["base"]] * CR / per[SI["base"]]
    IDEAS["3. Not-yet-sent (pre-execution hold)"] = dict(
        who_pays="Nobody. upay PAYS: a goodwill reimbursement budget plus review ops. "
                 "The recovered taka belongs to the victim, not to upay, and upay "
                 "cannot book it. A protection fee on the sender would need BB "
                 "prior approval as a customer charge.",
        mechanism="Changes when irreversibility happens: before settlement, not "
                  "after. Nothing settled is ever reversed (PSS Act 2024 finality).",
        unit=f"per hold-eligible send: Tk{per[0]:,.0f} / Tk{per[1]:,.0f} / "
             f"Tk{per[2]:,.0f} of VICTIM loss avoided",
        unit_social="per stopped fraud: Tk9,000 retained by the victim "
                    "(PRI 2022 mean; TIB 2025 publishes only a Tk300-Tk83,000 range)",
        upay_cr=upay_cr,
        social_cr=victim_cr,
        opex=goodwill,
    op_cr=goodwill[SI["base"]],
        breakeven=f"NEVER on upay's P&L: saving Tk0 to upay, cost "
                  f"Tk{goodwill[0]:.1f}-{goodwill[2]:.1f}cr. On a social-cost "
                  f"basis, Tk{goodwill[1]:.1f}cr of ops buys "
                  f"Tk{victim_cr[1]:.2f}cr of victim recovery "
                  f"({victim_cr[1]/goodwill[1]:.0f}x).",
        keys=["A10 per-send fraud incidence (unsourced; weakest number in the model)",
              "A11 pre-vs-post recovery delta (critique's 75%/19% pair had NO source "
              "and is dropped)"],
        verdict="CORRECTION TO critique.md. Its pitch number 'Tk9,000 -> Tk6,750 per "
                "stopped transfer' is victim economics, not upay economics. upay's "
                "annual P&L impact is NEGATIVE. Do not put an upay taka number on "
                "stage for this one.",
    )


# --- 4. QR payee-identity label at scan time --------------------------------
def idea_4():
    xop = band(0.01, 0.04, 0.10)              # A7
    disguised = band(0.03, 0.08, 0.12)         # A8
    prevented = band(0.25, 0.50, 0.75)         # A9
    rate = (5.0 + 8.0) / 2 / 1000              # Tk6.5 per Tk1,000 - SOURCED, upay's own words
    xop_cr = [UPAY["txn_value_cr"] * xop[i] for i in range(3)]
    saved_cr = [xop_cr[i] * disguised[i] * prevented[i] * rate for i in range(3)]
    gross_cr = [xop_cr[i] * rate for i in range(3)]   # ceiling: ALL cross-op QR is disguised
    op = band(0.2, 0.8, 1.5)                   # A23
    be_vol = op[SI["base"]] / rate
    be_vol_low = op[0] / rate
    p = disguised[SI["base"]] * prevented[SI["base"]]
    be_share = be_vol / p / UPAY["txn_value_cr"]
    be_share_low = be_vol_low / p / UPAY["txn_value_cr"]
    IDEAS["4. QR payee-identity label at scan time"] = dict(
        who_pays="Nobody. It is loss prevention and enforcement targeting under BB's "
                 "Apr 2026 circular, which already orders cancellation of cash-out "
                 "merchants - the model decides WHICH points get de-registered.",
        mechanism="Changes who decides: the customer, at scan time, instead of the "
                  "platform, after the fact.",
        unit=f"per Tk1,000 of DISGUISED cross-operator QR prevented: Tk6.50 "
             f"(upay's own stated Tk5-8/1,000 cost, midpoint)",
        unit_social="merchants de-registered are the only agents who lose; labelling "
                    "loses no merchant (bKash removed 7,000+ points instead)",
        upay_cr=saved_cr,
        social_cr=[0.0, 0.0, 0.0],
        opex=op,
    op_cr=op[SI["base"]],
        breakeven=f"needs Tk{be_vol:,.0f}cr/yr of disguised cross-op QR prevented "
                  f"= {be_share*100:.0f}% of upay's ENTIRE transaction value. "
                  f"NOT ACHIEVABLE at op cost Tk{op[1]}cr. Even at a stripped-down "
                  f"Tk{op[0]}cr op cost it needs {be_share_low*100:.0f}% - a stretch. "
                  f"Put differently: upay's TOTAL cross-operator QR loss, if every "
                  f"cross-op taka were a disguised cash-out, is Tk{gross_cr[2]:.2f}cr "
                  f"at the aggressive volume assumption, against a Tk0.8cr cost.",
        keys=["A7 cross-operator QR share of upay volume (upay publishes no QR split)",
              "A8 disguised-cash-out share (only public proxy is Nagad's 12.1% "
              "off-hours share of its own BDQR, 29 days)"],
        verdict=f"FAILS ITS OWN BREAK-EVEN. upay's ENTIRE cross-operator QR cost "
                f"ceiling is Tk{gross_cr[0]:.2f}-{gross_cr[2]:.2f}cr/yr - the "
                f"problem is real but at upay's 0.5% volume share it is not a P&L "
                f"event. Salvage as a compliance/BB-relationship story, not a "
                f"savings story.",
    )


# --- 5. Consignment-embedded QR + khata-marked escrow release ----------------
def idea_5():
    retailers = band(500, 2_000, 6_000)        # A17
    wholesale = band(50_000, 120_000, 250_000) # A18
    mdr = band(0.0025, 0.005, 0.010)          # A19
    vol_cr = [retailers[i] * wholesale[i] * 12 / CR for i in range(3)]
    upay_cr = [vol_cr[i] * mdr[i] for i in range(3)]
    social_cr = [vol_cr[i] * 0.015 for i in range(3)]   # distributor margin Tk1.50/Tk100
    op = 1.0                                   # A23
    be_vol = op / mdr[SI["base"]]
    be_ret = be_vol * CR / 12 / wholesale[SI["base"]]
    IDEAS["5. Consignment QR + khata escrow"] = dict(
        who_pays="Nobody pays upay a new fee - upay earns ordinary MDR on wholesale "
                 "volume that is currently 100% cash. The distributor's preserved "
                 "margin (Tk1.50 per Tk100) is the value created and it belongs to "
                 "the distributor.",
        mechanism="Changes settlement: payment and goods become one object, so the "
                  "distributor's goods release is backed by evidence rather than a "
                  "bag of notes. Escrow is a TSA question under PSS Act 2024 / PSO "
                  "Regulation 2025 and must be resolved before build.",
        unit=f"per Tk100 of wholesale: upay earns Tk{mdr[SI['base']]*100:.2f} MDR; "
             f"distributor keeps Tk1.50 of margin",
        unit_social="Tk15.00 of distributor margin preserved per Tk1,000 "
                    "(midpoint of BDT1-2 per BDT100, MicroSave)",
        upay_cr=upay_cr,
        social_cr=social_cr,
        opex=(op, op, op),
    op_cr=op,
        breakeven=f"Tk{be_vol:,.0f}cr/yr of wholesale volume = "
                  f"{be_ret:,.0f} retailers at Tk{wholesale[SI['base']]:,}/month. "
                  f"Modest - and the Agrani Distribution B2B channel announced "
                  f"Aug 2026 is the obvious route, but it discloses no volume.",
        keys=["A17 retailers reached (upay has 14,519 merchants total; Agrani volume "
              "undisclosed)",
              "A18 average wholesale ticket per retailer (no BD figure exists)"],
        verdict="The only idea here with a real revenue line, but it is a channel "
                "business whose size depends on a partnership nobody has quantified. "
                "Note the timing: MicroSave's blocker (a 1% MDR eating half a "
                "distributor's 1-2% margin) was REMOVED BY REGULATION on 1 Oct 2026. "
                "The remaining blocker is settlement confirmation - which is exactly "
                "what this sells. That is a genuinely better story than problems.md "
                "told.",
    )


# --- 6. Agent float priced as a public utility (float index) ----------------
def idea_6():
    days = band(0.5, 1.0, 2.0)               # A20
    part = band(0.05, 0.15, 0.35)             # A21
    fee = band(0.0005, 0.0015, 0.003)         # A22, per taka per day
    daily_co_cr = UPAY_CASHOUT_VALUE_CR / 365
    traded_day_cr = [daily_co_cr * days[i] * part[i] for i in range(3)]
    upay_cr = [traded_day_cr[i] * fee[i] * 365 for i in range(3)]
    social_cr = [0.0, 0.0, 0.0]
    op = 0.6                                   # A23
    be_day_cr = op / (fee[SI["base"]] * 365)
    IDEAS["6. Agent float priced as a public utility"] = dict(
        who_pays="Agents pay, for guaranteed next-day cash. upay earns a clearing fee "
                 "on allocated float. LEGAL RISK: a charge on agents is a levy and "
                 "needs BB prior approval under the PSO Regulation 2025.",
        mechanism="Changes an incentive: float goes from a free allocation to a "
                  "priced, traded capacity. BB's Feb 2026 96-hour decree rationed "
                  "cash-out by fiat for 96 hours, which is the scene-setting fact.",
        unit=f"per taka of float per day: Tk{fee[0]*1000:.2f} / "
             f"Tk{fee[1]*1000:.2f} / Tk{fee[2]*1000:.2f} per Tk1,000 (no market "
             f"reference price exists)",
        unit_social=f"float efficiency for upay: on Tk{daily_co_cr*days[1]:.2f}cr of "
                    "float at a ~1% yield = Tk0.06cr/yr. Negligible.",
        upay_cr=upay_cr,
        social_cr=social_cr,
        opex=(op, op, op),
    op_cr=op,
        breakeven=f"needs Tk{be_day_cr:.2f}cr of float traded per day at the base "
                  f"fee. Base case trades Tk{traded_day_cr[1]:.2f}cr/day - "
                  f"{'CLEARS' if traded_day_cr[1] >= be_day_cr else 'SHORT BY %.0f%%' % ((be_day_cr/traded_day_cr[1]-1)*100)}. "
                  f"The fee rate is the entire ballgame.",
        keys=["A21 share of agents who would bid for float (NO evidence found that "
              "float is scarce or contested - critique residual risk #4, unresolved)",
              "A22 clearing fee rate (no reference price exists anywhere)"],
        verdict=f"Base case Tk{upay_cr[1]:.2f}cr sits just BELOW its own break-even. "
                "The scene (a central bank rationing cash-out by decree) is verified "
                "and strong; the premise (that float is a tradable scarce good) is "
                "NOT. problems.md itself rated P9 U=3, conceding float shocks are "
                "'partly fixed'. No source establishes that agents bid for float.",
    )


for fn in (idea_1, idea_2, idea_3, idea_4, idea_5, idea_6):
    fn()

# ================================================================ PRINT ======
def cr(x: float) -> str:
    if x == 0:
        return "0"
    if abs(x) < 0.01:
        return f"{x:.4f}"
    return f"{x:.2f}"


def rule(ch="=", n=100):
    print(ch * n)


def main():
    rule()
    print("UPAY ECONOMICS - TOP 6 IDEAS BY UPSIDE (all six are mechanism-changers)")
    print("Base year 2023 = the last year upay published transaction value, revenue and loss.")
    rule()

    print("\nBASE FACTS, SOURCED\n" + "-" * 100)
    print(f"  upay FY2023 revenue                     Tk{UPAY['revenue_cr']:>10,.2f} cr")
    print(f"  upay FY2023 total transaction value     Tk{UPAY['txn_value_cr']:>10,.0f} cr")
    print(f"  upay FY2023 net loss                    Tk{UPAY['net_loss_cr']:>10,.2f} cr")
    print(f"  upay FY2023 accumulated losses          Tk{UPAY['accum_loss_cr']:>10,.0f} cr")
    print(f"  upay registered customers               {UPAY['customers']:>16,}")
    print(f"  upay retail agents                      {UPAY['agents']:>16,}")
    print(f"  upay merchants                          {UPAY['merchants']:>16,}")
    print(f"  -> upay realised take rate (A3)          {TAKE_RATE*100:>15.3f} %")
    print(f"  -> upay revenue per registered customer Tk{REV_PER_CUSTOMER:>10,.0f} /yr")
    print(f"  -> upay CAC proxy (A4, crude)            Tk{CAC:>10,.0f} /customer")
    print(f"  -> upay active base (A1, 35%)           {UPAY_ACTIVE:>16,.0f}")
    print(f"  -> upay active women (A1 x BB 42.2%)    {WOMEN_ACTIVE:>16,.0f}")
    print(f"  -> upay txn count/yr (A5, from value)   {UPAY_TXN_COUNT:>16,.0f}")
    print(f"  -> upay P2P count/yr (A6)               {UPAY_P2P_COUNT:>16,.0f}")
    print(f"  -> upay cash-out value/yr (A6)          Tk{UPAY_CASHOUT_VALUE_CR:>9,.0f} cr")
    print()
    print("  upay's share of the national market (SOURCED denominators):")
    print(f"    of MFS transaction value   ~{UPAY['txn_value_cr']/(164_726.30*12)*100:.2f} %")
    print(f"    of registered accounts      {UPAY['customers']/INDUSTRY['accounts']*100:.2f} %")
    print(f"    of merchant accounts        {UPAY['merchants']/INDUSTRY['merchants']*100:.2f} %")
    print(f"    of agents                   {UPAY['agents']/INDUSTRY['agents']*100:.2f} %")
    print()
    print("  THE COST STRUCTURE THAT SHOULD DISCIPLINE THIS WHOLE EXERCISE:")
    print(f"    upay 2021: revenue Tk{UPAY['revenue_2021_cr']:.2f}cr against selling &")
    print(f"    marketing Tk{UPAY['sm_2021_cr']:.2f}cr + G&A Tk{UPAY['ga_2021_cr']:.2f}cr = "
          f"Tk{UPAY['sm_2021_cr']+UPAY['ga_2021_cr']:.2f}cr of opex, i.e.")
    print(f"    {((UPAY['sm_2021_cr']+UPAY['ga_2021_cr'])/UPAY['revenue_2021_cr']):.1f}x revenue, "
          f"producing a Tk{UPAY['op_loss_2021_cr']:.2f}cr operating loss.")
    print(f"    2023: revenue Tk{UPAY['revenue_cr']:.2f}cr, net loss Tk{UPAY['net_loss_cr']:.2f}cr,")
    print(f"    so total costs run roughly Tk{UPAY['revenue_cr']+UPAY['net_loss_cr']:.0f}cr "
          f"= {(UPAY['revenue_cr']+UPAY['net_loss_cr'])/UPAY['revenue_cr']:.1f}x revenue.")
    print("    CONSEQUENCE: no fee-shaving idea can matter here. A 1bp improvement on")
    print("    upay's whole book is worth Tk0.98cr/yr. Volume and retention are the")
    print("    only levers large enough. Judge the six ideas below on mechanism,")
    print("    defensibility and revenue-NEW volume - not on fee savings.")

    # ---- main table ----
    print("\n\nTABLE 1 - ANNUAL TAKA IMPACT FOR UPAY, Tk crore/year\n" + "=" * 118)
    hdr = (f"{'#':<3}{'idea':<42}{'gross base':>11}{'opex':>7}{'NET base':>10}"
           f"{'NET cons':>10}{'NET aggr':>10}{'%rev':>7}{'%loss':>7}")
    print(hdr)
    print("-" * 118)
    for i, (name, d) in enumerate(IDEAS.items(), 1):
        g = d["upay_cr"]
        o = d["opex"]
        net = [g[k] - o[k] for k in range(3)]
        pct_rev = net[SI["base"]] / UPAY["revenue_cr"] * 100
        pct_loss = abs(net[SI["base"]]) / UPAY["net_loss_cr"] * 100
        print(f"{i:<3}{name:<42}{cr(g[1]):>11}{cr(o[1]):>7}{cr(net[1]):>10}"
              f"{cr(net[0]):>10}{cr(net[2]):>10}{pct_rev:>6.1f}%{pct_loss:>6.1f}%")
    print("-" * 118)
    print("  gross base = annual upay P&L effect BEFORE the mechanism's own operating cost")
    print("  opex       = annual operating cost assumed (A23). No public figure exists.")
    print("  NET        = gross base - opex. This is the honest upay number.")
    print("  %rev       = NET base as % of upay FY2023 revenue (Tk43.32cr)")
    print("  %loss      = NET base as % of upay FY2023 net loss (Tk85.43cr)")
    print("  Idea 3's gross is ZERO by construction: upay books none of the taka it helps")
    print("  a victim recover. Its whole cost is the goodwill budget, shown in opex.")
    tot_net = sum(d["upay_cr"][SI["base"]] - d["opex"][SI["base"]] for d in IDEAS.values())
    print(f"\n  PORTFOLIO TOTAL, all six, base case: Tk{tot_net:+.2f}cr/yr NET,")
    print(f"  against a Tk{UPAY['net_loss_cr']:.2f}cr annual loss = "
          f"{abs(tot_net)/UPAY['net_loss_cr']*100:.0f}% of it.")
    print("  No single idea in this set, and not all six together, moves upay's P&L.")
    print("  That is the honest headline. Rank on mechanism and new volume instead.")

    print("\n\nTABLE 2 - SOCIAL VALUE CREATED, Tk crore/year (NOT upay's money)\n" + "=" * 118)
    print(f"{'#':<3}{'idea':<44}{'cons':>8}{'base':>8}{'aggr':>8}   ratio to upay P&L (base)")
    print("-" * 118)
    for i, (name, d) in enumerate(IDEAS.items(), 1):
        s = d["social_cr"]
        u = d["upay_cr"][SI["base"]]
        ratio = ("n/a" if s[SI["base"]] == 0 else
                 f"{s[SI['base']]/abs(u):.0f}x" if u != 0 else "upay P&L is 0")
        print(f"{i:<3}{name:<44}{cr(s[0]):>8}{cr(s[1]):>8}{cr(s[2]):>8}   {ratio}")
    print("-" * 118)
    print("  Kept separate on purpose. critique.md's pitch numbers for ideas 3 and 5")
    print("  mix these two columns together. That is the error this script exists to fix.")

    # ---- detail ----
    print("\n\nDETAIL PER IDEA\n" + "=" * 118)
    for i, (name, d) in enumerate(IDEAS.items(), 1):
        print(f"\n[{i}] {name}")
        print(f"    mechanism : {d['mechanism']}")
        print(f"    who pays  : {d['who_pays']}")
        print(f"    per unit  : {d['unit']}")
        print(f"    unit(soc) : {d['unit_social']}")
        net = [d["upay_cr"][k] - d["opex"][k] for k in range(3)]
        print(f"    upay gross Tk cr: cons {cr(d['upay_cr'][0])} | base "
              f"{cr(d['upay_cr'][1])} | aggressive {cr(d['upay_cr'][2])}")
        print(f"    upay NET   Tk cr: cons {cr(net[0])} | base {cr(net[1])} | "
              f"aggressive {cr(net[2])}   (opex {cr(d['opex'][0])} / "
              f"{cr(d['opex'][1])} / {cr(d['opex'][2])})")
        print(f"    break-even: {d['breakeven']}")
        print(f"    top 2 keys: {d['keys'][0]}")
        print(f"               {d['keys'][1]}")
        print(f"    VERDICT   : {d['verdict']}")

    # ---- sensitivity ----
    print("\n\nTABLE 3 - SENSITIVITY: annual upay P&L, Tk crore (base case of the other parameter)\n"
          + "=" * 118)

    def grid(title, p1, p2, v1, v2, f):
        print(f"\n  {title}")
        print(f"    {'':<22}" + "".join(f"{v2[j]:>12}" for j in range(len(v2))))
        for a in v1:
            row = "".join(f"{f(a, b):>12.2f}" for b in v2)
            lab = f"{a:.4g}" if a < 0.01 else f"{a:,.4g}"
            print(f"    {lab:<22}{row}")
        print(f"    {'rows = ' + p1 + '   cols = ' + p2}")

    grid("1. shift share (A13)  x  CAC weight (A4)",
         "share", "CAC weight", [0.01, 0.03, 0.10], [0.0, 0.5, 1.0],
         lambda s, w: WOMEN_ACTIVE * s * (REV_PER_CUSTOMER + w * CAC) / CR)

    grid("2. borrower share (A15)  x  agency fee (A14)",
         "borrower share", "agency fee", [0.005, 0.02, 0.05], [0.01, 0.02, 0.03],
         lambda b, f: UPAY_ACTIVE * b * f * 24_000 / CR)

    grid("3. fraud incidence (A10)  x  recovery delta (A11)   [VICTIM value, not upay]",
         "incidence", "recovery delta", [0.02, 0.04, 0.08], [0.30, 0.45, 0.60],
         lambda i, d: UPAY_P2P_COUNT * 0.03 * (9000.0 * i * d) / CR)

    grid("4. cross-op QR share (A7)  x  disguised share (A8)   [upay P&L]",
         "cross-op share", "disguised share", [0.01, 0.04, 0.10], [0.03, 0.08, 0.12],
         lambda x, g: UPAY["txn_value_cr"] * x * g * 0.50 * 0.0065)

    grid("5. retailers reached (A17)  x  wholesale ticket (A18)   [upay P&L at 0.5% MDR]",
         "retailers", "wholesale/mo", [500, 2_000, 6_000], [50_000, 120_000, 250_000],
         lambda r, w: r * w * 12 / CR * 0.005)

    grid("6. float days (A20)  x  bidding participation (A21)   [upay P&L at 0.15%/day]",
         "float days", "participation", [0.5, 1.0, 2.0], [0.05, 0.15, 0.35],
         lambda d, p: (UPAY_CASHOUT_VALUE_CR / 365) * d * p * 0.0015 * 365)

    # ---- corrections ----
    print("\n\nCORRECTIONS TO THE INPUT DOCS (found while sourcing)\n" + "=" * 118)
    corr = [
        ("problems.md: 'agents take >=Tk6.40 per Tk1,000'",
         "WRONG. Tk6.40/1,000 is the MFS PROVIDER'S COST for cash-in, per TBS. The "
         "agent+distributor pool is 77% of the cash-out charge = Tk14.25/1,000 at "
         "Tk18.50, of which the retail agent's own take is ~Tk9+. "
         "This number is load-bearing for ideas 5 and 6 in critique.md."),
        ("problems.md: '~2.4m agents'",
         "WRONG. BB reports 1,856,190 MFS agents (Feb 2025). '2.4m' appears to be a "
         "slide of 239.24m ACCOUNTS. Agent-banking agents are a separate, much "
         "smaller channel: 15,838 (Mar 2025)."),
        ("problems.md: 'avg loss ~Tk9,000' attributed to TIB",
         "MISATTRIBUTED. Tk9,000 is PRI's 2022 MEAN (n=7,279). TIB's 2025 study "
         "publishes only a RANGE, Tk300-Tk83,000, with no mean. Two different "
         "surveys were merged."),
        ("problems.md: 'cash-out rate ~1.85%'",
         "ARITHMETICALLY OK but soft. It is 1 - 9,815/10,000 from ONE reported "
         "merchant-QR cash-out instance, and 9,815 is an industry-source estimate, "
         "not a published average. Normal cash-out is Tk13-18.50/1,000 = 1.3-1.85%."),
        ("critique.md: '75% recovery inside 1-2h vs 19% after'",
         "NO SOURCE. No publication states these figures. Dropped. Replaced by "
         "A11 (30/45/60pp), which is weaker but labelled."),
        ("critique.md: '16,000 agent-banking outlets'",
         "MINOR. BB Mar 2025: 15,838 agents operating 21,023 outlets. Also, the "
         "50% female mandate is a BRPD circular of 8 May 2025; female share of "
         "agent-banking agents was 9.11% at Dec 2024."),
        ("'BDQR Tk370m -> Tk1.1bn' (July->Aug 2026, daily)",
         "UNRECONCILED with UNB's 30 Sep 2026 figure of Tk143.54 CRORE/day from "
         "Tk28 crore in June. The two imply a 13x jump in one month. Both are "
         "carried; neither is used as a primary input, because neither is needed "
         "(upay's QR volume is modelled off upay's own value, not BDQR's)."),
        ("MicroSave's 1% MDR blocker for upstream digitisation",
         "OBSOLETE as of 1 Oct 2026. BB removed the 1% MDR floor and set IRF to "
         "zero. The fee blocker is legislated away; settlement CONFIRMATION is now "
         "the whole blocker. This strengthens idea 5 materially."),
    ]
    for a, b in corr:
        print(f"\n  * {a}\n      {b}")

    # ---- assumptions ----
    print("\n\nASSUMPTIONS - every unsourced input\n" + "=" * 118)
    for aid, txt, why, src in ASSUMPTIONS:
        s = f" [nearest source: {src}]" if src else " [NO SOURCE]"
        print(f"\n  {aid}. ASSUMPTION: {txt}{s}")
        print(f"      {why}")

    # ---- sources ----
    print("\n\nSOURCES - every verified figure\n" + "=" * 118)
    for k, (desc, url) in SOURCES.items():
        print(f"\n  {k}")
        print(f"    {desc}")
        print(f"    {url}")

    rule()
    print("Numbers that could not be sourced are ranges, and are listed above.")
    print("No scenario has been floored, capped or rounded in upay's favour.")
    rule()


if __name__ == "__main__":
    main()