# Spike 01 result — Puppeteer timing collector

Date: 2026-10-02. Environment: Windows, Python 3.14 venv.

## What was run
- `collector.py` — mock send-flow keypress-timing collector (recipient 11 digits → amount 4 digits → PIN 5 digits), logs per-key timestamps to `logs/*.json`.
- `typist.py` — scripted typist driving the collector under two conditions:
  - `direct`: uniform 90–140 ms keystrokes (self-directed proxy)
  - `coached`: 400–800 ms keystrokes with a 1.2–2.0 s "listen for next digit" pause every 3rd key (dictation proxy)

## Real numbers (scripted typist, n=2 — connectivity check, NOT human evidence)

| metric | direct | coached |
|---|---|---|
| total time (20 keys) | 2.18 s | 19.32 s |
| mean inter-key interval | 114.9 ms | 1017.0 ms |
| SD of IKI | 15.9 ms | 783.2 ms |
| pauses > 1 s | 0 | 5 |

## Interpretation
- The collector, log format, and feature extraction work end-to-end. The two scripted conditions separate trivially on mean IKI, IKI variance, and pause count — the statistic pipeline is sound.
- This says NOTHING about whether real coached/coerced humans differ from self-directed humans. That requires the 30–50 participant protocol in docs/04-feasibility/01-puppeteer.md §5. The critique's falsifier stands: held-out coached sessions must reach ≥65% recall at <10% false-alarm rate, beating a dwell-time threshold baseline.
- Known limitation of the scripted run: the "coached" delay distribution was invented by us; real dictation rhythm depends on the coach's speech rate.

## How to reproduce
```
python typist.py            # runs both conditions
python collector.py direct coached   # prints features
```
