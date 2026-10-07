# SPEC: Fairness Depth (intersectional slices, routed campaign export)

This spec proposes extending fairness reporting to joint demographic slices and carrying the routed strategy decision (D56) into the campaign export so that governance artifacts match what the money model actually recommends.

**Execution order:** Wave 4 — OPTIONAL (Tier 1). MUST run after SPEC_COST_SENSITIVE_REFUSAL if that spec shipped (shared files + number churn); can run after SPEC_METRIC_DEPTH if cost-sensitive was skipped. **File ownership:** `scripts/evaluate.py`, `scripts/export_seed.py`, `src/api/batches.py`, its tests, `web/src/Evidence.tsx`, seed.json re-export.

## Verified facts (pre-checked 2026-10-07)

- `scripts/evaluate.py::fairness()` slices `worker_type` and `pay_cycle` independently; no joint slice exists.
- `report.routing_plan` is exported (D56) but the campaign export endpoint (`GET /api/batches/{id}/export`, D47) predates routing — VERIFY what it currently emits before changing it.
- Tier-0 fairness requirement (A7) is already satisfied by the existing per-slice table; this spec is depth, not compliance.

## Goals

1. `fairness()` gains joint slices `worker_type × pay_cycle` (additive rows in the existing format: `slice: "worker_type×pay_cycle"`); groups with n < 30 are reported with an explicit low-n flag rather than dropped (honesty over tidiness).
2. Campaign export JSON/CSV includes, per wallet: the routed action (targeted/blanket/none, D56) and its cause — so an approved campaign's export reflects the routing decision, not just the raw attribution.
3. Evidence fairness table renders the joint slices (collapsible section so the page doesn't balloon).

## Non-Goals

- No new fairness metric families (no equalized-odds/demographic-parity ratio machinery — the existing macro-F1 + refusal-rate-per-slice framing stays).
- No changes to the generator, model, or thresholds.
- No per-group ECE (skip unless trivially available from SPEC_METRIC_DEPTH's bin refactor).

## Constraints

**Compatibility** — additive seed fields and additive export-object keys only; existing export consumers (the download blob shape) must keep working — VERIFY with the e2e export test before changing structure.
**Performance** — joint slices multiply rows ~9×; the collapsible UI keeps render cost flat.
**Security/Compliance** — export stays behind auth (D47); no PII (wallet IDs are pseudonymous, D13b); low-n groups flagged, never hidden.
**Operational** — API change requires a test covering the new fields (project rule: every endpoint change needs tests); `make check` + `make e2e` green.

## Acceptance Criteria

1. Given seed 42, when evaluate runs, then the fairness array contains `worker_type×pay_cycle` rows, each with n and a low-n flag where n < 30, and the sum of all slice n values equals the B population size.
2. Given an approved batch, when its export is downloaded, then each wallet row includes the routed action and cause, and the values match `report.routing_plan` logic for those wallets.
3. Given the Evidence fairness table, when rendered, then joint slices appear in a collapsible section and existing single-slice rows are unchanged.
4. Given the API test suite, when run, then a test asserts the export payload contains the new keys (endpoint-change rule).
5. Given `make check` and `make e2e`, when run, then everything is green.

## Open Questions

1. What does the export currently emit (verify first — D47 may already include cause) — who knows: `src/api/batches.py` reader; impact if wrong: duplicate fields.
2. Whether CSV export exists alongside JSON and needs the same fields — who knows: export endpoint; impact if wrong: inconsistent artifacts.
