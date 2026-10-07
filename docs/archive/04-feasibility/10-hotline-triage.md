# 10-hotline-triage.md — Feasibility: Dialect Hotline Triage (2026-10-02)

**Idea (D21, critique survivor #8):** caller speaks dialect; model extracts intent + urgency, routes to a human with transcript. Ben-10 (S1) + SLR53 (S14) + self dialect recordings (S3). Track 06.

## 1. DATA REALITY

| Source | URL | Size | Language | Licence | Hackathon use | Download friction | Status |
|---|---|---|---|---|---|---|---|
| Ben-10 (BengaliAI) | https://huggingface.co/datasets/bengaliAI/Ben-10 | 15,036 rows / 8.52 GB; train 13.4k, valid 1.67k; valid split covers 7 dialects (barishal 105, chittagong 178, habiganj 117, kishoreganj 204, narail 183, narsingdi 136, rangpur 76 files — counted from HF tree listing today) | bn, 10 BD dialects | CC0-1.0 | yes — train + person-level valid eval | direct HF download; **dataset viewer broken** (CastError on streaming — observed today); closed test set via maintainer eval-request only | VERIFIED (page opened; valid.csv + 6 wavs downloaded) |
| OpenSLR SLR53 | https://www.openslr.org/53/ | ~196K utterances; 16 zips ~900 MB each (~14.4 GB) | bn (read speech) | CC-BY-SA 4.0 | yes (ASR pretrain) | direct wget; large | VERIFIED (page opened) |
| Self-collected dialect calls | n/a | ~10 speakers × 5–10 calls | bn dialects | own (consent) | yes — held-out eval | recruit classmates/family | planned |

**Self-collection protocol:** ~10 speakers (Sylheti/Chittagonian/Noakhali/Barishal relatives of teammates), each records 3 mock hotline calls (billing problem, cash-out failure, PIN reset) on their own phone. Consent wording — Bangla: "আমি স্বেচ্ছায় এই কল রেকর্ড করছি, শুধু ছাত্র প্রোটোটাইপের জন্য। আমার নাম ও নম্বর মুছে ফেলা হবে।" English: "I voluntarily record this mock call for a student prototype only. My name and number will be removed." Redaction: strip phone numbers from transcripts; hold out ≥2 speakers entirely. Collectors: all 3 members, ~2–4 h. Intent/urgency labels: speaker-confirmed after each call.

## 2. PRECEDENT

- **bKash hotline 16247 + live chat, 24/7** — VERIFIED via search snippets of the official page (direct fetch returned 403): "customer care representatives are available 24/7 through 16247, live chat" (https://www.bkash.com/en/customer-service/contact-us); corroborated by TBS: 356 service centres + 16247/live chat/email/social (https://www.tbsnews.net/economy/corporates/bkash-offers-excellent-customer-support-247-call-centres-and-online-1054501). IVR menus + human agents already exist; no evidence of dialect ASR triage.
- **Agriculture Call Centre 16123 (VERIFIED, full article read):** 92,094 calls July 2025–June 2026, human experts answer in Bangla — https://www.bssnews.net/special-stories/401845 . Proves phone-advisory demand in BD; it is human-first, not AI-routed.
- **Global:** contact-center ASR+intent routing (Observe.AI, Cognigy etc.) — UNVERIFIED specifics, none BD-dialect.
- **Plainly:** hotline + IVR exists in BD; dialect free-speech triage does not. The moat is dialect ASR, which spike shows is genuinely unsolved zero-shot.

## 3. LEGAL/ETHICS (not legal advice)

- **Call recording:** no all-party-consent statute found; self-recording treated as lawful, interception is the offence (third-party source, detail UNVERIFIED against actual acts: https://www.recordinglaw.com/world-laws/world-recording-laws/bangladesh-recording-laws/). For a real hotline, record-notice at call start is standard practice — exact BD requirement UNVERIFIED.
- **Personal Data Protection Ordinance 2025** (gazetted 6 Nov 2025): voice recordings + transcripts are personal data; consent + retention limits needed — https://www.thedailystar.net/tech-startup/news/bangladeshs-personal-data-protection-ordinance-2025-key-takeaways-4015401 . Retention period specifics UNVERIFIED.
- **Cyber Security Ordinance 2025** (repealed CSA 2023): governs cyber offences; overlap with PDPO on incident handling — http://bdlaws.minlaw.gov.bd/act-1538.html (existence verified via search; contents not read).
- **Unclear:** whether an MFS provider may route account actions on AI-extracted intent (we don't — routing only, human acts); BB rules on voice as an auth factor (not used here).

## 4. 48-HOUR BUILD PLAN

Stack: faster-whisper/Whisper fine-tune on free-tier GPU (Colab/Kaggle) or the existing `bengaliAI/tugstugi_bengaliai-regional-asr_whisper-medium` checkpoint (listed on the Ben-10 dataset page; quality UNVERIFIED); intent classifier = fine-tuned Bangla encoder (e.g., small BERT-class) or LLM-API on transcript; FastAPI + Twilio-style mock call page (browser mic, no real telephony).

- H0–6: A downloads Ben-10 train subset + starts GPU fine-tune; B builds mock hotline web page (mic → upload → transcript → route card); C collects 10-speaker mock calls + labels.
- H6–18: A evaluates fine-tuned ASR WER on held-out speakers (kill bar: slot-exact accuracy <90% per critique #4/#8); C trains intent+urgency classifier on labelled calls; B builds agent-side routing view (transcript + intent + urgency + confidence).
- H18–30: end-to-end: judge speaks in dialect in browser → transcript → routed ticket with summary; measure intent accuracy on held-out speakers; fairness table per dialect.
- H30–36: **feature freeze.** H36–48: red-team (noisy audio, code-switching), rehearsal, pitch.

## 5. SPIKE TEST — RAN, real numbers

See spikes/10-hotline-triage/RESULTS.md. Downloaded Ben-10 valid.csv (1,666 rows) + 6 dialect wavs; ran zero-shot Whisper via faster-whisper 1.2.1 (PyAV 19 incompatible on py3.14 — stdlib WAV decode workaround):

- **whisper-tiny: WER 127.9%** (251 ref words, 6 dialects) — English hallucinations, empty outputs.
- **whisper-small: WER 123.1%** — cross-script hallucinations (Kannada/Telugu/Chinese tokens).

**FAIL for zero-shot; the ASR gap is the load-bearing number.** Fine-tuning on Ben-10 train (13.4k rows, CC0) is the required path and is feasible on free-tier GPU; post-fine-tune WER UNVERIFIED (not run — GPU fine-tune exceeds the 15-min spike budget).

## 6. BASELINE

LLM-API baseline: once a transcript exists, GPT-class zero-shot intent classification gets ~80% (critique #8) — so the moat is entirely the ASR. Non-AI baseline: IVR menu (press 1/2/3) — exists today. **Pointless-if number:** if fine-tuned ASR WER on held-out dialect speakers stays >30%, intent accuracy cannot reach the ≥85% bar and the tool misroutes more than it saves — kill or demote to menu-IVR + human.

## 7. RISKS

1. **ASR doesn't reach usable WER in 48h** (spike shows zero-shot dead). Mitigation: start fine-tune at H0; fallback to the bengaliAI whisper-medium checkpoint; final fallback: transcript-assisted human triage demo with pre-recorded calls.
2. **Misrouting harms callers** — wrong urgency sends a fraud victim to the back of the queue. Mitigation: urgency=high always rings a human; model never blocks.
3. **10 speakers is tiny** — model may fit speaker idiosyncrasies. Mitigation: person-level held-out split; report per-speaker variance.
4. **No real telephony in demo** — browser mic only. Mitigation: pre-recorded real calls as backup demo path.
5. **Consent/retention exposure** — recordings of family members. Mitigation: written consent, redaction, delete-after-hackathon commitment.

**P(working live demo) = 0.45.** Everything except ASR quality is easy; ASR is a genuine research risk with a fallback demo path (pre-recorded calls through the fine-tuned model, honest WER slide).

## 8. RESPONSIBLE AI

- **Fairness groups:** per-dialect WER/intent-accuracy table is the headline slide; also gender/age of speaker if available. If a dialect slice fails, that dialect routes straight to humans (no silent degradation).
- **Explainability:** routing card shows transcript + intent + urgency + confidence; agent sees raw audio player.
- **Security:** adversarial audio (noise, code-switching) tested at H36; prompt injection if LLM summarizes transcripts — sanitize and constrain; data leakage: held-out speakers never in training; no numbers stored.
- **Human oversight:** model routes; a human agent always performs any account action. No autonomous account changes.
