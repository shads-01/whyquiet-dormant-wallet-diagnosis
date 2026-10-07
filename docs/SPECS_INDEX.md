# SPECS INDEX — post-judging credibility round (2026-10-07)

Execution plan after Innovation 8.33/10. Thesis: the gap is credibility, not features. Every spec
converts an ASSUMED number into a measured/shown one or closes a named risk. Master context:
`docs/DECISIONS.md` D55. Specs are ordered; parallelism is safe ONLY within a wave because file
ownership is disjoint within each wave.

## Wave 0 (IN PROGRESS)
- `SPEC_CREDIBILITY_EXHIBIT.md` — refusal validity audit + falsifiability exhibit. Owns: evaluate.py, export_seed.py, Evidence.tsx, seed.json.

## Wave 1 — three specs in PARALLEL (all disjoint from Wave 0 files and each other)
| Spec | Owns | Effort |
| --- | --- | --- |
| `SPEC_BOUNDARY_TRANSPARENCY.md` | `web/src/Wallet.tsx`, `web/e2e/wallet.spec.ts` | ~2 h (pure UI; data already in seed.json) |
| `SPEC_REPO_OPS_HYGIENE.md` | `LICENSE`, `Makefile`, `docs/OPS_RUNBOOK.md`, README license line | ~1–2 h |
| `SPEC_PITCH_PACK.md` | `docs/DEMO_STORY.md`, `docs/PITCH_PACK.md` | ~2 h |

## Wave 2 — sequential (shares Wave 0 files)
1. `SPEC_METRIC_DEPTH.md` — calibration diagram, per-cause F1, cost-sweep-led money section. Owns the four Wave-0 files. ~3–4 h.

## Wave 3 — gated, sequential (re-exports everything)
1. `SPEC_COST_SENSITIVE_REFUSAL.md` — run Phase 0 gate FIRST; skip cleanly if < 2pp refusal delta AND < 5% net-value delta. If it ships, every published number refreshes. ~half day.

## Wave 4 — optional (Tier 1)
1. `SPEC_FAIRNESS_DEPTH.md` — joint fairness slices + routed campaign export. ~half day.

## Final pass
- `SPEC_PITCH_PACK.md` second pass: fill every `TBD` slot with the final shipped numbers; re-verify
  adversarial card wallet IDs still exist in the re-exported seed.json.

## Rules for the executor (Gemini)
- One spec at a time within a wave; never two specs editing the same file concurrently.
- Run `make check` and `make e2e` before declaring any spec done.
- Every spec's seed.json changes are additive-only unless the spec explicitly says otherwise.
- Record any design decision made during execution in `docs/DECISIONS.md` (append-only).
- STOP and report if measured values differ from a spec's "verified facts" table by more than rounding.
