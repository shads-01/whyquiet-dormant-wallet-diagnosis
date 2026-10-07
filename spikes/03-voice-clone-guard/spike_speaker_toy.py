# Spike 03 (voice-clone guard): TOY speaker-distance connectivity check.
# Uses two distinct bn-BD neural TTS voices (Pradeep=male, Nabanita=female) as
# stand-in "speakers". Computes log-mel spectral features (numpy only) and cosine
# distance for: same-voice pair (different sentences) vs cross-voice pair (same sentence).
# NOT evidence about real anti-spoofing performance. ASVspoof 5 itself requires
# registration (https://www.asvspoof.org/) — download NOT attempted; protocol in doc.
import asyncio, json, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
import edge_tts

OUT = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(OUT, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

SENT_A = "আমি উপায় অফিস থেকে বলছি, আপনার একাউন্ট ভেরিফাই করতে হবে।"
SENT_B = "কাল সকালে বাজার থেকে চাল আনতে ভুলবেন না।"

CLIPS = {
    "pradeep_A.mp3": ("bn-BD-PradeepNeural", SENT_A),
    "nabanita_A.mp3": ("bn-BD-NabanitaNeural", SENT_A),
    "pradeep_B.mp3": ("bn-BD-PradeepNeural", SENT_B),
}

async def synth():
    for fname, (voice, text) in CLIPS.items():
        p = os.path.join(AUDIO_DIR, fname)
        if not os.path.exists(p):
            await edge_tts.Communicate(text, voice).save(p)

def load_16k(path):
    import av
    container = av.open(path)
    resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)
    chunks = []
    for frame in container.decode(audio=0):
        for rf in resampler.resample(frame):
            arr = rf.to_ndarray()
            if arr.ndim == 2:
                arr = arr.mean(axis=0)
            chunks.append(arr.ravel())
    return np.concatenate(chunks).astype(np.float32) / 32768.0

def logmel(x, n_mels=24, frame=400, hop=160):
    # crude log-mel: FFT power -> triangular mel-ish band energies -> log
    frames = [x[i:i+frame] * np.hanning(frame) for i in range(0, len(x)-frame, hop)]
    spec = np.abs(np.fft.rfft(np.stack(frames), axis=1)) ** 2
    nb = spec.shape[1]
    edges = np.linspace(0, nb, n_mels + 1).astype(int)
    bands = np.stack([spec[:, edges[i]:edges[i+1]].mean(axis=1) for i in range(n_mels)], axis=1)
    return np.log(bands + 1e-8)

def embed(path):
    x = load_16k(path)
    return logmel(x).mean(axis=0)

def cos(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def main():
    asyncio.run(synth())
    e = {k: embed(os.path.join(AUDIO_DIR, k)) for k in CLIPS}
    same = cos(e["pradeep_A.mp3"], e["pradeep_B.mp3"])      # same voice, different sentence
    cross = cos(e["pradeep_A.mp3"], e["nabanita_A.mp3"])    # different voice, same sentence
    out = {"same_voice_cosine": round(same, 3), "cross_voice_cosine": round(cross, 3),
           "margin": round(same - cross, 3)}
    print(json.dumps(out))
    with open(os.path.join(OUT, "RESULT.json"), "w") as f:
        json.dump(out, f, indent=2)

if __name__ == "__main__":
    main()
