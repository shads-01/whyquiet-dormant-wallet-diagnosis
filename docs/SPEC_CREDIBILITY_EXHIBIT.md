# SPEC: Credibility Exhibit (refusal validity audit + falsifiability exhibit)

This spec proposes a refusal validity audit and a falsifiability exhibit so that the Evidence page proves its two central claims — "refusal is calibrated" and "robustness is tested" — with numbers instead of assertions.

Executor: Gemini 3.7 Flash. Reviewer: Shads. Verified pre-checks (2026-10-07, seed 42) are included as expected values; if your run differs by more than rounding, STOP and report.

## Verified evidence (pre-checks already run)

| Quantity | Measured value (seed 42) |
| --- | --- |
| tau / delta | 0.80 / 0.10 |
| Refusal rate, ground-truth blended wallets (n=902) | 0.326 |
| Refusal rate, clean wallets (n=2098) | 0.171 |
| Enrichment ratio | 1.91 |
| Forced-choice top-1 error among refused wallets | 0.491 |
| Forced-choice top-1 error among attributed wallets | 0.135 |

Thresholds 2.0 (enrichment) and 1.3 (failure floor) are ASSUMED pre-registered bars, not facts. Measured 1.91 sits between them; ship the numbers as-is with both bars shown — no retuning, no threshold shopping.

## Goals

1. `scripts/evaluate.py` report gains a `refusal_validity` block computed on population B joining `truth/b_labels.parquet` (`blended`, `cause`): refusal rate on blended vs clean wallets, enrichment ratio, forced-choice error among refused vs attributed wallets.
2. `web/public/seed.json` gains additive fields only: `report.ml.refusal_validity` (block above), `report.ml.verdict_flip_rate` (share of B wallets whose verdict — cause or refusal — changes across train seeds 1, 2, 3, 42), `report.population_c` (macro-F1 on attributed, refusal rate, wallet count for the hostile parameter-only population), `report.pilot` (424 wallets/arm, 3 arms, alpha 0.05, power 0.80 — re-used constants from `scripts/pilot_sample_size.py`).
3. Evidence page gains two panels: "Refusal validity" (the audit numbers + forced-choice error) and "Falsifiability" (flip rate, population C table, pilot stop rules). Both carry the mandatory caveat sentence.
4. Every existing number in seed.json reproduces byte-identically after re-export; only new fields are added.
5. `make check` and `make e2e` stay green with no test modifications other than additive assertions.

## Non-Goals

- No generator logic changes (`datagen/generate.py` stays untouched; population C is a params dict passed to the existing `make_population`).
- No cost-sensitive refusal this round (gated on a separate pre-computed delta check; deferred).
- No district/network-level supply_failure roll-up (killed: the generator has no district identifiers — `district` is a per-wallet "week changed" flag).
- No retuning of tau/delta and no changes to `src/model/train.py` thresholds or the ACCURACY_FLOOR.
- No new Python or npm dependencies.

## Constraints

**Compatibility**
- `src/model` must never import or read `truth/` (A2; enforced by existing test — the new code lives in `scripts/` and `web/`, which may read `truth/`).
- `web/public/seed.json` shape: existing keys, types and values unchanged; new keys are additive only (`web/src/api/schema.d.ts` regenerated via `make gen-types` if the OpenAPI contract changes — it should not, since these are seed fields, not API fields).
- Population C data must be written to a scratch/temp directory, never to `data/` (the seed-42 export stays the single frozen dataset; D33).

**Performance**
- Full re-export (`uv run python scripts/export_seed.py --seed 42`) completes in under 5 minutes on a laptop; 4 model retrains (seeds 1/2/3/42) are ~100 boosting rounds each on 4800 wallets — acceptable.

**Security/Compliance**
- No PII anywhere; wallet IDs are pseudonymous `W-XXXXXX` (D13b).
- The caveat sentence must appear verbatim in the UI: "Refusal is calibrated against the simulator's own ambiguity flag; whether real ambiguity looks like ours is what real upay data would answer first." (A3-mandated wording.)

**Operational**
- Everything reproducible by one command per artifact: `uv run python scripts/evaluate.py --seed 42`, `uv run python scripts/export_seed.py --seed 42`, population C via the new script (below).
- Population C params must be committed in the script (deterministic, no env-dependent config).

## Acceptance Criteria

1. Given seed 42, when `uv run python scripts/evaluate.py --seed 42` runs, then the JSON includes `refusal_validity` with keys `refusal_rate_blended`, `refusal_rate_clean`, `enrichment_ratio`, `forced_error_refused`, `forced_error_attributed`, matching the verified table within ±0.01.
2. Given the seed.json before and after re-export, when diffed, then every pre-existing value is identical and the diff contains only the four additive blocks from Goal 2.
3. Given the forced-choice computation, when run, then refused-wallet error (0.491 expected) exceeds attributed-wallet error (0.135 expected) by at least 2× — this is the audit's pass condition; if it ever fails, the exhibit shows the failure rather than hiding it.
4. Given the Evidence page, when a user opens it, then both new panels render the real seed.json values (not hard-coded), display ASSUMED badges on: the 2×/1.3× bars, population C param choices, pilot constants, and the caveat sentence appears verbatim.
5. Given the existing e2e suite, when `make e2e` runs, then all 41 prior tests pass unchanged and at least one new assertion covers the refusal-validity panel rendering a real number.
6. Given `make check`, when run, then ruff, pyright and `npx tsc -b --noEmit` are clean.
7. Given the flip-rate computation, when run, then `verdict_flip_rate` is a number in [0, 1] computed from B verdicts across train seeds 1/2/3/42 using the frozen seed-42 dataset (not re-generated data).

## Implementation notes (for the executor)

- Audit lives in `scripts/evaluate.py::report()` — it already loads B wallets, predictions and `truth/b_labels.parquet` (see `_split`); add the block there, then have `scripts/export_seed.py` carry it into seed.json.
- Forced-choice error: among refused wallets, take argmax cause, compare to truth. Among attributed wallets, same for contrast. (`src/model/train.py::decide` returns `None` for refusals; argmax of `proba` is the forced choice.)
- Flip rate: for each seed in {1, 2, 3, 42}, `train(seed, data/train)` → `decide` on B → verdict string (cause name or `"refused"`); flip rate = share of wallets where verdict differs from the seed-42 verdict.
- Population C: new `scripts/population_c.py` defining `PARAMS["C"]` as a hostile variant of `PARAMS["B"]` (e.g., invert the cause-prior mix, different pay-cycle shares, `fee_week` shifted, higher noise) — copy the B dict from `datagen/generate.py` and mutate values, do not import-and-mutate at runtime from B. Call `datagen.generate.make_population(PARAMS["C"], ids, rng)` with the same wallet-id space as B, write parquet to a `tempfile` dir, run the seed-42 model over it, keep only metrics. The model may read `data/train` (legal); the C labels go to the scratch dir and only aggregate metrics survive.
- Pilot block: import or copy the constants from `scripts/pilot_sample_size.py`; do not recompute.
- UI: follow `web/src/Evidence.tsx` existing panel patterns (4 states, ASSUMED badges, responsive to 375px). Two panels; do not restructure existing ones.

## Open Questions

1. Population C's exact hostile param values (invert priors fully vs 60/40 skew?) — who decides: Shads/user; impact if wrong: too gentle = boring exhibit, too harsh = model fails stupidly (confident wrong answers), which backfires. Rule: if population C refusal rate does not rise above B's 21.7%, tune params once; if it still doesn't, report the result honestly — robustness either way is a finding.
2. Does the flip-rate include refusals flipping to attributed and vice versa, or only cause-to-cause? Assumed: include both (a verdict is a verdict) — who knows: Shads; impact if wrong: slightly different headline number, nothing structural.
3. Panel copy: bilingual message previews are NOT needed here (operator-facing English-only per D13b read paths) — confirm with user if in doubt.
