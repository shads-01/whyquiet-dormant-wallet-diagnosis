# Spike 02 result — Bangla ASR for kill-chain listener

Date: 2026-10-02. Environment: Windows, Python 3.14 venv, faster-whisper 1.2.1 (CPU, int8), edge-tts bn-BD neural voices.

## What was run
- `spike_asr.py`: synthesized 3 short Bangla (bn-BD) clips with edge-tts (Pradeep = male, Nabanita = female voices) representing scam stages (authority / urgency+ask / neutral), decoded to 16 kHz mono via PyAV, transcribed with faster-whisper **tiny**, computed word error rate against the known reference text.
- `spike_asr_small.py`: same urgency clip with faster-whisper **small**.

## Real numbers

| model | clip | WER vs Bangla script | output script |
|---|---|---|---|
| tiny | authority | 1.000 | Latin transliteration ("Assalamu alaikum, ami upa'i office teke bolchi...") |
| tiny | urgency+ask | 1.000 | Latin transliteration ("Joruri, 5 minute mode pin number din...") |
| tiny | neutral | 1.000 | Latin transliteration |
| small | urgency+ask | 1.000 | **Devanagari** ("जोरुरी, पाच मिनिटर मद्धे पीन नमबर दिन...") |

Mean WER (tiny, 3 clips): **1.000**. Full outputs in `RESULT.json`.

## Interpretation (this is the important finding)
- Whisper tiny and small both FAIL to emit Bangla script on clean synthetic bn-BD speech: tiny outputs Latin transliteration, small outputs Devanagari. Content is partially recognizable in transliteration, but a Bangla-script stage classifier cannot consume this directly.
- Consequence for the 48h plan: vanilla Whisper is NOT a drop-in Bangla ASR. Options: (a) use a Bangla-fine-tuned model (e.g. bengaliAI's Ben-10-fine-tuned whisper-medium, listed on the Ben-10 HF page: https://huggingface.co/datasets/bengaliAI/Ben-10 → "Models trained or fine-tuned on"), (b) normalize transliteration/Devanagari back to Bangla before classification, or (c) classify stages on the transliteration directly. Each must be re-tested on real speech.
- Caveats: audio is synthetic TTS (clean, studio-quality); real scam calls are noisy, compressed, dialectal — WER will be worse. n=3 clips, ~10 s total. This is a pipeline connectivity check, not a WER benchmark.

## Environment notes (for the 48h build)
- Python 3.14 has no PyAV wheels <19; faster-whisper 1.2.1 passes a kwarg removed in av≥14. Workaround used: decode audio with av 19 directly and pass a float32 numpy array to `model.transcribe()` (see `load_audio_16k` in spike_asr.py). On the hackathon GPU (Linux) this is a non-issue, but on Windows pin `av==12.3.0` under Python ≤3.12 or reuse this workaround.
- Windows console needs `sys.stdout.reconfigure(encoding="utf-8")` to print Bangla.

## Reproduce
```
python spike_asr.py
python spike_asr_small.py
```
