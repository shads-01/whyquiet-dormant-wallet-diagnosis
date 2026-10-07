# 07-agent-scam-drill.md — Feasibility: Agent Scam Drill (synthetic Bangla scam calls + response scoring)

Written 2026-10-02 by the feasibility researcher. Inputs: docs/CONTEXT.md, docs/IDEA_POOL.md, docs/03-critique/02-critique.md (survivor #5 + mechanism_problems on D37), docs/01-data/inventory.md, docs/02-ideas/01-candidates.md (D37). Not legal advice.

**One-line problem statement:** For MFS agents (the cash-out gateway for scam victims), there is no realistic practice against scam calls, causing agents to wave through coerced cash-outs. We build a drill that uses SLR37 TTS (CC BY-SA) + real scam scripts (self-collected text) to generate synthetic Bangla scam calls for TRAINING ONLY, and a scoring model that rates trainee responses, with success measured by pre/post susceptibility drop on a fresh script.

## 1. DATA REALITY

### Public datasets (pages opened 2026-10-02)

| Source | URL | Size | Language | Licence | Hackathon use OK? | Download friction | Status |
|---|---|---|---|---|---|---|---|
| SLR37 Bengali TTS (bn-BD) | https://www.openslr.org/37/ | bn_bd.zip 586 MB; **1,891 utterances, 6 speakers** (read remotely from the zip via HTTP Range: line_index.tsv parsed live); transcribed multi-speaker TTS corpus collected by Google | bn-BD | CC BY-SA 4.0 | Yes (attribution + share-alike for derivatives) | Direct download, no registration; 586 MB feasible; individual wavs NOT separately fetchable (zip only) — but we read the TSV remotely without downloading | VERIFIED (page + README.txt + remote zip index read) |
| SLR53 Bengali ASR (optional, for transcribing trainee replies) | https://www.openslr.org/53/ | ~196K utterances, 16 zips ~900 MB each | bn | CC BY-SA 4.0 | Yes | Direct download; too big for 48h except one zip | VERIFIED (page) |

Caveat: SLR37 is READ speech (news-style sentences — first TSV lines are about textile outlets, banks, cement), NOT conversational scam dialogue. It can voice a script but its prosody is read-aloud, not threatening phone-call speech. This is a real quality ceiling for the drill's realism.

### Self-collected data

- **Real scam scripts (text):** 15–25 real scam call scripts/stories from the team's census collection (consented, redacted — same protocol as idea 05). Scripts are REAL text; only the AUDIO is synthetic. This keeps strict-ideation rule 2: the model's training signal (scripts) is real-world artefacts; synthetic audio is explicitly training-only, eval stays on real scripts + real people.
- **Trainee responses:** 15–30 consenting classmates/relatives each take a pre-drill call, the drill, and a post-drill call with a FRESH script. ~10 min per person, ~4–6 h total.
- **Scoring labels:** to avoid the critique's circularity finding ("the grader is the injection point"), use a fixed rubric anchored on 3 external anchors: (a) the real script's actual ask, (b) 2 published BD scam typologies (ScamCheck.gov.bd catalog — UNVERIFIED, page not opened), (c) blind second rater on 20% of responses; report inter-rater agreement.
- **Consent wording (verbatim):**
  - EN: "I voluntarily take part in a scam-awareness drill for a university hackathon. I will hear a SIMULATED, computer-generated scam call clearly labelled as fake; it uses no real person's voice. My spoken responses are recorded only to score the drill, stored locally, deleted after the demo, and I can withdraw any time. Signature: ____ Date: ____"
  - BN: "আমি স্বেচ্ছায় একটি বিশ্ববিদ্যালয় হ্যাকাথনের স্ক্যাম-সচেতনতা ড্রিলে অংশ নিচ্ছি। আমি শুনব একটি কম্পিউটার-তৈরি নকল স্ক্যাম কল, যা স্পষ্টভাবে ভুয়া হিসেবে চিহ্নিত এবং কোনো প্রকৃত ব্যক্তির কণ্ঠ নয়। আমার উত্তর শুধু ড্রিল স্কোর করতে রেকর্ড হবে, স্থানীয়ভাবে সংরক্ষিত থাকবে, ডেমোর পর মুছে ফেলা হবে, এবং আমি যেকোনো সময় প্রত্যাহার করতে পারব। স্বাক্ষর: ____ তারিখ: ____"
- **Redaction:** scripts redacted like idea 05 (numbers/names masked); trainee recordings deleted after scoring.

## 2. PRECEDENT

| Product | URL | What it does | What it does NOT do |
|---|---|---|---|
| Truecaller Scam Checker | https://www.truecaller.com/scam-checker (opened 2026-10-02) | Lookup numbers/URLs against scam database | No training/drill product |
| Google Messages scam detection | https://blog.google/products-and-platforms/platforms/android/new-android-features-march-2025/ (opened 2026-10-02) | On-device SMS scam warnings | No agent training |
| bKash 16247 hotline | widely referenced; no official page opened today | Victim reporting line | Reactive, not preventive training | UNVERIFIED |
| ScamCheck.gov.bd | https://scamcheck.gov.bd/common-scams-in-bangladesh/ (cited in candidates A2; not opened today) | Static catalog of common BD scams | No interactive drill | UNVERIFIED |
| Global: AI scam-practice chatbots (e.g. Jigsaw/Google's phishing quizzes) | UNVERIFIED — not searched today | Text quizzes | No Bangla voice drill for MFS agents found | UNVERIFIED |

**Plainly:** no Bangla voice scam-drill product for MFS agents was found. The nearest neighbours are text quizzes and static scam catalogs. The gap is real but the critique's mechanism problem stands: scoring labels must not be team-invented.

## 3. LEGAL/ETHICS (not legal advice)

- **Synthetic voice of a REAL person is criminal risk:** Telecom Act 2001 s.70(3) (added by the 2026 amendment) criminalizes using AI to copy a person's voice/image to cause harm (fine up to Tk 1 lakh). Source: https://www.recordinglaw.com/world-laws/world-recording-laws/bangladesh-recording-laws/ (opened 2026-10-02, cites bdlaws.minlaw.gov.bd). Mitigation: use only SLR37's generic corpus voices (anonymous speaker IDs, Google-collected research corpus) — never clone any real person; label every drill call "SIMULATED" at start and end.
- **Cyber Security Act 2026 s.25** covers publishing AI-edited harmful content for blackmail/harassment — a scam drill is consensual training, not publication to harm, but keep recordings private and delete them. Same source.
- **PDPA 2026 (Act No. 63 of 2026):** trainee voice recordings are personal data (voiceprints = biometric); consent per s.5, delete after scoring; household exemption does not cover our processing. Same source.
- **Deception ethics:** the pre/post test deliberately attempts to scam a consenting trainee — consent must say so explicitly (wording above); debrief immediately after each call; no real money or credentials ever requested.
- **Unclear:** whether Bangladesh Bank MFS agent-conduct rules restrict simulated fraud training (no BB circular read: UNVERIFIED); whether recording drill audio requires notice beyond consent (we give both).

## 4. 48-HOUR BUILD PLAN

Stack: Python; TTS via SLR37 wavs is NOT a synthesizer — it is a corpus. Realistic TTS options in 48h: (a) play pre-cut SLR37 wav fragments stitched per script line (ponytail option: the corpus sentences won't match scam scripts — poor), (b) a Bangla TTS model from HF (e.g. facebook/mms-tts-ben, UNVERIFIED quality) — needs a spike at hour 0, (c) fallback: human teammate reads the scripts (real voice, consented, disclosed as actor — kills the "synthetic" claim but keeps the drill). Plan assumes (b) with (c) fallback.

| Hours | Person A (data lead) | Person B (model lead) | Person C (drill app lead) |
|---|---|---|---|
| 0–6 | Collect + redact 15–25 real scam scripts; write rubric v1 | TTS spike: test facebook/mms-tts-ben or similar on 3 script lines; pick TTS path | Call-simulation web app: plays scam audio, records trainee reply |
| 6–12 | Recruit 15–30 trainees; run PRE-drill susceptibility calls (fresh script A) | Batch-generate drill audio for 5 scripts × 3 voices; ASR for trainee replies (whisper fine-tuned from idea 06 or API) | Scoring UI: rubric fields + model score |
| 12–24 | Run drill sessions; blind second rater on 20% | Scoring model v1: rubric features + response text → vulnerability score; measure rater agreement | Session manager, pre/post comparison view |
| 24–36 | Run POST-drill calls (fresh script B); compute susceptibility delta | Calibrate score vs rubric; **FEATURE FREEZE h36** | Demo: judge takes a live drill call, gets scored |
| 36–48 | Pitch: pre/post chart | Falsifier numbers | Rehearsal, canned fallback |

Real vs mocked: scripts real; TTS synthetic (disclosed); scoring model real but trained on ~30–60 rated responses (small); backend mocked.

## 5. SPIKE TEST — RUN + protocol

Script: `spikes/07-agent-scam-drill/spike_slr37_probe.py`. Real results (2026-10-02):

- SLR37 page + README.txt fetched: multi-speaker transcribed TTS data, Google-collected, CC BY-SA 4.0, direct download.
- **Remote zip probe (HTTP Range, no 586 MB download): bn_bd.zip contains 1,891 utterances, 6 distinct speakers** (speaker IDs 00737, 00779, 01232, 01701, 02194, 03042); first 3 TSV lines are read news-style sentences (textile/bank/cement) — confirming the read-speech (not conversational) caveat in §1.
- TTS-generation spike (turning a script line into audio with an HF Bangla TTS model): **NOT RUN — protocol only.** Protocol: at hour 0, try `facebook/mms-tts-ben` (HF, no registration) on 3 script lines; pass = intelligible Bangla audio < 10 s per line generated on CPU; fail = fall back to a consented human actor reading scripts. Marked UNVERIFIED until run.

PASS/FAIL: **PARTIAL — corpus verified with real numbers (1,891 utts / 6 speakers); TTS generation protocol only.**

## 6. BASELINE

- Simplest baseline: a one-page PDF of scam tips + role-play by a human teammate (no AI). Critique #5: "a PDF of scam tips gets 40% of the value; the interactive edge must show in the delta."
- LLM-API baseline: GPT scores trainee response transcripts against the rubric — likely strong; our scoring model must beat it or justify itself on cost/offline grounds.
- **Pointless-if number:** if susceptibility (measured on fresh script B) does not drop by ≥20 points for drilled vs undrilled peers (critique falsifier), the drill is pointless. Secondary pointless-if: model score agreement with the rubric rater < 70%, in which case just use the human rubric.

## 7. RISKS

1. **Scoring circularity** (critique mechanism_problems): team-invented "vulnerable response" labels. Mitigation: external rubric anchors + blind second rater + reported agreement (§1).
2. **TTS quality/realism** — read-speech corpus, not phone-call prosody; trainees may not take it seriously. Mitigation: hour-0 TTS spike; human-actor fallback; measure trainee "did it feel real?" rating.
3. **Tiny N (15–30 trainees)** — pre/post delta is anecdote-scale, one confound (motivation) away from noise. Mitigation: matched undrilled control group (even 8 people); report as pilot, not proof.
4. **Trainees game known scripts** (critique #5). Mitigation: fresh script B for post-test, written from census items not used in the drill.
5. **Ethics/consent failure** — a trainee feels deceived or a recording leaks. Mitigation: explicit consent wording, immediate debrief, local-only storage, deletion after demo.

**P(working live demo) = 0.55.** Reasoning: the drill app itself (play audio, record, score) is straightforward and demoable even with mediocre TTS; the human-actor fallback guarantees a working demo moment (judge takes a live scam call, gets scored). What is uncertain is the *measurement* (pre/post delta with N≈20 in-window) — the demo can show the mechanism but likely not a statistically meaningful delta. P reflects: demo works, evidence is weak.

## 8. RESPONSIBLE AI

- **Fairness groups:** trainee dialect (does ASR mis-score Sylheti speakers' replies?), gender, prior scam exposure. Report score distribution per slice; ASR errors must not read as "bad responses".
- **Explainability output:** score card lists which rubric criteria failed with the transcript excerpt ("gave OTP when asked" / "did not verify caller claim") — no bare number.
- **Security:** drill audio could be repurposed as an actual scam tool — mitigation: watermark audio ("SIMULATED" spoken every 30 s), never release audio files, delete after demo; adversarial trainees can prompt-inject via speech if an LLM scores transcripts (mitigation: transcript is data, structured rubric scoring, no free-form LLM decisions); data leakage: post-test script excluded from all drill material.
- **Human oversight:** no automated consequence attaches to a score; a human trainer reviews before any coaching action; scores are advisory.
