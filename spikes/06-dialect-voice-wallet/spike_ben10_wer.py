# Spike 06-dialect-voice-wallet — Ben-10 sample + whisper-tiny CPU WER (2026-10-02)
# Q: what is whisper-tiny's zero-shot WER on real Bangladeshi dialect speech (Ben-10 train rows)?
# Method: 8 wav files (~500KB each) downloaded directly from HF repo (NOT the 8.5GB full set),
# transcribed with openai/whisper-tiny via transformers on CPU, WER computed char-level + word-level.
import csv, json, urllib.request, time, re, sys

BASE = "https://huggingface.co/datasets/bengaliAI/Ben-10/resolve/main/train/folder_1/"

with open("spikes/06-dialect-voice-wallet/train.csv", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

# pick 1 file per dialect, first 8 dialects alphabetically
seen, picked = set(), []
for r in rows:
    d = r["district"]
    if d not in seen:
        seen.add(d)
        picked.append(r)
    if len(picked) == 8:
        break

for r in picked:
    fn = r["file_name"]
    out = "spikes/06-dialect-voice-wallet/" + fn.replace(" ", "_")
    urllib.request.urlretrieve(BASE + urllib.request.quote(fn), out)
    r["local"] = out
    print("downloaded", fn, r["district"])

print("\nLoading whisper-tiny (CPU)...")
t0 = time.time()
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="openai/whisper-tiny", device=-1)
print(f"loaded in {time.time()-t0:.0f}s")

def normalize(s):
    s = re.sub(r"[<>]", "", s)
    s = re.sub(r"[.,!?;:()\"'\u0964\u0965]", "", s)  # Bangla danda etc.
    return s.strip()

def wer(ref, hyp):
    r, h = normalize(ref).split(), normalize(hyp).split()
    # Levenshtein on word lists
    import functools
    d = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        prev, d[0] = d[0], i
        for j, hw in enumerate(h, 1):
            cur = min(d[j] + 1, d[j-1] + 1, prev + (rw != hw))
            prev, d[j] = d[j], cur
    return d[len(h)] / max(len(r), 1)

results = []
import soundfile as sf
import numpy as np
for r in picked:
    t0 = time.time()
    audio, sr = sf.read(r["local"], dtype="float32")
    if audio.ndim > 1: audio = audio.mean(axis=1)
    if sr != 16000:
        # crude decimation is wrong; use linear interp resample
        n_new = int(len(audio) * 16000 / sr)
        audio = np.interp(np.linspace(0, len(audio) - 1, n_new), np.arange(len(audio)), audio).astype("float32")
    out = asr({"array": audio, "sampling_rate": 16000}, generate_kwargs={"language": "bengali", "task": "transcribe"})
    w = wer(r["transcripts"], out["text"])
    results.append({"dialect": r["district"], "file": r["file_name"], "wer": round(w, 3),
                    "ref": r["transcripts"][:80], "hyp": out["text"][:80], "sec": round(time.time()-t0, 1)})
    print(f"{r['district']:12s} WER={w:.2f}  ({time.time()-t0:.1f}s)")

avg = sum(x["wer"] for x in results) / len(results)
print(f"\nMEAN WER (whisper-tiny, 8 Ben-10 dialect files, CPU): {avg:.2f}")
json.dump({"mean_wer": round(avg, 3), "per_file": results},
          open("spikes/06-dialect-voice-wallet/results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("saved spikes/06-dialect-voice-wallet/results.json")
