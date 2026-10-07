# SUPERSEDED — do not use this file as authority

**This file is retired. Read `docs/v3/CONTEXT_v3.md` instead.**

It is kept on disk only because files in this repo must not be deleted (`AGENTS.md`). Its contents are
historical and **several statements in it are wrong for this round** — see below.

## Read instead

| Need | File |
| --- | --- |
| Event, timeline, tracks, rubric, data rule, responsible AI, submission artifacts | `docs/v3/CONTEXT_v3.md` |
| Business model, revenue architecture, unit economics, upay assets, P&L levers | `docs/v3/upay-model.md` |
| Official source document | `AI_Hackathon_2026_DIU_CPC_x_upay_Student_Guideline_Official_docx.pdf` (repo root) |

## Withdrawn — do not follow these

- **"DATA-FIRST RULE"** — withdrawn. It required that training/evaluation data NOT be invented by the
  team, and treated synthetic-only data as circular. This contradicts the official brief §11, which
  explicitly permits synthetic, public and self-generated data, requires documenting every synthetic
  assumption, and requires a clean held-out test set. **The official brief governs.**
- **"Build window: 48 hours"** — wrong. The official rules specify a **72-hour** initial development
  period (`T+0` to `T+72`), followed by pre-evaluation, an on-site day where teams are given **new
  requirements to integrate**, and a final 90-minute evaluation. Final ranking uses marks from **both**
  evaluations. Plan for a second, unpredictable phase.
- **"Reserve the last 8 hours for demo freeze and pitch"** — derived from the wrong 48h figure and the
  wrong phase shape. Re-derive from `CONTEXT_v3.md` §1 and §9.
- **Fraud framed as the default lane** — the "Lessons" note that fraud is *the* most crowded lane is
  from an earlier round. Track 01 is one of seven tracks; do not treat it as the default or as banned.
  The open question about Track 01 is recorded in `CONTEXT_v3.md` §0.

## Still valid — carried forward, not withdrawn

These do not conflict with the official brief. Keep them as hard constraints.

- **The model is the product.** Remove the model and nothing valuable must remain — not a rule,
  threshold, or lookup in disguise. (Official §13: "AI adds value beyond a simple deterministic rule.")
- **Test on inputs you did not write.** Held-out data, judges' live inputs, or public benchmarks —
  never only on data you generated yourself.
- **Output must drive a concrete action with a measurable outcome.** (Official §13.)
- **Ethics, stricter than the official minimum.** Only consented, redacted data from people we know. No
  scraping of personal data. Check terms of service before scraping anything. Never use real personally
  identifiable information.
- **Evidence discipline.** Any external claim needs a URL, or is marked UNVERIFIED. Never invent
  numbers. Facts recalled from memory are UNVERIFIED until checked.
- **Every team member must be able to demo the project and explain its design, implementation and AI
  components.** Judges inspect source, dependencies, prompt history and working demos.
- **There is a live demo moment a judge can try**, and the judges' hardest question has an honest
  answer. Both worth more than another feature.