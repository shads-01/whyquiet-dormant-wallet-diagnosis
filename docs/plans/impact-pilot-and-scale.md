# Spec: pilot protocol, per-cause break-even rollout, Upay scale (section 2)

Executor: obey AGENTS.md (ponytail, stdlib only, ask before any new dependency, never delete files,
never invent numbers, every non-sourced input labelled `ASSUMED`). Do NOT edit `docs/slides/deck.html`
or any slide; only produce the files below. Context: BB data really ends at 2025-02 (later months are
unpublished on the portal), so "latest BB month = 2025-02" is correct; say so in outputs.

## A. Verification first (fix or report; paste real command output)
1. `make check` and `uv run pytest -q` must be green. Show output. Fix anything red (smallest change).
2. Confirm `docs/DECISIONS.md` has appended rows for (a) per-cause costing + solved_problem=0 recovery,
   (b) Bangladesh Bank MFS source + Upay dormant-pool method. If missing, append them (append-only table).
3. In `src/rules/money.py` add a comment + one `ASSUMPTIONS` line: the blanket `rule` baseline still credits
   recovery on solved_problem wallets while `model` credits 0 (conservative against the model), and the
   oracle is an approximation built from predicted counts, not a true upper bound.
4. Print the model-vs-rule net value table (rows: strategy x recovery_rate 1/4/8%, at cost_scale 1.0) from
   the current report, plus `break_even_rates()`. State plainly whether model beats rule at 1%, 4%, 8% and
   how the old "+74% at 8%" changed. Do not smooth bad news.

## B. `scripts/pilot_sample_size.py` -> `docs/PILOT_PROTOCOL.md`
Stdlib only (`statistics.NormalDist`). Two-proportion test, two-sided alpha=0.05, power=0.80.
- Control = blanket SMS; arm = cause-targeted remedy on ONE cheap cause first (supply_failure, then migration).
- Baseline control recovery = recovery_rate * GENERIC_FACTOR for rate in (0.01, 0.04, 0.08) (ASSUMED);
  treatment = recovery_rate. Compute n per arm for each rate and for each cause eligible.
- Protocol text in `docs/PILOT_PROTOCOL.md` (<= 1 page): 2-week window; randomised holdout (no message) +
  blanket arm + targeted arm; primary metric = reactivated wallets per 1,000 messaged (reactivated =
  >=1 transaction within 30 days of send); stop rule = pre-registered break-even per cause from
  `break_even_rates()` (go only if targeted recovery > break-even); guardrails: opt-out rate, complaint
  count, no PII leaves Upay (aggregate counts only); decision table go/hold/stop. All thresholds from code.
- Mark as "proposed; not yet run". Never claim measured results.

## C. `scripts/upay_scale.py` -> `data/public/upay_scale.json`
Inputs: `data/public/upay_dormant_pool.json` (3 scenarios), model per-cause mix and `money_table` from
the existing report (population B, headline set), `break_even_rates()`.
- net_value_per_triaged_wallet(rate, cost_scale) = model value_bdt / n_triaged (from the report).
- For each pool scenario x rate (1/4/8%) x cost_scale (0.5/1/1.5): total_net_value_bdt = pool * that, for
  BOTH `model` and `rule`, plus `model_minus_rule`. Negative values stay negative (do not clip).
- Add `cheap_first_rollout`: causes sorted by break-even ascending, with a boolean `pays_at_rate` for each
  of 1/4/8% (rate >= break-even). Add `blended_cost_if_cheap_first_only` for the causes that pay at 4%.
- Metadata: every input with provenance (`SOURCED:<url>` or `ASSUMED`), the BB month used, the
  caveats array copied from the dormant-pool JSON, and "pilot not run: all values are simulation".
- Add pytest: JSON loads, 3x3x3 rows per strategy, no NaN, negatives preserved, model_minus_rule consistent.

## D. `docs/IMPACT_SLIDE_COPY.md` (draft copy only, for me to paste later)
Short sections, every number pulled from the JSON/report (cite the file + key), none typed by hand:
1. Headline, break-even first: the per-cause break-even table and the sentence "pays off if recovery
   >= X% (cause-specific)".
2. Upay scale range (Industry Central scenario as central, other two as range), at the rate(s) where
   model beats rule. If model does not beat rule at some rate, say so in one line (honest refusal).
3. Cheap-first rollout and why (supply_failure, migration first; fee_shock waits for pilot evidence).
4. Pilot box: protocol one-liner + sample size per arm + stop rule.
5. Footnote: "Synthetic data. Economic inputs ASSUMED. Industry-wide BB data (Feb 2025); Upay base
   ~7M is STALE (late 2022). Not yet measured in production." Include the source URLs from the JSON.
Tone: judges criticised "unmeasured/simulation"; own it, show how to measure it, show the threshold.

## Done criteria
- `make check` and pytest green (paste output). New files: `scripts/pilot_sample_size.py`,
  `docs/PILOT_PROTOCOL.md`, `scripts/upay_scale.py`, `data/public/upay_scale.json`,
  `docs/IMPACT_SLIDE_COPY.md`, tests, DECISIONS rows appended.
- Final report: the A.4 table, the sample size per arm per rate, and Upay central net-value range, with
  every ASSUMED input listed.
