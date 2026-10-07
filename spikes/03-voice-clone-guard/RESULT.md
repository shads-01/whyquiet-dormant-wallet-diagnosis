# Spike 03 result — voice-clone guard toy speaker-distance check

Date: 2026-10-02. Environment: Windows, Python 3.14 venv, numpy-only spectral features.

## What was run
`spike_speaker_toy.py`: two distinct bn-BD neural TTS voices (edge-tts Pradeep = male, Nabanita = female) as stand-in "speakers". Crude log-mel band-energy embeddings (24 bands, mean over time), cosine similarity for:
- same-voice pair (Pradeep sentence A vs Pradeep sentence B)
- cross-voice pair (Pradeep sentence A vs Nabanita sentence A)

## Real numbers
```
same_voice_cosine:  0.999
cross_voice_cosine: 0.996
margin:             0.003
```

## Interpretation
- NEGATIVE result: naive mean log-mel embeddings do NOT separate even a male vs female voice (margin 0.003). Mean-pooling destroys speaker information.
- Lesson for the 48h build: a real speaker-verification / anti-spoof model (x-vector / ECAPA-TDNN / AASIST, e.g. via speechbrain pretrained checkpoints) is mandatory; hand-rolled spectral features are dead on arrival. This raises the compute and integration cost of idea 3 and is reflected in its P(demo).
- ASVspoof 5 itself was NOT downloaded: it requires registration/login at https://www.asvspoof.org/ (verified: the site shows "Download" behind login). Protocol documented in docs/04-feasibility/03-voice-clone-guard.md §5.
- All audio here is synthetic TTS — no claim about real speakers, real clones, or Bangla codecs is made.

## Reproduce
```
python spike_speaker_toy.py
```
