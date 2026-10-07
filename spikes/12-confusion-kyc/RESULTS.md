# Spike 12 results — Confusion/KYC mock flow, 2 conditions (2026-10-02)

## What ran
`python spike_confusion.py` — pure-stdlib console mock of a 5-step KYC flow (welcome → nid_number → selfie → otp → confirm). Two scripted self-run interaction logs (as the event logger would capture them): expert vs first-time (reading delays, one OTP re-entry, long idles). Features: total time, mean dwell, backtracks, long idles (>5 s). Risk score = total_time/30 + backtracks + long_idles.

## REAL output
```
expert      {"total_time_s": 14.2, "mean_dwell_s": 0.0, "backtracks": 0, "long_idles": 0}
first_time  {"total_time_s": 121.7, "mean_dwell_s": 16.1, "backtracks": 1, "long_idles": 6}
risk(expert)=0.47  risk(first_time)=11.06  ratio=23.4x
SPIKE RESULT: PASS
```

## Interpretation
- **n=2, both sessions scripted by the same author — a connectivity check, NOT evidence.** The 23.4x ratio only proves the logging→feature→score pipeline runs and separates the two conditions.
- Real signal requires ≥20–30 unscripted participants (incl. parents) on a clickable prototype; the critique's falsifier stands: drop-off prediction AUC ≥0.75 on held-out parents, else it's an observation.
- Known confound to design against: logs will pick up device/browser artefacts (critique #10 mechanism problem) — collect on participants' own phones, not our laptops.
