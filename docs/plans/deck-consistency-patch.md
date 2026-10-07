# Spec: deck + docs consistency patch (stale claims -> routed numbers)

Executor: obey AGENTS.md (no new features, docs/claims only; never invent numbers; every number comes from
`data/public/upay_scale.json`, the exported report (`web/public/seed.json` / `seed.sample.json`), or
`src/rules/money.py`; unsourced inputs stay `ASSUMED`; never delete files; append a row to `docs/DECISIONS.md`).
Do not change any model, rule, API or test logic. If a number you need is not in those sources, STOP and report it.

## 1. Sweep for stale claims
Run: `grep -rniE "74%|34,947|7,172|7172|11\.0|11 BDT|11\.00|average remedy|wasted spend|waste prevention|saved" docs README.md web/src web/public docs/slides`
(exclude `docs/plans/`, `docs/v3/`, `node_modules`). Produce a table of every hit: file, line, old text, action.
Known targets: `README.md` ~L444, `docs/report.md` ~L197 and ~L216, `docs/PROJECT_REPORT.md` ~L203, ~L221, ~L222,
`docs/DECISIONS.md` D19 (append-only: do NOT edit D19; add a new row noting it is superseded by D53/D56),
and `docs/slides/deck.html` (check every impact/economics/refusal slide).

## 2. Replacement facts (fill from sources, do not hand-type)
Pull from the report/JSON and put the exact values into the text:
- Costing: per-cause remedy cost (supply_failure 5, migration 10, job_exit 15, fee_shock 25, solved_problem 0 BDT,
  all ASSUMED). Delete every "11 BDT average" claim.
- Break-even recovery per cause: 1.39%, 2.78%, 4.17%, 6.94% (cost / (ARPU*RAMP=360)); read from `break_even_rates()`.
- Strategy table on population B (3,000 wallets), cost scale 1.0x, at 1% / 4% / 8%: rule, unrouted model, routed.
  Show all three rates, including the 1% row where routed is below rule, with the one-line reason:
  "blanket SMS also credits completed-lifecycle (solved_problem) wallets; like-for-like, routed matches blanket".
- Headline wording (use exactly this order and tone, filling numbers from the sources):
  1. "Never worse than blanket SMS like-for-like; break-even per cause is X%."
  2. "At 4% recovery routed beats blanket by Y%; at 8% by Z% (simulation, ASSUMED inputs)."
  3. "Upay scale (ASSUMED: Upay cause mix = synthetic population B; base ~7M stale late 2022; Bangladesh Bank
     industry inactive share 63.57% as of Feb 2025): central scenario routed net value at 1/4/8% vs blanket."
  4. "Not yet measured in production: proposed 2-week pilot (docs/PILOT_PROTOCOL.md), n per arm from
     scripts/pilot_sample_size.py, stop rule = per-cause break-even."
- Remove/replace "+74%" and "+34,947.20 BDT" everywhere.

## 3. Refusal reframe (important)
Old claim: refusal "saved 7,172 BDT in wasted spend". In `routed`, refused wallets get blanket SMS if
blanket EV > 0, else none; refusal now means "do not send the expensive targeted remedy".
- Recompute from the code what refusal avoids: spend if the targeted remedy had been sent to the refused
  wallets vs spend under routed (script or inline calculation, deterministic, from the report counts; show the
  formula). If you cannot reproduce 7,172 exactly from the current code, drop that number and use the
  recomputed one; say "recomputed under per-cause costs".
- Wording: "Calibrated refusal routes 652 ambiguous wallets (use the real count from the report) to the cheap
  blanket message instead of a costly targeted remedy; avoided targeted spend = N BDT (recomputed)."
- Keep refusal described as a first-class output with reasons (AGENTS.md).

## 4. Deck
- Edit only `docs/slides/deck.html` text/tables for the impact content. Keep layout/CSS/components unchanged.
  If adding a slide is unavoidable, copy an existing slide's markup. Order: break-even table, strategy
  table (1/4/8%), Upay range, pilot box, footnote (sources + ASSUMED list + "synthetic data; simulation").
- Footnote source URLs: Bangladesh Bank MFS page (https://www.bb.org.bd/en/index.php/financialactivity/mfsdata)
  and the TBS News URL stored in `data/public/upay_dormant_pool.json`.
- If the repo has `scripts/convert_deck_to_pptx.py` and a `.pptx` of the deck, regenerate it ONLY if the script
  runs without new dependencies; otherwise report that the pptx is stale.

## 5. Verify
- Re-run the grep from step 1: zero stale hits outside historical/append-only files (list the exceptions).
- `make check`, `uv run pytest -q` (and e2e if any text assertions reference changed strings). Paste output.
- Report: the before/after table of claims, the recomputed refusal number with its formula, and any number
  you could not source.
