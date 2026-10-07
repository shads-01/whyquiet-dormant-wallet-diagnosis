# WhyQuiet: Impact, Break-Even Economics & Pilot Scale (Slide Copy Draft)

> **Context & Provenance Notice:**  
> All numbers below are extracted directly from code artifacts (`data/public/upay_scale.json`, `data/public/upay_dormant_pool.json`, `web/public/seed.json`, and `docs/PILOT_PROTOCOL.md`).  
> **Status:** PILOT NOT RUN — ALL VALUES ARE SIMULATION. Non-public inputs are labelled `ASSUMED`.

---

## 1. Headline & Break-Even First

**Targeted triage pays off only when recovery exceeds cause-specific break-even thresholds (1.39% to 6.94%).**

| Cause | Intervention Remedy | Unit Cost (BDT) | Break-Even Recovery Rate | Payoff @ 4% Benchmark | Action Routed @ 4% |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `supply_failure` | Agent Liquidity Re-route & Cashback | 5.00 BDT | **1.39%** (`5 / 360`) | **PAYS OFF** (1.39% $\le$ 4%) | **Targeted Remedy** |
| `migration` | Destination Merchant Network Pack | 10.00 BDT | **2.78%** (`10 / 360`) | **PAYS OFF** (2.78% $\le$ 4%) | **Targeted Remedy** |
| `job_exit` | Micro-Savings / P2P Payroll Bridge | 15.00 BDT | **4.17%** (`15 / 360`) | *Deficit @ 4%* (Requires 4.17%) | **Blanket SMS Fallback** |
| `fee_shock` | Tiered Cashback & Fee Education | 25.00 BDT | **6.94%** (`25 / 360`) | *Deficit @ 4%* (Requires 6.94%) | **Blanket SMS Fallback** |
| `solved_problem` | Zero-Action (Natural Dormancy) | 0.00 BDT | **N/A** (0 cost) | **0 Cost / 0 Waste** | **No Action (0 BDT)** |

*Source: `web/public/seed.json` (`report.break_even`, `report.routing_plan`), `src/rules/money.py` (`break_even_rates`), `src/rules/routing.py` (`route`). Formula: Unit Cost / (ARPU 120 BDT $\times$ 3-month RAMP = 360 BDT).*

---

## 2. Price-Aware Routed Strategy on Upay Dormant Pool (Simulation)

**WhyQuiet Price-Aware Routing dynamically selects targeted remedies only when net-positive over blanket SMS, protecting campaign margins across all response rates.**

### Upay Industry Central Scenario (4,449,933 Dormant Wallets, 1.0x Cost Scale):

| Response Rate Scenario | Rule Baseline (Blanket SMS) | WhyQuiet Routed Strategy | Routed vs. Rule Advantage | Routing Action Policy |
| :--- | :--- | :--- | :--- | :--- |
| **1.0% Recovery** | **+1.78M BDT** | **+1.50M BDT** | *-0.28M BDT* (matches blanket; 0 outreach on completed lifecycles) | All blanket SMS except solved_problem (none) |
| **4.0% Benchmark** | **+13.79M BDT** | **+15.02M BDT** | **+1.22M BDT (+8.9%)** | Targeted for supply_failure & migration; blanket for others |
| **8.0% Upside** | **+29.81M BDT** | **+43.02M BDT** | **+13.20M BDT (+44.3%)** | Targeted for supply_failure, migration & job_exit |

- **Sensitivity Range for Routed Strategy (at 4.0% Benchmark, 1.0x Cost Scale):**
  - *Conservative (50% dormant / 3.50M wallets):* **+11.81M BDT** net recovery (+0.96M BDT over rule).
  - *Industry Central (63.57% dormant / 4.45M wallets):* **+15.02M BDT** net recovery (+1.22M BDT over rule).
  - *Aggressive (75% dormant / 5.25M wallets):* **+17.72M BDT** net recovery (+1.44M BDT over rule).

- **Sensitivity Range for Routed Strategy (at 8.0% Upside, 1.0x Cost Scale):**
  - *Conservative (50% dormant / 3.50M wallets):* **+33.83M BDT** net recovery (+10.38M BDT over rule).
  - *Industry Central (63.57% dormant / 4.45M wallets):* **+43.02M BDT** net recovery (+13.20M BDT over rule).
  - *Aggressive (75% dormant / 5.25M wallets):* **+50.75M BDT** net recovery (+15.57M BDT over rule).

---

## 3. Why Routing Matters: The Unrouted Model Baseline vs. Blanket Rule

**Without price-aware routing, blanket model deployment burns capital at low response rates due to expensive unvalidated remedies.**

| Response Rate | Rule Baseline (0.50 BDT SMS) | Unrouted Model (Full Rollout) | Model Deficit / Advantage | Why Routing Is Mandatory |
| :--- | :--- | :--- | :--- | :--- |
| **1.0% Recovery** | **+1.78M BDT** | **-30.57M BDT** | *-32.35M BDT* | High-cost remedies (fee_shock 25 BDT, job_exit 15 BDT) cannot break even at 1%. |
| **4.0% Benchmark** | **+13.79M BDT** | **-3.47M BDT** | *-17.27M BDT* | Unrouted portfolio remains net-negative; routing recovers +15.02M BDT. |
| **8.0% Upside** | **+29.81M BDT** | **+32.65M BDT** | **+2.84M BDT (+9.5%)** | Full portfolio turns net-positive only once response clears 6.94% hurdle. |

*Takeaway:* Price-aware routing converts a -3.47M BDT deficit at 4% into a **+15.02M BDT net gain (+1.22M BDT over blanket SMS)** by gating high-cost interventions.

---

## 4. Cheap-First Phased Rollout Strategy

**Do not deploy full-portfolio remedies immediately. Roll out cheap causes first where break-even is easily achievable.**

- **Phase 1 (Immediate Pilot & Rollout):** `supply_failure` (break-even **1.39%**) + `migration` (break-even **2.78%**).
  - Both comfortably clear the 4.0% response hurdle.
  - Blended unit cost: **7.50 BDT** (`cheap_first_rollout.blended_cost_if_cheap_first_only_bdt`).
- **Phase 2 (Evidence-Gated Rollout):** `job_exit` (**4.17%**) + `fee_shock` (**6.94%**).
  - Fall back to blanket 0.50 BDT SMS in production until controlled pilot demonstrates that cause-specific conversion exceeds these higher break-even hurdles.

---

## 5. Controlled Pilot Protocol (Proposed; Not Yet Run)

**Rigorous 3-Arm Randomized Control Trial before production capital commitment.**

- **Protocol Design:** 3-Arm RCT (Holdout vs. Blanket SMS @ 0.50 BDT vs. Cause Remedy) over a 2-week dispatch window + 30-day reactivation tracking ($\ge 1$ billable transaction).
- **Statistical Power & Sample Size:** **424 wallets per arm** (1,272 total across 3 arms) at 4.0% central recovery rate ($\alpha=0.05$, two-sided, Power=80%, `scripts/pilot_sample_size.py`).
- **Pre-Registered Stop Rule:** Proceed to full pool scaling for a cause *only* if treatment arm achieves statistical superiority over blanket SMS ($p < 0.05$) AND conversion rate exceeds the cause break-even threshold ($r^*$).
- **Data Privacy & Guardrails:** Zero PII leaves Upay premises (anonymized IDs only); hard stop if opt-out $> 0.50\%$ or complaints $> 5 / 1,000$.

---

## 6. Footnote & Provenance Disclosures

> **Footnote:** Synthetic data. Economic inputs ASSUMED. Industry-wide BB data (Feb 2025); Upay base ~7M is STALE (late 2022). Not yet measured in production.
>
> - **Bangladesh Bank Benchmark:** Latest available month is **February 2025** (`data/public/bb_mfs_monthly.csv`, sourced from [Bangladesh Bank MFS Portal](https://www.bb.org.bd/en/index.php/financialactivity/mfsdata)).
> - **Upay Base Provenance:** 7,000,000 registered accounts (STALE late 2022, sourced from [TBS News Interview](https://www.tbsnews.net/economy/mfs/we-seek-build-secure-affordable-mfs-ecosystem-through-innovations-549442)).
> - **Financial Multipliers:** ARPU = 120.0 BDT/mo (ASSUMED); RAMP = 3.0 months (ASSUMED); Generic factor = 25% (ASSUMED); Generic SMS = 0.50 BDT (ASSUMED).
> - **Routing Assumption:** Per-cause precision is assumed 1.0 (optimistic); replace with population-A validation precision upon production integration.
