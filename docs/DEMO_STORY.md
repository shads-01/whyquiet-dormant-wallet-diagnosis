# WhyQuiet: Demo Story & Defense Script (8-Minute Live Walkthrough)

> **Document Type:** Team Pitch & Rehearsal Playbook  
> **Target Demo Duration:** $\le$ 8 minutes (strict cut-off at 7:30 to reserve Q&A buffer)  
> **Data Environment:** 100% Offline-Ready from `web/public/seed.json` (D6)  
> **Mandatory Honesty Notice:**  
> *"The causes are simulated. What we show is that attribution survives a population the model never saw and that it refuses when the shape is ambiguous. Whether real causes look like ours is exactly what real upay data would answer first."* (AMENDMENT A3)

---

## 1. Demo Structure & Timing Overview

```
[0:00 - 1:30] Beat 1: The Problem & Triage Queue (Silence is not a single symptom)
[1:30 - 3:30] Beat 2: The Attributed Wallet (W-N0S673 — Supply Failure Diagnosis & Remedy)
[3:30 - 5:30] Beat 3: The Refusal & Adversarial Defense (W-1JRE6D / W-51Q2UN — Refusal Discipline)
[5:30 - 7:30] Beat 4: ML Rigor & Price-Aware Economics (+15.02M BDT Routed Recovery)
[7:30 - 8:00] Buffer / Q&A Transition
```

---

## 2. Step-by-Step Demo Script (Turn-by-Turn Guide)

### Beat 1: The Triage Queue (0:00 – 1:30)
**Screen:** `#/queue` (Triage Queue)  
**Goal:** Establish that MFS dormancy is heterogeneous and current operator heuristics fail.

* **Action 1:** Open `https://whyquiet.vercel.app` (or local `localhost:5173`). The Triage Queue loads immediately from static bundle.
* **Speaker Script:**
  > "In Bangladesh, MFS has over 237 million registered wallets, but only 37.6% are active. When a wallet goes quiet for 3 weeks, operators currently do one thing: send a generic broadcast SMS saying *'We miss you, cash in today.'*  
  > This is a single thermometer for five distinct diseases. Silence isn't homogeneous: users stop transacting due to job changes, migration, completed lifecycles, fee shock, or agent liquidity failures.  
  > WhyQuiet replaces mass broadcasting with **Cause Desk**: a diagnostic console that extracts 20 decline-shape features over a 26-week history, diagnoses the root cause, and routes targeted remedies."
* **Action 2:** Highlight the summary pills: *Total Wallets (400 Sample / 3,000 Shifted Eval)*, *Attributed (75.0%)*, *Refused (25.0%)*, and the 5 cause badges.

---

### Beat 2: The Attributed Wallet — Supply Failure (1:30 – 3:30)
**Screen:** Search `W-N0S673` or click from queue $\rightarrow$ `#/wallet/W-N0S673`  
**Goal:** Demonstrate explainable ML diagnosis, SHAP feature contributions, and cause-targeted remedy.

* **Action 1:** In the Quick Diagnostic search box, type `W-N0S673` and press Enter.
* **Speaker Script:**
  > "Let's inspect wallet `W-N0S673`, a domestic worker on a monthly pay cycle who has been silent for 5 weeks.  
  > The rule baseline would have sent a generic reactivation SMS. But look at the 26-week transaction shape: between weeks 18 and 21, the wallet was active, but failed transactions spiked.  
  > WhyQuiet diagnoses this as **Supply Failure** with **99.7% posterior confidence**."
* **Action 2:** Point to the **Top Feature Contributions (Tree SHAP)** card:
  - `fail_last6 = 5.0` (+4.94 log-odds contribution toward supply failure)
  - `fail_rate_last6 = 83.3%` (+0.54 contribution)
* **Speaker Script:**
  > "The model didn't just guess; it isolates the exact failure signature: 5 failed cash-out attempts in the last 6 active weeks (an 83.3% failure rate). The user didn't leave because they ran out of money—the local agent counter ran out of float.  
  > Instead of an unhelpful generic text, WhyQuiet routes our 5.00 BDT remedy: a field operations agent float alert and a targeted SMS in Bangla routing the user to high-liquidity nearby counters."

---

### Beat 3: The Refused Wallet & Refusal Discipline (3:30 – 5:30)
**Screen:** Search `W-1JRE6D` (or `W-51Q2UN`) $\rightarrow$ `#/wallet/W-1JRE6D`  
**Goal:** Showcase calibrated refusal ($\tau=0.80, \delta=0.10$), proving WhyQuiet refuses to guess on ambiguous data.  
**Engineered Judge Interaction:** *"Can your model refuse a diagnosis if the signals conflict?"* $\rightarrow$ Navigate immediately to `W-1JRE6D`.

* **Action 1:** Navigate to `W-1JRE6D` (transport worker, weekly pay cycle, 14 weeks silent).
* **Speaker Script:**
  > "Now, what happens when data is noisy or ambiguous? Most AI models are forced-choice classifiers: they will confidently return a wrong answer at 35% probability.  
  > Look at `W-1JRE6D`. The posterior distribution is fractured: 45.0% Fee Shock, 20.9% Solved Problem, 16.6% Job Exit, and 9.4% Supply Failure.  
  > WhyQuiet fires a calibrated refusal: **'No attributable cause. I will not spend your money here.'**"
* **Action 2:** Point to the Refusal Panel:
  - Explanation: *'Top cause fee_shock 0.45 is below the 0.80 bar (tau)'*
  - Action: Zero action buttons, 0 BDT capital committed.
* **Speaker Script:**
  > "Why does this matter? Our ground-truth audit proves that when the model is forced to guess on refused wallets, its error rate is **49.1%**, compared to only **13.5%** on attributed wallets.  
  > Refusing to guess on ambiguous wallets saves marketing capital and protects user trust."

---

### Beat 4: ML Rigor, Fairness & Price-Aware Economics (5:30 – 7:30)
**Screen:** `#/evidence` (ML Evidence & Economic Impact)  
**Goal:** Deliver the 4-number defense, show subgroup fairness, and prove price-aware routed economics (+15.02M BDT).

* **Action 1:** Navigate to Evidence tab (`#/evidence`).
* **Speaker Script:**
  > "Let's examine the system-wide evidence on **Population B (3,000 wallets)**, which was subjected to heavy distribution shift—lower baseline transactions, shifted festival dates, and 2.5× higher ambiguity:
  > 
  > 1. **Headline Macro-F1 on B:** **0.864** (vs 0.082 rule baseline and 0.162 shuffled-label chance).
  > 2. **Refusal Scaling:** Refusal rose from 9.3% on A-test to **21.7% on B**, proving the refusal gate adapts to noise.
  > 3. **Subgroup Fairness:** Performance is uniform across worker occupations (0.842 to 0.891 Macro-F1 across Transport, Retail, Garment, and Domestic workers).
  > 4. **Price-Aware Routed Economics:** At our central 4.0% recovery benchmark, deploying unrouted high-cost remedies causes a -3.47M BDT deficit. Our **Price-Aware Routing Engine** dynamically gates expensive remedies, producing **+15.02M BDT net recovery (+1.22M BDT over blanket SMS)**."
* **Action 2:** Point to the 1%/4%/8% interactive recovery rate toggle and the break-even table (Supply Failure: 1.39%, Migration: 2.78%).

---

## 3. Three Adversarial Story Cards (Hand-Picked Real Wallets)

These 3 cards equip the presenter to handle adversarial judge probing with exact data from `web/public/seed.json` and `truth/b_labels.parquet`.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CARD 1: THE MODEL IS WRONG                                                  │
│ Wallet ID: W-AO2AAL | Worker: Garment | Pay: Monthly | Silent: 11 wks       │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Model Diagnosis:  fee_shock (Posterior: 0.9579)                           │
│ • Ground Truth:     supply_failure (blended: False)                         │
│ • Why Model Erred:  User suffered an agent counter cash-out failure after a │
│                     fee tariff change; ticket ratio drop mimicked fee shock │
│ • Presenter Script: "We do not claim 100% accuracy. Here the model was     │
│   fooled by a fee-adjacent cash-out drop. This is why our pilot protocol    │
│   pre-registers 30-day reactivation stop-rules: if an arm fails to beat its │
│   break-even hurdle, rollout halts before full capital commitment."         │
└─────────────────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CARD 2: THE RAZOR'S EDGE BOUNDARY                                           │
│ Wallet ID: W-YVXO00 | Worker: Transport | Pay: Biweekly | Silent: 3 wks     │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Model Diagnosis:  solved_problem (Posterior: 0.8076 vs tau=0.8000)        │
│ • Margin to 2nd:    0.6382 (2nd: job_exit at 0.1894)                        │
│ • Boundary Dynamic: Cleared the 0.80 bar by just 0.0076 (0.76 percentage pts)│
│ • Presenter Script: "Here is a wallet on the razor's edge: 0.808 vs our     │
│   0.800 tau bar. A fraction of a point lower and it would be refused.       │
│   Because it attributed 'solved_problem', our price-aware routing assigns   │
│   Zero Cost (0 BDT spend), guaranteeing zero capital loss at the boundary." │
└─────────────────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CARD 3: REFUSING THE "OBVIOUS" CANDIDATE                                    │
│ Wallet ID: W-51Q2UN | Worker: Transport | Pay: Monthly | Silent: 14 wks     │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Top Posterior:    fee_shock (0.7705) | Margin to 2nd: 0.7075 (2nd: 0.0630)│
│ • Model Verdict:    REFUSED (Below tau=0.80 confidence threshold)           │
│ • Intuition Trap:   77% confidence looks like an 'obvious' win to a human   │
│ • Presenter Script: "To a naive model, 77% confidence looks like a clear win│
│   for Fee Shock. But Fee Shock costs 25 BDT and needs 6.94% to break even.   │
│   WhyQuiet refuses because 77% < 80%. Our audit proves forced-choice error   │
│   on refused wallets is 49.1%—refusing this 'obvious' case saves 25 BDT."   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Speaker Splits & Team Execution Matrix

Any of the three team members can run any beat. Recommended default split:

| Role | Primary Lead | Backup Lead | Focus Areas | Key Talking Points |
| :--- | :--- | :--- | :--- | :--- |
| **Beat 1: Problem & Queue** | **Shads** (UX Lead) | Arko | MFS dormancy context, UI workflow, 5-cause taxonomy | 37.6% active accounts, single-thermometer flaw, 4-state console |
| **Beat 2: Attributed Wallet** | **Hrittika** (ML Lead) | Shads | Decline shape, 20 features, Tree SHAP contributions | 26-week series, `fail_last6`, localized Bangla remedy copy |
| **Beat 3: Refused Wallet & Cards** | **Hrittika** (ML Lead) | Arko | Calibrated refusal ($\tau=0.80, \delta=0.10$), Adversarial Cards | Refusal discipline, 49.1% vs 13.5% error rate, cards 1–3 |
| **Beat 4: Rigor & Economics** | **Arko** (Econ/API) | Shads | Population B F1, Subgroup Fairness, Price-Aware Routing | 0.864 F1 on B, +15.02M BDT routed recovery, 424/arm pilot |
| **Maker-Checker Governance** | **Arko** (Gov Lead) | Shads | 2-role auth, PostgreSQL trigger, immutable audit log | `proposer != approver` barrier, zero-PII `W-XXXXXX` guarantee |

---

## 5. Offline Rehearsal Checklist

- [ ] Dev server running (`make dev` or `cd web && npm run dev`) OR live URL (`https://whyquiet.vercel.app`).
- [ ] Network tab verified: 100% offline-compatible; all read paths pull from `/seed.json`.
- [ ] Browser zoom set to 100%, screen resolution $\ge 1280 \times 800$.
- [ ] Light / Dark theme pre-selected (Light Mode default matches projector/screenshare best).
- [ ] Rehearsal stopwatch timer verified $\le 7\text{ min } 30\text{ sec}$.
