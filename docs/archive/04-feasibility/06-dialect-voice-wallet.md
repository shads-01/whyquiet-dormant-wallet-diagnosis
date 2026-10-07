# 06-dialect-voice-wallet.md — Feasibility: Dialect voice wallet (+ Confirm-Echo)

Written 2026-10-02 by the feasibility researcher. Inputs: docs/CONTEXT.md, docs/IDEA_POOL.md, docs/03-critique/02-critique.md (survivor #4), docs/01-data/inventory.md, docs/02-ideas/01-candidates.md (D9, D30, D38). Not legal advice.

**One-line problem statement:** For dialect-speaking, low-literacy MFS users, typing numbers and navigating menus causes failed or wrong payments. We build a free-speech voice payment flow that uses Ben-10 (CC0 dialect speech) + self-collected dialect recordings to extract intent + amount + recipient from spontaneous Bangla/dialect speech, validated by echo read-back, with success measured by slot-exact accuracy per dialect on held-out speakers.

## 1. DATA REALITY

### Public datasets/models (pages opened 2026-10-02)

| Source | URL | Size | Language | Licence | Hackathon use OK? | Download friction | Status |
|---|---|---|---|---|---|---|---|
| Ben-10 (BengaliAI) | https://huggingface.co/datasets/bengaliAI/Ben-10 | 15,036 rows / 8.52 GB; train 13,343 rows (CSV read directly: 13,343 rows, 10 districts — sylhet 2,903, kishoreganj 1,638, narail 1,488, chittagong 1,406, narsingdi 1,098, sandwip 1,049, rangpur 1,037, tangail 987, habiganj 940, barishal 796); validation 1.67k; closed test set held by maintainers | bn, 10 Bangladeshi regional dialects, spontaneous speech | CC0-1.0 | Yes (train); closed test only via eval-request issue on HF | Direct HF download; full set is 8.5 GB — download subset or stream; NOTE: HF auto-converted viewer streaming currently fails with a CastError (observed 2026-10-02), so pull files directly from the repo tree (`train/folder_1/*.wav` + `train.csv`) | VERIFIED (page + CSV + 8 WAVs downloaded) |
| SLR53 Bengali ASR | https://www.openslr.org/53/ | ~196K utterances; 16 zips ~900 MB each (~14 GB total) | bn (read speech, Google-collected) | CC BY-SA 4.0 | Yes | Direct download, no registration; too big for 48h except one zip | VERIFIED (page) |
| whisper-tiny (baseline ASR) | https://huggingface.co/openai/whisper-tiny | ~150 MB | multilingual | MIT (model card) | Yes | Direct HF download | VERIFIED (downloaded and ran) |

### Self-collected dialect recordings (S3)

- **Target size:** ≥10 speakers × 5–10 min each (≈60–100 min audio), covering Sylheti/Chittagonian/Noakhali plus standard Bangla controls; each speaker records: read payment phrases ("send five hundred to Karim bhai"), spontaneous intent utterances, echo confirmations, and 10 induced-error confirmations (wrong amount spoken on purpose) for Confirm-Echo eval.
- **Protocol:** quiet room, phone voice-memo, 44.1kHz→16kHz conversion; per-speaker consent form; per-speaker held-out split (never mix one speaker across train/test).
- **Consent wording (verbatim):**
  - EN: "I voluntarily record my voice speaking in my own dialect for a university hackathon prototype. I understand recordings are used only to build and test a speech-payment demo, stored locally, not published, and I can withdraw before the demo. Signature: ____ Date: ____"
  - BN: "আমি স্বেচ্ছায় আমার নিজ ভাষায়/উপভাষায় কথা বলে একটি বিশ্ববিদ্যালয় হ্যাকাথন প্রোটোটাইপের জন্য ভয়েস রেকর্ড করছি। রেকর্ডিং শুধু ভয়েস-পেমেন্ট ডেমো তৈরি ও পরীক্ষায় ব্যবহৃত হবে, স্থানীয়ভাবে সংরক্ষিত থাকবে, প্রকাশ করা হবে না, এবং ডেমোর আগে আমি প্রত্যাহার করতে পারব। স্বাক্ষর: ____ তারিখ: ____"
- **Redaction:** recordings contain no account numbers (use fake recipient names); delete any utterance where a real number slips in.
- **Who collects / hours:** all 3 people recruit classmates/relatives; ~4–6 h total including recording and labelling transcripts (transcripts needed for slot eval — budget 1 h labelling per speaker-hour).

## 2. PRECEDENT

| Product | URL | What it does | What it does NOT do |
|---|---|---|---|
| UPI 123PAY (India) | https://en.wikipedia.org/wiki/Unified_Payments_Interface#UPI_123PAY (opened 2026-10-02; NPCI page https://www.npci.org.in returns 403 to fetch) | Voice/IVR payments for feature phones, launched 8 Mar 2022; 4 modes incl. IVR; limit ₹10,000 (Oct 2024) | Menu/IVR-driven, standard Hindi/English + limited languages; NOT free-speech, NOT Bangladeshi dialects |
| ToneTag VoiceSE (India) | cited in the same Wikipedia section: voice UPI in 6 languages incl. Bengali (Indian bn) | Voice payments for feature phones | Indian Bengali, commercial, not dialect-robust, not BD | UNVERIFIED detail beyond Wikipedia |
| bKash hotline 16247 | widely referenced; no official page opened today | Human phone support in Bangla | Human-only, no dialect ASR, no self-service payment by voice | UNVERIFIED (no page opened) |
| Menu-IVR voice banking (generic) | — | Keypad/menu flows | The critique's baseline: "menu-IVR gets most of the value; the model's edge is dialect robustness — must be measured, not asserted" (critique #4) | — |

**Plainly:** voice *menu* payments exist in India; nothing does free-speech **Bangladeshi-dialect** payment intent extraction. The differentiator is dialect robustness, and our spike shows exactly how far the field is from it (§5).

## 3. LEGAL/ETHICS (not legal advice)

- **Voice recordings = biometric personal data** under the Personal Data Protection Act 2026 (Act No. 63 of 2026) — voiceprints expressly listed as biometric data. Consent must be voluntary, specific, clear, withdrawable (s.5); household/personal-use exemption (s.24) covers contributors' own use, not our processing; cross-border transfer (e.g., HF-hosted fine-tune) implicates s.29. Source: https://www.recordinglaw.com/world-laws/world-recording-laws/bangladesh-recording-laws/ (opened 2026-10-02, cites bdlaws.minlaw.gov.bd).
- **Recording calls:** participant self-recording is not criminalized (no all-party statute); eavesdropping on others is (Telecom Act s.71, up to 2 yrs / Tk 1.5 crore). Our recordings are staged, consented, first-party — low risk. Same source.
- **Synthetic voice:** not used in this idea (that is idea 07). If demo uses TTS read-back, use generic TTS voices, never cloned voices; Telecom Act 2026 amendment s.70(3) criminalizes AI imitation of a person's voice to cause harm (fine up to Tk 1 lakh). Same source.
- **Unclear:** whether voice is a permitted authentication factor under Bangladesh Bank MFS/e-money rules — the critique flags "check whether voice auth is a permitted factor" (critique #4). No BB circular found or read today: **UNVERIFIED**. Demo design answer: voice extracts intent; a typed/keypad PIN always confirms — voice never authenticates alone.

## 4. 48-HOUR BUILD PLAN

Stack: Python, transformers (Whisper fine-tune), torch (free-tier GPU, e.g. Colab T4), soundfile, FastAPI + simple web audio capture (or Twilio-mock IVR page). Compute: GPU mandatory — CPU inference measured at ~30–48 s per 30 s clip (spike), unusable live.

| Hours | Person A (data lead) | Person B (model lead) | Person C (flow/demo lead) |
|---|---|---|---|
| 0–6 | Recruit + record first 5 dialect speakers with consent; transcribe roughly | Start whisper-tiny/small fine-tune on Ben-10 train subset (2–4 h GPU) | Voice-capture web page + mock wallet UI |
| 6–12 | Record remaining 5+ speakers; label slots (amount/recipient/action) per utterance | Fine-tune continues; evaluate per-dialect WER on held-out speakers | Intent+slot parser (grammar over ASR output: Bangla number words → digits, name matching) |
| 12–24 | Collect Confirm-Echo eval set: 10 induced-error confirmations per speaker | Slot-extraction accuracy per dialect; echo-check logic (compare spoken confirm slots vs intent slots) | Full flow: speak → slots → read-back → confirm/catch |
| 24–36 | Freeze eval set; run falsifier measurement | Fix worst dialect; **FEATURE FREEZE h36** | Demo script: judge speaks, sees slots, tries a wrong-amount echo |
| 36–48 | Pitch data story | Falsifier numbers | Rehearsal, canned-audio fallback |

Real vs mocked: ASR + slot extraction real (fine-tuned); backend wallet fully mocked; live mic input real; fallback = pre-recorded audio if venue noise breaks mic demo.

## 5. SPIKE TEST — RUN, real numbers

Script: `spikes/06-dialect-voice-wallet/spike_ben10_wer.py`; results: `spikes/06-dialect-voice-wallet/results.json`. Environment: Python 3.14.6, torch 2.13 CPU, transformers 5.15, whisper-tiny (~150 MB), 8 Ben-10 WAVs (~500 KB each) downloaded directly from the HF repo (NOT the 8.5 GB set).

- CSV verified: 13,343 train rows, 10 dialects, columns file_name/transcripts/district; 3 example rows printed (spontaneous dialect speech, e.g. barishal: "মোর পছন্দের শখ হইলো গান হোনা...").
- **whisper-tiny zero-shot WER (language forced to Bengali, CPU):**
  - barishal 1.07, chittagong 10.57, habiganj 4.35, kishoreganj 6.92, narail 2.58, narsingdi 13.70, rangpur 10.09, sandwip 10.57
  - **MEAN WER = 7.48 (748%)** — i.e., transcripts are garbage; WER > 1 means the model hallucinates more words than the reference contains.
- Inference speed CPU: 30–48 s per ~30 s clip → live CPU demo infeasible; GPU required.
- Caveats: whisper-tiny is the smallest model and these are long spontaneous clips; whisper-small/medium or a fine-tune will do far better (bengaliAI's own fine-tuned whisper-medium exists on HF: https://huggingface.co/bengaliAI/tugstugi_bengaliai-regional-asr_whisper-medium — seen on the dataset page; its WER UNVERIFIED). But the zero-shot number is the honest floor.

PASS/FAIL (pre-set bar: zero-shot WER low enough that slot extraction could work without fine-tuning, i.e. WER < ~0.5): **FAIL — mean WER 7.48.** Consequence: the fine-tune on Ben-10 train is load-bearing and must start in hour 0; the critique's falsifier (slot-exact accuracy ≥90% per dialect) is at serious risk. The menu-IVR fallback (critique #4) should be built in parallel from hour 12.

## 6. BASELINE

- Simplest baseline: menu-IVR (existing pattern; user presses keys) — gets most of the value with zero ML (critique #4).
- LLM-API baseline: Whisper-API-class transcription + GPT slot extraction. Our spike bounds the zero-shot floor: whisper-tiny WER 7.48 on dialect speech; any baseline sharing that ASR inherits the failure.
- **Pointless-if number:** if fine-tuned slot-exact accuracy per dialect < 90% on held-out speakers (critique falsifier), the free-speech version is pointless — keep only the echo-check component and menu-IVR. Secondary pointless-if: if echo-check catches < 50% of induced wrong-amount confirmations, Confirm-Echo adds no safety.

## 7. RISKS

1. **Zero-shot ASR unusable on dialects (measured: WER 7.48).** Mitigation: fine-tune from hour 0 on Ben-10 (CC0, 13.3k rows); restrict demo vocabulary to payment phrases; menu-IVR fallback.
2. **Free-tier GPU time insufficient** for whisper fine-tune in-window. Mitigation: fine-tune whisper-tiny (smallest) on a 2k-row subset; or use bengaliAI's released fine-tuned whisper-medium directly (UNVERIFIED WER) and spend time on slot layer instead.
3. **Slot errors are money events** — a misheard amount. Mitigation: Confirm-Echo is mandatory in the flow; keypad PIN confirms; demo shows the catch, not just the success.
4. **Held-out speakers unrepresentative** (classmates ≠ upay's excluded users; critique unchallenged-assumption #4: dialect speakers may not want voice payments at all). Mitigation: test with ≥2 non-student adults (parents' network); present adoption as hypothesis, not fact.
5. **Venue noise breaks live mic demo.** Mitigation: canned-audio fallback path rehearsed.

**P(working live demo) = 0.45.** Reasoning: the measured zero-shot WER (7.48) means everything depends on a fine-tune completing and generalizing to held-out speakers within ~30 GPU-hours — plausible for whisper-tiny on payment-restricted vocabulary but genuinely uncertain; the echo-catch demo works even at mediocre WER (it demonstrates error detection), which is what keeps P above 0.4.

## 8. RESPONSIBLE AI

- **Fairness groups:** dialect (10 Ben-10 districts + our 3 target dialects), gender, age (≥1 older speaker), device/mic quality. Report slot accuracy per slice; the WER map IS the fairness artifact (critique #18).
- **Explainability output:** show transcript + parsed slots + confidence per slot; on mismatch, show exactly which slot disagreed ("you said পাঁচশ, we heard পঞ্চাশ").
- **Security:** adversarial audio (background scammer coaching the user — link to Coercion Shield family); prompt injection N/A (no LLM in the loop for decisions); data leakage: speaker-disjoint splits enforced; recordings never leave the team's machines except the GPU job (check Colab data terms; prefer Kaggle/local GPU).
- **Human oversight:** no money moves without explicit keypad PIN confirm after read-back; voice verdicts never auto-approve (BB voice-auth status UNVERIFIED — see §3).
