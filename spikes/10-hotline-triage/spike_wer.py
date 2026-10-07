# Spike 10/11: whisper-tiny (faster-whisper) WER on 6 Ben-10 dialect wavs
# Run: python spike_wer.py   (first run downloads ~75MB model)
import csv, io, sys, time, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from faster_whisper import WhisperModel

FILES = [
    ("barishal",    "valid_barishal (1).wav"),
    ("chittagong",  "valid_chittagong (1).wav"),
    ("habiganj",    "valid_habiganj (1).wav"),
    ("kishoreganj", "valid_kishoreganj (1).wav"),
    ("narail",      "valid_narail (1).wav"),
    ("rangpur",     "valid_rangpur (1).wav"),
]

def norm(s):
    s = re.sub(r"[<>.,!?;:()\[\]\"'।]", " ", s)
    return " ".join(s.split())

truth = {}
for r in csv.DictReader(open(r"spikes\10-hotline-triage\valid.csv", encoding="utf-8")):
    truth[r["file_name"]] = r["transcripts"]

def load_wav(path):
    # stdlib decode (PyAV 19 incompatible with faster-whisper 1.2.1 on py3.14)
    import wave, numpy as np
    w = wave.open(path, "rb")
    n = w.getnframes(); ch = w.getnchannels(); sw = w.getsampwidth(); sr = w.getframerate()
    raw = w.readframes(n); w.close()
    import struct
    if sw == 2:
        a = np.array(struct.unpack(f"<{n*ch}h", raw), dtype=np.float32) / 32768.0
    elif sw == 4:
        a = np.array(struct.unpack(f"<{n*ch}i", raw), dtype=np.float32) / 2147483648.0
    else:
        raise SystemExit(f"unsupported sample width {sw}")
    if ch > 1: a = a.reshape(-1, ch).mean(axis=1)
    return a, sr

t0 = time.time()
model = WhisperModel("tiny", device="cpu", compute_type="int8")
print(f"model loaded in {time.time()-t0:.1f}s")

tot_ref, tot_err = 0, 0
per = {}
for district, fn in FILES:
    ref = norm(truth[fn])
    audio, sr = load_wav(rf"spikes\10-hotline-triage\audio\{fn}")
    if sr != 16000:  # linear resample to 16k (whisper requirement)
        import numpy as np
        n_out = int(len(audio) * 16000 / sr)
        audio = np.interp(np.linspace(0, len(audio)-1, n_out), np.arange(len(audio)), audio).astype(np.float32)
    t1 = time.time()
    segs, info = model.transcribe(audio, language="bn")
    hyp = norm(" ".join(s.text for s in segs))
    dt = time.time() - t1
    # token-level edit distance (Levenshtein on words)
    r_w, h_w = ref.split(), hyp.split()
    import functools
    @functools.lru_cache(None)
    def lev(i, j):
        if i == 0: return j
        if j == 0: return i
        return min(lev(i-1, j)+1, lev(i, j-1)+1, lev(i-1, j-1)+(r_w[i-1] != h_w[j-1]))
    err = lev(len(r_w), len(h_w))
    tot_ref += len(r_w); tot_err += err
    per[district] = (err / max(1, len(r_w)) * 100, len(r_w), dt)
    print(f"{district:12s} WER {err/max(1,len(r_w))*100:6.1f}%  (ref {len(r_w)} words, {dt:.1f}s)")
    print(f"   HYP: {hyp[:100]}")

print(f"\nOVERALL WER (whisper-tiny, 6 dialect clips): {tot_err/max(1,tot_ref)*100:.1f}%  over {tot_ref} words")
