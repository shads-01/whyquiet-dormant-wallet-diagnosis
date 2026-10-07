# Spike 10 results — dialect ASR WER (Ben-10 valid split, zero-shot Whisper) (2026-10-02)

## Environment
- Python 3.14.6. `pip install faster-whisper` → faster-whisper 1.2.1 OK.
- PyAV incompatibility: av 19.0.0 installed; faster-whisper 1.2.1 calls `av.open(..., metadata_errors=...)` which av 19 removed; av<15 has **no cp314 wheels** → worked around by decoding WAV with stdlib `wave`+numpy and passing a 16 kHz float32 array to `model.transcribe()`.

## Data (real, downloaded)
- Ben-10 valid split: `valid.csv` (1,666 rows, real dialect transcripts) + 6 wavs (~0.5–1.9 MB each) from https://huggingface.co/datasets/bengaliAI/Ben-10 (CC0-1.0).
- Dialects covered: barishal, chittagong, habiganj, kishoreganj, narail, rangpur (valid split also contains narsingdi per file listing).

## REAL results (word-level Levenshtein WER, punctuation-stripped, 251 reference words)

| Model | Overall WER | Behaviour |
|---|---|---|
| whisper-tiny (int8, CPU) | **127.9%** | English hallucinations ("Oh no no no..."), empty output on narail |
| whisper-small (int8, CPU) | **123.1%** | Hallucinations in English/Kannada/Telugu/Chinese scripts; 100% on 4/6 clips |

Per-clip (tiny): barishal 228.6%, chittagong 100%, habiganj 100%, kishoreganj 100%, narail 100%, rangpur 136.8%.

## Interpretation
- **Zero-shot Whisper is unusable on Bangladeshi dialect speech.** WER >100% means hallucination, not just error.
- The ASR gap IS the project: any hotline-triage/callback idea must fine-tune on Ben-10 (train 13.4k rows, CC0) or use the existing fine-tuned checkpoint `bengaliAI/tugstugi_bengaliai-regional-asr_whisper-medium` (seen listed on the Ben-10 dataset page, UNVERIFIED quality) — then re-measure. Critique falsifier (intent accuracy ≥85%) cannot be met zero-shot.
- CPU inference speed: ~1–3 s per 10–20 s clip with tiny — fine for demo; small ~5–10 s/clip.

## Commands
```
pip install faster-whisper
python spikes\10-hotline-triage\spike_wer.py        # tiny
python spikes\10-hotline-triage\spike_wer_small.py  # small
```
