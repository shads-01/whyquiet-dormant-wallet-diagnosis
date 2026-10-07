# 03-round2.md — Round-2 candidates (INNOVATOR, not ranked, not defended)

Produced 2026-10-02. Inputs: docs/CONTEXT.md, docs/IDEA_POOL.md, docs/01-data/inventory.md, docs/02-ideas/01-candidates.md (D1–D64), critique 02-critique.md `missing_search_spaces` (10 territories) + `kill_list` (read via task brief; file itself permission-blocked). Do not repeat D1–D64; do not re-enter killed patterns (on-device SMS scam detection, LLM-API baselines incl. refund dossiers, mock-data circularity, uplift-without-real-data, price/agri IVR, name-confirm, provisional-credit pools, macro artifacts, noun-swap generics).

New source-ID extensions used this round (carry into inventory later):
- **S28** — published BD fraud case corpus: court judgments + major-newspaper reporting (Daily Star / Prothom Alo / Dhaka Tribune archives). Public, consent-free, but per-paper scraping ToS UNVERIFIED — flag before crawling. The round-2 flagship asset.
- **S29** — Bangladesh Bank Sep-2026 Bangla QR circular (fee cut + instant settlement), already VERIFIED in inventory section C.
- **S30** — public FX / corridor rate feeds (BB FX pages, remitter rate tables). UNVERIFIED access; fallback = BB monthly aggregates only.
- **S31** — self-collected, consented, redacted transaction/commission/statement SMS dumps (extends inventory B).
- **S32** — live booth randomized-experiment data (real visitors, consented; manufactured during the demo).

All candidates pass the CONTEXT.md strict test as argued in their "Why it passes" field; none approves/denies consequential financial decisions autonomously (all end in human action).

---

## Territory 1 — Fraud-RESPONSE speed as product

**R2-01. Money-Path Hop Predictor** [T01][COMBO] — from a fraud case's typology + first-hop facts, a sequence model predicts the likely cash-out hop chain and geography, so responders send freeze/tracing requests to the right providers first.
- Source dataset(s): S28 (structured case corpus: typology, amounts, channels, hops, outcomes) + S2 (scam census numbers) + S7 (district aggregates as priors).
- Problem: A16 — no fast fraud-response system; victims and responders lose the trace while money moves. Reframed from "better detection" (crowded lane) to "where does THIS case's money go next".
- Model (input→output): case features (typology R2-09 output, amount band, first-hop channel, elapsed hours) → ranked probability distribution over next hops (provider × region × channel), with confidence per hop.
- Held-out test (by person): held-out published cases excluded from training; judges run a mock case live at the booth.
- Action + metric: ordered freeze-request package for human filing; metric = top-3 next-hop hit rate on held-out cases vs most-frequent-hop-by-typology lookup.
- Live demo moment: judge picks a scam story, the predicted hop map animates with confidence bars.
- Hours (3 ppl): 16h (corpus structuring shared with R2-09/02/10/11).
- Why it passes the strict test: model predicts hop sequences not expressible as a rule (learned from real published cases); real public data, not team-invented; held-out cases + judges' live inputs; output = concrete freeze ordering with measurable hit rate. Not D24 (which asks "is this number known"): this asks "where does this case's money go next".
- 80%-baseline to beat: most-frequent-hop-by-typology lookup.

**R2-02. Recovery-Decay Clock** [T01][ODD] — a survival model outputs P(stolen funds still recoverable) as a function of elapsed hours × case features; the decay curve itself is the product: it tells responders whether to spend the next hour tracing or filing.
- Source dataset(s): S28 (cases with dates, amounts, channels, recovered/lost outcomes) + S27 (response-desk priors).
- Problem: A16 — responders and victims lack any evidence-based answer to "is it too late?"; effort is spent uniformly instead of where recovery is still possible.
- Model (input→output): (elapsed hours, amount, channel mix, typology) → survival curve of recovery probability + per-case urgency score.
- Held-out test (by person): held-out judgments with known outcomes; judges dial elapsed hours live.
- Action + metric: urgency-ranked response queue; metric = Brier calibration + AUC on held-out cases vs a base-rate rule ("recovery = f(elapsed) only").
- Live demo moment: judge drags a time dial; the recovery curve and urgency verdict move live.
- Hours (3 ppl): 12h.
- Why it passes: real dated public cases (not invented); survival modelling is a genuine learned function of multiple features; held-out case evaluation; output drives a concrete queueing decision. Distinct from D49 (predicts time-to-resolution; this predicts loss probability = whether-to-act). No provisional credit anywhere (that pattern is killed) — the output is prioritization only.
- 80%-baseline to beat: fixed "recovery probability = base rate × decay constant".

## Territory 2 — Interoperability boundary fraud (Binimoy / P2P Bangla QR)

**R2-03. Boundary Dispute Router** [T01][T06] — P2P Bangla QR cross-provider payment disputes ("paid from app A, merchant's app B shows nothing") classified into settle-lag vs wrong-QR vs scam vs user error, each with a different next action (wait / re-request / escalate / report).
- Source dataset(s): S10 (real Play-review complaint language on MFS/QR, ToS-flagged, use sparingly) + S29 (BB dispute-resolution circular classes) + booth-collected live dispute descriptions (extends S27).
- Problem: A18 + A13-adjacent — with Bangla QR now cross-provider, disputes cross a provider boundary no single helpdesk sees; dispute volume PROBLEM UNVERIFIED (mark honestly).
- Model (input→output): dispute text (Bangla/Banglish) → root-cause class + evidence-needed list + routed action.
- Held-out test (by person): fresh disputes collected from booth visitors and judges' live phrasings.
- Action + metric: routed ticket + expected-resolution checklist per class; metric = classification F1 on held-out disputes vs keyword rules; misroute cost tracked.
- Live demo moment: judge reads a dispute aloud or types it, model routes it and names the missing evidence.
- Hours (3 ppl): 12h.
- Why it passes: trained on real complaint language (reviews + collected disputes), not mock data; judges' inputs are held-out; output is a concrete per-class action. Cross-provider boundary framing is new (post-Sep-2026), so it does not collide with killed complaint-router LLM baselines — the model must beat an LLM zero-shot baseline to survive (honest bar stated in pitch).
- 80%-baseline to beat: keyword-rule routing; LLM zero-shot classification.

**R2-04. Interop Timeline Fuser** [T01][COMBO] — scam cash hops across providers; from victim screenshots spanning MULTIPLE wallets, an event-alignment model builds one unified money timeline and flags the cross-provider boundary moments where each provider's own view is blind.
- Source dataset(s): S2 (self-collected multi-provider scam screenshots, consented, redacted) + S28 (case narratives for structure priors).
- Problem: A1 + A16 — cross-wallet hops defeat per-provider tracing; victims hold fragments across apps and nobody stitches them (kill-chain stage reading, D2, does something else).
- Model (input→output): heterogeneous screenshots → OCR events → learned event-coreference/alignment → single timeline with boundary flags (provider A→B transfer points) + gaps needing the other provider's records.
- Held-out test (by person): contributors not in the training set; judges upload their own mixed screenshots.
- Action + metric: unified timeline PDF feeding cross-provider freeze requests (human files); metric = timeline event-recovery F1 vs manual assembly time.
- Live demo moment: judge uploads 3–5 screenshots from different wallet styles; the fused timeline assembles live with boundary moments highlighted.
- Hours (3 ppl): 16h.
- Why it passes: the corpus (real multi-provider screenshots) exists nowhere publicly — max uniqueness; held-out contributors; concrete action (cross-provider freeze package). Model does alignment/fusion, not verdicts.
- 80%-baseline to beat: manual timestamp-sorted screenshot assembly.

## Territory 3 — Regulatory-window products ON the BB Sep-2026 Bangla QR measures

**R2-05. Baki→QR Conversion Ranker** [T05][PAY] — riding the Sep-2026 fee cut + instant settlement (S29): model predicts which baki-carrying shops gain most from switching sales to Bangla QR, producing a ranked agent-visit list for onboarding.
- Source dataset(s): S5 (khata sales-mix pages) + S12 (OSM context: agent/ATM proximity, shop type) + S27 (shopkeeper surveys around campus).
- Problem: A5 + A18 — merchants avoided QR for fees; the fee cut removes the objection, but upay can't visit everyone: who converts first is now the question.
- Model (input→output): shop features (credit-customer share, ticket sizes, repeat frequency, location context) → adoption-likelihood + expected QR volume per shop.
- Held-out test (by person): held-out shops not in the survey; sign-up observed later where reachable.
- Action + metric: ranked visit list for the agent team; metric = predicted-vs-actual adoption in held-out shops (sign-up rate lift vs size-heuristic ordering).
- Live demo moment: judges mark shops on a campus map; the model re-ranks them and shows why (top features).
- Hours (3 ppl): 14h.
- Why it passes: features from REAL khata pages and surveys; held-out shops; concrete action (visit list) with measurable conversion. Distinct from D17 (which targets informal cash-out points for conversion): different conversion target (sales QR adoption), different data (khata sales mix).
- 80%-baseline to beat: rank by shop size / footfall heuristic.

**R2-06. Merchant Tariff Overcharge Finder** [T05][T06] — merchants can't verify they are charged the NEW Sep-2026 rate; a learned fee-line parser reads consented merchant transaction/statement SMS, recomputes expected fees under the published tariff, and flags overcharges with reasons.
- Source dataset(s): S31 (consented merchant fee/transaction SMS) + S29 (published tariff schedule) — extension of inventory B; collection risk flagged (need ≥10 consenting merchants, else demote).
- Problem: A18 — tariff changes create silent overcharge risk; merchants have no verification tool; PROBLEM UNVERIFIED for actual overcharge frequency.
- Model (input→output): noisy vendor SMS → trained field-extraction + fee-recomputation model → per-transaction expected vs observed fee + overcharge flags with line-level explanation.
- Held-out test (by person): fresh merchants' SMS at the booth; judges paste a mock fee SMS live.
- Action + metric: merchant files a fee dispute with the flagged lines; metric = extraction F1 on held-out SMS + overcharge precision; Tk recovered per merchant in corpus.
- Live demo moment: judge scans a merchant statement; an overcharged line highlights with the computed delta.
- Hours (3 ppl): 14h.
- Why it passes: trained on real SMS artefacts; held-out merchants; concrete action (dispute with evidence). A trained extraction model on varied vendor formats — must beat regex/LLM baselines; not the killed "bill OCR" lane (that was utility bills for consumers).
- 80%-baseline to beat: regex per SMS template.

## Territory 4 — Agent business tooling beyond fraud

**R2-07. Statement–Khata Reconciler** [T05][T06] — agent's paper khata vs provider SMS statement: a learned cross-artefact matcher aligns entries and ranks unexplained discrepancies for the agent to dispute.
- Source dataset(s): S5 (agent khata photos, consented) + S31 (provider statement SMS).
- Problem: A6 + A7-adjacent — agents reconcile cash against digital statements by hand; errors mean unpaid commissions or unexplained shortfalls discovered late (L3 pain).
- Model (input→output): khata OCR entries + parsed statement SMS → learned entity/amount matching with assignment confidence → ranked discrepancy list with reason (missing / amount mismatch / duplicate / timing).
- Held-out test (by person): held-out agents' real khata+SMS pairs; judges reconcile a mock day live.
- Action + metric: dispute file per discrepancy; metric = discrepancy recall vs fuzzy-string matching baseline; reconciliation minutes saved.
- Live demo moment: judge photographs a khata page and pastes statement SMS; discrepancies light up in under a minute.
- Hours (3 ppl): 16h.
- Why it passes: real paired artefacts (khata + SMS) no public dataset covers; held-out agents; concrete action (dispute). The learned matcher must demonstrably beat fuzzy-string, which is the entire point of the model.
- 80%-baseline to beat: fuzzy string + amount equality matching.

**R2-08. Commission-Anomaly Detector** [T05] — learns each agent's normal commission pattern across many consenting agents' statements; flags missing, mis-tiered, or unexplained commission entries with explanations.
- Source dataset(s): S31 (consented commission/statement SMS across N≥10 agents) + S27 (agent interviews for labels).
- Problem: A5/A6-adjacent — agent income is commission; errors and tier changes go unnoticed; PROBLEM UNVERIFIED for frequency (mark honestly).
- Model (input→output): agent's commission history + peer context → learned per-agent expected-commission model → anomaly score + reason per flagged entry.
- Held-out test (by person): held-out agents' statements; agent-confirmed errors as ground truth.
- Action + metric: agent claims missing commission with evidence lines; metric = anomaly precision vs agent confirmation; caught-missed-commission count.
- Live demo moment: judge flips a commission line in a mock statement; the model flags it and explains against the agent's own pattern.
- Hours (3 ppl): 12h.
- Why it passes: real statements, real agent-confirmed anomalies; held-out agents; concrete action. Honest limitation: needs enough consenting agents; if N is small, per-agent pooling degrades — say so in the pitch.
- 80%-baseline to beat: fixed tariff recompute (pure rule) — must catch pattern-level anomalies a rule cannot.

## Territory 5 — Public court/news case corpus

**R2-09. BD Fraud Typology Classifier (corpus flagship)** [T01][T07][COMBO] — curate the first structured dataset of published BD fraud cases (typology, amounts, dates, geography, outcome) from court judgments + newspaper reporting, then train a Bangla classifier mapping any scam narrative → typology + discriminative phrases.
- Source dataset(s): S28 (court judgments + Daily Star / Prothom Alo / Dhaka Tribune fraud reporting; per-paper ToS UNVERIFIED — flag) — annotation ~300–500 cases by the team (labeling is our labour, not our invention of data).
- Problem: A1, A14, A15 — everyBD fraud discussion is anecdotal; no structured typology of real BD cases exists, so prevention and response are untargeted.
- Model (input→output): Bangla scam narrative (text or transcript) → typology (OTP/lottery/love/job/Ponzi/fake-loan-app/hundi/gambling/…) + confidence + top discriminative phrases.
- Held-out test (by person): held-out articles excluded from training; judges' own scam messages/descriptions typed live.
- Action + metric: typology routes the response playbook (feeds R2-01/02/11) + a public prevention digest; metric = macro-F1 on held-out articles + agreement with judge-labeled live inputs.
- Live demo moment: judge pastes a scam they received; typology + two matched real published cases appear.
- Hours (3 ppl): 14h (≈4h annotation each; corpus shared with R2-01/02/10/11).
- Why it passes: public consent-free data; the model is the product (typology prediction is not a lookup — it generalizes to unseen phrasings); held-out articles + judges; concrete action (routing + digest). The dataset itself is a defensible moat no other team will have.
- 80%-baseline to beat: keyword classifier AND LLM zero-shot (must beat both, stated honestly).

**R2-10. Tactic Half-Life Forecaster** [T01][T07][ODD] — survival model over the dated case corpus estimates each fraud typology's "half-life" (appearance → enforcement decay), predicting which current tactics are fading vs rising — steering prevention effort.
- Source dataset(s): S28 (dated corpus) + S25/Trends as secondary attention signal (UNVERIFIED, optional).
- Problem: A14 + A15 — anti-scam effort is static while tactics churn; nobody measures tactic decay.
- Model (input→output): typology × time-series of case counts/outcomes → per-tactic survival curve + current-phase classification (rising / plateau / decaying).
- Held-out test (by person): backtest on held-out years — did the model rank the tactics that actually faded?
- Action + metric: prevention-education priority list for the next quarter; metric = rank correlation between predicted decay and realized decline on held-out years.
- Live demo moment: judges see current tactics ranked by predicted remaining life, with the underlying dated case counts.
- Hours (3 ppl): 12h.
- Why it passes: real dated public data; a genuine survival/forecast model; out-of-time held-out evaluation; concrete prioritization action. Honest risk: corpus date coverage and density UNVERIFIED — if sparse, the idea degrades to descriptive and should be dropped rather than faked.
- 80%-baseline to beat: "rank tactics by raw recent count change".

**R2-11. Case-Link Retriever** [T01] — a new report retrieves the nearest published cases by modus-operandi embedding, surfacing shared artefacts (number patterns, script fragments) that suggest the same syndicate — an investigative lead sheet for a human investigator.
- Source dataset(s): S28 (corpus + constructed same-syndicate pairs via shared numbers/entities across articles) + S2 (live reports).
- Problem: A14, A19 — syndicates span many small cases; only retrieval across a corpus reveals the pattern.
- Model (input→output): case narrative → dense embedding → ranked precedent cases + shared-entity highlights (retrieval + reranker trained on same-syndicate pairs from the corpus).
- Held-out test (by person): held-out articles; judges file a mock report live.
- Action + metric: lead sheet (precedent cases + shared artefacts); metric = recall@5 on constructed same-syndicate pairs.
- Live demo moment: judge files a mock report; matched precedent cases with highlighted shared details appear.
- Hours (3 ppl): 12h.
- Why it passes: real public corpus; learned retrieval is not a lookup (generalizes to unseen phrasings); held-out evaluation; concrete action. Distinct from R2-09 (classification) and R2-01 (forward path prediction): this is retrospective linkage.
- 80%-baseline to beat: BM25 keyword retrieval.

## Territory 6 — Offline / weak-network AI

**R2-12. SMS Statement Digest** [T03][T06][DEL] — no app, no net: a user forwards a month of transaction SMS (or a USSD dump); a trained noisy-Banglish extraction model returns one digest SMS: total fees paid, largest outflows, odd charges.
- Source dataset(s): S31 (consented real MFS transaction SMS from students/agents — Bangla + Banglish, mixed vendor formats).
- Problem: A9-adjacent + L3 — feature-phone and low-data users never see their own fee trail; the killed lane was on-device scam DETECTION (Google Messages/Truecaller), not fee transparency — different task, different value.
- Model (input→output): raw SMS sequence → learned field extraction (type, amount, fee, balance, timestamp) despite format variation → aggregated digest + fee-anomaly lines.
- Held-out test (by person): held-out contributors' SMS dumps; judges' forwarded sample SMS at the booth.
- Action + metric: digest SMS reply + disputed fee lines; metric = field-extraction F1 on held-out people vs regex baseline; Tk of surfaced fees per user.
- Live demo moment: judge forwards 5 sample MFS SMS (or the booth replays them); the digest SMS arrives on screen.
- Hours (3 ppl): 14h.
- Why it passes: real consented SMS artefacts; held-out people; concrete action (fee claim / awareness). The model must beat regex across vendor format drift — that is where the learning lives.
- 80%-baseline to beat: per-template regex parsing.

**R2-13. 2G Voice Case Line** [T01][T06] — weak-network fraud intake: victim leaves a dialect voice note; Ben-10-tuned ASR extracts structured case slots (amount, time, channel, numbers) and scores urgency so a human responder calls the right cases back first.
- Source dataset(s): S1 (Ben-10 base) + S3 (self-collected dialect recordings) + S2 (real story scripts as eval material).
- Problem: A16 + A9 — victims who can't write a complaint (dialect, literacy, 2G) are invisible to any response system; intake is the bottleneck.
- Model (input→output): dialect audio → ASR + trained slot-filling → structured case fields + urgency score + transcript.
- Held-out test (by person): held-out dialect speakers telling real (consented) stories; judges leave a Bangla voice note live.
- Action + metric: responder call-back queue ordered by urgency; metric = slot F1 + triage-rank agreement with human assessors; transcription minutes saved.
- Live demo moment: judge speaks a scam story in Bangla/dialect; extracted slots and urgency appear live.
- Hours (3 ppl): 18h.
- Why it passes: person-level held-out evaluation via real speakers; the model (dialect ASR + slot filling) is the product — no LLM wrapper; output = prioritized human call-backs, human decides everything. Kill-list adjacency stated honestly: the killed "refund dossier" was an LLM drafting documents; this is trained slot extraction for triage, and the deliverable is a call-back queue, not a generated dossier.
- 80%-baseline to beat: generic Whisper-zero-shot transcription + manual reading.

## Territory 7 — Remittance corridor depth (sender side)

**R2-14. Corridor Spread Forecaster** [T03][T04] — forecasts tomorrow's corridor FX spread / landed-BDT for Malaysia/Saudi corridors, turning "send now vs wait 3 days" from a guess into a forecast with confidence.
- Source dataset(s): S30 (public rate feeds — UNVERIFIED access; fallback: BB S7 aggregates at weekly resolution) + S7.
- Problem: A17 — legal-channel value must visibly beat hundi; timing is an unclaimed lever; spread-variance magnitude PROBLEM UNVERIFIED.
- Model (input→output): rate history + calendar features → next-day(s) spread forecast with interval → landed-amount estimate per corridor.
- Held-out test (by person): rolling out-of-sample next days' actual rates; judges pick corridor + amount live.
- Action + metric: send-window alert; metric = directional accuracy + mean landed-Tk gain vs always-send-now baseline.
- Live demo moment: judge selects a corridor and amount; forecast band and "wait vs send" verdict render live.
- Hours (3 ppl): 12h.
- Why it passes: a genuine time-series forecast (not a lookup of today's rate); evaluated on future real rates the team cannot control; concrete action with measurable gain. Data access is the honest weak point — flagged, with the BB-aggregate fallback stated.
- 80%-baseline to beat: "send now" (no model) and random-walk forecast.

**R2-15. Landed-Amount Distribution Model** [T03] — receiver credits sometimes differ from the sender's expectation (spread, intermediate fees, informal routing); a learned per-corridor × per-day landed-amount distribution flags credits outside the expected band with a probability, telling the family whether to query or accept.
- Source dataset(s): S30 (rate/spread history, UNVERIFIED) + S27 (real remittance receipts from consenting relatives of teammates — amounts, corridors, dates).
- Problem: A17-adjacent — receivers can't tell a normal spread from a problem; PROBLEM UNVERIFIED for divergence frequency.
- Model (input→output): (corridor, day, sent amount) → learned landed-amount distribution → P(observed credit | normal) + flag with reason.
- Held-out test (by person): held-out relatives' real receipts; judges input corridor + expectation live.
- Action + metric: query/accept recommendation to the receiver; metric = flagged-discrepancy precision + expected-band coverage on held-out receipts.
- Live demo moment: judge inputs a corridor and taka expectation; the model shows the expected band and where a test credit falls.
- Hours (3 ppl): 12h.
- Why it passes: real receipts (consented) as data; the learned per-corridor distribution is the model; held-out people; concrete action. Honest caveat: at small sample sizes this approaches an interval rule — must demonstrate corridor-specific learned variance to stay a model.
- 80%-baseline to beat: fixed ±2% tolerance band.

## Territory 8 — Learning measurement

**R2-16. Scam-Drill Mastery Tracer** [T02][T03][COMBO] — measurement IS the product: a knowledge-tracing model (BKT/DKT) over per-tactic scam-drill responses outputs each person's mastery vector and selects the next drill item adaptively — proving whether the drill taught anything.
- Source dataset(s): S2 (census items as drill content) + S28 (typology-grounded items) + self-collected drill responses from 30–50 consenting classmates (real people, real answers).
- Problem: A1/A3 — scam-awareness content is delivered but never measured; nobody knows which tactic a given person actually failed; D37 scores one drill session, this models learning across items.
- Model (input→output): response sequence → per-tactic mastery probability → next-item selection + who-needs-what report.
- Held-out test (by person): new trainees at the booth (judges included) — predicted vs actual next-item accuracy.
- Action + metric: adaptive drill path + per-person weakness report; metric = next-item prediction AUC + drill time saved vs fixed sequence.
- Live demo moment: judge takes a 3-minute drill; the mastery map fills and the next question is chosen live by the model.
- Hours (3 ppl): 14h.
- Why it passes: real human response data collected by us; person-level held-out evaluation is the core metric; the model (knowledge tracing) is the product — remove it and you have a static quiz; concrete action (adaptive path). Not the killed uplift-referee: no campaign, no borrowed uplift data — measurement of one learner.
- 80%-baseline to beat: fixed question sequence + raw score.

**R2-17. Warning-Modality Effectiveness Model** [T02][COMBO][ODD] — a live booth randomized experiment delivers the same scam warning in 4 modalities (visual card / Bangla text / voice / mini-drill) to consenting visitors; a model learns per-segment which modality maximizes measured comprehension and retention.
- Source dataset(s): S32 (the live experiment itself — real intervention data manufactured at the booth) + S4 (interaction telemetry) + S27.
- Problem: A1/A2 — warnings exist but nobody knows which format actually lands for which person; the killed uplift-referee died for lack of real uplift data — this manufactures it in the room.
- Model (input→output): participant features + comprehension quiz outcomes → per-person/per-segment modality-effect estimate → recommended delivery modality.
- Held-out test (by person): judges and later visitors are the holdout — predicted best modality vs realized best on their quiz.
- Action + metric: per-segment warning-delivery policy for upay; metric = incremental comprehension vs random assignment, in-experiment.
- Live demo moment: judges take the 2-minute micro-experiment themselves and see their segment's recommended modality with the estimated lift.
- Hours (3 ppl): 14h (experiment design + instrument is most of it).
- Why it passes: randomized real data beats any borrowed uplift dataset on strict-test rule 2; held-out participants; concrete action (delivery policy); measurable incremental outcome by design.
- 80%-baseline to beat: "show everyone the visual card" (single-modality policy).

## Territory 9 — Employer-side RMG payroll anomalies

**R2-18. Dormant-Wage Detector** [T03][T02] — employer/HR view: a sequence-anomaly model flags wage credits that landed in wallets never meaningfully used (dormant) so HR triggers in-person verification and education — the employer acts, not the algorithm.
- Source dataset(s): S31 + S27 — proxy cohort of consenting DIU students receiving stipends/scholarships into wallets (activity-after-credit sequences); RMG validation explicitly deferred to post-hackathon partner data (A9/A10).
- Problem: A9 + A10 — digital wages land but part stay unopened/unspent (empowerment gap); dormancy rate UNVERIFIED; reframed from the killed wage-split advice (D13): this is an employer-side anomaly detector, not worker advice.
- Model (input→output): account-level activity sequence after credit → dormancy probability + engagement-stage (never-opened / checked-only / partial-use) with reasons.
- Held-out test (by person): held-out students; their self-reported actual usage as ground truth.
- Action + metric: HR follow-up/education list; metric = dormant recall at fixed precision k on held-out accounts.
- Live demo moment: judge flips mock accounts between "active" and "dormant" patterns; the model flags them with reasons live.
- Hours (3 ppl): 12h.
- Why it passes: real consented sequences (proxy cohort honestly labeled); held-out people; concrete action (verification visit). Honest limitation: student-stipend proxy ≠ RMG wages — stated in pitch; the pathway to RMG validation is the post-hackathon governed-data route.
- 80%-baseline to beat: "zero transactions after credit" threshold rule.

**R2-19. Payroll Pre-Flight Checker** [T06][T05] — before a payroll run, a model predicts which wallet IDs will fail or misroute (inactive SIM, recycled number, name–number mismatch risk) and produces a verification shortlist — batch, employer-side, pre-credit.
- Source dataset(s): S31 (recycled-number and inactivity signals) + S27 + BTRC stats (UNVERIFIED). Distinct from D26 (consumer-side recycled-SIM exposure): this is batch pre-flight for the payer.
- Problem: A9/A10-adjacent — failed wage credits cost re-runs and worker trust; misroute rate PROBLEM UNVERIFIED.
- Model (input→output): payroll ID-list features → per-row failure/misroute probability + reason → verification shortlist.
- Held-out test (by person): held-out ID lists from the proxy cohort; observed credit outcomes as truth.
- Action + metric: pre-payroll verification list; metric = failed-credit recall at precision k per run.
- Live demo moment: judge submits a 20-row mock payroll; flagged rows and reasons appear before "run".
- Hours (3 ppl): 12h.
- Why it passes: real signal data (consented); held-out lists; concrete action. Honest limitation: validated on the proxy cohort, not a real factory run — flagged.
- 80%-baseline to beat: "flag IDs with no transaction in 90 days" rule.

## Territory 10 — Time-shifting lens

**R2-20. Collect-Day Shift Advisor** [T03][T04] — time-shifting the *moment*: a model forecasts receiver-side agent cash pressure by day-of-month (salary cycle, festival calendar, district aggregates, agent surveys) and advises families to collect remittances/wages on non-peak days — "collect Wednesday: ~12 min shorter queue".
- Source dataset(s): S7 (BB aggregates) + S24 (festival calendar, UNVERIFIED) + S27 (agent wait-time surveys) + S12.
- Problem: A6 + L3 — queues on salary/festival days ARE the product experience; the shift is free value nobody claims. Distinct from D16 (replenishment scheduling for providers) and D63 (Eid cash map): consumer-facing day choice.
- Model (input→output): district + day features → day-level congestion forecast → collect-day recommendation with expected wait delta.
- Held-out test (by person): next week's surveyed wait times at held-out agent points; judges pick district+day live.
- Action + metric: in-app "best day to collect" nudge (opt-in); metric = predicted vs observed wait reduction.
- Live demo moment: judge picks a district and date; the congestion forecast and recommended day render live.
- Hours (3 ppl): 12h.
- Why it passes: public + survey data; genuine forecast model; out-of-sample evaluation on future waits; concrete action; no money movement, no incentive manipulation (pure information).
- 80%-baseline to beat: "avoid the 1st and Eid" static calendar rule.

**R2-21. Booth Uplift Lab** [T04][COMBO][ODD] — time-shifted incentives, measured live: a booth randomized experiment gives visitors off-peak-day offers vs none, and a model estimates per-segment incremental willingness to shift payment timing — the data is manufactured in the room, not borrowed.
- Source dataset(s): S32 (live randomized experiment: consented visitors, randomized arms, measured choices) + S4.
- Problem: A6-adjacent — upay wants demand spread off peak, but incentive targeting is guesswork; the killed uplift ideas died for lack of real uplift data; this creates it.
- Model (input→output): participant segment + assignment → incremental-shift estimate per segment (uplift model, e.g. transformed-outcome learner) → targeting policy.
- Held-out test (by person): judges and later visitors as holdout; realized shift behavior vs predicted.
- Action + metric: segment-level incentive targeting; metric = realized incremental shift rate of the model-targeted arm vs random in the live experiment.
- Live demo moment: judges draw a random arm, make the choice, then see their segment's estimated uplift versus control.
- Hours (3 ppl): 12h.
- Why it passes: a real randomized experiment run by us satisfies rule 2 and rule 3 simultaneously; the uplift model is the product; concrete targeting action with a measured incremental outcome. Smallest honest scale: ~60–100 booth visitors — sufficient for a 2–3 segment split, stated plainly.
- 80%-baseline to beat: uniform incentive to everyone.

---

## Round-2 rollup

### (a) Territories with 2+ candidates each
All ten filled: T1 ×2 (R2-01, R2-02), T2 ×2 (R2-03, R2-04), T3 ×2 (R2-05, R2-06), T4 ×2 (R2-07, R2-08), T5 ×3 (R2-09, R2-10, R2-11), T6 ×2 (R2-12, R2-13), T7 ×2 (R2-14, R2-15), T8 ×2 (R2-16, R2-17), T9 ×2 (R2-18, R2-19), T10 ×2 (R2-20, R2-21). Total: 21.

### (b) Territories not filled honestly — and why
None left empty, but four carry flagged weaknesses: (1) T7 rests on S30 rate-feed access that is UNVERIFIED; with only BB monthly aggregates, R2-14 degrades to weekly resolution and may stop passing the demo bar. (2) T9 validates on a student-stipend proxy cohort, not real RMG payroll — honest, but the judges' hardest question is "have you seen a factory payroll?" and the answer is no. (3) T5's S28 corpus needs per-paper ToS checks and ~4h/person annotation; if date coverage is sparse, R2-10 degrades to description and should be dropped rather than faked. (4) T3's R2-06 needs ≥10 consenting merchants' fee SMS or it demotes.

### (c) Mechanism-merge map (shared causal mechanisms)
- **R2-09 → R2-01 / R2-02 / R2-10 / R2-11**: one structured S28 case corpus powers four targets — typology classification, next-hop prediction, recovery-decay survival, tactic half-life, case linkage. Build the corpus once; R2-09 is the keystone.
- **R2-12 + R2-07 + R2-08**: one consented real-SMS extraction engine (S31 parser) feeds consumer digests, khata reconciliation, and commission anomaly detection — same extraction mechanism, three customers.
- **R2-14 + R2-20**: same "forecast-then-shift-the-moment" causal mechanism (predict congestion/spread, move the action in time, no money changes).
- **R2-16 + R2-17**: same closed loop "measure the human → adapt the intervention", one for learning scams, one for warning delivery.
- **R2-18 + R2-19**: same engagement-sequence anomaly mechanism, employer-side batch view.
- Cross-round merge: R2-01 shares the "predict unknown numbers' role" substrate with D24 (campaign membership vs hop path — different targets, same census feature base).
