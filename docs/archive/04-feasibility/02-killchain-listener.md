# 02-killchain-listener.md — Feasibility: Coercion Shield (b) "Kill-chain listener"

Bangla speech → scam-stage classifier (hook / authority / urgency / ask) + sequence model over stages. Track 01. Status: HARDEST OF THE FOUR — ASR is the load-bearing risk and the spike shows it is real.

## 1. DATA REALITY

**Public datasets (verified by opening pages 2026-10-02):**

| Dataset | URL | Size | Language | Licence | Hackathon use | Friction |
|---|---|---|---|---|---|---|
| Ben-10 (BengaliAI) | https://huggingface.co/datasets/bengaliAI/Ben-10 | 15,036 rows / 8.52 GB; train 13.4k, val 1.67k | bn, 10 BD dialects | CC0-1.0 (stated on page) | Yes | Direct HF download; HF viewer currently broken (CastError) — download files directly; closed test set only via maintainer eval |
| OpenSLR SLR53 Bengali ASR | https://www.openslr.org/53/ | ~196K utterances (index page) | bn | per-resource page (not read) UNVERIFIED | Yes | Direct wget; large download |
| OpenSLR SLR37 Bengali TTS | https://www.openslr.org/37/ | bn_bd.zip 586 MB | bn-BD + bn-IN | CC BY-SA 4.0 (stated on page) | Yes (training-only synthetic scam audio) | Direct download; too large to sample casually — small-file access UNVERIFIED |
| Google FLEURS | https://huggingface.co/datasets/google/fleurs | bn_in subset only | bn-IN (Indian) | CC-BY-4.0 | Weak fit | Direct |

**Self-collected: scam-call re-enactments.**
- Sample size: 25–40 consenting classmates/relatives performing 4-stage scam scripts (hook → authority → urgency → ask) in Bangla + optionally Sylheti/Chittagonian; 30–60 s per clip; target 100–150 clips, ≈1.5–2.5 h audio.
- Protocol: read from a shared script bank (real scam patterns from own phones' scam SMS, redacted), one recording per stage per speaker, phone-mic quality, some with background noise added at training time.
- Consent wording:
  - English: "I agree to record scam-script sentences in Bangla/dialect for a fraud-detection research prototype. My voice recordings will be stored locally, used only for this project, never published, and deleted after the hackathon. I can withdraw at any time."
  - Bangla: "আমি প্রতারণা-প্রতিরোধ গবেষণার জন্য বাংলা/আঞ্চলিক ভাষায় স্ক্রিপ্টের বাক্য রেকর্ড করতে সম্মত। আমার কণ্ঠস্বর শুধু এই প্রজেক্টে ব্যবহৃত হবে, কখনো প্রকাশ করা হবে না, হ্যাকাথন শেষে মুছে ফেলা হবে। আমি যেকোনো সময় প্রত্যাহার করতে পারব।"
- Redaction: no real phone numbers, names, or amounts in scripts; speaker IDs are codes.
- Who collects / hours: all 3 members, 4–6 h including labelling stage tags (labels come free from the script structure).

## 2. PRECEDENT

- **Google Messages scam detection** (SMS text, on-device, Mar 2025): https://blog.google/products-and-platforms/platforms/android/new-android-features-march-2025/ (VERIFIED). Does not touch call audio.
- **Truecaller Scam Checker**: https://www.truecaller.com/scam-checker (verified in critique; not re-opened — UNVERIFIED by me). Call-ID/reputation based, not speech-content based.
- **Pindrop** (commercial, global): deepfake detection + call risk scoring for contact centers — https://www.pindrop.com/ (VERIFIED today). Enterprise-priced; no Bangla consumer product.
- **In Bangladesh: no call-speech scam-stage detector found.** But the platform constraint below limits where it can run.

## 3. LEGAL/ETHICS (not legal advice)

- **Android platform restriction (technical, not law):** since Android 10, third-party apps cannot capture call audio; the call gets the audio and ordinary apps are denied it (rules quoted in https://stackoverflow.com/questions/57822073/is-voice-call-recording-back-with-android-10-2019 ; official doc https://developer.android.com/media/platform/capture — timed out on fetch today, UNVERIFIED by me). Live on-device call capture is therefore not buildable in 48h; demo must use speakerphone→second-device mic or uploaded recordings.
- **BD recording law:** no statute requires participant consent to record one's own call; the Telecommunication Act 2001 s.71 (as substituted 2026) criminalises eavesdropping on OTHER people's conversations (up to 2 years / Tk 1.5 crore); Personal Data Protection Act 2026 requires consent/lawful basis for organisational processing (s.5) with a household-use exemption (s.24); Cyber Security Act 2026 s.25 punishes publishing recordings to blackmail/harass. Source: https://www.recordinglaw.com/world-laws/world-recording-laws/bangladesh-recording-laws/ (secondary source, self-described as checked against bdlaws.minlaw.gov.bd — treat as UNVERIFIED against primary texts).
- **Telecom Act s.70(3) (2026):** using AI to copy a person's voice to cause harm is an offense — relevant to our synthetic-audio training data (we generate generic scam voices, never clones of real people).
- Unclear: whether an MFS provider processing call audio for fraud detection needs a specific lawful basis beyond consent, and retention limits. UNVERIFIED.
- Ethics: re-enactment scripts must not teach attack skill (scripts are defensive patterns already public); recordings deleted post-hackathon unless participants opt in.

## 4. 48-HOUR BUILD PLAN

Stack: Python, faster-whisper (or a Bangla-fine-tuned Whisper from the Ben-10 model list) → text → stage classifier (fine-tuned Bangla BERT-class model on free-tier GPU, or TF-IDF+logreg fallback) → stage-sequence scorer. GPU: one free-tier Colab/Kaggle session for fine-tuning.

- H0–2: A sets up ASR pipeline (spike 02 code is the seed; swap in Bangla-fine-tuned model). B writes 4-stage script bank + consent forms, recruits re-enactors. C starts stage-classifier training data prep (scripts + SentNoB-adjacent Bangla text as auxiliary).
- H2–10: record 100–150 clips (parallel with build). A tests 2–3 ASR options on REAL re-enactment audio (the spike showed vanilla Whisper fails on script output — this is the critical path). C trains stage classifier on script text (text-side model is low-risk and can be done by H10).
- H10–24: A gets ASR→text quality ≥ usable on clean re-enactments; C wires text→stage classifier→sequence scorer (stage n-gram / small HMM). B builds demo UI: live mic → transcript → kill-chain timeline lighting up hook→authority→urgency→ask.
- H24–36: end-to-end integration, held-out speakers test, noise-robustness check (add phone-bandpass + noise). FEATURE FREEZE H36.
- H36–48: demo freeze + pitch. Fallback demo if live ASR is flaky: pre-recorded clips played through the pipeline (still real model, real audio).
- Real vs mocked: audio + ASR + classifier real; "on-device" claim mocked (runs on laptop); no live phone-call capture (platform-blocked).

## 5. SPIKE TEST

Ran: `spikes/02-killchain-listener/` (see RESULT.md). edge-tts bn-BD clips → faster-whisper CPU.
- **Result: whisper-tiny WER = 1.000 on all 3 clips (outputs Latin transliteration); whisper-small WER = 1.000 (outputs Devanagari).** Vanilla Whisper does not emit Bangla script even on clean synthetic bn-BD speech.
- PASS (pipeline): TTS→decode→transcribe→WER all work; transliteration content is partially semantically recoverable.
- FAIL (ASR quality): the default model choice is unusable for a Bangla-script stage classifier. Mitigation must be tested in the first 10h: Bangla-fine-tuned Whisper (e.g. bengaliAI's Ben-10-tuned whisper-medium, listed on https://huggingface.co/datasets/bengaliAI/Ben-10) or transliteration-normalised classification. Real-speech WER: UNVERIFIED (no real Bangla speech tested in this spike; SLR37 bn_bd.zip is 586 MB — not sampled; protocol: download, extract 5 clips, rerun spike).

## 6. BASELINE

- Non-AI baseline: keyword rules on the transcript ("পিন", "জরুরি", "অফিস থেকে" → stage keywords). Works if ASR works; dies on ASR noise and dialect.
- LLM-API baseline: GPT-class model on the transcript classifies stages near-perfectly — so the ASR, not the classifier, is the moat. If ASR works, the LLM baseline gets ~80% of the value; our trained classifier must win on noise/dialect robustness and on-device cost.
- Pointless-if number: if stage-classification accuracy on held-out re-enactments is <70% end-to-end (ASR+classifier), the demo misleads more than it protects — kill.

## 7. RISKS

1. **ASR quality on real Bangla/dialect speech** (spike shows vanilla Whisper fails): mitigation: Bangla-fine-tuned models + transliteration fallback; kill-switch to text-input mode (paste scam SMS) which reuses the same classifier. P(mitigation works): moderate.
2. **Android blocks call capture**: mitigation: demo via speakerphone/second device; pitch as "provider-side or uploaded-audio" integration. Platform fact, not fixable.
3. **Re-enactment ≠ real scam calls** (prosody, code-switching, background noise): mitigation: add noise/bandpass augmentation; state limitation.
4. **Free-tier GPU time for fine-tuning**: mitigation: text classifier is tiny (CPU-trainable); only ASR needs the big model — use existing fine-tuned checkpoints instead of training one.
5. **Demo flakiness (mic, latency)**: mitigation: pre-recorded clip fallback; feature freeze at H36 with full rehearsal.

**P(working live demo) = 0.45.** Reasoning: the spike found a real blocker (Whisper script failure) on the critical path; the fallback (text-mode classifier + pre-recorded audio through a fine-tuned ASR) is plausible but unproven on real speech; two compounding unproven steps (ASR on real speech, end-to-end latency) put this below a coin flip despite the text-side being low-risk.

## 8. RESPONSIBLE AI

- Fairness groups: dialect speakers (Sylheti/Chittagonian/Noakhali slices), gender (voice pitch vs ASR), elderly-speech pace. Report stage-classification F1 per slice; the dialect WER gap is itself a deliverable (critique's D20 component).
- Explainability: show transcript + highlighted trigger phrases + stage timeline — inherently interpretable; never a bare score.
- Security: adversarial users (scammer speaks in dialect/low volume to dodge ASR — test it); prompt injection N/A (no LLM in the decision path); data leakage (speaker-level held-out split mandatory); recordings encrypted-at-rest, deleted post-event.
- Human oversight: output is a warning + timeline for the USER or a human fraud analyst; never an automatic block.
- Transparency: synthetic re-enactment audio disclosed everywhere it is shown; no real victim audio in the demo.
