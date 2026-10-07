# Plan: per-cause money model + break-even + cost sweep

Executor: obey AGENTS.md (ponytail, no new deps without asking, no file deletion, never invent numbers,
every cost/rate stays `ASSUMED`). Run `make check` and `uv run pytest -q` before claiming done; show output.
Append one row to `docs/DECISIONS.md` (id, decision, reason) for this change.

## Why
`src/rules/money.py` costs every targeted wallet at one blended `AVG_REMEDY_COST_BDT = 11.0`, ignoring
`src/rules/remedies.py` (per-cause `unit_cost_bdt`: supply_failure 5, migration 10, job_exit 15,
fee_shock 25, solved_problem 0). It also credits solved_problem wallets with recovery although no
message is sent. Per-wallet value on recovery = ARPU_BDT * RAMP = 360 BDT.

## Changes (approved: money table shape MAY change)

### 1. `src/rules/money.py`
- Remove `AVG_REMEDY_COST_BDT`; cost each wallet via `REMEDIES[cause]["unit_cost_bdt"]`.
- New signature: `money_table(per_cause: dict[str, dict[str, int]], n_refused: int, n_triaged: int, cost_scale: float = 1.0)`
  where `per_cause[cause] = {"correct": int, "wrong": int}` (wrong = wallets truly of this cause that
  were predicted as another cause is NOT needed; use predicted cause: wallets ACTIONED under that remedy,
  split by whether the prediction was correct). Keep same 3 strategies x 3 recovery rates rows, same keys.
- model strategy: for each predicted cause c: actioned = correct+wrong; cost = actioned * unit_cost[c] * cost_scale;
  recovered = (correct*rate + wrong*rate*GENERIC_FACTOR); for c == "solved_problem": recovered = 0, cost = 0.
- oracle strategy: cost = sum over TRUE cause counts (correct+wrong per cause is not the truth; take
  true-cause counts from the same input as `correct` where predicted==true plus misclassified mapped back;
  if true counts are not available at the call site, derive oracle from `correct+wrong` per cause as
  an approximation and say so in a code comment `# ASSUMED approximation`).
- rule (blanket) strategy: unchanged.
- Update `ASSUMPTIONS` text: replace the blended-cost line with a per-cause line and add one line
  "ASSUMED: solved_problem wallets receive no action and recover at 0."

### 2. Break-even (add to `money.py`, pure functions)
- `break_even_rate(cause) -> float | None` = unit_cost / (ARPU_BDT * RAMP); `None` for solved_problem.
- `break_even_rates() -> dict[str, float | None]` over all five causes.
- Expect: supply_failure ~0.0139, migration ~0.0278, job_exit ~0.0417, fee_shock ~0.0694.

### 3. Cost sweep (safety net)
- `COST_SCALES = (0.5, 1.0, 1.5)`. Add `money_sweep(...)` returning rows for each scale
  (add key `cost_scale`). Do not change the blanket baseline cost for any scale.

### 4. Callers
- `grep -rn "money_table\|AVG_REMEDY" src scripts tests api datagen web/src` and fix every caller.
- Where the report/export is built (see `tests/test_export_seed.py`, `scripts/`), include
  `break_even` and `sweep` in the report JSON. Regenerate `web/public/seed.sample.json` ONLY if the
  repo's existing script does it; then run `make gen-types` if the OpenAPI schema changed.
- Frontend: do NOT redesign UI. If `web/src/seed.ts` types fail typecheck, add the new optional fields only.

### 5. Tests (update, do not delete)
- `tests/test_rules.py`: update money assertions for the new numbers; add: break-even values within 1e-3;
  solved_problem recovers 0 and costs 0; cost_scale=2.0 doubles model/oracle cost but not rule cost;
  refused wallets cost 0.
- `tests/test_export_seed.py`, `tests/test_sample_seed.py`: adapt to the new rows/fields.
- Never import `truth/` from `src/model`.

## Done criteria
- `make check` and `uv run pytest -q` green (paste output).
- Report to me, as a table, the NEW model-vs-rule net value at 1%, 4%, 8% (scale 1.0) and the
  change vs the old +74% at 8%. State plainly if it went down. Do not edit slides or claims.
- DECISIONS.md row appended.
