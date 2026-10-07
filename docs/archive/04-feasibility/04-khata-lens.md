# 04-khata-lens.md — Feasibility: Khata Lens

Photograph paper credit books (khata/baki) → read Bangla handwriting (digits via NumtaDB-seeded model, names, dates) → match names to contacts → rank overdue → upay payment requests. Track 05. Status: DATA FEASIBLE, COMPETITOR WALL IS THE STORY.

## 1. DATA REALITY

**Public datasets (verified 2026-10-02):**

| Dataset | URL | Size | Language | Licence | Hackathon use | Friction |
|---|---|---|---|---|---|---|
| NumtaDB | paper: https://arxiv.org/abs/1806.02452 (85,000+ images, stated in abstract); mirror: https://github.com/Siamul/NumtaDB (training-a CSV: 19,702 rows, verified); Kaggle: https://www.kaggle.com/datasets/BengaliAI/numta | ~85k images | bn digits | **UNVERIFIED** — no licence statement found on mirror/paper pages fetched; Kaggle page requires login | Yes (digit pretraining) | GitHub mirror works without auth (spike-proved); Kaggle needs account; bengali.ai/datasets page is a thin index (buttons to Kaggle/HF, no licence text) |
| Bengali.AI grapheme (CV19) | https://github.com/BengaliAI/graphemePrepare | ~200k graphemes (Kaggle) | bn | MIT (repo, per inventory) | Yes (grapheme side) | Kaggle account |
| BADLAD (layout) | https://github.com/BengaliAI/BADLAD | UNVERIFIED | bn | repo, not read | Layout prior | GitHub |

**Self-collected: real khata pages — the actual product data.**
- Sample size: 10–15 shops/family credit books; 5–15 pages each; target 80–150 photographed pages, ≈1,000–3,000 line entries. Digitise (transcribe) a subset: ≥300 entries for fine-tuning/eval, 100 held-out entries from shops NOT photographed for training.
- Protocol: photograph with phone (flat light, ruler for scale); transcribe ground truth in a spreadsheet (name, item, amount, date, due-mark); shopkeeper reviews the digital read-back for 2 pages (this doubles as the demo's human-oversight moment).
- Consent wording:
  - English: "I agree to let the team photograph my credit book for a handwriting-reading research prototype. Customer names will be blurred in any public material, photos stay on the team's devices, are never published, and will be deleted after the hackathon. I can withdraw at any time."
  - Bangla: "আমি হাতের-লেখা পড়ার গবেষণার জন্য আমার খাতার ছবি তুলতে সম্মত। ক্রেতার নাম প্রকাশ্য সামগ্রীতে অস্পষ্ট করা হবে, ছবি শুধু দলের ডিভাইসে থাকবে, কখনো প্রকাশ করা হবে না, হ্যাকাথন শেষে মুছে ফেলা হবে। আমি যেকোনো সময় প্রত্যাহার করতে পারব।"
- Redaction: blur customer names/numbers in any screenshot used in slides; shopkeeper names anonymised in the deck.
- Who collects / hours: all 3 members, 4–6 h (campus shops + family books; collection starts H2 per CONTEXT.md).

## 2. PRECEDENT — the competitor reality check (required)

- **TallyKhata (Progoti Systems Ltd) — VERIFIED today** (https://www.tallykhata.com/million-shopkeepers-using-tallykhata-app-for-records-and-payments/): launched 2020; **more than 1 million monthly active users**; Bangla UI; Pelam/Dilam entries in 3–10 seconds; free shop QR under Bangladesh Bank's Bangla QR; eKYC wallets; BB Payment Service Provider licence; explicitly building credit scoring + bank partnerships on "the largest active database of Bangladeshi shopkeepers". It is free, offline-capable, and rural-skewed.
- **Hishabee**: the critique lists it as an existing competitor, but https://www.hishabee.business/ returned HTTP 525 (unreachable) today and https://www.hishabee.com/ now serves a DIFFERENT product (ZamZamIT's AI ERP for larger businesses). The shopkeeper-app Hishabee's current status: **UNVERIFIED** — verify before naming it in the pitch.
- **What TallyKhata does NOT do (from its own feature pages):** it has no photo-of-paper-book ingestion — every entry is typed by the shopkeeper. The migration cost from an EXISTING paper khata (often years of entries) is the adoption wall TallyKhata itself lives with.
- **Plain statement:** digital khata already exists in Bangladesh at 1M-user scale, free, in Bangla, with payments attached. Khata Lens is NOT "digital khata" — it can only be the **migration tool**: "photograph your existing book, we read it, you start where your paper left off." If that photo-first differentiator does not beat typing 10 entries manually, the product has no reason to exist next to TallyKhata.

## 3. LEGAL/ETHICS (not legal advice)

- Personal Data Protection Act 2026 (Act No. 63 of 2026): khata photos contain third-party customer names — processing needs a lawful basis (shopkeeper consent covers the shopkeeper, NOT the customers written in the book). Mitigation: blur/redact customer identifiers before storage beyond the demo; delete photos post-hackathon. Source: https://www.recordinglaw.com/world-laws/world-recording-laws/bangladesh-recording-laws/ (secondary — UNVERIFIED against Act text).
- Bangladesh Bank class: sending payment requests to customers touches MFS transaction-messaging rules; our demo sends nothing real (mock requests). BB MFS guidance circular not opened today: UNVERIFIED — check https://www.bb.org.bd.
- TallyKhata operates under a BB Payment Service Provider licence (stated on their page) — a student prototype must not imply it is a licensed payment instrument; frame as a reading/assist layer that could connect to upay APIs.
- Unclear: whether photographing a book that contains third parties' debt records and processing names requires those customers' consent. UNVERIFIED — treat conservatively (blur everything, keep data local).
- Not legal advice.

## 4. 48-HOUR BUILD PLAN

Stack: Python; digit model = small CNN fine-tuned from NumtaDB (free-tier GPU, ~1–2 h train); name/date lines = off-the-shelf Bangla OCR (bbocr, BSD-3, https://github.com/BengaliAI/bbocr) or a vision-LLM API for the demo with the trained digit model as the "our model" core; matching = fuzzy string + contact list; overdue ranking = rules over parsed dates (business rules separate from ML, per CONTEXT.md architecture rule).

- H0–2: A starts NumtaDB download + CNN training script (spike 04 is the seed). B + C hit campus shops/family with consent forms; photograph first books.
- H2–10: continue collection (target 10 shops by H10). A trains digit CNN on NumtaDB (target ≥90% on NumtaDB test). C builds page pipeline: photo → line segmentation (simple projection/contour) → per-cell digit model.
- H10–24: C fine-tunes/calibrates on real khata digits (the fine-tune gap IS the project — NumtaDB digits alone are not khata pages, per critique). A builds name-line OCR + contact matching + overdue ranking. B builds the demo app: phone camera → annotated digital khata → "send upay request" mock → overdue list.
- H24–36: measure entry-level accuracy on held-out shops (falsifier: ≥90% with per-entry confidence, else verification burden exceeds typing). Add confidence triage (D12 component: only low-confidence lines need human check). FEATURE FREEZE H36.
- H36–48: demo freeze + pitch: judge photographs a page live (pre-shot fallback pages ready), sees entries read with confidence, taps "send request". Comparison slide: TallyKhata typing flow vs photo flow, with the honest migration story.
- Real vs mocked: OCR/matching/ranking real on real photographed books; payment request mocked; contact matching against a mock contact list (no real customer PII).

## 5. SPIKE TEST

Ran: `spikes/04-khata-lens/spike_numta.py` (see RESULT.md).
- Downloaded NumtaDB training-a CSV (19,702 rows) + 550 images from the GitHub mirror without auth; trained softmax regression on 16×16 pixels.
- **Result: held-out digit accuracy 0.320 (chance 0.10), train <1 s, download 317 s for 550 images.**
- PASS (data access): NumtaDB is downloadable and trainable in this environment today, no Kaggle auth needed via the mirror.
- FAIL (model capacity): 32% is a floor from a linear model on 400 samples — confirms a real CNN + GPU is required for the ≥90% bar; also confirms Bengali digits are genuinely non-trivial (good for the AI-depth story, bad for the 48h clock).
- Not tested (UNVERIFIED): real khata-page photos (none collected in this research pass); line segmentation; name OCR. Protocol: photograph 5 pages, run segmentation + digit model, measure entry-level accuracy.

## 6. BASELINE

- Non-AI baseline: shopkeeper types entries into TallyKhata (free) — 3–10 s per entry (TallyKhata's own claim). Our tool must save net time: read ≥90% of entries correctly with confidence flags so verification touches <30% of lines.
- LLM-API baseline: a vision LLM (GPT-4V-class) reads clean khata pages ~80% per the critique — our win must be on MESSY pages + offline + per-entry confidence + cost (on-device CNN vs per-photo API fees).
- Pointless-if number: if entry-level accuracy on real khata pages is <90% with per-entry confidence, the shopkeeper corrects more than they'd type — the idea is pointless next to free TallyKhata.

## 7. RISKS

1. **The fine-tune gap** (NumtaDB digits ≠ khata graphemes+layout+arithmetic marks): mitigation: collect real pages from H2, fine-tune by H24, confidence-triage the rest. This is the project's make-or-break.
2. **TallyKhata wall**: 1M users, free, Bangla, payments included (VERIFIED). Mitigation: position strictly as the migration/onboarding layer ("bring your paper book"), not a khata app; the pitch must name TallyKhata before a judge does.
3. **Shops refuse photography** (khata = customer lock-in; privacy of debtors): mitigation: family books + friendly campus shops first; blur commitments; offer the shopkeeper the digital read-back as immediate value.
4. **Name matching across Bangla/English spellings**: mitigation: fuzzy matching + human confirm step; do not overclaim NER.
5. **Demo-day lighting/handwriting variance**: mitigation: pre-shot pages on two devices; confidence-triage makes partial reads look honest rather than broken.

**P(working live demo) = 0.70.** Reasoning: data access proven by spike; digit CNN on GPU is low-risk; the deductions are for the untested fine-tune gap on real khata pages (the critique's falsifier) and shop-collection friction. Even at 80–85% entry accuracy, the confidence-triage demo still works — it just weakens the headline number.

## 8. RESPONSIBLE AI

- Fairness groups: handwriting styles (neat vs rushed), age of book (faded ink), photo quality, Bangla-only vs mixed Bangla/English entries. Report entry accuracy per slice (critique's D27 fairness audit folds in here).
- Explainability: per-entry confidence + highlighted image region for every read value; low-confidence lines visibly queued for human check — the human-oversight point is built into the product flow.
- Security: adversarial inputs (a page designed to make the OCR misread an amount — test one); data leakage (held-out SHOPS, not just held-out pages); photos stored locally, customer names blurred in all outputs; no autonomous sending — every payment request is shopkeeper-tapped.
- Transparency: separate the ML predictions (OCR values + confidence), business rules (overdue ranking), and any generated text (request message draft) in the UI, per CONTEXT.md architecture rules.
- Human oversight: shopkeeper confirms every entry before any request is sent; the model never sends anything.
