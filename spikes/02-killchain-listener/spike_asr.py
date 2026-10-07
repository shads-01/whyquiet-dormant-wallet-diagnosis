# Spike 02: Bangla ASR connectivity check for the kill-chain listener idea.
# Generates 3 short Bangla (bn-BD) TTS clips with edge-tts (two distinct neural voices),
# transcribes them with faster-whisper "tiny" on CPU, and computes WER against the known text.
# NOTE: TTS audio is synthetic. This is a PIPELINE CHECK, not evidence about real scam calls.
import asyncio, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import edge_tts

OUT = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(OUT, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

CLIPS = [
    # (file, voice, text, stage)
    ("hook_authority.mp3", "bn-BD-PradeepNeural",
     "আসসালামু আলাইকুম, আমি উপায় অফিস থেকে বলছি। আপনার একাউন্ট ভেরিফাই করতে হবে।",
     "authority"),
    ("urgency_ask.mp3", "bn-BD-NabanitaNeural",
     "জরুরি! পাঁচ মিনিটের মধ্যে পিন নম্বর দিন, নাহলে একাউন্ট বন্ধ হয়ে যাবে।",
     "urgency+ask"),
    ("neutral.mp3", "bn-BD-PradeepNeural",
     "আজ বিকালে বাজার থেকে চাল আনতে ভুলবেন না।",
     "neutral"),
]

async def synth():
    for fname, voice, text, _ in CLIPS:
        path = os.path.join(AUDIO_DIR, fname)
        await edge_tts.Communicate(text, voice).save(path)
        print(f"synthesized {fname} ({os.path.getsize(path)} bytes)")

def normalize(s):
    s = re.sub(r"[^\u0980-\u09FF\s]", "", s)  # keep Bangla block + spaces
    return " ".join(s.split())

def wer(ref, hyp):
    r, h = normalize(ref).split(), normalize(hyp).split()
    # Levenshtein on word lists
    d = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        prev, d[0] = d[0], i
        for j, hw in enumerate(h, 1):
            cur = min(d[j] + 1, d[j-1] + 1, prev + (rw != hw))
            prev, d[j] = d[j], cur
    return d[len(h)] / max(1, len(r))

def load_audio_16k(path):
    # av>=14 removed the metadata_errors kwarg faster-whisper 1.2.1 passes,
    # so decode with av directly and hand whisper a float32 numpy array.
    import av
    import numpy as np
    container = av.open(path)
    resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)
    chunks = []
    for frame in container.decode(audio=0):
        for rf in resampler.resample(frame):
            arr = rf.to_ndarray()
            if arr.ndim == 2:
                arr = arr.mean(axis=0)  # collapse channels
            chunks.append(arr.ravel())
    if not chunks:
        return np.zeros(0, dtype=np.float32)
    pcm = np.concatenate(chunks).astype(np.float32) / 32768.0
    return pcm

def main():
    asyncio.run(synth())
    from faster_whisper import WhisperModel
    t0 = time.time()
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    print(f"model load: {time.time()-t0:.1f}s")
    results = []
    for fname, _, text, stage in CLIPS:
        t0 = time.time()
        audio = load_audio_16k(os.path.join(AUDIO_DIR, fname))
        segments, info = model.transcribe(audio, language="bn")
        hyp = " ".join(s.text for s in segments)
        w = wer(text, hyp)
        results.append({"file": fname, "stage": stage, "wer": round(w, 3),
                        "ref": text, "hyp": hyp.strip(),
                        "lang_prob": round(getattr(info, "language_probability", 0) or 0, 2),
                        "sec": round(time.time()-t0, 1)})
        print(json.dumps(results[-1], ensure_ascii=False))
    with open(os.path.join(OUT, "RESULT.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    mean_wer = sum(r["wer"] for r in results) / len(results)
    print(f"MEAN WER (tiny, synthetic bn-BD TTS): {mean_wer:.3f}")

if __name__ == "__main__":
    main()
