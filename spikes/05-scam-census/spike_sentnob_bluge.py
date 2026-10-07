# Spike 05-scam-census — SentNoB + BLUGE-NER zero-shot baselines (2026-10-02)
# Q: can we load these HF datasets directly and get a real baseline number on a 20-row slice?
import json, urllib.request, io, csv, re
from collections import Counter

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "spike/1.0"})
    return urllib.request.urlopen(req, timeout=60).read()

results = {}

# ---- SentNoB: parquet via HF auto-convert (viewer showed train 15.7k rows, labels 0/1/2) ----
# Use the datasets-server rows API for a 20-row slice (no heavy download needed)
sn_url = "https://datasets-server.huggingface.co/rows?dataset=khondoker%2FSentNoB&config=default&split=train&offset=0&length=100"
sn = json.loads(fetch(sn_url))
rows = [(r["row"]["Data"], r["row"]["Label"]) for r in sn["rows"]]
print("SentNoB rows fetched:", len(rows))
for t, l in rows[:3]:
    print("  ex:", l, "|", t[:60])

# Lexicon baseline: small hand-built Bangla sentiment lexicon (negative/positive cue words)
# This is a ZERO-SHOT, LLM-free baseline — deliberately crude.
neg = ["না", "ভালো না", "খারাপ", "বাজে", "ঘৃণা", "মূর্খ", "চুরি", "প্রতারণা", "ক্ষতি", "দুঃখ", "অভিযোগ", "ভুল", "শালা", "কুত্তা", "নরক", "বরখাস্ত", "গ্রেপ্তার", "মৃত্যু", "আক্রমণ", "হামলা", "দুর্নীতি", "ভয়াবহ", "অভাব", "সমস্যা"]
pos = ["ভালো", "সুন্দর", "ধন্যবাদ", "প্রেম", "ভালবাসা", "চমৎকার", "অসাধারণ", "মজা", "পছন্দ", "শুভকামনা", "সফল", "জয়"]

def lexicon_sentiment(text):
    n = sum(text.count(w) for w in neg)
    p = sum(text.count(w) for w in pos)
    if n > p: return 2
    if p > n: return 1
    return 0

slice20 = rows[:20]
pred = [lexicon_sentiment(t) for t, _ in slice20]
gold = [l for _, l in slice20]
acc = sum(p == g for p, g in zip(pred, gold)) / len(gold)
maj = Counter(g for _, g in rows).most_common(1)[0]
maj_acc = maj[1] / len(rows)
print(f"SentNoB lexicon baseline on 20-row slice: acc={acc:.2f} ({sum(p==g for p,g in zip(pred,gold))}/20)")
print(f"SentNoB majority-class (label {maj[0]}) on same 100 rows: {maj_acc:.2f}")
print("SentNoB label distribution (100 rows):", Counter(l for _, l in rows))
results["sentnob_lexicon_acc_20"] = round(acc, 2)
results["sentnob_majority_acc_100"] = round(maj_acc, 2)

# ---- BLUGE NER: gazetteer heuristic baseline on a 20-row slice of test split ----
ner_url = "https://datasets-server.huggingface.co/rows?dataset=nahid-hub%2FBLUGE-bengali-ner&config=default&split=test&offset=0&length=20"
nr = json.loads(fetch(ner_url))
ner_rows = [(r["row"]["tokens"], r["row"]["ner_tags"]) for r in nr["rows"]]
print("\nBLUGE-NER test rows fetched:", len(ner_rows))
for toks, tags in ner_rows[:3]:
    print("  ex:", " ".join(toks[:12]), "| tags:", tags[:12])

# Heuristic: token ends with typical location suffixes OR is in a tiny gazetteer -> LOC
loc_gaz = {"ঢাকা", "বাংলাদেশ", "ভারত", "কলকাতা", "চট্টগ্রাম", "সিলেট", "খুলনা", "রাজশাহী", "খ্রিস্টাব্দে"}
suffixes = ("পুর", "গ্রাম", "জেলা", "উপজেলা", "বাজার", "নগর", "দেশ", "স্থান")

def heuristic_tags(tokens):
    out = []
    for i, t in enumerate(tokens):
        if t in loc_gaz or t.endswith(suffixes):
            out.append(5 if (i == 0 or out[-1] not in (5, 6)) else 6)
        else:
            out.append(0)
    return out

tp = fp = fn = 0
for toks, gold_tags in ner_rows:
    pred_tags = heuristic_tags(toks)
    for p, g in zip(pred_tags, gold_tags):
        g_is_loc = g in (5, 6); p_is_loc = p in (5, 6)
        if p_is_loc and g_is_loc: tp += 1
        elif p_is_loc: fp += 1
        elif g_is_loc: fn += 1
prec = tp / (tp + fp) if tp + fp else 0
rec = tp / (tp + fn) if tp + fn else 0
f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0
print(f"BLUGE-NER gazetteer LOC baseline on 20-row test slice: P={prec:.2f} R={rec:.2f} F1={f1:.2f} (tp={tp} fp={fp} fn={fn})")
results["bluge_loc_f1_20"] = round(f1, 2)

with open("spikes/05-scam-census/results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("\nSaved spikes/05-scam-census/results.json")
