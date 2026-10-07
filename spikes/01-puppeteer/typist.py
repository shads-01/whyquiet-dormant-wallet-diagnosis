# Spike 01 driver: scripted typist producing two conditions through collector.py.
# "direct"  = fast uniform typing (self-directed proxy)
# "coached" = slow bursty typing with >1s pauses between digits (dictation proxy)
# Connectivity check only — scripted delays, not human data.
import random, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import collector

random.seed(7)

def type_condition(label, delay_fn):
    keys, t = [], time.time()
    for field, n in collector.FIELDS:
        for i in range(n):
            c = random.choice("0123456789")
            keys.append((field, c, time.time()))
            time.sleep(delay_fn(field, i))
    collector.collect(label, keys)
    return label

# direct: 90-140 ms per key, no long pauses
type_condition("direct", lambda f, i: random.uniform(0.09, 0.14))
# coached: 0.4-0.8 s per key with a 1.2-2.0 s "listen to next digit" pause every 3rd key
def coached_delay(field, i):
    d = random.uniform(0.4, 0.8)
    if i % 3 == 2:
        d += random.uniform(1.2, 2.0)
    return d
type_condition("coached", coached_delay)

for label in ("direct", "coached"):
    print(label, collector.features(collector.logs_path(label)) if hasattr(collector, "logs_path")
          else collector.features(f"{collector.LOGS}\\{label}.json"))
