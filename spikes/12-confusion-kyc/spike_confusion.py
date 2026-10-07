# Spike 12: confusion/KYC drop-off mock — 2 self-run conditions, separation stat
# n=2 connectivity check, NOT evidence. Run: python spike_confusion.py
import json, time, statistics, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

STEPS = ["welcome", "nid_number", "selfie", "otp", "confirm"]

def run_session(condition, log):
    """Replays a scripted interaction log (as if captured by the mock flow's event logger)."""
    # log: list of (event, step, timestamp_seconds)
    events = []
    for ev, step, ts in log:
        events.append({"event": ev, "step": step, "t": ts})
    return events

def struggle_score(events):
    """Per-session features: total time, mean dwell per step, backtracks, long idles (>5s)."""
    total_t = events[-1]["t"] - events[0]["t"]
    step_first = {}
    step_last = {}
    backtracks = 0
    prev_idx = -1
    order = {s: i for i, s in enumerate(STEPS)}
    for e in events:
        if e["event"] == "enter":
            step_first.setdefault(e["step"], e["t"])
            step_last[e["step"]] = e["t"]
            i = order[e["step"]]
            if prev_idx != -1 and i < prev_idx:
                backtracks += 1
            prev_idx = i
    idles = sum(1 for a, b in zip(events, events[1:]) if b["t"] - a["t"] > 5)
    dwells = [step_last[s] - step_first[s] for s in step_first if s in step_last]
    return {
        "total_time_s": round(total_t, 1),
        "mean_dwell_s": round(statistics.mean(dwells), 1) if dwells else 0,
        "backtracks": backtracks,
        "long_idles": idles,
    }

# Condition A: expert (self-run, fast, no re-entries) — scripted from a real fast run-through
expert_log = [("enter","welcome",0.0),("enter","nid_number",2.1),("enter","selfie",6.3),
              ("enter","otp",11.0),("enter","confirm",14.2)]
# Condition B: first-time (scripted with reading delays, an OTP re-entry, a long idle)
firsttime_log = [("enter","welcome",0.0),("enter","nid_number",14.5),("enter","selfie",41.0),
                 ("enter","otp",58.3),("enter","nid_number",70.0),("enter","otp",83.5),
                 ("enter","confirm",121.7)]

for name, log in [("expert", expert_log), ("first_time", firsttime_log)]:
    ev = run_session(name, log)
    print(name, json.dumps(struggle_score(ev)))

a = struggle_score(run_session("expert", expert_log))
b = struggle_score(run_session("first_time", firsttime_log))
# separation statistic: simple risk score = total_time/30 + backtracks + long_idles
def risk(f): return f["total_time_s"]/30 + f["backtracks"] + f["long_idles"]
ra, rb = risk(a), risk(b)
print(f"\nrisk(expert)={ra:.2f}  risk(first_time)={rb:.2f}  ratio={rb/max(ra,0.01):.1f}x")
print("PASS if ratio > 2x (pipeline separates conditions); n=2 is a connectivity check only")
print("SPIKE RESULT:", "PASS" if rb / max(ra, 0.01) > 2 else "FAIL")
