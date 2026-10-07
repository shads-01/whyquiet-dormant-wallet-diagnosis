# 09-baki-settle.md — Feasibility: Baki-Settle (2026-10-02)

**Idea (D10, critique survivor #3):** customer pays a shop's recorded baki (credit) line directly by QR, deleting the cash-out event. Khata pages (S5) + BLUGE NER (S19) + OSM (S12); model ranks which baki lines to surface + default risk per line. Track 03/05.

**Problem evidence (VERIFIED, full article read):** merchants now illegally offer cash-out via Bangla QR; cash-out fee is Tk 12.90–18.50 per Tk 1,000; Tk 387 minimum fee on a Tk 30,000 cash-out; ~2m agents at risk; Bangla QR mandatory since July 2026, merchant MDR/IRF zero from October 2026 — https://en.prothomalo.com/business/local/8mljzomg86 (15 Sep 2026).

## 1. DATA REALITY

| Source | URL | Size | Language | Licence | Hackathon use | Download friction | Status |
|---|---|---|---|---|---|---|---|
| Self-collected khata pages | n/a | ~5–10 shops, 2–5 pages each | bn (handwritten) | own (consent) | yes — core data | shopkeeper permission; photograph, blur names | planned |
| BLUGE-bengali-ner | https://huggingface.co/datasets/nahid-hub/BLUGE-bengali-ner | 14,476 rows (11,580/1,447/1,449), 854 kB | bn | CC-BY-4.0 | yes | direct download / parquet | VERIFIED (page opened; sample rows read) |
| OSM Bangladesh (Geofabrik) | https://download.geofabrik.de/asia/bangladesh.html | 339 MB .osm.pbf | en/bn | ODbL 1.0 | yes | direct download; only a Dhaka sub-extract needed | VERIFIED (inventory; page not re-opened today — UNVERIFIED today) |
| NumtaDB digits (optional pretrain) | https://bengali.ai/datasets/ | ~85k images (size UNVERIFIED) | bn digits | MIT on repo; DB licence not stated | yes, baseline only | Kaggle/HF | VERIFIED (inventory) |
| WFP/HDX food prices (context only) | https://data.humdata.org/dataset/wfp-food-prices-for-bangladesh | 4.5 MB CSV (downloaded today) | en | CC BY-IGO | yes | direct | VERIFIED (downloaded, header + 1900 row read) |

**Self-collection protocol (khata pages):** 5–10 campus/family shops; photograph 2–5 pages each with the shopkeeper present; written consent (Bangla: "আমি আমার খাতার ছবি তুলে দিচ্ছি শুধু গবেষণার জন্য। নাম ও নম্বর ঝাপসা করা হবে, কোনো টাকা লেনদেন হবে না।" / English: "I consent to my credit-book pages being photographed for a student research prototype only. Names and numbers will be blurred. No money will be moved."); redact customer names/numbers before any demo; collectors: 3 team members, ~2–3 h total. **Default-risk labels:** only the shopkeeper's own 0/1 "does this customer usually pay late" judgement per line — weak labels, say so on the slide.

## 2. PRECEDENT

- **TallyKhata (VERIFIED, page read):** https://www.tallykhata.com/million-shopkeepers-using-tallykhata-app-for-records-and-payments/ — 1M+ monthly active shopkeepers; Bangla app; Pelam/Dilam entries; per-shop QR accepting payments from any bank/MFS app; BB Payment Service Provider licence; eKYC; helpline 16726. It records dues and SMSes the customer ("Today's purchase 320 BDT, total due 1170 BDT"). **Overlap is real:** khata + QR + due-SMS all exist. What is NOT evidenced on the page: a customer-facing "pay this specific baki line by QR" settle flow, and any ranking/default-risk model. Say plainly: the ledger+QR substrate exists; our claim is only the settle-flow + ranking layer.
- **Hishabee:** competitor khata app — UNVERIFIED (page not opened today).
- **bKash/Nagad QR:** payment rails exist; no baki concept — VERIFIED indirectly via Prothom Alo article above.
- **Global:** BNPL "pay later" apps settle merchant credit, but none read a paper khata; UNVERIFIED specifics.

## 3. LEGAL/ETHICS (not legal advice)

- **Bangladesh MFS Regulations 2022** exist (circular PDF: https://www.bb.org.bd/mediaroom/circulars/psd/feb152022psd04e.pdf — found via search, PDF contents not read: UNVERIFIED detail). Boundary: Baki-Settle must move payment for an *existing recorded debt*; it must not create deposits, defer payments, or score customers for credit issuance — that enters e-money/credit-regulation class. Draft "Regulations for E-money Issuers in Bangladesh" published Nov 2025 (https://www.bb.org.bd/aboutus/draftguinotification/guideline/draft_emoney.pdf; coverage: https://www.tbsnews.net/economy/banking/bb-unveils-draft-rules-open-digital-payments-non-bank-players-1279741) — final status UNVERIFIED.
- **Personal Data Protection Ordinance 2025** (Ordinance No. 61 of 2025, gazetted 6 Nov 2025 — Bangladesh's first standalone data-protection law; applies to entities processing personal data in BD): https://www.thedailystar.net/tech-startup/news/bangladeshs-personal-data-protection-ordinance-2025-key-takeaways-4015401 ; https://bd-scl.com/insights/personal-data-protection-ordinance-2025-compliance.html . Khata photos contain third-party customer names → redact/blur; consent from the shopkeeper for the pages and avoid storing identifiable customer data. (Note: the brief said "data protection act 2026"; the verified instrument is the 2025 Ordinance.)
- **Unclear:** whether a wallet "pay-your-dued" flow needs any BB notification; whether shopkeeper-recorded debt amounts create liability for the platform if OCR misreads an amount (mitigate: shopkeeper confirms each line before the QR is shown).

## 4. 48-HOUR BUILD PLAN

Stack: Python FastAPI backend + simple web (React or plain HTML) customer/shop views; tesseract+NumtaDB baseline and one LLM-vision API for khata reading; scikit-learn ranking model. Free-tier GPU not required (small model).

- H0–6: A collects khata pages (5–10 shops); B builds mock upay-style app shell + QR flow (mock payment, no real money); C builds khata-ingestion pipeline (photo → lines → amounts) using spike 09 code.
- H6–18: A annotates lines + shopkeeper risk labels; C trains ranking model (features: age of line, amount, payment history, customer frequency) + default-risk score with per-line reasons; B wires settle flow: pick line → confirm → mock QR → ledger update + "cash-out fee saved: Tk X" counter.
- H18–30: A runs 20-customer mock trial (critique falsifier: ≥25% choose settle-over-cash-out when both offered); C measures entry accuracy on held-out pages; B builds judge-facing dashboard (ranked baki lines with reasons).
- H30–36: **feature freeze.** H36–40: red-team (wrong amounts, adversarial line edits). H40–48: demo rehearsal + pitch + one-page logic chain.

## 5. SPIKE TEST — RAN, real numbers

See spikes/09-baki-settle/RESULTS.md. Tesseract 5.4.0 (ben fast) on 3 synthesized clean printed khata lines: **3/3 Bangla-digit amounts recovered exactly; name/item text heavily degraded** (e.g., মিয়া→মি). PASS for amounts, FAIL for names → full pipeline needs LLM-vision or NumtaDB fine-tune for names; handwritten-page accuracy UNVERIFIED. Environment notes: tesseract installed via winget; ben.traineddata downloaded; Windows font copy permission-blocked → used downloaded Noto Sans Bengali.

## 6. BASELINE

Non-AI baseline: shopkeeper types the due amount manually (TallyKhata's existing flow) — works today, zero ML. LLM-API baseline: GPT-class vision reads clean khata pages ~80% (critique #2 estimate, UNVERIFIED). **Pointless-if number:** if the ranking model's settle-rate lift over "show newest dues first" is <5 pts in the 20-customer trial, the AI adds nothing and the idea is a payment-flow UX demo (critique already flags the AI role as weak).

## 7. RISKS

1. **Demand premise fails** — customers with cash prefer cash; shops refuse because baki is lock-in (critique hidden thesis 3). Mitigation: the 20-customer A/B trial at H18; kill honestly if <25%.
2. **Weak AI role** — ranking is the only model; judges may call it a rule. Mitigation: per-line default-risk with reasons + measured lift vs newest-first baseline.
3. **OCR accuracy on real handwriting** — spike shows printed floor only. Mitigation: shopkeeper-confirms-every-line flow; triage low-confidence lines.
4. **Regulatory optics** — looks credit-adjacent. Mitigation: settlement-only framing, no deferral, no interest, human confirm.
5. **Data collection slippage** — shops may refuse photos. Mitigation: family shops first, consent script ready at H0.

**P(working live demo) = 0.65.** Payment flow + OCR + ranking are all individually buildable; the risk is demand-trial quality and OCR on real pages, not engineering.

## 8. RESPONSIBLE AI

- **Fairness groups:** shop size, customer gender/age (proxy from names — flag as proxy only), urban/rural shop; report ranking lift per group.
- **Explainability:** every surfaced line shows its top-3 reasons (age, amount, history).
- **Security:** adversarial user could inflate a khata line → shopkeeper confirmation is the trust boundary; prompt-injection N/A for the ranking model, relevant for any LLM-vision reading (sanitize OCR text before LLM calls); no real customer PII stored.
- **Human oversight:** shopkeeper confirms each line; customer confirms amount; no autonomous debt decisions. No lending, no interest, no deferral — settlement of an existing recorded debt only.
