# 08-proof-forensics.md — Feasibility: Payment-proof forensics (forged-screenshot detector)

Written 2026-10-02 by the feasibility researcher. Inputs: docs/CONTEXT.md, docs/IDEA_POOL.md, docs/03-critique/02-critique.md (survivor #12 + VerifyTaka repositioning), docs/01-data/inventory.md. Not legal advice.

**One-line problem statement:** For F-commerce sellers and MFS merchants, buyers send FORGED payment screenshots and sellers ship goods before discovering the fraud, causing direct inventory loss. We build a forgery detector that uses self-collected real payment proofs + a deliberately forged set (built by a blind teammate) to flag edited screenshots, with success measured by ≥90% detection at <5% false-positive on a held-out blind set.

## 1. DATA REALITY

### Public datasets

None found. No public dataset of Bangladeshi MFS payment screenshots exists (inventory A10 lists only self-collection for this artefact class; MIDV-500/SROIE document-forgery sets unreachable per inventory — and they are ID documents, not MFS proofs anyway). **The corpus is 100% self-collected. This is both the moat and the risk (rule 2: real artefacts, not invented).**

### Self-collected data

- **Real proofs:** 40–80 real payment-success screenshots (bKash/Nagad/Rocket/upay) from teammates, classmates, family, and campus F-commerce sellers. Each is a genuine app screenshot from the owner's own phone.
- **Forged set:** built by ONE teammate ("the forger") who is blind to the detector's features; they edit real screenshots with any tool they like (Photoshop, Snapseed, re-typing amounts, re-rendering). 20–40 forgeries. The modeler never sees the forgeries until final eval — this is the critique's falsifier design ("held-out forged-vs-real set built by a teammate the modeler never talks to").
- **Protocol:** (1) contributors send own screenshots to a collection form; (2) consent signed; (3) redaction pass: blur third-party names/numbers on any image shown publicly (demo uses masked overlays); (4) split: 70% train / 30% real-test, plus the blind forged set.
- **Consent wording (verbatim):**
  - EN: "I voluntarily share payment screenshots from my own phone for a university hackathon forgery-detection prototype. I understand personal names and numbers will be masked before any public display, images are stored locally, not published, and I can withdraw before the demo. Signature: ____ Date: ____"
  - BN: "আমি স্বেচ্ছায় আমার নিজ ফোনের পেমেন্ট স্ক্রিনশট একটি বিশ্ববিদ্যালয় হ্যাকাথনের জালিয়াতি-শনাক্তকরণ প্রোটোটাইপের জন্য শেয়ার করছি। প্রকাশ্য প্রদর্শনের আগে ব্যক্তিগত নাম ও নম্বর লুকানো হবে, ছবি স্থানীয়ভাবে সংরক্ষিত থাকবে, প্রকাশ করা হবে না, এবং ডেমোর আগে আমি প্রত্যাহার করতে পারব। স্ক্রিনশটে থাকা অন্যের তথ্যের দায়ভার আমার সম্মতিতে শেয়ার করা হচ্ছে। স্বাক্ষর: ____ তারিখ: ____"
- **Redaction steps:** blur/box names, sender/receiver numbers, and balances in any demo material; keep originals only in the local training folder; no provider logos in pitch slides (trademark hygiene, critique #12).
- **Who collects / hours:** Person A + C collect reals (~3 h); the designated forger works separately (~2 h); total ~5 person-hours.

## 2. PRECEDENT

| Product | URL | What it does | What it does NOT do |
|---|---|---|---|
| VerifyTaka | https://verifytaka.com (opened 2026-10-02) | Verifies REAL transfers: TrxID matched against SMS receipts relayed from the merchant's Android phone; ৳0.5/check; bKash Send Money + Cash In, Nagad/Rocket Send Money; WooCommerce plugin; FAQ includes "How does VerifyTaka detect fake bKash/Nagad screenshots?" (answer content not expanded on the fetched page — their fake-screenshot capability UNVERIFIED) | Requires the merchant's phone to relay SMS (device-bound); verifies transaction IDs, does not (visibly) analyse an arbitrary screenshot's pixels; Send Money only — no Payment/Pay Bill |
| bKash recipient-name display | https://www.tbsnews.net/economy/corporates/bkash-send-money-now-more-secure-accurate-831161 (cited in critique; not opened today) | Shows registered name pre-send | Not about proof screenshots | UNVERIFIED (not opened) |
| Global: screenshot-fraud tools for P2P payments (e.g. Indian "fake payment screenshot" detectors) | UNVERIFIED — not searched today | — | No BD MFS-specific detector found | UNVERIFIED |

**Plainly:** VerifyTaka already solves the *verification* problem for merchants willing to run its SMS relay — and its FAQ claims some fake-screenshot detection (UNVERIFIED depth). The repositioned gap (critique: "VerifyTaka verifies real transfers; nobody detects forged screenshots") is: **pixel-level forgery detection on an arbitrary screenshot, no device relay, works for any seller including those outside VerifyTaka.** That gap is real but narrow — the pitch must name VerifyTaka and state the delta honestly.

## 3. LEGAL/ETHICS (not legal advice)

- **Screenshots contain third-party personal data** (names, numbers, balances) → Personal Data Protection Act 2026 (Act No. 63 of 2026) applies to our processing; consent per s.5; masking before any display; s.24 household exemption does not cover our processing. Source: https://www.recordinglaw.com/world-laws/world-recording-laws/bangladesh-recording-laws/ (opened 2026-10-02, cites bdlaws.minlaw.gov.bd).
- **False accusations are the harm vector:** a "forged" verdict against a real customer is defamatory-adjacent and commercially damaging. Design rule: output is "needs manual verification" + reasons, never an accusation; the seller always decides (critique falsifier: <5% FP or unusable).
- **Provider trademarks:** demo materials must not reproduce bKash/Nagad branding beyond what analysis requires; use masked mock-ups in slides.
- **Forging for the dataset:** teammates forging screenshots for internal test data is not fraud (no third party, no gain), but forged images must never leave the team or be posted (they could circulate as usable fakes). Watermark forged set filenames; delete after demo.
- **Unclear:** whether VerifyTaka's terms restrict building a competing analysis on their outputs (we don't use their outputs — independent); whether MFS providers' terms restrict screenshot analysis (no ToS read: UNVERIFIED — low risk for analysis of user-owned screenshots).

## 4. 48-HOUR BUILD PLAN

Stack: Python, PIL/OpenCV (installed: pillow 12.3), scikit-learn, torch (free-tier GPU for a small CNN if time allows), Streamlit. Compute: CPU sufficient for feature-based model; GPU optional.

| Hours | Person A (data lead) | Person B (model lead) | Person C (app lead) |
|---|---|---|---|
| 0–6 | Collect 40–80 real proofs + consent; brief the forger (separately) | Feature extraction pipeline: ELA, noise residual, quantization tables, EXIF, font/region stats | Streamlit upload → verdict UI |
| 6–12 | Label reals (provider, amount region); redact demo copies | Baseline: pixel/EXIF heuristics (critique: ~70% on lazy forgeries); train classifier v1 on features | Verdict display with highlighted suspicious regions |
| 12–24 | Forger delivers blind forged set (modeler excluded) | Train improved model (features + small CNN on amount region); internal eval on 30% real holdout | Region-overlay visualization |
| 24–36 | Run BLIND eval: forger's set, modeler's model, first contact | Tune threshold for <5% FP; **FEATURE FREEZE h36** | Demo: judge uploads any screenshot, sees verdict + reasons |
| 36–48 | Pitch: falsifier-first slide | Report blind numbers honestly | Rehearsal, canned set fallback |

Real vs mocked: corpus real; classifier real; "verified against provider" is explicitly out of scope (that is VerifyTaka's lane) — say so.

## 5. SPIKE TEST — RUN, real numbers

Script: `spikes/08-proof-forensics/spike_proof_forensics.py`; results: `spikes/08-proof-forensics/results.json` + 6 generated JPEGs in the same folder. Environment: Python 3.14.6, Pillow 12.3.

- Generated 3 mock "real" payment screenshots (PIL-rendered MFS-style success screen, single JPEG encode q=92, with synthetic sensor noise) and 3 forgeries (amount region wiped + re-typed, re-encoded q=88 → double compression).
- Measured statistics per image (real numbers):
  - ELA mean — REAL: 0.207, 0.207, 0.212; FORGED: 0.168, 0.169, 0.170 → **zero overlap; threshold 0.189 classifies 6/6 (100%)**. Direction note: forged ELA is LOWER here because the edit wipes a flat region then re-encodes — the sign of the effect is forgery-method-dependent, so a threshold must be learned, not assumed.
  - Noise variance — REAL: 40.7, 39.7, 42.6; FORGED: 50.5, 50.5, 51.2 → also separable in this setup (re-encode amplifies high-frequency residual).
  - EXIF: absent in all 6 (PIL strips it; phone screenshots also typically lack useful EXIF) → EXIF is NOT a usable signal for this artefact class.
- **Honest caveat (mandatory in pitch):** these are mock-rendered images, not real phone screenshots. The spike proves the *measurement pipeline works and separates double-encoded edits*, NOT that it survives real forger tools (Snapseed re-saves, partial re-renders, AI inpainting). The blind-teammate eval in §4 is the real test.

PASS/FAIL (pre-set bar: a distinguishing statistic with clear separation on a 3v3 set): **PASS on the mock set (ELA separation 6/6, zero overlap); real-world generalization UNVERIFIED pending blind eval.**

## 6. BASELINE

- Simplest baseline: pixel/EXIF heuristics — critique estimates ~70% on lazy forgeries; our spike's ELA threshold got 6/6 on mock forgeries (optimistic, mock set).
- LLM-API baseline: GPT-vision prompted "is this screenshot edited?" — likely 70–85% on obvious forgeries, weak on subtle re-encodes; must be measured at hour 12 on the same blind set.
- **Pointless-if number:** if blind-set detection < 90% at < 5% FP on real proofs (critique falsifier), the detector is unusable (false accusations) and the idea dies. Secondary pointless-if: VerifyTaka's SMS-relay verification (৳0.5/check) is strictly better for any merchant willing to install it — the detector only earns its place for relay-unwilling sellers, so the pitch must quantify that segment or the idea is a feature, not a product.

## 7. RISKS

1. **Arms race / generalization** (critique #12): detector trained on today's forgeries fails on tomorrow's tools; 48h corpus cannot cover the forgery space. Mitigation: blind forger with free tool choice; report per-forgery-method breakdown; position as "raises the bar", not "solves forgery".
2. **False positives accuse real customers** — the worst failure. Mitigation: threshold tuned for <5% FP; output is "verify manually" with reasons; never auto-block.
3. **VerifyTaka already-dominant for merchants** (§2). Mitigation: target non-relay sellers (informal F-commerce); name VerifyTaka on the first slide.
4. **Small blind set (20–40 forgeries)** — accuracy estimate has ±15–20 pt error bars. Mitigation: report confidence interval; don't claim 95% from n=25.
5. **Real screenshots vary wildly** (device, app version, dark mode, screenshots-of-screenshots). Mitigation: collect across ≥3 providers and ≥5 devices; screenshots-of-screenshots included deliberately (that is the actual scam path — a forged image arrives re-sent via Messenger/WhatsApp).

**P(working live demo) = 0.60.** Reasoning: the demo moment (judge uploads a screenshot, sees verdict + highlighted regions) works with the feature pipeline alone and needs no training to function; the blind eval may or may not hit 90/5, but the demo shows mechanism + honest numbers either way. Main downside risk is the blind forger producing trivially different images (too easy) or the LLM-vision baseline matching us.

## 8. RESPONSIBLE AI

- **Fairness groups:** provider (bKash/Nagad/Rocket/upay formats), device/OS (screenshot compression differs), image path (direct vs re-sent via chat app — re-sent REAL proofs may look "edited"; must measure FP rate on re-sent reals specifically, this is the top fairness trap).
- **Explainability output:** verdict + per-signal reasons ("double JPEG compression in amount region", "font metrics differ from header") + highlighted region overlay; confidence band, not a binary accusation.
- **Security:** adversarial users will probe the detector to learn what evades it (mitigation: never expose per-signal scores publicly; rate-limit the demo); prompt injection if an LLM reads screenshot text (mitigation: OCR text is data, structured feature pipeline decides); data leakage: forger-modeler separation is the leakage control — enforce it physically.
- **Human oversight:** the seller always makes the ship/no-ship decision; the tool recommends manual verification; no automated order cancellation or account flagging.
