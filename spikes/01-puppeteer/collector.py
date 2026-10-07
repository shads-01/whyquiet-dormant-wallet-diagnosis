# Spike 01 (Puppeteer): send-flow interaction-timing collector + analysis.
#
# collector.py — logs keypress timestamps for a mock send flow:
#   stage 1: type recipient number (11 digits)
#   stage 2: type amount (4 digits)
#   stage 3: type PIN (5 digits)
# Usage (human):  python collector.py mylabel
#   then type the three fields, pressing Enter after each. Writes JSON to logs/.
#
# This run: an AUTOMATED typist (typist.py) drives the collector twice —
#   condition "direct"  : confident self-directed typing (fast, uniform)
#   condition "coached" : reading digits dictated one-by-one (slow, bursty pauses)
# THIS IS A PIPELINE CONNECTIVITY CHECK ONLY. The "human" is a script with
# hand-chosen delay distributions. n=2 scripted runs are NOT evidence that
# coercion has a timing signature; they only prove the collector + statistic work.
import json, os, sys, time

OUT = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(OUT, "logs")
os.makedirs(LOGS, exist_ok=True)

FIELDS = [("recipient", 11), ("amount", 4), ("pin", 5)]

def collect(label, keystrokes):
    """keystrokes: list of (field, char, timestamp) already recorded by a driver."""
    events = [{"field": f, "char": c, "t": round(t, 3)} for f, c, t in keystrokes]
    path = os.path.join(LOGS, f"{label}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"label": label, "events": events}, fh, indent=1)
    print(f"wrote {path} ({len(events)} events)")
    return path

def features(path):
    with open(path, encoding="utf-8") as fh:
        ev = json.load(fh)["events"]
    t = [e["t"] for e in ev]
    ikis = [b - a for a, b in zip(t, t[1:])]
    pauses = sum(1 for x in ikis if x > 1.0)          # >1s gap = hesitation/dictation pause
    return {
        "n_keys": len(ev),
        "total_s": round(t[-1] - t[0], 2),
        "mean_iki_ms": round(1000 * sum(ikis) / len(ikis), 1),
        "sd_iki_ms": round(1000 * (sum((x - sum(ikis)/len(ikis))**2 for x in ikis) / len(ikis))**0.5, 1),
        "pauses_gt_1s": pauses,
        "field_gaps_s": [round(b - a, 2) for a, b, e0, e1 in
                         zip(t, t[1:], ev, ev[1:]) if e0["field"] != e1["field"]],
    }

if __name__ == "__main__":
    for label in sys.argv[1:]:
        print(label, json.dumps(features(os.path.join(LOGS, f"{label}.json"))))
