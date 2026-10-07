# WhyQuiet Pilot Protocol: Controlled Field Trial for Dormant Wallet Reactivation

> **Status: PROPOSED; NOT YET RUN.**  
> All parameters, sample sizes, and break-even metrics below are derived from code simulation (`scripts/pilot_sample_size.py`, `src/rules/money.py`). No production test has been executed.

---

## 1. Objective & Design

Evaluate whether cause-targeted remedies outperform standard generic broadcast messaging in reactivating dormant user wallets before scaling to full operator volume.

- **Trial Duration:** 2-week campaign execution window, followed by a 30-day post-send observation window.
- **Trial Scope:** Cheap-first rollout starting on **Supply Failure** (`supply_failure`, unit cost 5.00 BDT) and **Migration** (`migration`, unit cost 10.00 BDT).
- **Randomization (3-Arm Design):**
  1. **Arm 0 (Control - Natural Holdout):** No message sent ($n$).
  2. **Arm 1 (Baseline - Blanket Broadcast):** Standard generic reactivation SMS at 0.50 BDT ($n$).
  3. **Arm 2 (Treatment - Cause-Targeted Remedy):** Specific remedy SMS with localized cause remediation copy ($n$).

---

## 2. Statistical Power & Sample Sizes

- **Design:** Two-proportion hypothesis test, two-sided $\alpha = 0.05$, Power $(1 - \beta) = 0.80$.
- **Control Baseline:** ASSUMED $p_{\text{control}} = p_{\text{treatment}} \times 0.25$ (`GENERIC_FACTOR`).

| Recovery Assumption | Control $p_1$ | Treatment $p_2$ | Required $n$ / Arm | Total (3 Arms incl. Holdout) |
| :--- | :--- | :--- | :--- | :--- |
| **Conservative (1.0%)** | 0.25% | 1.00% | **1,733** | 5,199 |
| **Central (4.0%)** | 1.00% | 4.00% | **424** | 1,272 |
| **Aggressive (8.0%)** | 2.00% | 8.00% | **206** | 618 |

*At Central (4.0%), a pilot of **424 wallets per arm** (1,272 total across 3 arms) provides 80% power to detect treatment superiority over blanket broadcast.*

---

## 3. Metrics & Pre-Registered Break-Even Stop Rules

- **Primary Metric:** Reactivated wallets per 1,000 messaged ($\ge 1$ billable MFS transaction within 30 days of intervention).
- **Break-Even Thresholds:** $r^* = \text{Unit Cost} / (\text{ARPU} \times \text{RAMP}) = \text{Unit Cost} / 360\text{ BDT}$ (ASSUMED: ARPU = 120 BDT, RAMP = 3.0 months).
  - `supply_failure`: **1.39%** (5 BDT)
  - `migration`: **2.78%** (10 BDT)
  - `job_exit`: **4.17%** (15 BDT)
  - `fee_shock`: **6.94%** (25 BDT)
  - `solved_problem`: **0.00%** (0 BDT / No Action)

### Decision Framework (Go / Hold / Stop)

| Outcome | Criteria (30-day Post-Send) | Action |
| :--- | :--- | :--- |
| **GO (Scale Cause)** | Treatment recovery rate significantly $> p_{\text{control}}$ ($p < 0.05$) AND Treatment recovery $> r^*$ (Break-even). | Approve batch scaling for that specific cause across the full dormant pool. |
| **HOLD (Iterate Copy)** | Treatment recovery significantly $> p_{\text{control}}$ BUT $< r^*$ (Net-negative payoff at current cost). | Revise SMS copy/channel or negotiate lower unit cost; re-test on small cohort. |
| **STOP (Cease Remedy)** | Treatment recovery $\le p_{\text{control}}$ OR opt-out/complaint guardrails breached. | Cease cause-targeted remedy. Default to zero-intervention or holdout. |

---

## 4. Operational Guardrails & Data Privacy

1. **Privacy Guarantee:** Zero PII (Personally Identifiable Information) leaves operator infrastructure. WhyQuiet operates purely on anonymized wallet IDs (`W-XXXXXX`) and transaction frequency aggregates.
2. **Opt-Out Rate Guardrail:** If campaign opt-out / STOP replies exceed **0.50%** in any arm within 48 hours, campaign paused immediately.
3. **Customer Complaints Guardrail:** Customer support escalations related to remedy messaging must not exceed **5 per 1,000 sent**.
