# 03-voice-clone-guard.md — Feasibility: Coercion Shield (c) "Voice-clone guard, dialect-fair"

Anti-spoofing (is this voice synthetic?) + speaker verification (is this the enrolled person?), calibrated so dialect speakers are not misclassified. Track 01. Status: DATA ACCESS BLOCKED AT THE CRITICAL DATASET; fairness slice is the only defensible sliver (per critique).

## 1. DATA REALITY

**Public datasets:**

| Dataset | URL | Size | Language | Licence | Hackathon use | Friction |
|---|---|---|---|---|---|---|
| ASVspoof 5 | https://www.asvspoof.org/ (download behind login at /database) | large (multi-GB) | en/multilingual | research registration | Yes in principle | **Registration/login required — NOT downloaded in this research pass**; licence terms unread: UNVERIFIED |
| Ben-10 | https://huggingface.co/datasets/bengaliAI/Ben-10 | 15,036 rows / 8.52 GB | bn, 10 BD dialects | CC0-1.0 (stated on page) | Yes — bona-fide dialect speech | Direct download; viewer broken (CastError) |
| OpenSLR SLR37 TTS | https://www.openslr.org/37/ | bn_bd.zip 586 MB | bn-BD | CC BY-SA 4.0 (stated on page) | Yes — synthetic "spoof" side (TTS, not clones) | Direct download; size manageable on GPU box, not sampled here |
| VoxCeleb 1/2 | https://www.robots.ox.ac.uk/~vgg/data/voxceleb/ | 2000+ h | en | form-gated academic | Marginal | Form + password — skip in 48h |

**Key gap:** ASVspoof 5 is English/multilingual-centric; no public Bangla spoof corpus exists. The dialect-fairness claim rests on self-collected data.

**Self-collected: dialect voice set (S3) + toy "clone" attacks.**
- Sample size: 15–25 speakers across ≥3 dialects (Sylheti, Chittagonian, Noakhali) + standard Bangla controls; 8–10 short utterances each (fixed phrases + free sentences); ≈1–1.5 h audio. Enrollment utterances vs verification utterances split per speaker.
- Spoof side for the demo: SLR37 TTS audio + edge-tts bn-BD voices + a consumer voice-cloning tool applied to ONE team member's own voice (self-consent only) — clearly labelled synthetic.
- Protocol: quiet room, phone mic, 16 kHz; each speaker reads the same phrase bank so cross-dialect comparison is controlled.
- Consent wording:
  - English: "I agree to have my voice recorded for a voice-verification research prototype. Recordings stay on the team's devices, are used only for this project, are never published, and will be deleted after the hackathon. Voice is biometric data; I can withdraw and have my recordings deleted at any time."
  - Bangla: "আমি ভয়েস-যাচাই গবেষণার জন্য আমার কণ্ঠস্বর রেকর্ড করতে সম্মত। রেকর্ডিং শুধু দলের ডিভাইসে থাকবে, শুধু এই প্রজেক্টে ব্যবহৃত হবে, কখনো প্রকাশ করা হবে না, এবং হ্যাকাথন শেষে মুছে ফেলা হবে। কণ্ঠস্বর বায়োমেট্রিক তথ্য; আমি যেকোনো সময় প্রত্যাহার ও মুছে ফেলার অনুরোধ করতে পারব।"
- Redaction: speaker codes only; no names attached to audio files.
- Who collects / hours: all 3 members, 4–6 h.

## 2. PRECEDENT

- **Pindrop** (global, commercial): synthetic-speech detection (Pulse) + caller authentication (Passport) for contact centers; claims 14 of top 20 banks as customers — https://www.pindrop.com/ (VERIFIED today). Enterprise-priced, English-centric deployment; no BD consumer product found.
- **Nuance/other voice-biometrics vendors**: existence known from memory — UNVERIFIED (not opened today).
- **ASVspoof challenge series** defines the research state of the art — https://www.asvspoof.org/ (VERIFIED).
- **In Bangladesh: no voice-clone-guard product found.** But per critique: "upay asks why we need this before BB mandates it" — the honest-no stands.

## 3. LEGAL/ETHICS (not legal advice)

- **Voiceprints are biometric personal data** under the Personal Data Protection Act 2026 (Act No. 63 of 2026) — its biometric definition expressly lists voiceprints (per https://www.recordinglaw.com/world-laws/world-recording-laws/bangladesh-recording-laws/, secondary source — UNVERIFIED against the Act text). Consent (s.5) required; our written consent form above is mandatory, not optional.
- **Telecommunication Act 2001 s.70(3) (2026 substitution):** AI imitation of a person's voice to cause harm is an offense (fine up to Tk 1 lakh) — our demo must clone only a consenting team member's voice and must say so on-screen.
- **Cyber Security Act 2026 s.25:** publishing harmful synthetic content — we publish nothing.
- **BB rules on biometric authentication factors:** whether voice is a permitted auth factor for MFS is UNVERIFIED — check Bangladesh Bank circulars (https://www.bb.org.bd) before pitching integration.
- Unclear: cross-border transfer of voice embeddings (s.29 PDPA) if we use overseas GPU/cloud — prefer on-device/local inference in the demo.
- Not legal advice; confirm with a Bangladeshi advocate before any deployment claim.

## 4. 48-HOUR BUILD PLAN

Stack: Python, speechbrain pretrained ECAPA-TDNN (speaker verification) + an anti-spoofing checkpoint (AASIST/RAWNet from ASVspoof literature, if downloadable) on free-tier GPU; calibration layer in sklearn.

- H0–2: A registers for ASVspoof 5 (may be instant or delayed — if delayed, proceed with SLR37-TTS + edge-tts as the synthetic side and say so). B writes consent forms, recruits 15–25 dialect speakers. C sets up speechbrain + tests pretrained checkpoints on CPU/GPU.
- H2–10: record dialect set. A runs pretrained speaker-verification on our speakers (zero-shot baseline EER). C runs pretrained anti-spoof on TTS-vs-real pairs.
- H10–24: C calibrates score thresholds per dialect slice; measures EER per dialect (the falsifier: held-out dialect EER ≤2× clean-speech EER). A builds demo: judge's voice enrollment (30 s) → verification verdict; clone attack (TTS of a teammate) → spoof verdict. B builds UI + fairness-slice chart.
- H24–36: integration, threshold tuning, failure-mode rehearsal. FEATURE FREEZE H36.
- H36–48: demo freeze + pitch: live judge enrollment + clone attack + fairness table. Fallback: pre-recorded judge audio.
- Real vs mocked: verification/spoof models real (pretrained, calibrated on our data); "production MFS integration" mocked; ASVspoof-scale training NOT attempted (data gated).

## 5. SPIKE TEST

- **ASVspoof 5: NOT downloaded — requires registration/login at https://www.asvspoof.org/ (verified: download page is behind login). Protocol: register (1 person), accept research terms, download LA training subset, run a pretrained AASIST-style checkpoint, report EER. Marked UNVERIFIED — do not attempt during the 48h build; use TTS-vs-real self-collected pairs instead.**
- Ran: `spikes/03-voice-clone-guard/spike_speaker_toy.py` (see RESULT.md): two bn-BD neural voices, numpy log-mel embeddings.
- **Result: same-voice cosine 0.999 vs cross-voice 0.996 — margin 0.003. NEGATIVE: naive spectral features do not separate even male vs female voices.**
- PASS (pipeline): audio synthesis, decoding, feature extraction run end-to-end.
- FAIL (feature adequacy): proves a real pretrained model (ECAPA/x-vector + anti-spoof CM) is mandatory — no hand-rolled shortcut exists. This is the spike's actual value: it kills the "just use simple features" plan before the hackathon.

## 6. BASELINE

- Non-AI baseline: knowledge-based verification (security questions / registered-number callback) — the incumbent policy per critique; imposter success ~100% against social engineering in drills (critique's number for Spoof-Proof Hotline Callback).
- LLM-API baseline: not applicable (audio modality).
- Pointless-if number: if held-out dialect-speaker EER is >2× the clean-speech EER (critique's falsifier), the "dialect-fair" claim is dead and the idea collapses into an existing commercial product with no differentiator — kill.

## 7. RISKS

1. **ASVspoof 5 access friction** (registration, multi-GB, licence unread): mitigation: skip it; use SLR37/edge-tts synthetic side + self-collected bona-fide speech; disclose that the spoof detector is trained on TTS, not clones. P(demo without ASVspoof): high.
2. **Pretrained anti-spoof models transfer poorly to Bangla codecs/noise** (critique's mechanism): mitigation: calibrate on our data, report per-slice EER honestly; if it fails, the fairness FAILURE CHART is still a demoable responsible-AI artifact (pivot: "we measured the gap").
3. **Small speaker count (15–25) makes EER estimates noisy**: mitigation: report confidence intervals; use fixed phrase sets to reduce variance.
4. **Biometric-data ethics**: voiceprints are sensitive; mitigation: written consent, local storage, deletion commitment, no publication.
5. **Live demo variance (mic, room noise, judge's voice)**: mitigation: rehearse enrollment flow; pre-recorded fallback; feature freeze H36.

**P(working live demo) = 0.55.** Reasoning: pretrained speaker-verification is mature and works zero-shot (high confidence); the spoof side is demoable with TTS attacks; deductions for (a) unproven transfer of anti-spoof models to Bangla audio, (b) ASVspoof data gated (weaker training story), (c) live biometric demos are inherently flaky. The fairness-slice chart is the most reliable part of the demo.

## 8. RESPONSIBLE AI

- Fairness groups: dialect (Sylheti/Chattogram/Noakhali/standard), gender, age, mic quality. The per-dialect EER table IS the responsible-AI deliverable.
- Explainability: verdict + score + which slice calibration applied ("Sylheti-calibrated threshold"); anti-spoof score with attack-type guess (TTS vs replay) where possible.
- Security: adversarial users (replay attacks, TTS with our own training voices — test both); data leakage (speaker-level splits); voiceprint storage encrypted, local-only; no voice data leaves the demo machine.
- Human oversight: verdict is advisory to a human operator/step-up flow; never an automatic account action.
- Transparency: synthetic attack audio labelled on-screen; consent forms shown in the pitch; deletion commitment stated.
