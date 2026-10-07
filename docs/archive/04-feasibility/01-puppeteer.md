# 01-puppeteer.md — Feasibility: Coercion Shield (a) "Puppeteer"

Sequence model over send-flow interaction timing distinguishing self-directed sends from sends dictated/coerced by a phone partner. Track 01. Status: FEASIBLE AS DEMO, UNPROVEN AS SIGNAL.

## 1. DATA REALITY

**Public datasets: none exist for this.** No public dataset of coerced/dictated mobile-money interaction timings was found (searched 2026-10-02; absence-of-evidence noted). The idea therefore rests entirely on self-collected data.

**Self-collected: send-flow interaction logs, 30–50 participants.**
- Sample size: 30–50 students (DIU classmates), each performing 4–6 send sessions: 2–3 self-directed, 2–3 coached (a phone partner reads a scam script and dictates recipient/amount/PIN). ≈150–250 labelled sessions; ~20 keystroke events each. Held-out split BY PERSON (≥8 people never seen in training).
- Protocol: web mock send flow (no real money, no real upay app) logging per-keystroke timestamps, per-field dwell, backspaces, confirm-screen dwell. Coach calls the participant on a real phone; session recorded as audio ONLY for label verification, deleted after labelling.
- Consent wording (must be shown on screen and signed):
  - English: "I agree to participate in a study of typing behaviour in a mock payment app. I understand no real money is moved, my keystroke timings will be recorded, sessions may be audio-recorded only to confirm labels and deleted within 7 days, and I can withdraw at any time without reason."
  - Bangla: "আমি একটি নকল পেমেন্ট অ্যাপে টাইপিং আচরণের গবেষণায় অংশ নিতে সম্মত করছি। এখানে কোনো প্রকৃত টাকা লেনদেন হয় না, আমার কী-প্রেসের সময় রেকর্ড হবে, লেবেল নিশ্চিত করার জন্য সেশনের অডিও সর্বোচ্চ ৭ দিন রেখে মুছে ফেলা হবে, এবং আমি যেকোনো সময় কোনো কারণ ছাড়াই অংশগ্রহণ বন্ধ করতে পারব।"
- Redaction: no phone numbers, no names in logs; participant IDs are random codes; audio deleted post-labelling.
- Who collects / hours: all 3 team members, ~6–8 h total (collection can run in parallel with building; participants recruited in first 6 h per CONTEXT.md).
- Known validity gap (from critique 02-critique.md): scripted role-play may not produce the same timing signature as real coercion under fear — UNVERIFIED and probably false as a perfect proxy; the pitch must state this as the #1 limitation.

## 2. PRECEDENT

- **Google Messages on-device scam detection** (text, not timing): AI flags conversational scam patterns on-device, real-time warnings, since Mar 2025 — https://blog.google/products-and-platforms/platforms/android/new-android-features-march-2025/ (VERIFIED today). Covers SMS scams, not live-call-coerced app sends.
- **bKash send-money recipient-name display** with unsaved-number disclaimers — https://www.tbsnews.net/economy/corporates/bkash-send-money-now-more-secure-accurate-831161 (verified in critique round; not re-opened today — UNVERIFIED by me).
- **Behavioural biometrics vendors** (BioCatch, BehavioSec) model typing/interaction patterns for banks globally — existence known from memory, URLs not opened today: UNVERIFIED.
- **In Bangladesh: no product found that models send-flow timing for coercion.** The interaction-timing angle appears unoccupied locally; the general "scam warning" space is occupied by Google/Truecaller.

## 3. LEGAL/ETHICS (not legal advice)

- Bangladesh Bank MFS regulation governs transaction intervention; any friction/veto on sends touches customer-protection and agent-conduct rules. The specific BB circular class was not opened today: UNVERIFIED — check https://www.bb.org.bd before the pitch.
- Personal Data Protection Act 2026 (Act No. 63 of 2026): keystroke timings tied to a person are personal data; consent required (s.5), personal/household-use exemption (s.24) likely covers our self-study; cross-border transfer rules s.29 if we upload logs to non-BD servers — prefer local storage or anonymised features. Source: https://www.recordinglaw.com/world-laws/world-recording-laws/bangladesh-recording-laws/ (secondary source, checked against bdlaws per its own note — treat specifics as UNVERIFIED against the Act text).
- Cyber Security Act 2026 s.25 covers misuse of recordings; we delete audio after labelling.
- Ethics: participants are classmates (power-differential low but real); coercion role-play must be clearly framed as role-play; no deception about what is recorded.
- Unclear: whether an MFS provider may legally slow down or gate a send based on a behavioural score (consumer-protection vs fraud-prevention tension). UNVERIFIED — flag for judges' Q&A.

## 4. 48-HOUR BUILD PLAN

Stack: Python + FastAPI backend, React (or plain HTML) mock send flow, scikit-learn/XGBoost sequence features (no GPU needed), on-device-style scoring mocked server-side.

- H0–2: A builds mock send flow with keystroke logger (spike 01 collector is the seed). B finalises consent form + recruits 30–50 participants, schedules slots. C writes scam scripts (3 variants: OTP/lottery/army-officer) and trains the phone-partner coaches.
- H2–10: DATA COLLECTION SPRINT. A/B/C each run participant slots (5 min/session). Meanwhile A wires feature extraction (per-field IKI stats, pauses, backspaces, confirm dwell — spike 01 features already work).
- H10–18: C trains model (logistic/XGBoost on session-level features; person-level held-out split). B builds the demo shell: risk banner + "guardian confirm" screen triggered by score. A runs the dwell-threshold baseline (critique: ~60% expected).
- H18–30: iterate: collect 10 more participants if signal is weak; tune features; build the live judge moment (judge does a coached send on a second phone, sees the banner fire).
- H30–36: FEATURE FREEZE. Model locked, metrics table printed (recall@FA-rate on held-out people vs baseline).
- H36–48: demo freeze + pitch: logic-chain one-pager, falsifier slide (≥65% recall at <10% FA or the signal doesn't exist), fairness slice (timing features by phone-type/typing-skill), limitations slide (role-play ≠ real coercion).
- Real vs mocked: send flow is real (mock app, real humans, real timing); the "upay integration" is mocked; no real transactions.

## 5. SPIKE TEST

Ran: `spikes/01-puppeteer/` — collector + scripted typist, two conditions (see RESULT.md).
- **Result: direct mean IKI 114.9 ms (SD 15.9), coached mean IKI 1017.0 ms (SD 783.2), pauses>1s: 0 vs 5.** Pipeline works end-to-end.
- PASS (pipeline): collector, logging, feature extraction all functional.
- FAIL (evidence): n=2 scripted runs prove nothing about humans. The human signal question is UNVERIFIED until the 30–50 participant study runs. Falsifier from critique: <65% recall on held-out coached sessions at <10% FA ⇒ signal does not exist.

## 6. BASELINE

- Non-AI baseline: dwell-time threshold rule (e.g., flag sessions with >3 pauses>1s or confirm-dwell >5s). Critique estimates ~60% — the model must beat it visibly on the same held-out people.
- LLM-API baseline: not applicable (no text input) — timing is the modality; this is actually favourable (no LLM can trivially replicate it).
- Pointless-if number: if the threshold rule and the model both land ~60% recall, the model adds nothing — kill or pivot to D3-style "assistance detection" framing.

## 7. RISKS

1. **Role-play ≠ coercion** (critique's unchallenged assumption): coached-calm students may mimic dictation, but real fear changes motor behaviour unpredictably. Mitigation: state it as limitation #1; frame output as "assistance/dictation detected", not "coercion detected" — dictation itself is the risk proxy. P(demo still lands): high.
2. **Signal too weak at n=30–50**: person-level variance (typing skill) swamps condition variance. Mitigation: within-person features (each person is their own control: compare to their first self-directed session), person-level held-out eval.
3. **False alarms on slow/elderly typists** — fairness failure. Mitigation: fairness slice by typing speed; threshold per-person baseline, not global.
4. **Scam-actor adaptation**: a scammer simply waits 2s per digit. Mitigation: pitch honestly — this raises attacker cost (slow, unnatural calls), not a permanent defense; combine with name-display and guardian-veto components.
5. **Demo day variance**: judge's coached send may not trigger. Mitigation: rehearsed demo participants on standby; pre-recorded fallback video.

**P(working live demo) = 0.75.** Reasoning: the pipeline is proven (spike), data collection is cheap and controllable, no GPU/model risk; the deduction is for demo-day variance and the risk that the model barely beats the threshold baseline (which still leaves a demoable system, just a weaker AI-depth story).

## 8. RESPONSIBLE AI

- Fairness groups: typing speed quartiles, phone type (touchscreen vs keyboard familiarity), age (students vs parents), gender. Report recall/FA per group.
- Explainability: output must show top reasons ("5 pauses >2s during PIN entry", "confirm dwell 3× your usual") — per-session feature attributions, not a bare score.
- Security: adversarial users (scammer coaching the victim to type fast) — test a "counter-coached" condition; data leakage (participant in both train/test — prevented by person-level split); no raw keystrokes stored, only derived features after the study.
- Human oversight: the system NEVER blocks a send; it triggers a human-readable confirmation screen / guardian prompt. Final decision always the user's (CONTEXT.md rule: no autonomous approve/deny).
- Transparency: predictions, assumptions (role-play proxy) and any generated text kept separate in the demo UI.
