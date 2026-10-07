# Spike 04 result — NumtaDB download + minimal digit baseline

Date: 2026-10-02. Environment: Windows, Python 3.14 venv, scikit-learn + Pillow.

## What was run
`spike_numta.py`:
1. Downloaded `training-a.csv` (19,702 labelled rows) from the GitHub mirror https://github.com/Siamul/NumtaDB (raw.githubusercontent.com).
2. Sampled 400 train / 150 test images (seeded), downloaded each PNG individually (~317 s for 550 images over this connection — individual raw fetches are slow; the Kaggle zip or a bulk mirror would be faster at hackathon scale).
3. Trained softmax (logistic) regression on 16×16 grayscale pixels; evaluated on the 150 held-out images.

## Real numbers
- CSV verified: 19,702 rows, columns `filename, original filename, scanid, digit, database name original, contributing team, database name`.
- Held-out accuracy: **0.320** (chance = 0.10), training time <1 s.

## Interpretation
- Connectivity check PASSED: dataset is downloadable without auth from the GitHub mirror, labels parse, images decode.
- 32% is a FLOOR from a linear model on 400 samples, not a meaningful benchmark. Published NumtaDB results with CNNs are far higher (paper: https://arxiv.org/abs/1806.02452). It does confirm Bengali digits are not trivially separable — a real model (small CNN, GPU) is needed for the ≥90% khata-entry bar set in the critique.
- Licence: the GitHub mirror and arXiv paper do not state a dataset licence on the pages fetched; the Kaggle page (https://www.kaggle.com/datasets/BengaliAI/numta) requires login. Licence status: UNVERIFIED — check before public redistribution; internal hackathon use of a public research dataset is low-risk but must be stated.

## Reproduce
```
python spike_numta.py
```
