# SPEC: Metric Depth on Evidence (calibration diagram, per-cause F1, cost-sweep lead)

This spec proposes upgrading the Evidence page from aggregate scores to decision-grade diagnostics — a calibration diagram, per-cause breakdown, and cost-sensitivity-led money story — so judges see measured behavior, not just headline numbers.

**Execution order:** Wave 2 — MUST run after `docs/SPEC_CREDIBILITY_EXHIBIT.md` merges (shared files: `scripts/evaluate.py`, `scripts/export_seed.py`, `web/src/Evidence.tsx`, e2e). **File ownership (after credibility exhibit):** same four, plus `README.md` results block.

## Verified facts (pre-checked 2026-10-07)

- `report.ml.ece_b = 0.100` exists; the per-bin data behind it does NOT — `scripts/evaluate.py::ece()` computes bins internally and discards them.
- The confusion matrix on B exists in `report.confusion_b`; per-cause precision/recall/F1 is derivable from it but not exported.
- `report.sweep` (cost scales 0.5/1.0/1.5, 36 rows, D53/D56) and `report.break_even` are exported — VERIFY whether the Evidence money section renders the cost sweep or only the 1%/4%/8% recovery toggle (D25); if unrendered, render it.
- Remedy unit costs (5–25 BDT, D53) are invented numbers — currently framed as fixed in `report.money`; break-even rates are derived from them.
- Multi-seed spread (D33) is intentionally NOT in this spec — the credibility exhibit's flip-rate retrain loop emits it.

## Goals

1. `scripts/evaluate.py` exports `report.calibration_bins`: 10 equal-width confidence bins on population B, each `{mean_confidence, empirical_accuracy, n}` — computed by refactoring `ece()` to return bins (same math, reused by the ECE number; no behavior change to existing fields).
2. `scripts/evaluate.py` exports `report.per_cause_f1_b`: per cause `{cause, precision, recall, f1, support}` on attributed B wallets (sklearn, same split rules as `confusion()`).
3. Evidence page adds: (a) **Reliability diagram** — Recharts, bars/bins of mean confidence vs empirical accuracy with the identity line, ECE stated beside it; (b) **Per-cause F1 bars** — horizontal, with support counts; (c) the money section **leads with the cost sweep** (0.5×/1.0×/1.5×) and shows `report.break_even` per cause, with ASSUMED badges on the 5–25 BDT unit costs.
4. README results block refreshes with the new fields.

## Non-Goals

- NO model recalibration (no temperature/isotonic scaling — that retrains and churns every published number; presenting the measured ECE honestly is the move).
- No multi-seed table (credibility exhibit owns it), no refusal-validity panel (same), no new thresholds.
- No changes to `src/model/`, `src/rules/`, or the OpenAPI/API contract (seed fields only — `make gen-types` not needed).

## Constraints

**Compatibility** — additive seed fields only; every pre-existing seed.json value reproduces identically after re-export (same invariant as the credibility exhibit). The ece() refactor must keep `report.ml.ece_b` byte-identical.
**Performance** — re-export stays under 5 minutes; no model retrains in this spec (bins/F1 come from the existing single seed-42 run).
**Security/Compliance** — ASSUMED badges required on: remedy unit costs, cost-scale choices, bin count; honesty line stays on the page.
**Operational** — panels follow existing Evidence patterns (4 states, responsive 375px, `scope` attributes on tables).

## Acceptance Criteria

1. Given seed 42, when `uv run python scripts/evaluate.py --seed 42` runs, then `calibration_bins` has 10 entries, their bin-mass-weighted |confidence−accuracy| reproduces `ece_b`, and `per_cause_f1_b` covers all 5 causes.
2. Given the reliability diagram, when rendered, then it plots the real `calibration_bins` (not hard-coded) with an identity reference line and the ECE value beside it.
3. Given the money section, when rendered, then the cost sweep and per-cause break-even rates are visible before the point estimates, and each remedy cost carries an ASSUMED badge.
4. Given seed.json before/after re-export, when diffed, then only `calibration_bins` and `per_cause_f1_b` (and README text) differ.
5. Given `make e2e`, when evidence specs run, then prior assertions pass and one new assertion covers the reliability diagram rendering.
6. Given `make check`, when run, then ruff/pyright/tsc/oxlint are clean.

## Open Questions

1. Is `report.sweep` already rendered in the UI? Executor verifies first and only builds what's missing — who knows: Shads; impact if wrong: duplicate panels.
2. Whether per-cause F1 should also slice A-test for the gap story — who decides: user; impact if wrong: none structurally, one extra export field either way.
