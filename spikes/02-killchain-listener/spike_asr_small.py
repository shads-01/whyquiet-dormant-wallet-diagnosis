# Follow-up: does whisper-small emit Bangla script where tiny emits Latin transliteration?
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spike_asr import load_audio_16k, wer, AUDIO_DIR, CLIPS

from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
fname, _, ref, stage = CLIPS[1]  # urgency+ask clip
t0 = time.time()
audio = load_audio_16k(os.path.join(AUDIO_DIR, fname))
segments, info = model.transcribe(audio, language="bn")
hyp = " ".join(s.text for s in segments).strip()
w = wer(ref, hyp)
print(json.dumps({"model": "small", "file": fname, "wer": round(w, 3),
                  "ref": ref, "hyp": hyp, "sec": round(time.time()-t0, 1)},
                 ensure_ascii=False))
