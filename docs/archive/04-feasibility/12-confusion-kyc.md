# 12-confusion-kyc.md — Feasibility: Confusion detector + KYC drop-off predictor (2026-10-02)

**Idea (pool finalist + D25/D39, critique survivor #10):** interaction logs on a clickable prototype predict where users (esp. older/low-literacy) struggle or abandon; per-person live adaptation + per-segment funnel report. Track 02/06.

## 1. DATA REALITY

| Source | URL | Size | Language | Licence | Hackathon use | Download friction | Status |
|---|---|---|---|---|---|---|---|
| Self-collected interaction logs | n/a | ~20–30 participants incl. parents, 1–2 sessions each | bn UI | own (consent) | yes — core data | recruit + run sessions | planned |
| Global Findex 2025 (segment priors) | https://www.worldbank.org/en/publication/globalfindex | country CSV/microdata | en | World Bank open | context only | direct | VERIFIED (inventory) |

**Self-collection protocol:** clickable mock upay KYC/send flow (web, Bangla UI) logging every event client-side: step enter/exit, dwell, backtracks, idle gaps, taps-on-disabled, error retries. Participants: 20–30 (students + ≥8 parents/relatives 45+), on their OWN phones (device-artefact control — critique #10). Consent wording — Bangla: "আমি স্বেচ্ছায় এই প্রোটোটাইপ ব্যবহার করছি। আমার ট্যাপ ও সময়ের তথ্য শুধু গবেষণার জন্য সংরক্ষিত হবে; কোনো আসল টাকা বা অ্যাকাউন্ট জড়িত নয়।" English: "I voluntarily use this prototype. My tap and timing data is stored for research only; no real money or account is involved." Redaction: no names in logs, random IDs; demographic fields (age band, literacy self-report) collected separately with consent. Collectors: all 3 members, ~2–4 h across H0–18. Ground truth per session: observer-marked "needed help" + completion/abandonment.

## 2. PRECEDENT

- **Hotjar → Contentsquare (VERIFIED, site read):** session replay, heatmaps, funnels, error/frustration detection; free plan 200k sessions/month; new accounts on Contentsquare — https://www.hotjar.com/ . **Plainly:** session-replay UX tooling is a mature global category; drop-off funnels are a standard report.
- What is NOT standard: per-person *live* adaptation (simplify the next screen for THIS struggling user) and Bangla/low-literacy MFS KYC specifically. The funnel report alone is already-dominant tooling — the model's claim must be the live adaptation + prediction, not the report (critique #10: funnel counts get ~60% of the value).
- BD-specific: no published MFS KYC drop-off model found — UNVERIFIED absence (nothing surfaced in searches today).

## 3. LEGAL/ETHICS (not legal advice)

- **Personal Data Protection Ordinance 2025** (gazetted 6 Nov 2025): behavioural telemetry is personal data; consent + purpose limitation + minimization — https://www.thedailystar.net/tech-startup/news/bangladeshs-personal-data-protection-ordinance-2025-key-takeaways-4015401 ; https://bd-scl.com/insights/personal-data-protection-ordinance-2025-compliance.html . Cross-border transfer rules for cloud storage: UNVERIFIED — keep logs local.
- **No real KYC data:** the prototype collects no NID/selfie/OTP — mock only; say this explicitly to judges.
- **Vulnerable-group ethics:** adapting UI for struggling users is assistive; the same signal could be used to manipulate (dark patterns) — commit to assist-only adaptation.
- **Unclear:** whether age/literacy-based UI differentiation triggers any anti-discrimination duty — no BD statute found; UNVERIFIED.

## 4. 48-HOUR BUILD PLAN

Stack: single-page web prototype (plain JS or React) + tiny event-logging API (FastAPI + SQLite); scikit-learn logistic regression / gradient boosting on session features; no GPU needed.

- H0–6: B builds the mock KYC flow + event logger (reuse spike 12 schema); A recruits participants, prepares consent script; C builds feature extraction + first model on pilot logs (3 teammates).
- H6–18: A+C run sessions (20–30 participants, own phones); C trains drop-off/struggle predictor with person-level held-out split (kill bar: AUC ≥0.75 on held-out parents); B builds live-adaptation: when risk crosses threshold mid-session, swap in simplified screen (bigger text, voice hint button).
- H18–30: A runs held-out parents live; C produces per-segment funnel report (age band × step); B builds judge demo: judge runs the flow, watches their own risk score and the adaptation fire.
- H30–36: **feature freeze.** H36–48: fairness table, red-team (rapid-tap spam), rehearsal, pitch.

## 5. SPIKE TEST — RAN, real numbers

See spikes/12-confusion-kyc/RESULTS.md. Pure-stdlib console mock, 5-step KYC, 2 scripted self-run conditions (expert vs first-time with reading delays + OTP re-entry):

- expert: total 14.2 s, 0 backtracks, 0 long idles → risk 0.47
- first-time: total 121.7 s, mean dwell 16.1 s, 1 backtrack, 6 long idles → risk 11.06
- **Separation ratio 23.4x → pipeline PASS** — but **n=2, both scripted by the same author: a connectivity check, NOT evidence.** Real signal requires the 20–30-person unscripted collection; AUC ≥0.75 on held-out parents is the falsifier.

## 6. BASELINE

Non-AI baseline: funnel-step completion counts + session replay (Contentsquare free tier does this today) — ~60% of the value (critique #10). LLM-API baseline: feed a session's event JSON to an LLM and ask "struggling?" — plausible, UNVERIFIED; must be beaten or absorbed. **Pointless-if number:** if drop-off prediction AUC on held-out parents <0.65 (barely better than "older users struggle more" prior), the model is an observation, not a product — ship only the funnel report and kill the AI claim.

## 7. RISKS

1. **Model learns demo artefacts, not struggle** (browser, trackpad, our prototype's quirks) — critique #10 mechanism. Mitigation: participants use own phones; features restricted to timing/backtrack/idle, not device fingerprints.
2. **Classmates/parents ≠ upay's real base** — fairness exposure. Mitigation: include ≥8 parents/relatives 45+; report per-segment metrics; state the limitation on the slide.
3. **Tiny sample** — 20–30 sessions, high variance. Mitigation: simple features, regularized model, person-level held-out split, honest confidence intervals.
4. **Live adaptation misfires** — simplifying UI for a user who was just reading. Mitigation: adaptation is additive (help button appears), never removes function; threshold conservative.
5. **"Just watch session replays" objection** — product teams distrust tiny-sample UX models. Mitigation: the pitch leads with the falsifier and the live judge-try moment, not the AUC.

**P(working live demo) = 0.70.** Highest of the four: no GPU, no ASR gamble, data collection is fast, and the judge-try moment (their own risk score moving live) is reliable. Risk is model quality, not demo existence.

## 8. RESPONSIBLE AI

- **Fairness groups:** age band, self-reported literacy, gender, device type — per-segment AUC + adaptation-trigger-rate table; check the model doesn't just flag "old = struggling".
- **Explainability:** risk score shows top-3 contributing events ("idle 22 s at OTP step, 2 backtracks"); segment report shows step-level completion deltas.
- **Security:** adversarial manipulation (rapid-tap to fake competence or spam to fake struggle) tested at H36; data leakage: held-out people strictly excluded; logs local, random IDs, deleted after event; prompt injection N/A (no LLM in the loop for the model; if LLM baseline used, sandbox it).
- **Human oversight:** adaptation only suggests help; a human (agent/family) performs any real account action; no autonomous KYC decisions.
