# Spec: price-aware routing (`routed` strategy)

Executor: obey AGENTS.md (ponytail, no new deps, never delete files, never invent numbers, inputs `ASSUMED`
unless sourced, business rules deterministic in `src/rules`, `src/model` never imports `truth/`).
Do NOT edit `docs/slides/deck.html`. Run `make check` and `uv run pytest -q`; paste output.
Append a row to `docs/DECISIONS.md` (next free id) for this change.

## Why
Current model loses to blanket SMS at 1% and 4% recovery because it sends expensive remedies
(fee_shock 25 BDT, job_exit 15 BDT) where they cannot pay back. Fix: a deterministic routing rule that
picks, per predicted cause, the cheapest action that is net-positive, falling back to blanket SMS or no action.

## Routing rule (put in `src/rules/routing.py`, pure functions, no I/O)
Constants come from `money.py`/`remedies.py` (ARPU_BDT, RAMP, GENERIC_FACTOR, MSG_COST_BDT, unit costs).
V = ARPU_BDT * RAMP (value per recovered wallet).

For a predicted cause c at recovery rate r and cost_scale s, with precision p_c (share of wallets predicted c
that truly are c):
- EV_targeted(c) = r * (p_c + (1 - p_c) * GENERIC_FACTOR) * V - unit_cost[c] * s
- EV_blanket     = r * GENERIC_FACTOR * V - MSG_COST_BDT
- action(c) = "targeted" if EV_targeted > max(EV_blanket, 0)
              else "blanket" if EV_blanket > 0
              else "none".
- solved_problem: always "none" (no action, recovers 0, cost 0), as in the existing model.
- Refused wallets: use the same blanket-or-none test (cause unknown). ASSUMED; state it in ASSUMPTIONS.
- Expose `route(cause, rate, cost_scale, precision) -> str` and `routing_plan(per_cause_precision, rate,
  cost_scale) -> dict[str, str]`.

### Precision source (important: no leakage)
Headline accuracy is population B only, so routing must NOT be tuned on population B. Use per-cause
precision from population A (out-of-fold or validation predictions) if the training code already produces
it (check `src/model/train.py` and its saved metrics). If it does not, use precision-free routing
(p_c = 1.0, optimistic) AND flag it with a code comment + ASSUMPTIONS line + report note
"precision assumed 1.0; replace with population-A validation precision". Report which path you took.

## `src/rules/money.py`
- Add a fourth strategy `routed` to `money_table` (same row keys, `strategy="routed"`), so each rate yields
  rule, model, oracle, routed. Keep `money_sweep` working across cost scales.
- `routed` per predicted cause c: actions from `routing_plan`; targeted actioned wallets use the model
  recovery formula (correct*r + wrong*r*G) at unit_cost[c]*s; blanket wallets recover at r*G at MSG_COST_BDT;
  none = 0/0. Refused wallets follow the refused rule above.
- Keep existing strategies' numbers unchanged. Update `ASSUMPTIONS`.
- Property to enforce in tests: at every (rate, scale), routed value >= rule value on the same inputs
  (only up to the rule's solved_problem asymmetry; if that asymmetry breaks the inequality, assert
  routed >= rule - (solved_problem wallets * r * G * V) and explain in a comment).

## Plumbing
- `grep -rn "money_table\|money_sweep\|strategy" src scripts tests api web/src` and update every caller.
- Report/export JSON: routed rows appear automatically via the same rows list; add `routing_plan` per
  rate to the report so the UI/slides can show "which cause gets which action at which rate".
- Frontend: only widen the types in `web/src/seed.ts` (strategy union gets `"routed"`) and make
  `Evidence.tsx` render the extra row if it iterates strategies. No redesign. `make gen-types` if the API
  schema changed. Existing e2e must still pass.

## Upay scale
- Update `scripts/upay_scale.py` / `data/public/upay_scale.json` so each scenario x rate x cost_scale grid
  also includes `routed` and `routed_minus_rule`. Keep negative values unclipped. Show ALL of 1%, 4%, 8%.
- Metadata must state: scaling assumes Upay's cause mix and error rates equal synthetic population B
  (ASSUMED), BB data month 2025-02, Upay base ~7M stale late 2022, pilot not run.
- Update `docs/IMPACT_SLIDE_COPY.md` to lead with `routed` (still break-even first), pulling every
  number from the JSON/report. Include the 1% and 4% rows even if routed equals rule there (say "matches
  blanket; no loss"). Do not delete the earlier honest model-vs-rule table; keep it as the "why routing".

## Tests
- Unit: `route()` for each cause at r in {1%, 4%, 8%}, p=1.0 and p=0.7 (e.g. at r=1% supply_failure is NOT
  targeted because break-even is 1.39%; at 4% migration and supply_failure are; fee_shock only at >= ~6.94%/(p adj.)).
- solved_problem always none. cost_scale monotonic: higher cost never turns "blanket" into "targeted".
- `money_table` has 12 rows (4 strategies x 3 rates); routed >= rule property; refused handling.
- Extend `tests/test_upay_scale.py` for the new columns.

## Done criteria
- `make check` and `uv run pytest -q` green (paste output).
- Final report, as tables: (1) routing plan per rate, (2) rule vs model vs routed net value at 1/4/8% on
  population B, cost_scale 1.0 and the 0.5/1.5 sweep for routed, (3) Upay central scenario net value
  range for routed vs rule at all three rates, (4) which precision path was used, (5) every ASSUMED input.
- State plainly if routed fails to beat rule anywhere and why. No claims beyond the numbers.
