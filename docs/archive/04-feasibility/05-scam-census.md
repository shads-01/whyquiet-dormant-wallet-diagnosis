# 05-scam-census.md — Feasibility: Scam Census family (kill-chain reader + number clusters + grammar drift)

Written 2026-10-02 by the feasibility researcher. Inputs: docs/CONTEXT.md, docs/IDEA_POOL.md, docs/03-critique/02-critique.md (survivor #7), docs/01-data/inventory.md, docs/02-ideas/01-candidates.md (D1, D2, D24, D47). Not legal advice.

**One-line problem statement:** For MFS users and upay's fraud team, scam tactics evolve faster than blocklists, causing repeated victimization by recycled scripts. We build a scam-census pipeline that uses a self-collected corpus of real scam SMS/screenshots/call stories to extract kill-chain stage + entities, cluster campaigns, and flag grammar drift, with success measured by stage-extraction F1 and held-out campaign-membership hit rate.

## 1. DATA REALITY

### Public datasets (each page opened 2026-10-02)

| Dataset | URL | Size | Language | Licence | Hackathon use OK? | Download friction | Status |
|---|---|---|---|---|---|---|---|
| SentNoB | https://huggingface.co/datasets/khondoker/SentNoB | 15,728 rows / 3.34 MB (train only on HF) | bn (social-media comments) | CC-BY-ND-4.0 (no derivatives — share verbatim, no modified redistribution) | Yes for training/eval inside prototype; do not publish a modified dataset | Direct HF download; verified via datasets-server rows API | VERIFIED |
| BanFakeNews-2.0 | https://huggingface.co/datasets/hrshihab/BanFakeNews-2.0 | 61,581 rows / 305 MB; columns: Headline, Content, Label | bn (news) | Apache-2.0 | Yes | Direct HF download | VERIFIED |
| BLUGE-bengali-ner (S19) | https://huggingface.co/datasets/nahid-hub/BLUGE-bengali-ner | 14,476 rows (train 11,580 / val 1,447 / test 1,449) / 854 kB; 9 IOB tags: PER/ORG/LOC/OBJ | bn (news/wiki text) | CC-BY-4.0 | Yes | Direct HF download or parquet | VERIFIED |

Caveat: none of these are scam corpora. They are seed/transfer sources for noisy-Bangla text understanding. The scam corpus itself is self-collected (below) — nothing public covers Bangladeshi MFS scam messages (inventory A3/A4; UNVERIFIED that no private BD corpus exists, but none is publicly listed).

### Self-collected scam census (the core asset)

- **Target size:** 50–100 real items minimum (CONTEXT/critique falsifier scale): ~40 SMS texts, ~20 chat screenshots, ~10 call-story transcripts. Realistic in 48h from 3 students' own phones + relatives.
- **Protocol:** (1) each contributor forwards/screenshots scam items from their own phone to a team collection form; (2) contributor signs consent (below); (3) team redacts before anything enters the dataset; (4) one contributor's items held out entirely as the test set (critique falsifier: ≥70% of held-out items must place into prior clusters or prediction claims die).
- **Consent wording (use verbatim):**
  - EN: "I voluntarily share scam messages/screenshots/call stories from my own phone for a university hackathon research prototype. I understand the team will remove phone numbers, names and account details before use, will not publish my identity, and I can ask to withdraw my items any time before the demo. Signature: ____ Date: ____"
  - BN: "আমি স্বেচ্ছায় আমার নিজ ফোনের প্রতারণামূলক বার্তা/স্ক্রিনশট/কলের বিবরণ একটি বিশ্ববিদ্যালয় হ্যাকাথন প্রোটোটাইপের গবেষণার জন্য শেয়ার করছি। টিম ব্যবহারের আগে ফোন নম্বর, নাম ও অ্যাকাউন্টের তথ্য মুছে ফেলবে, আমার পরিচয় প্রকাশ করবে না, এবং ডেমোর আগে আমি যেকোনো সময় আমার তথ্য প্রত্যাহার করতে পারব। স্বাক্ষর: ____ তারিখ: ____"
- **Redaction steps:** regex phone numbers (01[3-9]\d{8} and +880 variants) → `01XXXXXXXXX`; names → role labels ("caller claimed bKash officer"); amounts kept (they are the signal); TrxIDs → first 3 chars + mask; screenshots: crop or black-box over contact names/numbers before OCR.
- **Who collects / hours:** all 3 people, first 6 hours (CONTEXT rule); ~2–3 h total including consent forms and redaction.

## 2. PRECEDENT

| Product | URL | What it does | What it does NOT do |
|---|---|---|---|
| Google Messages scam detection | https://blog.google/products-and-platforms/platforms/android/new-android-features-march-2025/ (opened 2026-10-02) | On-device AI flags conversational scam patterns in SMS, real-time warning, block/report (since Mar 2025) | English/conversational-pattern focused; no BD-MFS corpus, no kill-chain stage extraction, no campaign clustering, no public BD radar |
| Truecaller Scam Checker | https://www.truecaller.com/scam-checker (opened 2026-10-02) | Free lookup of phone numbers/URLs against global scam database + community posts | Crowdsourced number reputation only; no Bangla message-structure model, no stage/tactic extraction |
| ScamCheck.gov.bd | https://scamcheck.gov.bd/common-scams-in-bangladesh/ (cited in candidates A2; page not opened today) | Government catalog of common BD scams | Static list, no model, no live census | UNVERIFIED (not opened today) |

**Plainly:** per-message scam *detection* already exists (Google Messages, Truecaller). What does not exist publicly is a **Bangla MFS-specific structured census**: kill-chain stage extraction, campaign clustering, number-cluster prediction, grammar-drift tracking on real BD scam artefacts. The census/radar layer is the defensible sliver; a standalone "is this SMS a scam" classifier is already-dominant (critique D1 kill).

## 3. LEGAL/ETHICS (not legal advice)

- **Recording/participation:** no Bangladeshi statute requires all-party consent for a participant recording their own conversation; s.71 Telecommunication Act 2001 (as substituted 2026) punishes eavesdropping on *other people's* conversations (up to 2 yrs / Tk 1.5 crore). Source: https://www.recordinglaw.com/world-laws/world-recording-laws/bangladesh-recording-laws/ (opened 2026-10-02; cites bdlaws.minlaw.gov.bd primary texts). For this idea we mostly handle *text/screenshots*, not recordings — lower risk.
- **Personal Data Protection Act 2026 (Act No. 63 of 2026):** screenshots/messages containing identifiable people are personal data; consent must be voluntary, specific, clear, withdrawable (s.5); personal/household-use exemption (s.24) covers contributors' own items but NOT our processing/publication; voiceprints and facial images are biometric data; cross-border transfer rules s.29; fines up to Tk 25–50 lakh (enforcement provisions deferred ~18 months). Same source as above.
- **Publication risk:** publishing a blocklist naming numbers/persons has defamation exposure (critique #7) — demo should show masked numbers only. Cyber Security Act 2026 s.25 covers harmful publication; not directly applicable to redacted research use, but keep everything masked. Same source.
- **Unclear:** whether a student team counts as a "data fiduciary" under PDPA 2026; whether scammer phone numbers themselves are personal data (we treat them as such and mask). State both as open questions in the pitch.

## 4. 48-HOUR BUILD PLAN

Stack: Python, HF datasets, transformers (Bangla OCR: easyocr or Tesseract ben — UNVERIFIED which installs cleanly on Windows; fallback: LLM-vision API for OCR only), scikit-learn/HDBSCAN for clustering, sentence-transformers (already installed) for embeddings. Compute: CPU + one free-tier GPU for fine-tune.

| Hours | Person A (data lead) | Person B (model lead) | Person C (app/demo lead) |
|---|---|---|---|
| 0–6 | Consent forms + collect 50–100 items from own phones/relatives; redact as they arrive | Download SentNoB/BLUGE; fine-tune Bangla NER (BLUGE) for PER/ORG/LOC on scam-style text | Streamlit app skeleton: upload screenshot/text → pipeline |
| 6–12 | Label 60 items with kill-chain stage (hook/authority/urgency/ask) — 2 annotators, measure agreement | OCR on screenshots → text; stage classifier v1 (fine-tuned BanglaBERT-class model or logistic on embeddings) | Upload UI + redaction display |
| 12–24 | Label campaign clusters (same script family?) for ground truth | Embeddings + clustering (HDBSCAN); number-cluster features (prefix, report count) | Timeline visualization: item → stage → campaign |
| 24–36 | Hold out contributor X's items; run falsifier eval | Drift tracker: embedding-novelty score; **FEATURE FREEZE h36** | Polish demo script, judge-tries-it flow |
| 36–48 | Pitch data story | Falsifier numbers on slides | Demo rehearsal, fallback canned inputs |

Real vs mocked: corpus real; OCR may be API-mocked if local OCR fails; clustering/stage model real.

## 5. SPIKE TEST — RUN, real numbers

Script: `spikes/05-scam-census/spike_sentnob_bluge.py`; results: `spikes/05-scam-census/results.json`. Environment: Python 3.14.6, datasets-server rows API (no full download needed).

- SentNoB: 100 rows fetched live from HF; 3 example rows printed (bn comments, labels 0/1/2). Label distribution in slice: {1: 46, 2: 31, 0: 23}.
- **SentNoB zero-shot lexicon baseline (20-row slice): accuracy 0.20 (4/20)** — worse than majority class 0.46. Real number. Interpretation: naive keyword sentiment fails on noisy Bangla; a trained model is genuinely needed → the fine-tune is load-bearing, not a rule in disguise.
- BLUGE-NER: 20 test rows fetched live; 3 examples printed (IOB tags verified: 1/2=PER, 3/4=ORG, 5/6=LOC).
- **BLUGE-NER gazetteer LOC baseline (20-row test slice): P=0.00, R=0.00, F1=0.00 (tp=0, fp=0, fn=18)** — real number. A hand gazetteer catches nothing; learned NER is required for entity extraction in the kill-chain reader.

PASS/FAIL: **PASS (data reachable, baselines measured)** — but the baselines being near-zero means the 48h model must actually train; there is no free win here.

## 6. BASELINE

- Simplest baseline: keyword/lexicon scam flagger + manual clustering in a spreadsheet. Measured lexicon performance on adjacent noisy-Bangla text: 0.20 acc (spike above) — a trained classifier must beat 0.46 majority-class on any labelled slice.
- LLM-API baseline: GPT-class model prompted "extract stage + entities from this scam message" will likely get ~70–80% of the value (critique #7: "LLM clusters scam texts well"). **Pointless-if number:** if our trained pipeline's stage-F1 and cluster-hit-rate do not exceed the LLM prompt's on the same held-out items, the idea is pointless as an AI contribution and survives only as a data exhibit.

## 7. RISKS

1. **Corpus too small for drift prediction** (critique #7): 50–100 items cannot support "grammar drift tracking" as more than anecdote. Mitigation: make the census exhibit + stage extraction the product; drift = demo-only novelty score on injected texts, labelled as such.
2. **OCR on real screenshots fails** (mixed Bangla/English, screenshots of chats). Mitigation: LLM-vision API fallback; text-only SMS path always works.
3. **LLM-API baseline beats our model** (see §6). Mitigation: measure both on the same held-out set and show the delta honestly; if negative, pivot the pitch to the census dataset itself.
4. **Redaction failure leaks a contributor's contact.** Mitigation: regex + manual review of every item; masked-only display in demo.
5. **Held-out falsifier fails** (<70% cluster placement). Mitigation: pre-agreed fallback — present as "census + extraction tool", drop prediction claims.

**P(working live demo) = 0.65.** Reasoning: data collection is near-certain (own phones), stage-classifier on ~60 labelled items will train to something usable, clustering demos well; main failure modes are OCR quality and the LLM-baseline comparison looking bad. The demo moment (judge uploads their own scam SMS → stage + campaign placement) is reliable because judges' phones contain real scam texts.

## 8. RESPONSIBLE AI

- **Fairness groups:** contributor dialect/region (Sylheti vs standard Bangla phrasing), sender-type (SMS vs Messenger vs WhatsApp). Check stage-F1 per source type; report the slice table.
- **Explainability output:** each verdict shows extracted entities + matched campaign exemplars ("flagged because: urgency phrase X, number prefix Y seen in campaign Z") — traceable, not a bare score.
- **Security:** adversarial users can poison the census with fake reports (mitigation: contributor identity + rate limits); prompt injection if an LLM reads scam text (mitigation: scam text is data, never instructions; structured extraction only); data leakage: held-out contributor enforced at split time, not random row split.
- **Human oversight:** blocklist candidates go to a human fraud analyst; no automatic blocking/publishing. Numbers are masked everywhere; no autonomous action on any account.
