# SPEC: Cost-Sensitive Refusal (gated)

This spec proposes re-tuning refusal thresholds by expected money instead of a flat accuracy floor so that refusing a 0-BDT remedy and refusing a 25-BDT remedy are no longer treated identically — but ONLY if a pre-computed gate shows the change is demo-visible.

**Execution order:** Wave 3 — MUST run after SPEC_METRIC_DEPTH merges (it re-exports seed.json and refreshes every published number). **File ownership:** `src/model/train.py`, `scripts/evaluate.py`, `scripts/export_seed.py`, `src/rules/money.py` (read-only), `README.md`, `docs/DECISIONS.md` (append), seed.json re-export.

## Verified facts (pre-checked 2026-10-07)

- Current refusal: `decide()` refuses when top prob < tau (0.80) or top-2 margin < delta (0.10); `_tune()` picks the loosest pair keeping attributed accuracy ≥ 0.97 on the A-train validation slice (D27/D28). The floor is ASSUMED (D28) — a product choice, not a law.
- Remedy unit costs exist in `src/rules/money.py::REMEDIES`: supply_failure 5, migration 10, job_exit 15, fee_shock 25, solved_problem 0 BDT (ASSUMED, D53).
- `solved_problem` already receives zero action and zero recovery — the current flat threshold still refuses these wallets at the same bar as 25-BDT remedies: the incoherence this spec fixes.
- Changing thresholds changes EVERY published metric (refusal rates, F1 on attributed-only, ECE, fairness, seed.json, UI). The e2e real-data spec uses no hard-coded IDs (D31) and should survive; sample-based specs (`smoke`, `queue`, `wallet`) run on `seed.sample.json` and may break — that re-export is part of this spec's cost.

## Goals

1. **Phase 0 — GATE (do this first, stop if it fails).** On the A-train validation slice and on B, compute refusal rate and expected net value (using `src/rules/money.py` constants, labelled ASSUMED) under: (a) current thresholds, (b) the value-maximizing pair from the SAME tau/delta grid with objective = expected net value instead of the 0.97 accuracy floor. **Skip the whole spec if** B refusal rates differ by < 2 percentage points AND net value differs by < 5%. Record the gate result in `docs/DECISIONS.md` either way.
2. **If the gate passes:** change `_tune()`'s objective to expected net value per correct/wrong attribution on the validation slice, keeping the floors tau ≥ 0.50, delta ≥ 0.10 (A5 protection against 0% refusal) and the same grid. One global pair — NOT per-cause thresholds (simplest version; see Non-Goals).
3. Full re-export: seed.json, seed.sample.json, README results block; every number in the UI updates; a `docs/DECISIONS.md` row records the change with before/after refusal rates and net value.

## Non-Goals

- No per-cause threshold vectors (the 2-parameter grid stays 2-parameter; per-cause is the upgrade path if the global version shows value).
- No change to `decide()`'s refusal semantics (still: top < tau OR margin < delta), no third verdict, no UI logic changes — only values flow through.
- No change to the generator, features, or boosting rounds.

## Constraints

**Compatibility** — the OpenAPI contract and UI components are unchanged (values only); `src/model` still never reads `truth/` (tuning uses A-train validation slice only — the same discipline as D27/D28).
**Performance** — same grid search complexity; no new training runs beyond the existing one.
**Security/Compliance** — money constants used in tuning must carry the ASSUMED label in any doc or badge that cites them; DECISIONS.md entry is mandatory (project rule) BEFORE the code merges.
**Operational** — `make check` and `make e2e` green after re-export; the flip-rate/credibility-exhibit numbers must be recomputed if that spec already merged (its seeds 1/2/3/42 loop re-runs automatically as part of re-export).

## Acceptance Criteria

1. Given the gate computation, when run, then its before/after table (refusal rates on A-test and B, net value at 1%/4%/8%) exists in the DECISIONS.md row or a linked scratch output, and PASS/SKIP is unambiguous against the 2pp/5% thresholds (which are labelled ASSUMED pre-registered bars).
2. If SKIP: no production file other than DECISIONS.md changes, and the task ends.
3. If PASS: given seed 42, when the pipeline re-runs, then new tau/delta come from the value objective, refusal rate on B stays in [5%, 40%] (sanity band — 0% refusal is a failing test, A5), and `report.ml` reflects the new pair.
4. Given the re-export, when diffed against the old seed.json, then ONLY value-derived fields change and the diff is reviewed field-by-field before commit.
5. Given `make e2e`, when run, then all specs pass (with sample-fixture regeneration where needed) — any spec hard-coding a removed wallet ID is fixed by re-picking, not by loosening assertions.
6. Given `make check`, when run, then ruff/pyright/tsc/oxlint are clean.

## Open Questions

1. Does the value objective replace the 0.97 accuracy floor entirely, or keep accuracy as a secondary constraint (e.g., maximize value subject to accuracy ≥ 0.95)? Recommendation: keep a floor at 0.95 (ASSUMED) so value-seeking cannot collapse accuracy — who decides: user; impact if wrong: refusal rate swings wide.
2. Whose net-value formula — `src/rules/money.py::money_table` logic per wallet, or a simpler correct/wrong cost pair? Recommendation: the simpler pair first (correct = +ARPU×RAMP − cost; wrong = −cost), full money_table only if the gate result is ambiguous — who decides: executor with user sign-off.
