# 05-decision.md — JUDGE's decision (2026-10-02)

Inputs read: docs/CONTEXT.md, docs/IDEA_POOL.md, docs/03-critique/02-critique.md, docs/04-feasibility/00-summary-partA/B/C.md + docs 01–12, docs/02-ideas/01-candidates.md (PART A). docs/02-ideas/03-round2.md NOT read (out of scope). All P(demo) values verified against the feasibility summaries; **no file disagrees with the brief's P(demo) numbers** (01:0.75, 02:0.45, 03:0.55, 04:0.70, 05:0.65, 06:0.45, 07:0.55, 08:0.60, 09:0.65, 10:0.45, 11:0.40, 12:0.70). Spike numbers verified: whisper-tiny zero-shot WER 7.48 (00-summary-partB, idea 06) and 127.9%/123.1% (00-summary-partC, idea 10); NumtaDB softmax floor 32% (partA + 04-khata-lens.md §5); proof-forensics ELA 6/6 on MOCK set (partB + 08 §5); Puppeteer IKI 114.9 vs 1017 ms, n=2 scripted (partA + 01 §5); confusion 23.4x, n=2 scripted (partC + 12 §5); tesseract 3/3 amounts on clean print, names degraded (partC + 09 §5); SentNoB lexicon 0.20 vs majority 0.46 (partB + 05 §5). One correction to the brief: the researchers B and C WER numbers (7.48 and 127.9%) are two different spikes (idea 06 vs idea 10), not conflicting measurements of the same thing.

Citation shorthand: `doc##` = docs/04-feasibility/##-….md; `A#` = pain-point row in docs/02-ideas/01-candidates.md PART A.

---

## 1. SCORES

Criteria: Problem relevance 20% · AI/ML depth 20% · Business/customer impact 20% · Prototype quality 15% · Innovation 10% · Scalability & integration 10% · Responsible AI & security 5%. N/E = no evidence found in feasibility files; scored 1.

| # | Idea | Problem (20%) | AI depth (20%) | Business (20%) | Prototype (15%) | Innovation (10%) | Scale/Integr (10%) | RespAI (5%) |
|---|------|---|---|---|---|---|---|---|
| 01 | Puppeteer | 5 — A1: PIN/OTP scams "most prevalent MFS fraud pattern"; doc01 §2: no BD product models send-flow timing | 4 — doc01 §5: IKI 114.9 vs 1017 ms separation, sequence features; must beat ~60% dwell-rule baseline (§6) | 4 — doc01 §1: 30–50 participants/150–250 sessions cheap to collect; risk = role-play proxy (§1 known gap) | 4 — doc01 §5: collector+pipeline works end-to-end; "n=2 scripted prove nothing" is its own caveat | 4 — doc01 §2: "interaction-timing angle appears unoccupied locally"; Google/Truecaller cover text only | 3 — critique §mechanism: works only if app controls the send screen; "unclear as upay integration" | 5 — doc01 §8: never blocks, feature attributions, fairness by typing-speed, person-level split |
| 02 | Kill-chain listener | 4 — A1/A2: fake MFS calls asking OTP documented; doc02 §2: no BD call-speech detector found | 3 — doc02 §5: spike FAILED — whisper WER 1.000 (Latin/Devanagari out); classifier moat is only the ASR | 3 — doc02 §3: Android blocks call capture since v10; provider-side/uploaded-audio only | 2 — doc02 §5: "FAIL (ASR quality): default model unusable for Bangla script"; real-speech WER UNVERIFIED | 3 — doc02 §2: Pindrop exists globally (VERIFIED); unoccupied locally but platform-blocked | 2 — doc02 §7: Android platform restriction "not fixable"; demo via speakerphone workaround | 4 — doc02 §8: interpretable timeline, dialect F1 slices, human analyst oversight |
| 03 | Voice-clone guard | 3 — A20: deepfake voice scams regional, "BD-specific prevalence UNVERIFIED" (doc11 §7); critique #6 "why before BB mandates it" | 4 — doc03 §5: toy features NEGATIVE (cosine margin 0.003) → ECAPA/AASIST mandatory; real ML required | 2 — critique #6: "upay asks why do we need this before BB mandates it" | 2 — doc03 §5: ASVspoof 5 NOT downloaded (login-gated); Bangla transfer UNVERIFIED | 3 — critique #6: "dialect-fairness slice is the only defensible sliver" | 3 — doc03 §2: commercial vendors (Pindrop-class) exist; BB voice-auth factor UNVERIFIED | 4 — doc03 §8: per-dialect EER table IS the deliverable; biometric consent + local storage |
| 04 | Khata Lens | 4 — L3 lens: "khata is the real ledger of the economy"; doc04 §2: TallyKhata migration wall is real (typing 3–10 s/entry) | 4 — doc04 §5: NumtaDB floor 32% (chance 10%) proves digits non-trivial; CNN+GPU fine-tune is load-bearing | 4 — doc04 §2: positions against a VERIFIED 1M-MAU wall as migration tool; Track-05 fit | 3 — doc04 §5: data access PASS but only softmax on 400 imgs; real khata pages UNVERIFIED | 3 — doc04 §2: photo-first ingestion is the only thing TallyKhata "does NOT do"; LLM-vision reads clean pages ~80% | 4 — doc04 §4: on-device CNN, offline, connectable to upay APIs | 5 — doc04 §8: per-entry confidence, shopkeeper confirms every entry, held-out SHOPS, name blurring |
| 05 | Scam Census family | 5 — A3: 1-in-10 MFS users defrauded (PRI); A14: Tk 21,000 crore lost 2006–2021 | 4 — doc05 §5: SentNoB lexicon 0.20 acc vs majority 0.46, BLUGE gazetteer F1 0.00 → trained model genuinely load-bearing | 3 — critique #7: "upay already runs a fraud team; '60 scam texts' is not a dataset to them" | 4 — doc05 §7: 16h build, corpus near-certain from own phones, judge uploads own SMS reliably | 2 — partB §1: Google Messages + Truecaller verified free → per-message detection already-dominant; census is the sliver | 3 — doc05 §1: 50–100 items cannot support drift prediction; corpus grows only with users | 4 — doc05 §8: regex redaction protocol, held-out contributor, human blocklist approval |
| 06 | Dialect voice wallet | 4 — A9: literacy barrier; B10: "voice in dialect is the users' actual channel" | 5 — doc06 §4: Whisper fine-tune + slot parser + Confirm-Echo = hardest, deepest ML in the pool | 3 — critique #4: "menu-IVR gets most of the value"; hidden thesis 4: dialect speakers may not want voice payments | 2 — doc06 §5: zero-shot WER 7.48 — "transcripts are garbage"; fine-tune + generalization unproven on free-tier GPU | 4 — doc06 §2: UPI 123PAY exists (menu, Indian); free-speech BD-dialect payments: nothing found | 3 — doc06 §5: CPU 30–48 s/clip → GPU mandatory; feature-phone reach but heavy compute | 4 — doc06 §8: WER map = fairness artifact; echo + keypad PIN, voice never authenticates alone |
| 07 | Agent Scam Drill | 3 — A1/A7-adjacent: agents are the cash-out gateway; critique #5: "training agents is cost centre, not product" | 3 — doc07 §5: TTS-generation spike NOT RUN (protocol only); scoring circularity (critique §mechanism) | 2 — critique #5: upay sees training as cost centre; N≈20 pre/post is anecdote-scale (doc07 §7) | 3 — doc07 §7: human-actor fallback guarantees a demo; TTS realism ceiling (SLR37 is read speech, 1,891 utts/6 speakers) | 3 — doc07 §2: no Bangla voice scam-drill found; nearest = text quizzes (UNVERIFIED global) | 3 — doc07 §1: SLR37 read-speech, not conversational; scales to any MFS with same limits | 4 — doc07 §8: SIMULATED watermark, s.70(3) compliance, blind second rater, immediate debrief |
| 08 | Proof forensics | 4 — A13: Tk 58 crore stuck in e-commerce refunds; forged proofs ship goods (doc08 §1) | 3 — doc08 §5: ELA 6/6 separation but mock-rendered set; feature-based + small CNN, not deep | 4 — doc08 §2: VerifyTaka is device-bound SMS-relay; arbitrary-screenshot forgery detection gap is real | 3 — doc08 §7: demo works on features alone, no training needed; blind eval may miss 90/5 bar | 3 — doc08 §2: "nobody detects forged screenshots" — gap real but narrow; pixel/EXIF heuristic baseline ~70% | 3 — doc08 §7: arms race against evolving forger tools; per-provider format variance | 4 — doc08 §8: <5% FP threshold, verdict = "verify manually" never accusation, forger-modeler separation |
| 09 | Baki-Settle | 5 — A5 (VERIFIED, full read): Tk 387 min fee on Tk 30,000 cash-out, ~2m agents at risk; F3: kill the cash-out event | 2 — doc09 §7 risk 2: "judges may call it a rule"; ranking lift <5 pts = AI adds nothing (§6) | 5 — doc09 §1: deletes the fee event itself on a 1M-shop substrate; demand premise is the risk (critique thesis 3) | 3 — doc09 §5: tesseract 3/3 amounts but names degraded; handwritten pages UNVERIFIED; 20-customer trial unrun | 4 — doc09 §2: customer-facing baki-line settle flow "not evidenced" on TallyKhata or anywhere | 3 — doc09 §3: credit-adjacent regulatory optics; shops guard baki as lock-in (critique) | 4 — doc09 §8: settlement-only, no lending/deferral, shopkeeper confirms each line |
| 10 | Hotline triage | 3 — A9/A20-adjacent; doc10 §2: bKash 24/7 hotline + IVR exist; misrouting harms callers (§7) | 4 — doc10 §4: dialect ASR fine-tune + intent/urgency classifier; genuine research-grade ML | 3 — doc10 §2: ops savings real but bKash runs human-first support; 16123 proves phone demand (92,094 calls/yr) | 2 — doc10 §5: zero-shot WER 127.9% (tiny) / 123.1% (small) — "unusable"; fine-tune is a gamble | 3 — doc10 §2: dialect free-speech triage not found in BD; ASR is the whole moat | 3 — doc10 §4: hotline scale if ASR works; browser-mic only, no real telephony in demo | 4 — doc10 §8: per-dialect WER table, failed dialects route to humans, never auto-block |
| 11 | Hotline callback | 2 — doc11 §7 risk 1: "no documented BD hotline-callback fraud wave"; critique #9: fraudsters call out, not in | 4 — doc11 §4: liveness + speaker embed + anti-spoof + facts = multi-signal ML | 2 — doc11 §6: registered-number policy is a free incumbent; gate that fails both directions is worse (§6) | 1 — doc11 §5: "protocol only (no numeric result)"; ASVspoof not downloaded; no anti-spoof number exists | 3 — doc11 §2: nothing dialect-fair published; but no verified BD problem | 2 — doc11 §7: niche; problem prevalence UNVERIFIED | 4 — doc11 §8: three-signal verdict card, fail-open to human, biometric consent |
| 12 | Confusion + KYC | 4 — A9: literacy barrier; KYC drop-off = inclusion loss; doc12 §2: funnel reports alone are already-dominant tooling | 3 — doc12 §4: logistic/GBM on session features + live adaptation; modest but real | 4 — doc12 §5: KYC completion is direct revenue; 12h build; Track-02 fit | 4 — doc12 §5: 23.4x mock separation (n=2 scripted — "NOT evidence", file says so); P=0.70 highest of part C | 3 — doc12 §2: Hotjar/Contentsquare mature; claim must be per-person live adaptation, not the report | 4 — doc12 §3: plugs into any flow; free 200k-session tier verified; telemetry consent needed | 4 — doc12 §8: assist-only adaptation, per-segment AUC, rapid-tap adversarial test |

---

## 2. RISK-ADJUST

Weighted = Σ(score × weight), out of 5. Final = weighted × P(demo).

| Rank | Idea | Weighted | P(demo) | Final |
|---|---|---|---|---|
| 1 | 01 Puppeteer | 4.15 | 0.75 | **3.11** |
| 2 | 04 Khata Lens | 3.80 | 0.70 | **2.66** |
| 3 | 12 Confusion + KYC | 3.70 | 0.70 | **2.59** |
| 4 | 09 Baki-Settle | 3.75 | 0.65 | **2.44** |
| 5 | 05 Scam Census | 3.70 | 0.65 | **2.41** |
| 6 | 08 Proof forensics | 3.45 | 0.60 | 2.07 |
| 7 | 06 Dialect voice wallet | 3.60 | 0.45 | 1.62 |
| 8 | 03 Voice-clone guard | 2.90 | 0.55 | 1.60 |
| 9 | 07 Agent Scam Drill | 2.85 | 0.55 | 1.57 |
| 10 | 10 Hotline triage | 3.10 | 0.45 | 1.40 |
| 11 | 02 Kill-chain listener | 3.00 | 0.45 | 1.35 |
| 12 | 11 Hotline callback | 2.45 | 0.40 | 0.98 |

Note: Baki-Settle (09) ranks 4th despite AI-depth 2 — its business/problem scores carry it, and the files themselves warn the ranking model may be "a rule" (doc09 §7). It survives on the strength of the VERIFIED fee evidence (A5) and the 20-customer falsifier.

---

## 3. SENSITIVITY

(a) Prototype 25% / Innovation 5%, rest renormalized (÷1.05). (b) AI depth 30%, rest renormalized (÷1.10). Both multiplied by P(demo).

| Idea | Base rank | (a) Final | (a) Rank | (b) Final | (b) Rank |
|---|---|---|---|---|---|
| 01 Puppeteer | 1 | 3.11 | 1 | 3.10 | 1 |
| 04 Khata Lens | 2 | 2.63 | 2= | 2.67 | 2 |
| 12 Confusion + KYC | 3 | 2.63 | 2= | 2.55 | 3 |
| 05 Scam Census | 5 | 2.48 | 4 | 2.42 | 4 |
| 09 Baki-Settle | 4 | 2.38 | 5 | 2.33 | 5 |
| 08 Proof forensics | 6 | 2.06 | 6 | 2.05 | 6 |
| 06 Voice wallet | 7 | 1.54 | 8 | 1.68 | 7 |
| 03 Voice-clone guard | 8 | 1.55 | 7 | 1.65 | 8 |
| 07 Agent drill | 9 | 1.57 | 9 | 1.58 | 9 |
| 10 Hotline triage | 10 | 1.35 | 10 | 1.43 | 10 |
| 02 Kill-chain | 11 | 1.31 | 11 | 1.35 | 11 |
| 11 Callback | 12 | 0.91 | 12 | 1.04 | 12 |

**Robust top 5 under ALL THREE rankings: 01 Puppeteer, 04 Khata Lens, 12 Confusion+KYC, 05 Scam Census, 09 Baki-Settle.** (Order shuffles: 12 ties 04 under (a); 05 overtakes 09 under (a); no idea enters or leaves the top 5.) The whole voice/ASR lane (02, 06, 10, 11) never cracks the top 5 under any weighting — the measured WER evidence makes that lane a research gamble, not a hackathon build.

---

## 4. JUDGE PANEL (top 5 by risk-adjusted rank)

Judges: **R** = senior ML researcher, **B** = upay business executive, **D** = product designer, **S** = security/compliance officer, **F** = skeptical founder. Answers are strictly from the files; UNANSWERED = no file supports an answer.

### Idea 01 — Puppeteer

| Judge | Question | Best honest answer from files |
|---|---|---|
| R | Your n=2 spike is scripted connectivity. Why believe humans show the same separation? | We don't yet — doc01 §5: "n=2 scripted runs prove nothing about humans… UNVERIFIED until the 30–50 participant study runs." The falsifier is pre-registered: <65% recall at <10% FA ⇒ signal doesn't exist. |
| R | Isn't a dwell-threshold rule ~60% already? What does the model add? | doc01 §6: the model must beat the threshold "visibly on the same held-out people" or die; within-person features (each person their own control) are the mechanism the global rule lacks. Whether it beats 60% is UNANSWERED until data is collected. |
| R | Role-play coercion ≠ fear-driven coercion — is your label even valid? | doc01 §1: stated as limitation #1; the pitch reframes the output as "dictation/assistance detected" — dictation itself is the risk proxy — not "coercion detected." Real-fear equivalence: UNVERIFIED, probably false as a perfect proxy (critique §unchallenged). |
| B | Why would upay gate its own send flow on a student timing model? | doc01 §4: the demo never blocks — it triggers a guardian-confirm screen; business value is fraud-loss reduction on a flow upay already owns. Actual integration cost/decision: UNANSWERED (no file quantifies upay-side effort). |
| B | What's the market size? Who pays? | UNANSWERED — no feasibility file gives a fee/loss number for coerced sends specifically (A1 documents prevalence, not value at risk). |
| D | A scammer coaches the victim to type slowly. Now what? | doc01 §7 risk 4: pitch honestly — it "raises attacker cost (slow, unnatural calls), not a permanent defense"; combined with guardian-veto and name-display components. Detection of counter-coached typing: tested as a "counter-coached" condition (§8), result UNANSWERED. |
| D | Elderly users get false alarms constantly — how is that not worse than the scam risk? | doc01 §7 risk 3 + §8: per-person baseline, not global threshold; fairness slice by typing-speed quartiles with recall/FA reported per group. Whether FA stays acceptable for slow typists at n=30: UNANSWERED until measured. |
| S | What law lets an MFS slow a transaction on a behavioural score? | doc01 §3: "unclear whether an MFS provider may legally slow down or gate a send based on a behavioural score — UNVERIFIED, flag for judges' Q&A." Honest answer: nobody knows; the demo never auto-blocks, human decision only. |
| S | Keystroke timing is biometric-adjacent. Consent? Retention? | doc01 §1: written consent (EN+BN verbatim in file), no raw keystrokes stored post-study, audio deleted within 7 days, random participant IDs; PDPA 2026 s.5 consent + s.24 household exemption argued (UNVERIFIED against Act text). |
| F | Google/Truecaller already warn users. You're a feature. | doc01 §2: Google Messages covers SMS text, not live-call-coerced in-app sends; "in Bangladesh: no product found that models send-flow timing." The timing modality is also LLM-proof (no text input, §6). |
| F | 48h, 30–50 participants, coaching scripts — what slips first? | doc01 §4: collection is parallel to build; the pre-named failure is model ≈ baseline at weak n → pivot to "assistance detection" framing (§6). |

### Idea 04 — Khata Lens

| Judge | Question | Best honest answer from files |
|---|---|---|
| R | NumtaDB digits ≠ khata pages. What's your evidence the fine-tune gap closes? | None yet — doc04 §5: "Not tested (UNVERIFIED): real khata-page photos… line segmentation; name OCR." The 32% softmax floor proves difficulty, not solvability; CNN ≥90% on NumtaDB is H12 target. |
| R | Names are worse than digits — tesseract degraded মিয়া→মি (doc09 §5). How do you match contacts? | doc04 §4: fuzzy matching + human confirm step, "do not overclaim NER"; LLM-vision or bbocr for name lines with the trained digit CNN as the core model. Name accuracy on real khata: UNANSWERED. |
| R | Why not just use a vision LLM API? | doc04 §6: vision LLM reads clean pages ~80% (critique estimate, UNVERIFIED); the win claimed is messy pages + offline + per-entry confidence + cost. Beating GPT-4V-class on messy pages is UNPROVEN. |
| B | TallyKhata is free, Bangla, 1M+ MAU, with QR. Why does your product exist? | doc04 §2: TallyKhata has "no photo-of-paper-book ingestion — every entry is typed"; Khata Lens is strictly the migration tool ("start where your paper left off"). If photo flow doesn't beat typing 10 entries, "the product has no reason to exist." |
| B | What does upay get? Shops on TallyKhata, not upay. | UNANSWERED directly — the files position it as connectable to upay APIs (doc04 §4) and a Track-05 merchant-onboarding wedge, but no file shows why a TallyKhata shop would switch rails. |
| D | Shopkeeper photographs 5 pages, gets 85% accuracy — now they proofread everything. Value? | doc04 §6/§7: confidence triage means verification touches <30% of lines; below 90% entry accuracy "verification burden exceeds typing" — that's the pre-registered kill line. Current accuracy on real pages: UNANSWERED. |
| D | Lighting, faded ink, curved pages at a real shop? | doc04 §7: family books + friendly campus shops first; pre-shot pages on two devices as demo fallback; fairness slices include faded-ink age and photo quality. Real-shop condition performance: UNANSWERED. |
| S | The book lists third parties' debts. Do those customers consent? | doc04 §3: "UNVERIFIED — treat conservatively (blur everything, keep data local)"; shopkeeper consent covers the shopkeeper, NOT the customers written in the book — mitigation is blur/redact + delete post-hackathon. |
| S | An OCR misread creates a wrong debt record. Liability? | doc09 §3 (same OCR family): "mitigate: shopkeeper confirms each line before the QR is shown"; doc04 §8: shopkeeper confirms every entry; model never sends. Formal liability analysis: UNANSWERED. |
| F | Shops refuse — the khata is their customer lock-in. | doc04 §7 risk 3: mitigations are family books, blur commitments, and giving the shopkeeper the digital read-back as immediate value; critique §unchallenged notes digitizing baki "may weaken the lock-in that makes baki work" — stated, not solved. |
| F | NumtaDB licence is UNVERIFIED (doc04 §1). Red flag? | doc04 §1: "licence UNVERIFIED — no licence statement found on mirror/paper pages"; mirror works without auth (spike-proved). Must be resolved before pitching; UNANSWERED in files. |

### Idea 12 — Confusion + KYC

| Judge | Question | Best honest answer from files |
|---|---|---|
| R | Your model learns browser/trackpad artefacts, not struggle. | doc12 §5: the file itself says the 23.4x spike is "n=2, both scripted by the same author: a connectivity check, NOT evidence"; mitigation (§7): participants use their OWN phones, features restricted to timing/backtrack/idle. AUC ≥0.75 on held-out parents is the falsifier — unmeasured. |
| R | 20–30 sessions? That's a toy sample. | doc12 §7 risk 3: conceded — "simple features, regularized model, person-level held-out split, honest confidence intervals." No file claims statistical power; the pitch leads with the falsifier, not the AUC. |
| R | An LLM fed the event JSON probably matches you. | doc12 §6: "plausible, UNVERIFIED; must be beaten or absorbed" — no measurement exists yet; the pointless-if is AUC <0.65 ⇒ ship funnel report only, kill the AI claim. |
| B | Hotjar does this free. Why does upay care? | doc12 §2: session-replay is mature, "the funnel report alone is already-dominant tooling"; the claim is per-person LIVE adaptation + KYC-specific drop-off, "no published MFS KYC drop-off model found" (UNVERIFIED absence). |
| B | What's the revenue story? KYC completion worth what? | UNANSWERED — no file quantifies upay's KYC drop-off rate or completion value; Findex priors are context only (doc12 §1). |
| D | A help button popping up mid-task is annoying. | doc12 §7 risk 4: adaptation is "additive (help button appears), never removes function; threshold conservative." Whether trigger precision is good enough at n=25: UNANSWERED. |
| D | Different UI per demographic — dark pattern risk? | doc12 §3: assist-only commitment is explicit; "the same signal could be used to manipulate — commit to assist-only adaptation." No BD anti-discrimination statute found (UNVERIFIED). |
| S | Behavioural telemetry = personal data under PDPO 2025. | doc12 §3: consent + purpose limitation + minimization cited; logs local, random IDs, deleted post-event; no NID/selfie/OTP collected — mock only. Cross-border cloud storage: UNVERIFIED, keep local. |
| S | Rapid-tap spam to fake struggle or competence? | doc12 §8: adversarial manipulation "tested at H36" — a plan, not a result; UNANSWERED. |
| F | "We'll just watch session replays" — why does this survive? | doc12 §7 risk 5: "the pitch leads with the falsifier and the live judge-try moment, not the AUC." Whether judges buy tiny-sample UX models: UNANSWERED. |
| F | 12h build — what do you do with the other 36? | doc12 §4: sessions H6–18, model + live adaptation H6–30, held-out parents live at H18–30; slack absorbs the collection problem the idea actually has. |

### Idea 09 — Baki-Settle

| Judge | Question | Best honest answer from files |
|---|---|---|
| R | Remove the ranking model and the demo still works. Where's the AI? | doc09 §7 risk 2 concedes it: "judges may call it a rule"; the AI claim is per-line default-risk with reasons + measured lift vs newest-first baseline, pointless-if <5 pts lift (§6). Lift is unmeasured. |
| R | Default-risk labels are the shopkeeper's own 0/1 guess. | doc09 §1: "weak labels, say so on the slide" — the file pre-concedes label quality; no stronger ground truth exists in 48h. |
| R | OCR on handwriting is unproven — names degraded even on PRINT (doc09 §5). | doc09 §5: "handwritten-page accuracy UNVERIFIED"; mitigation is shopkeeper-confirms-every-line; amounts 3/3 on clean print only. |
| B | Customers with cash prefer cash. When does settle win? | doc09 §7 risk 1: the exact moment they'd rather owe is when they lack cash (critique mechanism); the 20-customer A/B at H18 with the ≥25% settle-rate falsifier is the pre-registered answer — unrun. |
| B | TallyKhata records dues and SMSes them already. Overlap? | doc09 §2: khata + QR + due-SMS "all exist"; the un-evidenced claim is ONLY the customer-facing per-line settle flow + ranking. Defensible sliver, stated plainly. |
| B | Why wouldn't this look like lending to Bangladesh Bank? | doc09 §3/§7: settlement-only framing, "no deferral, no interest, human confirm"; MFS Regs 2022 PDF found but unread (UNVERIFIED); must not create deposits or score for credit issuance. |
| D | Shop confirms every line — that's typing again, isn't it? | UNANSWERED — no file measures the confirm-flow time vs TallyKhata's 3–10 s/entry typing claim (doc04 §2). The verification-burden critique of Khata Lens applies here too. |
| D | Customer can't read the khata amount — trust? | doc09 §8: customer confirms the amount; QR shows the line. Display design for low-literacy confirm: UNANSWERED. |
| S | An inflated khata line becomes a fraudulent QR demand. | doc09 §8: "shopkeeper confirmation is the trust boundary"; OCR text sanitized before any LLM call; no real customer PII stored. Adversarial-shop scenario testing: planned H36 red-team, unrun. |
| S | Shops guard baki as lock-in — do they even want this? | critique §unchallenged: "digitizing it may weaken the lock-in that makes baki work" — acknowledged, not refuted anywhere; demand premise is the #1 falsifier. |
| F | 20 customers, one campus. Generalizable evidence? | UNANSWERED — the file's own falsifier is campus-scale (doc09 §4); no file claims more than a pilot. |
| F | Prothom Alo fee article is your whole problem case. One source? | doc09 §1: A5 is VERIFIED with full read (Tk 12.90–18.50/1000, Tk 387 min, ~2m agents, Bangla QR mandatory Jul 2026, MDR zero Oct 2026); A6 (cash settlement/liquidity as major MFS challenge) corroborates. Two sources, both read — stronger than most ideas' evidence, still thin on customer-side demand. |

### Idea 05 — Scam Census family

| Judge | Question | Best honest answer from files |
|---|---|---|
| R | 50–100 items. Drift prediction on that is astrology. | doc05 §7 risk 1: conceded — drift is "demo-only novelty on injected texts, labelled as such"; product = census exhibit + stage extraction; the ≥70% held-out cluster-placement falsifier is pre-registered. |
| R | Naive baselines at 0.20/0.00 just mean YOUR baselines were bad. Does the trained model beat GPT? | doc05 §6: the LLM prompt "will likely get ~70–80%"; the pointless-if is stage-F1/cluster-hit not exceeding the LLM on the same held-out items — "then the idea is pointless as an AI contribution and survives only as a data exhibit." Measured head-to-head: UNANSWERED. |
| R | SentNoB is social-media comments, not scam SMS. Transfer? | doc05 §1: "none of these are scam corpora… seed/transfer sources"; the scam corpus is self-collected. Transfer quality: UNANSWERED. |
| B | upay has a fraud team. Why do they need your 60 texts? | critique #7: "students collected 60 scam texts is not a dataset to them" — the honest answer is the pitch targets the RADAR/census layer (structured kill-chain extraction, campaign clustering) which the fraud team doesn't publish, not the raw corpus. upay-side interest: UNANSWERED. |
| B | Google Messages does on-device scam detection for free. | partB §1: VERIFIED, and the files accept it — "per-message scam detection is already-dominant; the census/forensics layers are the defensible slivers"; the census is BD-MFS-specific structure, not per-message verdicts. |
| D | Judge uploads a screenshot; OCR fails on a chat screenshot. | doc05 §7 risk 2: LLM-vision API fallback; text-only SMS path always works; OCR may be API-mocked if local fails (disclosed). Real-screenshot OCR success rate: UNANSWERED. |
| D | What does the weekly radar actually look like? | doc05 §4: timeline visualization item → stage → campaign; judge-tries flow is upload → stage + campaign placement. No mockup exists yet. |
| S | Contributor redaction fails once — someone's number leaks. | doc05 §7 risk 4: regex + manual review of EVERY item, masked-only display; PDPA 2026 consent protocol verbatim in file (§1). Residual risk stated, not eliminated. |
| S | Are scammer phone numbers personal data? Blocklist defamation? | doc05 §3: "we treat them as such and mask"; publishing a blocklist "has defamation exposure — check with legal, not guessed law"; demo shows masked numbers only, human analyst approves blocklist candidates. |
| F | Campaign clustering on 100 messages — why is this a company? | doc05 §7: pre-agreed fallback — "present as census + extraction tool, drop prediction claims"; the census dataset itself is the pitch's surviving asset. |
| F | Every team with relatives can collect scam texts. Where's the moat? | UNANSWERED — no file articulates a moat beyond being first to structure BD-MFS artefacts; IDEA_POOL notes the data edge is real but the criticism of low barriers is not addressed. |

---

## 5. DECIDE

### Primary, backup, combination

**PRIMARY: 01 Puppeteer.** Highest risk-adjusted score (3.11) and #1 under all three weightings. Pipeline proven (spike IKI 114.9 vs 1017 ms), no GPU/model risk, data collection cheap and controllable, falsifier pre-registered, Responsible-AI story is the strongest in the pool (doc01 §8), and the modality is LLM-baseline-proof (doc01 §6).

**BACKUP: 12 Confusion detector + KYC drop-off.** Shares the most code with Puppeteer, explicitly: (1) the instrumented mock-flow web shell with a client-side event logger (doc01 §4 keystroke logger ≈ doc12 §1 event-logging schema); (2) timing/dwell/idle/backtrack feature extraction; (3) person-level held-out split + scikit-learn model; (4) the risk-banner / human-confirm UX; (5) the same consent apparatus and participant-recruitment pipeline. One mock upay app serves both: send flow (Puppeteer) and KYC flow (confusion).

**COMBINATION: yes — genuinely coherent.** The combined demo is one Bangla mock upay app logging every interaction event to one pipeline: a judge first completes a mock KYC onboarding where a struggle-risk score rises live and a simplified screen/help hint fires when they dawdle at the OTP step (idea 12's head), then performs one self-directed send and one send while a teammate coaches them over a phone — the dictation-risk head fires a guardian-confirm banner with top feature reasons ("5 pauses >2s at PIN entry, confirm dwell 3× your usual") (idea 01's head). One data-collection session per participant feeds both heads (KYC attempt + coached/self sends ≈ 12 minutes); one feature store, two model outputs, one "the model is the product" story spanning Track 01 + Track 02. Both heads inherit the same person-level held-out evaluation and the same falsifier slide.

### Day-one decision tree (spike checkpoints + switch rules)

- **H2 — Collection start gate:** ≥10 participants consented and scheduled for the combined flow. If <10 by H2, redeploy all 3 members to recruiting; the combined design means ONE participant serves both models.
- **H6 — Pilot signal gate (Puppeteer head):** run the first 8 participants. If median coached-session mean-IKI is not ≥2× their own self-directed baseline (spike showed ~9×; require ≥2× on humans), the human signal is suspect → demote Puppeteer to secondary; confusion head becomes primary.
- **H6 — Dialect lane gate (not our lane, but pre-committed):** if the Ben-10 fine-tune WER at hour 6 is >1.5 on held-out valid clips, abandon ALL voice ideas permanently for this event (they are already ranked 7–12).
- **H12 — Khata side-bet gate:** only if someone is free: digit CNN ≥90% on NumtaDB test AND ≥8 khata pages photographed. Miss either → drop Khata Lens entirely, keep its contact-matching/overdue-ranking OUT of scope.
- **H18 — Held-out gate (Puppeteer):** person-level held-out recall ≥65% at <10% FA (critique falsifier). Pass → Puppeteer primary for pitch. Fail → pivot primary to confusion head (AUC gate below); Puppeteer demo stays as "dictation detector" with honest baseline comparison.
- **H24 — Held-out gate (Confusion):** drop-off/struggle AUC on held-out parents ≥0.75 → full AI claim. 0.65–0.75 → ship with the funnel report as the headline and the model as assist-trigger only. <0.65 → kill the AI claim, ship assist-trigger as heuristic + funnel report; the demo moment (judge's own live risk score) survives regardless.
- **H30 — Baseline-beating gate:** the trained models must visibly beat the dwell-threshold rule (Puppeteer) and the "older users struggle more" prior (confusion) on the same held-out people, per doc01 §6 and doc12 §6 pointless-if numbers. If not, pitch leads with the honest negative result — judges were told in critique that a named kill condition earns respect (critique §revision_directions).
- **H36 — Feature freeze, both heads.** H40 red-team (rapid-tap spam; counter-coached typing). H44 demo rehearsal + fallback video. H48 pitch.

### First 8 hours — data-collection schedule (all times from build start; 3 members A/B/C)

| Hours | Who | What | Where | How many | Consent |
|---|---|---|---|---|---|
| H0–1 | B | Print/queue digital consent forms (verbatim EN+BN wordings from doc01 §1 and doc12 §1), 2 recruitment desks at campus | Campus common areas | — | Forms ready at door |
| H0–1 | A | Stand up combined mock app: send flow + KYC flow + event logger (spike 01 + spike 12 schemas) | Laptop | — | — |
| H1–4 | A+B+C (one per desk, rotating) | Combined sessions: KYC mock on participant's OWN phone, then 2 self-directed sends + 1 coached send (teammate phones the participant with a scam script) | Campus desks | 20 participants (~80 logged flows, ~5–6 min KYC + 3×2 min sends each) | Signed at door BEFORE any logging; role-play framed as role-play |
| H1–4 | C (parallel) | Census side-collection for pitch material: teammates/relatives forward real scam SMS to collection form | Own phones | 30–50 items | doc05 §1 consent wording |
| H4–6 | B | Label, redact, backfill: recruit 10 more participants + ≥8 parents/relatives 45+ (phone-recruited for H6–18 slots, own devices) | Campus + phone | +10 students, ≥8 parents | Same forms |
| H6–8 | A+C | Feature extraction + first model on H1–4 logs; person-level split decided NOW (≥8 people reserved as never-seen) | Laptops | — | — |

Running totals by H8: ~30 participants, ~120 flows, ≥8 parents scheduled, ~40 scam texts. Collection continues in parallel with model work per doc01 §4 / doc12 §4; audio of coaching calls deleted after label verification (doc01 §1).

### Most memorable on paper, rejected as primary

**07 Agent Scam Drill.** The demo moment — a judge takes a LIVE simulated scam call and gets scored on their own vulnerability — is the single most memorable beat in the pool, and nobody else will have it. Rejected because the files convict it three ways: the scoring labels are team-invented, "the grader is the injection point" (critique §mechanism_problems); the TTS spike was never run ("protocol only," doc07 §5) and SLR37 is read news-speech, not phone-call menace (doc07 §1); and the only efficacy metric (pre/post susceptibility delta) is anecdote-scale at N≈20 (doc07 §7). It is a training product upay itself files under cost centre (critique #5). Memorable theatre on top of unverifiable measurement loses to a falsifiable signal. If the primary runs long, a 60-second drill cameo in the pitch is free theatre without the scoring claim.

### Blunt honesty

The thinnest evidence in this decision is the thing we're betting on: **the Puppeteer human signal rests on n=2 scripted keystroke runs, and nobody — including the feasibility author — believes role-play coercion mimics fear-driven coercion** (doc01 §1 calls it limitation #1; critique calls it "probably false as a perfect proxy"). Second thinnest: the combined plan's confusion head has one 23.4x number the file itself labels "NOT evidence," and every "held-out parents" claim depends on recruiting 45+ relatives who may never show. We are really betting that cheap, controllable, consented data collection is worth more than deep-but-unprovable ML — that a demoable falsifiable behavioural model beats a heroic dialect-ASR fine-tune (WER 7.48 and 127.9% say the voice lane is a research paper, not a hackathon demo). The single most likely reason this decision is wrong: the coached-vs-self timing signal collapses at n=30 (calm students mimic dictation, person variance swamps condition variance), the H18 falsifier fires, and the team pivots to a confusion detector whose AUC lands at 0.66 — technically alive, judged as a Hotjar clone with extra steps.
