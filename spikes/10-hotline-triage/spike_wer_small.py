# Spike 10b: whisper-small WER on same 6 Ben-10 dialect clips
import csv, io, sys, functools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from faster_whisper import WhisperModel
import numpy as np, wave, struct, re

def load_wav(path):
    w = wave.open(path, "rb"); n = w.getnframes(); ch = w.getnchannels()
    sw = w.getsampwidth(); sr = w.getframerate()
    raw = w.readframes(n); w.close()
    if sw == 2:
        a = np.array(struct.unpack(f"<{n*ch}h", raw), dtype=np.float32) / 32768.0
    elif sw == 4:
        a = np.array(struct.unpack(f"<{n*ch}i", raw), dtype=np.float32) / 2147483648.0
    else:
        raise SystemExit(f"unsupported sample width {sw}")
    if ch > 1: a = a.reshape(-1, ch).mean(axis=1)
    if sr != 16000:
        n_out = int(len(a) * 16000 / sr)
        a = np.interp(np.linspace(0, len(a)-1, n_out), np.arange(len(a)), a).astype(np.float32)
    return a

def norm(s): return " ".join(re.sub(r"[<>.,!?;:()\[\]\"'।]", " ", s).split())

truth = {r["file_name"]: r["transcripts"] for r in csv.DictReader(open(r"spikes\10-hotline-triage\valid.csv", encoding="utf-8"))}
FILES = [("barishal","valid_barishal (1).wav"),("chittagong","valid_chittagong (1).wav"),
         ("habiganj","valid_habiganj (1).wav"),("kishoreganj","valid_kishoreganj (1).wav"),
         ("narail","valid_narail (1).wav"),("rangpur","valid_rangpur (1).wav")]

model = WhisperModel("small", device="cpu", compute_type="int8")
tr, te = 0, 0
for d, fn in FILES:
    ref = norm(truth[fn])
    hyp = norm(" ".join(s.text for s in model.transcribe(load_wav(rf"spikes\10-hotline-triage\audio\{fn}"), language="bn")[0]))
    rw, hw = ref.split(), hyp.split()
    @functools.lru_cache(None)
    def lev(i, j):
        if i == 0: return j
        if j == 0: return i
        return min(lev(i-1,j)+1, lev(i,j-1)+1, lev(i-1,j-1)+(rw[i-1] != hw[j-1]))
    e = lev(len(rw), len(hw)); tr += len(rw); te += e
    print(f"{d:12s} WER {e/max(1,len(rw))*100:6.1f}%  HYP: {hyp[:80]}")
print(f"OVERALL whisper-small WER: {te/max(1,tr)*100:.1f}% over {tr} words")
