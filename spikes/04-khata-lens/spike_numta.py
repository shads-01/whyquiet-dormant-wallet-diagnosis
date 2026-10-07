# Spike 04 (Khata Lens): NumtaDB connectivity + minimal digit-recognition baseline.
# Downloads a small sample of training-a PNGs from the GitHub mirror
# (https://github.com/Siamul/NumtaDB), trains a softmax regression on 16x16
# grayscale pixels, reports held-out accuracy. Connectivity check + floor baseline,
# NOT the khata-page model (khata pages add layout, graphemes, arithmetic marks).
import csv, io, os, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
from PIL import Image
from sklearn.linear_model import LogisticRegression

OUT = os.path.dirname(os.path.abspath(__file__))
RAW = "https://raw.githubusercontent.com/Siamul/NumtaDB/master/training-a/"
N_TRAIN, N_TEST = 400, 150

def fetch(fname):
    with urllib.request.urlopen(RAW + fname, timeout=30) as r:
        return Image.open(io.BytesIO(r.read())).convert("L")

def to_vec(img):
    img = img.resize((16, 16))
    a = np.asarray(img, dtype=np.float32) / 255.0
    a = 1.0 - a  # ink = high
    return a.ravel()

def main():
    with open(os.path.join(OUT, "training-a.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rng = np.random.default_rng(0)
    idx = rng.permutation(len(rows))
    train_rows = [rows[i] for i in idx[:N_TRAIN]]
    test_rows = [rows[i] for i in idx[N_TRAIN:N_TRAIN + N_TEST]]

    t0 = time.time()
    def load(rs):
        X, y, ok = [], [], 0
        for r in rs:
            try:
                X.append(to_vec(fetch(r["filename"])))
                y.append(int(r["digit"]))
                ok += 1
            except Exception as e:
                print("skip", r["filename"], e)
        return np.stack(X), np.array(y), ok

    Xtr, ytr, ntr = load(train_rows)
    Xte, yte, nte = load(test_rows)
    print(f"downloaded {ntr} train / {nte} test images in {time.time()-t0:.0f}s")

    clf = LogisticRegression(max_iter=2000, C=0.05)
    t0 = time.time()
    clf.fit(Xtr, ytr)
    acc = clf.score(Xte, yte)
    print(f"train {time.time()-t0:.0f}s  held-out accuracy: {acc:.3f}  (chance=0.10)")
    with open(os.path.join(OUT, "RESULT.json"), "w") as f:
        json.dump({"n_train": ntr, "n_test": nte, "model": "softmax regression 16x16",
                   "heldout_accuracy": round(float(acc), 3), "chance": 0.10}, f, indent=2)

import json
if __name__ == "__main__":
    main()
