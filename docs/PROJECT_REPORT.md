# WhyQuiet: Dormant-Wallet Diagnosis Console (Cause Desk)
## Project Report & Technical Blueprint

---

### Executive Summary

Mobile Financial Services (MFS) enable digital financial inclusion for millions of users. However, retaining user engagement remains a fundamental operational challenge: a substantial portion of registered accounts eventually stop transacting and enter a dormant state.

When attempting to re-engage inactive users, a common baseline approach is blanket mass-messaging (e.g., generic broadcast SMS campaigns). This report demonstrates that treating dormancy as a homogeneous condition is inherently inefficient. A wallet ceases activity for fundamentally different root causes—such as payroll disruptions, geographical relocation, completed lifecycle goals, tariff sensitivity, or agent-level liquidity constraints. Blasting identical generic reminders to all dormant accounts misallocates outreach budgets on unfixable accounts and creates user friction.

**WhyQuiet (Cause Desk)** re-frames dormant wallet management from indiscriminate broadcast messaging to **precision diagnosis, calibrated refusal, and governed remediation**:
- **5-Cause Behavioral Taxonomy**: Analyzes 26-week transaction decline shapes using 20 mathematical ratios to distinguish between *Job Exit*, *Migration*, *Solved Problem*, *Fee Shock*, and *Supply Failure*.
- **Calibrated Refusal Gate**: Refuses to make arbitrary guesses on ambiguous or noisy transaction patterns ($\tau \ge 0.80, \delta \ge 0.10$), explicitly stating: *"No attributable cause. I will not spend your money here."*
- **Empirical Validation**: Evaluated on an out-of-distribution, shifted synthetic population (Population B, $N=3,000$), achieving an attributed **Macro-F1 score of 86.4%** with a **21.7% calibrated refusal rate**, outperforming the standard heuristic baseline (8.2%) and shuffled-label controls (16.2%).
- **Two-Person Maker-Checker Governance**: Integrates a two-person proposal and approval workflow enforced by PostgreSQL triggers and an append-only audit trail.

---

## 1. Problem Statement: The Inefficiency of Blanket Re-engagement

In mobile financial ecosystems, user dormancy represents lost transactional velocity and unrealized revenue. However, addressing dormancy through broad, untargeted re-engagement campaigns presents structural shortcomings:

1. **Circumstance Mismatch**: Inactivity is not a single behavioral state. An individual who stopped transacting because they relocated to an area with no nearby cash-out points cannot be reactivated by a generic text message saying *"We miss you"*.
2. **Budget Waste on Non-Actionable Accounts**: Certain accounts go quiet because their specific use case has naturally concluded (e.g., a one-time project remittance or seasonal tuition payment). Spending outreach funds on satisfied, completed-lifecycle users yields zero return.
3. **Budget Waste on Structural Friction**: Accounts experiencing repeated transaction failures due to local cash shortages require operational intervention on the supply side, not promotional messaging directed at the consumer.
4. **Lack of Diagnostic Memory**: Blanket campaigns leave operations teams with no structured insight into *why* accounts become inactive or how market conditions influence churn patterns over time.

---

## 2. Pain Point Identification: The Five Underlying Churn Causes

Rather than treating silence as a single symptom, WhyQuiet identifies **five distinct behavioral mechanisms** that lead to wallet inactivity:

```
                            ┌─────────────────────────────────┐
                            │    Dormant Account in Ledger    │
                            └────────────────┬────────────────┘
                                             │
        ┌───────────────┬────────────────────┼───────────────────┬───────────────┐
        │               │                    │                   │               │
  ┌─────▼─────┐   ┌─────▼─────┐       ┌──────▼──────┐      ┌─────▼────┐    ┌─────▼──────┐
  │  Job Exit │   │ Migration │       │Solved Problem│     │Fee Shock │    │Supply Fail │
  └─────┬─────┘   └─────┬─────┘       └──────┬──────┘      └─────┬────┘    └─────┬──────┘
        │               │                    │                   │               │
  ┌─────▼─────┐   ┌─────▼─────┐       ┌──────▼──────┐      ┌─────▼────┐    ┌─────▼──────┐
  │ Re-Link   │   │ Geotarget │       │  No Spend   │      │Fee Waiver│    │Float Alert │
  │ Guide     │   │ Agent Map │       │  (৳0 Cost)  │      │ Voucher  │    │& Alt Route │
  └───────────┘   └───────────┘       └─────────────┘      └──────────┘    └────────────┘
```

1. **Job Exit (Payroll Discontinuation)**
   * *Mechanism*: Regular wage or salary inflows suddenly cease, followed by immediate cash-out and account silence.
   * *Appropriate Action*: Suppress immediate re-engagement messages; provide self-service instructions for re-linking payroll once new employment commences.
2. **Migration (Geographic Relocation)**
   * *Mechanism*: Transacting geolocations shift away from historical agent clusters, and transactions at previous neighborhood counters drop to zero.
   * *Appropriate Action*: Send localized agent referrals guiding the user to verified agents and cash-in points in their new district.
3. **Solved Problem (Completed Lifecycle)**
   * *Mechanism*: A temporary surge of high-value transactions fulfilling a specific goal (e.g., tuition payment, medical emergency transfer, seasonal harvest payout), followed by dormancy.
   * *Appropriate Action*: **No spend (৳0 expenditure)**. Recognize user satisfaction and avoid sending irrelevant promotional messages.
4. **Fee Shock (Tariff Sensitivity)**
   * *Mechanism*: Transaction velocity plummets immediately following a high cash-out tariff or fee bracket threshold.
   * *Appropriate Action*: Provide a targeted, subsidized fee-waiver voucher on the subsequent cash-out to rebuild transacting habit.
5. **Supply-Side Failure (Agent Counter Liquidity Depletion)**
   * *Mechanism*: Multiple failed cash-out attempts within a narrow window due to agent float depletion or terminal timeouts, followed by abandonment.
   * *Appropriate Action*: Alert field operations to replenish local liquidity float, while routing the user to high-liquidity merchant points nearby.

---

## 3. Proposed Idea: Diagnostic Attribution & Calibrated Refusal

WhyQuiet transforms dormancy management through two core concepts:

### A. Shape-Based Causal Diagnosis
Instead of observing whether a wallet has been inactive for a given number of weeks, WhyQuiet analyzes the **multi-week trajectory leading up to inactivity**. By examining the velocity of cash-ins versus cash-outs, failure rates, ticket size shifts, and channel choices (App vs. USSD), the system infers the most probable driver of dormancy.

### B. Calibrated Refusal as a First-Class Output
In real-world data, transaction patterns are frequently noisy, irregular, or ambiguous. Traditional machine learning classifiers force a prediction for every input, leading to overconfident mistakes and wasted spend. 

WhyQuiet enforces a mathematical **Calibrated Refusal Gate**:
$$\text{Verdict} = \begin{cases} \text{"refused"} & \text{if } \max_{c} P(c \mid \mathbf{x}) < \tau \quad \lor \quad \left(P_{(1)} - P_{(2)}\right) < \delta \\ \text{"attributed"} & \text{otherwise} \end{cases}$$
- Confidence floor: $\tau = 0.80$
- Margin separation floor: $\delta = 0.10$

When an account's decline curve does not clearly distinguish between causes, WhyQuiet deliberately refuses attribution, protecting marketing capital from being allocated on ambiguous guesses.

---

## 4. Implemented Solution & System Architecture

WhyQuiet is implemented as a production-grade, enterprise diagnostic console adhering to the **Ponytail Principle** (radical minimalism, native platform capabilities, and zero unnecessary dependencies).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          WEB CLIENT (Vite + React 19)                       │
│  Claymorphic UI • Recharts Trends • Bilingual Remedies • Offline-First Seed │
└───────────────────────┬─────────────────────────────▲───────────────────────┘
                        │ Read (Offline / Public)     │ Write (Authenticated)
                        ▼                             │
┌───────────────────────────────────────┐   ┌─────────────────────────────────┐
│     STATIC SEED DATA (seed.json)      │   │   FASTAPI SERVERLESS BACKEND    │
│  400 Sample Wallets • Full Eval Stats │   │  Input Validation • Session Auth│
└───────────────────────────────────────┘   └────────────────┬────────────────┘
                                                             │
                                                             ▼
                                            ┌─────────────────────────────────┐
                                            │      SUPABASE (PostgreSQL)      │
                                            │  remedy_batches • batch_wallets │
                                            │  Trigger-Enforced 2-Person Rule │
                                            │  Append-Only audit_log          │
                                            └─────────────────────────────────┘
```

### Core Architecture Highlights
1. **Hybrid Public-Read / Protected-Write Architecture**:
   - Diagnostic screens, ML evidence metrics, and economic sweeps are bundled into a static offline artifact (`seed.json`). This ensures 100% reliability, instant load times, and offline operability for evaluators and operators.
   - Batch proposal and approval operations connect to authenticated serverless API endpoints backed by PostgreSQL.
2. **Zero-PII Compliance**:
   - The system strictly operates on pseudonymous tokens (`W-XXXXXX`). No phone numbers, national IDs, or personal customer data are ever ingested or stored.
3. **Deterministic Business Logic**:
   - Economic models and remedy costs reside in pure Python modules (`src/rules/`), completely separated from machine learning inference to guarantee auditability.

---

## 5. Key Product Features (The Cause Desk Console)

The web console ([whyquiet.vercel.app](https://whyquiet.vercel.app)) provides five interconnected operational interfaces:

* **Triage Queue (`#/`)**: Central dashboard displaying diagnosed wallets with cause attribution, confidence ratings, silent week duration, and status filters (All, Attributed, Refused). Includes instant search and identifier lookup.
* **Wallet Detail (`#/w/<id>`)**: Interactive 26-week transaction decline area chart with highlighted inactivity windows, 5-cause posterior probability distribution bars, SHAP-style signed feature contribution breakdowns, and cause-targeted remedy cards featuring English and Bengali message copy with associated unit costs.
* **Refusal Screen (`#/w/<refused_id>`)**: Transparent refusal interface detailing the exact mathematical condition that triggered refusal (e.g., confidence below $\tau=0.80$ or margin below $\delta=0.10$), explicitly confirming zero marketing spend.
* **Evidence & ML Rigor Center (`#/evidence`)**: Comprehensive transparency dashboard displaying out-of-distribution performance metrics, multi-class confusion matrices, demographic subgroup fairness audits, and an interactive 1% / 4% / 8% economic recovery sweep.
* **Batches & Governance (`#/batches`)**: Two-person authorization workspace where analysts aggregate eligible wallets into remedy batches, and approvers authorize executions with mandatory audit notes. Generates structured campaign JSON files for downstream distribution.

---

## 6. AI & Machine Learning Approach

### 6.1 Feature Engineering (20 Shape Ratios)
Rather than passing raw transaction counts directly, the model extracts **20 normalized mathematical shape features** per wallet from historical ledger records. Using internal ratios ensures robustness even when baseline transaction volumes fluctuate across populations:

1. `weeks_silent`: Number of weeks since the last recorded transaction.
2. `slope_last8`: Linear regression slope of weekly transaction counts over the final 8 active weeks.
3. `burst_ratio`: Peak weekly transaction volume divided by average weekly volume.
4. `weeks_since_burst`: Time lag in weeks between the peak activity burst and final dormancy.
5. `last4_txn_ratio`: Share of total transaction volume occurring in the final 4 weeks.
6. `ticket_ratio`: Average transaction value in the last 4 weeks relative to lifetime average ticket size.
7. `weeks_since_cashin`: Weeks elapsed since the last cash-in or salary deposit.
8. `cashin_ratio_last4`: Ratio of cash-in count to cash-out count in the final 4 active weeks.
9. `cashout_ok_ratio_last4`: Successful cash-out ratio in the last 4 active weeks.
10. `fail_last6`: Total count of failed transaction attempts in the final 6 weeks.
11. `fail_rate_last6`: Failure rate (failed attempts / total attempts) in the final 6 weeks.
12. `post_fee_ratio`: Ratio of post-fee transaction frequency to pre-fee frequency.
13. `weeks_after_fee`: Weeks elapsed between a high-fee transaction and wallet dormancy.
14. `weeks_since_district_change`: Weeks since a detected GPS/agent district shift.
15. `app_share_shift`: Change in mobile app usage share vs USSD channel in the final 8 weeks.
16. `payday_concentration`: Proportion of transactions occurring strictly on detected paydays.
17. `active_weeks`: Total count of active transacting weeks across the lifetime.
18. `base_txn_mean`: Average weekly transaction count during the wallet's active lifespan.
19. `pay_cycle`: Encoded pay cycle category (weekly, bi-weekly, monthly).
20. `fade_weeks`: Duration in weeks of gradual transaction decline before complete silence.

*Note: Demographic attributes (such as occupation or gender) are strictly excluded from model feature inputs to prevent demographic leakage, and are reserved solely for post-hoc fairness auditing.*

### 6.2 Model Architecture & Training
- **Model Family**: Gradient Boosted Decision Trees via LightGBM multiclass objective (100 boosting rounds, learning rate 0.05, max depth 5, balanced class weights).
- **Explainability**: Inference-time Tree SHAP values computed natively via LightGBM `pred_contrib`, returning the top 8 signed feature contributions toward the predicted cause.
- **Calibrated Refusal Calibration**: $\tau=0.80$ and $\delta=0.10$ tuned strictly on an internal 20% validation split of training data to maintain $\ge 0.97$ accuracy on attributed cases.

### 6.3 Empirical Validation on Unseen Shifted Population B ($N=3,000$)
To ensure the model does not merely memorize simulation artifacts, evaluation was conducted on an out-of-distribution Population B generated with lower baseline activity, altered pay-cycle priors, shifted holiday periods, and 2.5× higher ambiguity noise:

| Metric / Dimension | WhyQuiet Result | Baseline / Control Reference | Operational Interpretation |
| :--- | :--- | :--- | :--- |
| **Headline Macro-F1 on B** | **`86.36%` (0.8636)** | Rule Baseline: **8.19%** | +78.17 percentage points improvement over the standard heuristic. |
| **Multi-Seed Stability** | **`0.8680` Mean** | Range: [0.8471, 0.8864] | Evaluated across Seeds 1, 2, and 3; consistent performance across RNG seeds. |
| **Generalization Gap** | **`9.83%` (0.0983)** | A-Test F1: 96.18% | Controlled, modest drop under substantial distribution shift. |
| **Calibrated Refusal Rate on B** | **`21.73%`** (652 / 3,000) | A-Test Refusal: 9.33% | Refusal rate automatically scales up as data ambiguity increases. |
| **Expected Calibration Error (ECE)** | **`0.1001` (10.0%)** | 10 equal-width bins | Predicted probabilities reflect genuine statistical calibration. |
| **Shuffled-Label Control** | **`16.21%`** | Chance Level: $\approx 20.0\%$ | Confirms model cannot learn from scrambled ground-truth labels. |
| **Best Single Feature Control** | **`37.30%`** (`cashin_ratio_last4`) | — | Proves no single proxy feature leaks cause labels. |

### 6.4 Demographic Parity & Fairness Slices
Evaluating Population B across occupational cohorts demonstrated equitable diagnostic reliability across different user segments:
- **Domestic Workers** ($n=765$): Macro-F1 = **87.55%**, Refusal Rate = **23.79%**
- **Garment Workers** ($n=698$): Macro-F1 = **89.11%**, Refusal Rate = **21.78%**
- **Retail Workers** ($n=554$): Macro-F1 = **84.93%**, Refusal Rate = **17.87%**
- **Transport Workers** ($n=983$): Macro-F1 = **84.21%**, Refusal Rate = **22.28%**

---

## 7. Economic Sensitivity Modeling

To evaluate financial viability without relying on undisclosed proprietary data, WhyQuiet incorporates a transparent economic model using explicitly labeled assumptions:

$$\text{Net Economic Value} = (\text{Users Recovered} \times \text{ARPU} \times \text{RAMP}) - \text{Campaign Cost}$$

### Assumptions Specification (`src/rules/money.py`)
- **ARPU**: 120.00 BDT / month per active user (`# ASSUMED`)
- **RAMP**: 3.0 months active lifetime value multiplier (`# ASSUMED`)
- **Generic Factor**: Generic SMS achieves 25% of targeted remedy effectiveness (`# ASSUMED`)
- **Generic SMS Cost**: 0.50 BDT / wallet (`# ASSUMED`)
- **Targeted Remedy Costs**: Cause-specific unit costs from `REMEDIES` (`supply_failure`: 5.00 BDT, `migration`: 10.00 BDT, `job_exit`: 15.00 BDT, `fee_shock`: 25.00 BDT, `solved_problem`: 0.00 BDT) (`# ASSUMED`)
- **Break-Even Recovery Rates**: $\text{Cost} / (\text{ARPU} \times \text{RAMP}) = \text{Cost} / 360\text{ BDT}$ (`supply_failure`: 1.39%, `migration`: 2.78%, `job_exit`: 4.17%, `fee_shock`: 6.94%, `solved_problem`: N/A)

### Sensitivity Sweep Across 3,000 Population B Wallets (Cost Scale 1.0x)

| Recovery Rate Scenario | Strategy | Actioned Wallets | Recovered Users | Campaign Spend | Net Value (BDT) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1% (Pessimistic)** | Blanket SMS Rule | 3,000 | 7.50 | 1,500.00 BDT | **+1,200.00 BDT** |
| | Unrouted Model | 1,875 | 16.91 | 26,695.00 BDT | -20,606.50 BDT |
| | **WhyQuiet Routed Strategy** | **2,527** | **6.32** | **1,263.50 BDT** | **+1,010.80 BDT\*** |
| | Oracle (Upper Bound) | 1,875 | 18.75 | 26,695.00 BDT | -19,945.00 BDT |
| **4% (Base Case)** | Blanket SMS Rule | 3,000 | 30.00 | 1,500.00 BDT | **+9,300.00 BDT** |
| | Unrouted Model | 1,875 | 67.65 | 26,695.00 BDT | -2,341.00 BDT |
| | **WhyQuiet Routed Strategy** | **2,527** | **45.46** | **6,240.50 BDT** | **+10,125.10 BDT** |
| | Oracle (Upper Bound) | 1,875 | 75.00 | 26,695.00 BDT | +305.00 BDT |
| **8% (Optimistic / High LTV)** | Blanket SMS Rule | 3,000 | 60.00 | 1,500.00 BDT | **+20,100.00 BDT** |
| | Unrouted Model | 1,875 | 135.30 | 26,695.00 BDT | +22,013.00 BDT |
| | **WhyQuiet Routed Strategy** | **2,527** | **125.60** | **16,216.50 BDT** | **+28,999.50 BDT** |
| | Oracle (Upper Bound) | 1,875 | 150.00 | 26,695.00 BDT | +27,305.00 BDT |

*\*At 1% recovery, blanket SMS also credits completed-lifecycle (`solved_problem`) wallets; like-for-like on actionable wallets, routed matches blanket.*

### Key Economic Takeaways
1. **Never Worse Than Blanket SMS Like-for-Like**: Break-even rates range from 1.39% to 6.94%. Price-aware routing dynamically prevents spending on expensive remedies that cannot clear unit economics, falling back to 0.50 BDT blanket SMS.
2. **Profit Superiority at Scale**: At a 4% recovery rate, routed remedies generate **+10,125.10 BDT net value (+8.9% over blanket)**; at 8% recovery, they generate **+28,999.50 BDT net value (+44.3% over blanket)** on Population B (simulation, ASSUMED inputs).
3. **Upay Macro Scaling**: On Upay's central scenario (4,449,933 dormant wallets derived from Bangladesh Bank Feb 2025 industry inactive share 63.57%), routed net value reaches **+15.02M BDT at 4%** (+1.22M BDT advantage over rule) and **+43.02M BDT at 8%** (+13.20M BDT advantage over rule).
4. **Refusal Waste Avoidance**: By refusing attribution on 652 ambiguous wallets and routing them to cheap blanket SMS, WhyQuiet avoided **9,170.00 BDT** in targeted remedy spend (8,844.00 BDT net of SMS; recomputed under per-cause costs).
5. **Controlled Pilot Protocol**: Not yet measured in production; proposed 2-week pilot (`docs/PILOT_PROTOCOL.md`), $n=424$ wallets per arm (1,272 total across 3 arms) from `scripts/pilot_sample_size.py` at 4% benchmark, with pre-registered stop rule = per-cause break-even rate $r^* = \text{cost} / 360\text{ BDT}$.

---

## 8. Intended Real-Life Impact & Responsible Governance

### 1. Two-Person Maker-Checker Approval
To prevent unauthorized mass communications or misallocated budgets:
- **Analyst Role**: Authorized to query triage data and propose batch remedies.
- **Approver Role**: Authorized to review pending batches, inspect cost projections, and record binding approval or rejection notes.
- **PostgreSQL Constraint**: The database enforces `CHECK (decided_by <> proposed_by)` and trigger verification, mathematically blocking self-approval.

### 2. Append-Only Compliance Trail
All administrative actions write to `public.audit_log`. Database triggers block `UPDATE`, `DELETE`, and `TRUNCATE` operations, providing an immutable audit trail for governance compliance.

### 3. Customer-Centric Experience
By replacing blanket messaging with cause-specific solutions (or no action for completed use cases), users receive relevant, timely support rather than repetitive spam that damages brand trust.

---

## 9. Limitations & Mandatory Honesty Disclosure

Per project specifications:
> *"Real transaction ledgers contain no ground-truth churn cause labels. We train on simulated causes (Population A) and evaluate on a shifted, unseen synthetic population (Population B). We demonstrate robustness to distribution shift in simulation, not real-world ground truth. Whether real-world causes mirror these decline shapes is what deployment on live production ledgers would establish."*

Additional operational boundaries:
- **Single-Tenant Scope**: Configured for single-operator deployments without multi-tenant partitioning.
- **Batch Export Hand-Off**: Outputs campaign JSON artifacts rather than integrating live outbound messaging webhooks, ensuring operators maintain complete oversight before customer contact.

---

## 10. Conclusion

WhyQuiet demonstrates that resolving wallet dormancy is not a matter of sending more messages, but of **diagnosing root causes, exercising refusal discipline when data is ambiguous, and enforcing human-in-the-loop governance**. 

By pairing high-accuracy gradient boosted shape analysis with calibrated refusal, WhyQuiet provides a scalable, auditable, and commercially sustainable foundation for mobile financial services operations.
