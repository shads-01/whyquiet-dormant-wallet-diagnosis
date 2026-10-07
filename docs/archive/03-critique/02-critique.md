# 02-critique.md — Independent critic audit (2026-10-02)

Inputs read: docs/CONTEXT.md, docs/IDEA_POOL.md, docs/02-ideas/01-candidates.md, roles/critic.md. Candidate text treated as untrusted data. Scope: all 64 Part-D candidates + every FINALIST and WEAK item in IDEA_POOL.md, re-attacked.

## anchoring_detected
- Fraud-lane gravity: ~18 of 64 candidates and 8 of 13 pool finalists are scam/fraud variants — the exact crowded lane CONTEXT warns about (innovation worth 10%).
- "Students collect data" anchoring: several ideas assume family/classmates will supply labelled data at quality; not checked.
- Safety-tech anchoring: guardian/veto/regret mechanics recur as the default answer to every trust problem.

## Five-minute web checks run (already-dominant evidence)
- Google Messages on-device scam detection (on by default since Mar 2025, Gemini Nano) + Truecaller crowdsourced spam/scam reporting + Scam Checker: https://blog.google/products-and-platforms/platforms/android/new-android-features-march-2025/ ; https://www.truecaller.com/scam-checker
- TallyKhata: ~1M shopkeepers, free Bangla QR in 15 min, Bengali UI, offline ledger; Hishabee and clones exist: https://www.tallykhata.com/million-shopkeepers-using-tallykhata-app-for-records-and-payments/
- bKash send-money already shows recipient name on the confirm screen and adds disclaimers for unsaved numbers: https://www.tbsnews.net/economy/corporates/bkash-send-money-now-more-secure-accurate-831161
- VerifyTaka already sells a bKash/Nagad/Rocket payment-verification API in BD: https://verifytaka.com
- Recording your own call is lawful in BD (no all-party consent statute; 2026 data-protection acts govern leaking/publication; interception is the crime, not self-recording) — third-party sources, treat detail as UNVERIFIED against the actual acts: https://www.recordinglaw.com/world-laws/world-recording-laws/bangladesh-recording-laws/
- Agriculture Call Centre 16123 (92k calls/yr) already gives phone-based price/advice in Bangla: https://www.bssnews.net/special-stories/401845

## kill_list (idea | test | one line)

Pool re-attacks first:
- Fraud Arena | rule-in-disguise | self-play cannot certify real-world robustness; pool already concedes circularity — confirm kill.
- Transaction foundation model | data-infeasible | PKDD'99 unreachable (inventory), no replacement pretraining corpus named — kill.
- Ledger-grounded Banglish resolver | LLM-API baseline | function-calling GPT on a ledger gets ~80%+ of the value; rule 1 fails — kill.
- Name Confirm | already-dominant | bKash (and presumably upay) already displays the registered name pre-send with unsaved-number disclaimers; residual novelty is only cross-script spelling fuzz — demote to component, kill as product.
- Chanda Trust | complexity | stolen-photo reuse needs image-search infra + charity verification liability in 48h — kill.
- Silence/uplift engine | data | still no verified public uplift dataset; dunnhumby fails rule 2 — confirm kill.
- Remittance envelopes / Digital Samity / Rain-Day / Peak Shaver / Bulk-Buy / salary-day reducer / bazaar budgeting / cash-drawer vision / shop-snapshot / Vouch Graph | previously killed, re-affirmed | no new data or mechanism rescues them.
- Dialect voice wallet (pool finalist) | survives but merges | see survivor V4; the free-speech variant (D38) is the live differentiator, not the IVR menu.

Part-D candidates:
- D1 Scam SMS Verdict | already-dominant | Google Messages does on-device scam SMS detection by default; Truecaller blocks spam — only the BD-MFS-corpus sliver remains, which belongs to the census, not a product.
- D5 Refund Dossier Automator | LLM-API baseline | an off-the-shelf LLM extracts entities and drafts the dossier; the moat is the corpus, not the model — kill as standalone.
- D6 Wrong-Name Early Warning | importance + PROBLEM UNVERIFIED | no documented wrong-send loss source; near-miss rate too low to matter in a 48h demo.
- D7 Scam Attention Nowcast | importance | even perfect lead-time moves awareness pushes marginally; no top-line movement; access to Trends/pageviews UNVERIFIED.
- D8 Consent-Chain Voice | hidden assumption | assumes senders happily record voice consents and beneficiaries accept voice as proof; adds friction to the one flow people want frictionless — kill.
- D12 Khata Triage Verifier | feature-extension | confidence-threshold triage is a knob on Khata Lens, not a product.
- D13 Wage-Split Advisor | noun-swap | "budgeting advice for payroll" survives swapping MFS for any HR/banking product; unverified problem.
- D14 Bazar Price Oracle | already-dominant + noun-swap | 16123 already delivers phone price/agri advice in Bangla; forecast adds value nobody asked sellers for.
- D15 Complaint Router Banglish | AI-bolt-on | helpdesk auto-routing exists everywhere; LLM API gets 80% — ops backlog item.
- D19 Proof-Demand Detector | AI-bolt-on | "send a request link instead of a screenshot" is a product flow; the model does nothing load-bearing.
- D22 Agent Onboarding Dialect Coach | AI-bolt-on | quiz scoring is forms+rules; dialect voice is delivery, not the product.
- D23 Price-Shock Early Warning | importance | upay-link thin; public-data exercise survives any industry noun.
- D26 Recycled-SIM Risk | importance + data UNVERIFIED | BTRC number-history unobtainable in 48h; problem undocumented for BD.
- D28 Community Blocklist Co-op | already-dominant | Truecaller *is* the crowdsourced blocklist; merchant-governance angle is real but is a policy product, not a model.
- D29 Agent Trust Scorecard | data (rule 2) | real agent-quality data cannot be collected beyond a dozen campus shops in 48h; everything else is invented — circular.
- D32 Affordability Insight | rule 1 + PROBLEM UNVERIFIED | author's own block admits it survives only as an explanation product; no BD pain source.
- D33 Uplift Referee | data (rule 2) | Criteo UNVERIFIED, dunnhumby synthetic-derived; CONTEXT already killed the silence engine for exactly this — kill.
- D34 Inclusion White-Space Report | noun-swap + artifact | a GIS siting study; not a model-is-the-product demo.
- D36 Coverage Fairness Slice | artifact | board chart, not AI product.
- D40 Fraud-Buffer Pool | regulatory | provisional credit from a pooled buffer sits squarely in e-money/deposit/insurance territory (Bangladesh Bank e-money rules class); CONTEXT's regulatory-risk lessons apply — kill.
- D41 Frustration Escalation | AI-bolt-on | sentiment-threshold alerting with an LLM baseline.
- D43 Queue-Length Vision | importance | wait-time estimation is a gimmick; nobody switches shops over a 4-minute guess.
- D44 Bill-Photo Validator | LLM-API baseline | modern LLM OCR reads bills nearly perfectly; no learned edge survives.
- D45 Remittance Landing Planner | noun-swap | generic household budgeting; remittance envelopes already killed.
- D46 Hotline Empathy Meter | importance + privacy | prosody scoring of staff calls is surveillance-adjacent and value-thin.
- D49 Long-Loop Recovery Tracker | mechanism-thin | duration prediction on mock cases fails rule 2 and moves nothing.
- D51 Cash-In Ritual Models | data-infeasible | two-week diaries from real households cannot happen inside the build window.
- D52 Hundi-Pressure Monitor | artifact | macro index from UNVERIFIED sources; no user, no demo.
- D54 Agent Liquidity Social Feed | data (rule 2) | posts are self-generated in the demo — the model learns only what we injected.
- D56 Festival Demand Calendar | rule-in-disguise | calendar lookup + seasonality arithmetic.
- D57 Wallet-Language QA | noun-swap | "predict which screen text confuses users" is generic UX-tooling.
- D59 Ghost-Agent Detector | data (rule 2) | constructed mock dossiers — circular.
- D60 Price-Speech Bazar Bot | noun-swap + already-dominant | 16123 exists; the MFS link is a bolted-on CTA.
- D61 Overdue-Reason Classifier | noun-swap + unverified | "empathetic collections advice" works for any credit book; hardship labels invented.
- D62 Deposit-Slip Digitizer | duplicate mechanism | same OCR family as Khata Lens; merge and drop.
- D63 Festival Travel Wage Access | complexity + unverified | migration-cash demand needs longitudinal data we lack.
- D64 Review-Answer Draftsman | LLM-API baseline | the LLM is the product and it is not ours.
- D55 Banglish parser / D20 Dialect WER Map / D27 Fairness Audit / D42 Voice PIN Recovery / D9 Confirm-Echo | components | real and useful but not standalone products — fold into the survivors below.

## Calibration
Killed ~40/64 Part-D ideas (~60%) plus 6 pool items — above the 30–50% normal band. Direction of error: I erred toward killing data-infeasible and bolt-on ideas and toward merging aggressively; if anything I under-killed the fraud-lane cluster (survivors 1, 5, 6, 7, 12, 13, 15 are all Track-01) — the Reviser should rebalance toward Tracks 02–07.

## unchallenged_assumptions (reclassification)
- Innovator's B8 ("users want more friction when vulnerable") survives, but Coercion Shield's harder assumption is unchallenged: scripted role-play produces the same timing signature as real victimization under genuine fear — UNVERIFIED and probably false (fear changes motor behaviour).
- B15 ("person-level held-out evals satisfy rule 3") is sound, but for interaction-log ideas the held-out *people* are classmates whose phones and habits are non-representative of upay's actual base — fairness across groups (rule) is exposed.
- Innovator's B3/B2 chain (merchant cash-out as the emergent system) is well-evidenced (Prothom Alo) but Baki-Settle silently assumes shops *want* digital baki settlement — a shop's baki is also its customer lock-in; digitizing it may weaken the lock-in that makes baki work.
- "Voice is the channel for the excluded" is asserted from literacy stats, not from any collected evidence that excluded users prefer voice to asking a relative.

## mechanism_problems
- D37 Agent Scam Drill: synthetic audio trains, but the *scoring* model's labels come from the same team's judgement of "vulnerable responses" — the grader is the injection point (mild circularity); needs an expert-anchored rubric or blind second rater.
- D16 Agent Float Pre-Positioning: survey-of-12-agents demand data is anecdote-scale; the model will fit interviewer effects, not demand.
- Pool Puppeteer: Android call-recording API restrictions mean the strongest variant (live-call audio) may be technically impossible on-device; the interaction-timing variant survives only if the app controls the send screen (fine for demo, unclear as upay integration).
- VerifyTaka overlap: pool's payment-proof forensics must be repositioned as *forgery detection* (VerifyTaka verifies real transfers; nobody detects forged screenshots) or it dies on already-dominant.

## strong_ideas (survivors, ranked 1–20, near-duplicates merged)

**1. Coercion Shield — Puppeteer variant** (pool a, absorbs D3, D9) [T01]. Timing/interaction model over send flow distinguishing self-directed vs dictated sends.
- Failure mechanism: coached-but-calm students mimic dictation patterns; model learns the *coach's* style, not coercion's.
- Honest no: an elderly user mid-scam will not tolerate an extra prompt that a scammer can talk them past.
- Reg/privacy: Bangladesh Bank MFS transaction-intervention rules class; also Telecommunication Act / 2026 data-protection acts for any audio path.
- Falsifier: if held-out coached sessions score below ~65% recall at <10% false-alarm on self-directed sends, the signal does not exist.
- Baseline: a dwell-time threshold rule gets maybe 60% — the model must beat it visibly or die.

**2. Khata Lens** (pool; absorbs D12, D27, D62 as components) [T05].
- Failure mechanism: real khata pages mix Bangla/English, scripts, arithmetic marks; NumtaDB digits don't cover graphemes+layout together — the fine-tune gap is the whole project.
- Honest no: TallyKhata is free, offline, Bengali and has 1M shops — the shopkeeper's reason to refuse is "I already have the app I never opened."
- Reg/privacy: shopkeeper consent + customer-name blurring; Bangladesh data-protection act (2026) class for any stored photos.
- Falsifier: if entry-level accuracy on real khata pages is below ~90% with per-entry confidence, verification burden exceeds typing.
- Baseline: LLM vision-API reads clean pages ~80%; win must be on messy pages + offline.

**3. Baki-Settle** (D10) [T03/T05].
- Failure mechanism: customers with cash prefer cash; the wallet-settle option only matters when the customer lacks cash — the exact moment they'd rather owe.
- Honest no: shops refuse because baki is their customer lock-in; upay refuses because it looks like credit-adjacent product.
- Reg/privacy: e-money rules (BB) — ensure settlement is payment, not deferred-deposit.
- Falsifier: if in a 20-customer mock trial fewer than ~25% choose settle-over-cash-out when both are available, the demand premise fails.
- Baseline: none — the mechanism is payment flow; the model only ranks which baki lines to surface (weak AI role — flag for reviser).

**4. Voice wallet family: dialect free-speech payments + Confirm-Echo** (pool finalist, D30, D38, D9) [T03/T06].
- Failure mechanism: free-speech slot extraction on dialect speech fails silently — a misheard amount is a money event; echo-check is the mitigation and it is also speech.
- Honest no: users with any literacy prefer taps; voice users are precisely those who cannot verify a read-back.
- Reg/privacy: BB e-money authentication rules class; check whether voice auth is a permitted factor.
- Falsifier: Ben-10 closed-test WER on amount/recipient slots; if slot-exact accuracy <90% per dialect, kill the free-speech version, keep menu-IVR.
- Baseline: menu-IVR (existing) gets most of the value; the model's edge is dialect robustness — must be measured, not asserted.

**5. Agent Scam Drill** (D37) [T05/T01].
- Failure mechanism: trainees game the drill's known voices; scoring labels are team-invented (see mechanism_problems).
- Honest no: agents say "I've heard it all" and skip; upay says training agents is cost centre, not product.
- Reg/privacy: consent for voice recordings; synthetic-audio disclosure norms (BTRC/ICT Act class on synthetic voice).
- Falsifier: pre/post drill — if susceptibility (measured on a fresh script) doesn't drop by ≥20 pts for drilled vs undrilled peers, dead.
- Baseline: a PDF of scam tips gets 40% of the value; the interactive edge must show in the delta.

**6. Voice-clone guard, dialect-fair** (pool c + D4) [T01].
- Failure mechanism: anti-spoof models trained on ASVspoof (English/multilingual) may transfer poorly to Bangla codecs/noise; fairness slice may reveal it just fails dialect speakers.
- Honest no: upay asks "why do we need this before BB mandates it?"
- Reg/privacy: biometric data class — Bangladesh data-protection act (2026); BB rules on biometric auth factors.
- Falsifier: EER on held-out dialect speakers ≤2× the clean-speech EER, else not shippable.
- Baseline: existing commercial voice-biometrics vendors cover spoofing; the dialect-fairness slice is the only defensible sliver.

**7. Scam Census family: kill-chain screenshot reader + number prophet + grammar drift** (pool + D2, D24, D47) [T01].
- Failure mechanism: corpus too small in 48h (~50–100 real messages) for drift prediction to be anything but anecdotes.
- Honest no: upay already runs a fraud team; "students collected 60 scam texts" is not a dataset to them.
- Reg/privacy: redaction discipline; publishing a blocklist has defamation exposure — check with legal, not guessed law.
- Falsifier: hold out one contributor's messages; if campaign clustering can't place ≥70% of them into prior clusters, prediction claims die and only the census exhibit remains.
- Baseline: LLM clusters scam texts well; the model must show extraction + drift the LLM prompt can't replicate reliably.

**8. Dialect Hotline Triage** (D21) [T06].
- Failure mechanism: IVR providers already do keyword routing; dialect ASR errors route people wrongly — worse than a queue.
- Honest no: bKash runs a 24/7 human hotline with live chat; upay may prefer humans for trust.
- Reg/privacy: call recording + retention under data-protection act; consent at call start.
- Falsifier: intent accuracy ≥85% on held-out dialect calls or the tool misroutes more than it saves.
- Baseline: LLM-on-transcript gets 80% once ASR works — the moat is the ASR, so WER is the load-bearing number.

**9. Spoof-Proof Hotline Callback** (D31) [T01/T06].
- Failure mechanism: knowledge-fact verification is socially engineerable; liveness in noisy Bangla calls is the actual hard model.
- Honest no: hotline ops say callbacks already verify via registered-number policy; adding AI changes nothing about the fraud path (fraudsters call *out*, not in).
- Reg/privacy: biometric verification rules; data-protection act.
- Falsifier: red-team drill — imposter success rate must fall from ~100% (baseline policy) to <20% in a 10-attempt drill.
- Baseline: registered-number-only callback policy is the incumbent; model must beat a rule by a wide margin in the drill.

**10. Confusion detector + KYC drop-off + friction-by-demographic** (pool + D25, D39) [T02].
- Failure mechanism: classmates' prototype logs ≠ real-user logs; the model learns demo artefacts (browser, trackpad) not struggle.
- Honest no: product teams distrust tiny-sample UX models; "we'll just watch session replays."
- Reg/privacy: interaction telemetry consent; upay data-governance class for behavioural data.
- Falsifier: drop-off prediction AUC ≥0.75 on held-out parents; else it's an observation, not a model.
- Baseline: funnel-step completion counts (a report) get 60% of the value; the per-user live adaptation is the model's claim.

**11. Merchant-Cannibalization Converter** (D17) [T05].
- Failure mechanism: informal cash-out likelihood inferred from shop *type* is stereotyping; the survey ground truth is 20 shops max.
- Honest no: upay channel team already knows where informal points are — their agents tell them weekly.
- Reg/privacy: BB merchant-agreement class; incentive-compliance (paying informal agents may breach agent rules — check BB MFS agent regulations).
- Falsifier: model must rank the 20 surveyed shops with ≥0.8 AUC against the informal-cash-out ground truth; else it's intuition.
- Baseline: ask the campus agents for a list — 80% of the value, zero ML.

**12. Payment-proof forensics (forgery detector)** (pool; repositioned against VerifyTaka) [T01/T05].
- Failure mechanism: forgeries evolve (better apps); detector trained on today's forgeries — the classic arms race with a 48h corpus.
- Honest no: sellers say "I just call the buyer's number and check."
- Reg/privacy: screenshots contain third-party names — redaction; no provider trademarks in demo materials.
- Falsifier: held-out forged-vs-real set built by a teammate the modeler never talks to; ≥90% detection with <5% false-positive on real proofs, else unusable (false accusations).
- Baseline: pixel/EXIF heuristics catch lazy forgeries (~70%); the model must beat that on good forgeries.

**13. Agent Bounty Guardian** (pool) [T05/T01].
- Failure mechanism: bounty incentives create false stops (agents farm bounties); ranking model trained on what data? — confirmed-stopped-cash-outs don't exist yet.
- Honest no: upay legal says rewarding agents for interrogating customers creates liability.
- Reg/privacy: BB MFS agent conduct rules; anti-harassment exposure.
- Falsifier: in a mock ledger of 200 cash-outs with 15 planted scams, the ranking model must place ≥10 in the top 20 with agent effort capped.
- Baseline: a simple amount/velocity rule list gets 60%; model must beat it.

**14. Agent Float Pre-Positioning** (D16, rescuing weak pool Float Radar with real survey data) [T05/T06] — conditional.
- Failure mechanism: 12-agent survey demand data is anecdote-scale; forecast looks scientific, isn't.
- Honest no: ops teams run replenishment by routine; "AI schedule" must beat a 2-line heuristic they already use.
- Reg/privacy: none heavy; agent commercial data confidentiality.
- Falsifier: next-week stockout prediction beats day-of-week average by ≥30% on held-out agents, else the heuristic wins.
- Baseline: day-of-week + payday heuristic ≈ 80% — model must visibly beat it on the demo chart.

**15. Scam-Victim Pathway Replay** (D58) [T01/T07].
- Failure mechanism: story transcripts are survivorship-biased (only victims who escaped/reported); the pathway model inherits the bias silently.
- Honest no: upay says "we know the pathways" — the deliverable must be an interception *ranking*, not a diagram.
- Reg/privacy: victim stories are sensitive; consent + redaction under data-protection act.
- Falsifier: expert fraud analysts (2) must agree with ≥70% of model-nominated interception points on held-out stories.
- Baseline: an LLM summarizing the stories into a pathway diagram gets 70% — model must add the ranked interception layer.

**16. Elder Check-In Beacon** (D50) [T03/T07] — borderline.
- Failure mechanism: the model must infer "distress" from one weekly sentence — near-impossible; false alarms burn guardian trust in week two.
- Honest no: families say "we just call Ma every Friday."
- Reg/privacy: biometric + health-adjacent inference; data-protection act; consent from the elderly person, not the guardian.
- Falsifier: 10-week mock trial with families; ≤1 false guardian alert per month and 100% voice-verification on held-out imposters, else kill.
- Baseline: a calendar reminder gets 70% of the value; the voice check adds verification only.

**17. Fair-Freeze Auditor** (D11) [T01] — conditional.
- Failure mechanism: mock case dossiers are team-invented — rule 2 exposure; only real survey-grounded cases (news-documented freeze episodes) survive.
- Honest no: upay risk teams don't outsource review ordering to a student model; compliance owns it.
- Reg/privacy: BB freezing-order procedure class; explainability minimums from the hackathon rules.
- Falsifier: on held-out documented cases, model's FP-ranking must beat random review order by a measured margin (precision-at-k uplift ≥20%).
- Baseline: severity-sorted queue gets 60%.

**18. Dialect WER Map** (D20) — demoted to component. Not a product; it is the evidence slide behind ideas 4, 8, 9. Keep as deliverable, not candidate.
**19. Banglish parser + NC-SentNoB noise handling** (D55) — demoted to component feeding 7 and 8.
**20. Review miner (Competitor pain miner + D35 merged)** [T04] — conditional on Play-ToS discipline; LLM baseline risk high; keep only as the Track-04 story if the census needs a growth sibling.

## hidden_theses (what must be true about reality)
- 1: Coerced sends have a detectable motor signature distinct from role-play coercion.
- 2: Khata handwriting is consistent enough per shop to fine-tune in hours, and shops will let us photograph it.
- 3: Customers want to settle shop credit digitally more than they want cash in hand.
- 4: Dialect speakers will conduct money transactions by voice at all.
- 5/7: Agents and victims will rehearse/report with students, and 50–100 real artefacts is enough to demonstrate real signal.
- 11: Informal cash-out merchants are identifiable from observable shop features and convertible.
- 14: Agents will share demand data truthfully and upay will act on a schedule a heuristic already approximates.

## missing_search_spaces (drives the Reviser)
1. **Fraud-response speed as a product** (F1 reformulation, barely explored): simulate the A16 Fast-Fraud-Response pipeline — tracing/freeze orchestration across BB/BFIU/MFS as a demo — no candidate built it because D5/D49 were killed for baselines; the *simulation* angle is untouched.
2. **Interoperability boundary fraud**: Binimoy and P2P Bangla QR (Sep 2026) create cross-provider flows nobody covers — boundary dispute routing, cross-wallet scam tracing.
3. **Regulatory-window products**: building *on* the BB Sep-2026 Bangla QR measures (instant settlement, low merchant cost) rather than beside them — e.g., merchant settlement-reconciliation intelligence.
4. **Agent business tooling beyond fraud**: commission reconciliation, provider-statement auditing for agents — completely absent.
5. **Public court/news case corpus as data**: structured typology classifier from published fraud court judgments — public, consent-free, zero collection risk; no candidate used it.
6. **Offline/weak-network operation**: all voice/app ideas assume connectivity; USSD+SMS AI (async, sync-later models) unexplored.
7. **Remittance corridor depth**: sender-side FX/fee transparency for specific corridors (Malaysia, KSA) — only generic remittance ideas tried and killed.
8. **Learning measurement**: knowledge-tracing over scam-drill performance (does the drill teach?) — pool's sparring partner gestured at it; nobody made measurement the product.
9. **Employer-side RMG payroll anomalies** — killed D13 as noun-swap, but the employer pain (misrouted wages, dormant wallet wages) was never actually attacked.
10. **Time-shifting lens applied**: nothing moved incentives/prompts to non-salary days (lens 19 unused in practice).

## revision_directions
- Rebalance: at most 5 survivors should sit in Track 01; the Reviser should push 2–3 toward Track 05/06/07 using the missing spaces above.
- For each kept idea, make the falsifier the *first demo slide*: judges respect a project that names its own kill condition.
- Merge map applied: D3→1, D12/D27/D62→2, D9/D30/D38→4, D2/D24/D47→7, D25/D39→10, D35→20, D20/D55→components.
