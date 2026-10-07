# 11-hotline-callback.md — Feasibility: Spoof-Proof Hotline Callback (2026-10-02)

**Idea (D31, critique survivor #9):** hotline callbacks verify the caller via liveness + dialect-tuned anti-spoof + knowledge facts before any account action. ASVspoof 5 (S17) + self dialect voices (S3) + FLEURS bn_in (S18, weak). Track 01/06.

## 1. DATA REALITY

| Source | URL | Size | Language | Licence | Hackathon use | Download friction | Status |
|---|---|---|---|---|---|---|---|
| ASVspoof 5 | https://www.asvspoof.org/ (download at /database) | large (multi-GB) | en/multilingual | research registration | training only | **login/registration required** (verified: site shows Download → login; challenge registration windows 2023–2024) | VERIFIED (page opened; data NOT downloaded) |
| Self-collected dialect voices | n/a | ~10 speakers × 3–5 clips + attack set | bn dialects | own (consent) | yes — eval | recruit family/classmates | planned |
| FLEURS bn_in | https://huggingface.co/datasets/google/fleurs | ~4.3k rows | bn-IN (Indian Bengali — weak fit) | CC-BY-4.0 | marginal | direct | VERIFIED (inventory) |

**Self-collection protocol:** 10 speakers (2 dialect groups minimum), 3 enrollment clips each on phone mic. Attack set built by a teammate the modeler never talks to: (a) replay attack — enrolled clip played through a phone speaker, re-recorded; (b) imposter speaker; (c) one disclosed synthetic/voice-clone clip if a free tool allows. Consent wording — Bangla: "আমি স্বেচ্ছায় আমার কণ্ঠস্বরের নমুনা দিচ্ছি, শুধু ছাত্র প্রোটোটাইপের জন্য। এটি অন্য কোথাও ব্যবহার হবে না।" English: "I voluntarily provide my voice samples for a student prototype only. They will not be used elsewhere." Biometric data → PDPO 2025 sensitive class; delete after event. Collectors: 3 members, ~2–3 h.

## 2. PRECEDENT

- **bKash 16247 + live chat 24/7** — VERIFIED via official-page search snippets (direct fetch 403): https://www.bkash.com/en/customer-service/contact-us . Callback verification practice in BD MFS: registered-number policy; detailed callback-verification procedures UNVERIFIED (internal ops).
- **Commercial voice-biometrics with anti-spoof** (Nuance/Pindrop-class, banks worldwide) — exists globally; UNVERIFIED specifics; none published for Bangla dialects.
- **ASVspoof challenge series** — the research baseline; English/multilingual, no Bangla — VERIFIED (site).
- **Plainly:** nothing in Bangladesh publishes dialect-fair anti-spoof; but also no documented BD hotline-callback fraud wave — the problem's BD prevalence is UNVERIFIED (critique #9: fraudsters call *out*, not in — the honest-no stands).

## 3. LEGAL/ETHICS (not legal advice)

- **Biometric/voice data:** Personal Data Protection Ordinance 2025 (gazetted 6 Nov 2025) — first standalone BD data law; voice as personal data; consent + purpose limitation required — https://www.thedailystar.net/tech-startup/news/bangladeshs-personal-data-protection-ordinance-2025-key-takeaways-4015401 ; https://bd-scl.com/insights/personal-data-protection-ordinance-2025-compliance.html . Whether voice templates are a "sensitive/biometric" subclass with extra duties: UNVERIFIED.
- **BB rules on authentication factors:** whether speaker verification is a permitted factor for account actions — UNVERIFIED (MFS Regulations 2022 PDF not read: https://www.bb.org.bd/mediaroom/circulars/psd/feb152022psd04e.pdf).
- **Synthetic voice disclosure:** creating a clone clip for the attack set — label it synthetic, consent of the voice owner, never publish. BTRC/ICT-law angle on synthetic voice UNVERIFIED.
- **Call recording:** as in doc 10 — self-recording lawful per third-party source (UNVERIFIED against acts): https://www.recordinglaw.com/world-laws/world-recording-laws/bangladesh-recording-laws/
- **Unclear:** liability if the system wrongly rejects a genuine customer mid-fraud; that failure mode must route to human review.

## 4. 48-HOUR BUILD PLAN

Stack: Python; speaker embeddings from a small pretrained model (e.g., ECAPA via speechbrain — installability on py3.14 UNVERIFIED, fallback resemblyzer); liveness = spectral/replay heuristics; knowledge facts = 2 questions from a mock profile DB; FastAPI + browser mic "callback simulator".

- H0–6: A collects 10-speaker enrollment + attack set (attack builder isolated); B builds callback simulator UI (verdict card: liveness / speaker-match / facts, each with reason); C integrates speaker-embedding scoring + calibrates thresholds.
- H6–18: C adds dialect-slice evaluation (EER per speaker/dialect); A builds the red-team drill harness (10 attempts, logged); B wires the mock "account action" gate (verdict gates a mock PIN change).
- H18–30: full drill: baseline policy (registered-number-only) vs our gate; measure imposter success rate + genuine acceptance; fairness table.
- H30–36: **feature freeze.** H36–48: judge live red-team moment (judge plays imposter), rehearsal, pitch.

## 5. SPIKE TEST — protocol only (no numeric result)

See spikes/11-hotline-callback/RESULTS.md. ASVspoof 5 NOT downloaded (registration friction verified on site). No anti-spoof number exists yet. Reused real evidence from spike 10: zero-shot Whisper WER **127.9% (tiny) / 123.1% (small)** on Ben-10 dialect clips — transcript-based knowledge verification is unreliable for dialect callers unless ASR is fine-tuned first. Pass/fail bar for the build: imposter success <20% in a 10-attempt drill with genuine acceptance ≥90%; worst-dialect EER ≤2× clean EER.

## 6. BASELINE

Incumbent baseline: **registered-number-only callback policy** — costs nothing, and in the drill imposters succeed ~100% against it (critique #9 falsifier framing). LLM-API baseline: none meaningful for liveness. **Pointless-if number:** if our gate's imposter success stays >50% (i.e., barely better than the policy) or genuine acceptance <80% (locks out real customers), the idea is dead — a verification gate that fails both directions is worse than the policy.

## 7. RISKS

1. **Problem prevalence UNVERIFIED in BD** — hotline callback fraud may be rare; judges ask "why now?". Mitigation: frame as forward-looking defense + cite regional deepfake-voice scam reporting (A20, UNVERIFIED for BD).
2. **Anti-spoof transfer failure** — models trained on ASVspoof (English) may fail on Bangla codecs/noise; fairness slice may expose it. Mitigation: calibrate on self-collected dialect voices; publish the per-slice EER honestly.
3. **Knowledge facts are socially engineerable** (critique #9). Mitigation: facts are a second factor, never the only one; liveness+speaker must also pass.
4. **False rejection of genuine distressed customers** — worst failure mode. Mitigation: fail-open to human agent with extra questions, never auto-block.
5. **Biometric consent/retention** — PDPO 2025 class. Mitigation: explicit written consent, on-device-style processing, delete after event.

**P(working live demo) = 0.40.** The drill harness and gate UI are easy; the anti-spoof model working on Bangla phone audio in 48h is a real research gamble, and the problem's prevalence is unproven.

## 8. RESPONSIBLE AI

- **Fairness groups:** per-dialect and per-gender EER/acceptance table; a gate that fails dialect speakers is an exclusion machine — measured, not asserted.
- **Explainability:** verdict card shows three independent signals (liveness score, speaker similarity, facts passed/failed) — never a single opaque score.
- **Security:** this IS a security product; red-team drill is the evaluation; threats include replay, cloning, imposter, and coercion of the genuine user (gate cannot detect coercion — say so); data leakage: enrollment audio isolated, attack builder blind to thresholds.
- **Human oversight:** verdict only gates; a human agent approves any account action; rejected customers get a human path.
