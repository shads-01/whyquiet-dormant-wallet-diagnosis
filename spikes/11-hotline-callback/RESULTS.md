# Spike 11 results — Spoof-Proof Hotline Callback (2026-10-02)

## What ran
NOTHING model-side. ASVspoof 5 requires registration/login (verified: https://www.asvspoof.org/ shows Download → /database behind `user/login`; registration deadlines for the challenge phases were 2023–2024). No download attempted, per plan.

## Reused real evidence from spike 10
- Zero-shot whisper-tiny/small WER on Ben-10 dialect clips: **127.9% / 123.1%** (see spikes/10-hotline-triage/RESULTS.md). Any transcript-based knowledge-fact verification inherits this failure on dialect callers.

## Liveness/anti-spoof evaluation protocol (for the 48h build, no ASVspoof download)
1. Enroll 5–10 consenting speakers (teammates + family), 3 clips each, phone mic.
2. Attack set: (a) replay of an enrolled clip through a phone speaker recorded by another phone; (b) a different speaker imitating; (c) optionally one TTS/voice-clone clip (disclose synthetic origin).
3. Baseline policy: registered-number-only callback → imposter success expected ~100% in drill (critique #9 falsifier).
4. Model: speaker-embedding cosine (e.g., a small ECAPA/x-vector checkpoint) + simple liveness features (spectral flatness of replay) + 2 knowledge facts. Metric: imposter success rate in a 10-attempt drill; pass if <20% while genuine-user acceptance ≥90%.
5. Fairness slice: EER per dialect speaker; pass if worst-slice EER ≤2× clean-speech EER (critique #6 falsifier).

## Status
Protocol only — no numeric result. All anti-spoof performance claims UNVERIFIED until the drill is run.
