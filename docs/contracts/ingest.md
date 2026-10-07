# Contract 3 — Ledger ingest (live scoring)

> Owner: `src/api/score.py` (D55). Machine-readable source of truth: `ScoreRequest` in the live OpenAPI at
> `/api/docs`. Sample file: `web/public/sample-ledger.csv` (20 synthetic population B wallets).

## What upay sends

Weekly **aggregates** per dormant-candidate wallet. No names, phone numbers, NIDs or transaction-level rows
(FR-11). The wallet ID is upay's own pseudonym in the form `W-XXXXXX`.

The window is the **52 weeks ending at the scoring date**: week 51 is the most recent full week, week 0 is 51
weeks earlier. A wallet acquired inside the window starts at its `acquired_week`.

### Flat file (CSV or Parquet): one row per wallet-week

Used by the console's Score page and by `scripts/score_batch.py`.

| Column | Type | Required | Meaning |
| --- | --- | --- | --- |
| `wallet_id` | `W-[0-9A-Z]{6}` | yes | Pseudonymous wallet ID |
| `acquired_week` | int 0..51 | yes | First week in the window the wallet existed (repeat on every row) |
| `fee_week` | int 0..51 | yes | Week the last fee change reached this wallet (repeat on every row) |
| `pay_cycle` | `weekly` / `biweekly` / `monthly` | yes | Salary cycle on file (repeat on every row) |
| `week` | int 0..51, ≥ `acquired_week` | yes | Week index in the window |
| `txn_count` | int ≥ 0 | yes | Transactions that week |
| `amount_bdt` | number ≥ 0 | yes | Value of those transactions |
| `cashin_count` | int ≥ 0 | no (0) | Cash-ins that week |
| `cashout_ok` | int ≥ 0 | no (0) | Successful cash-outs |
| `cashout_fail` | int ≥ 0 | no (0) | Failed cash-out attempts (agent out of float, etc.) |
| `app_share` | 0..1 or empty | no (empty) | Share of that week's transactions made in the app; empty if none |
| `district_changed` | 0/1 | no (0) | 1 if the wallet transacted from a new district that week |

Weeks that are left out count as silent (all zeros), so a ledger can send active weeks only.

### JSON (`POST /api/score`)

The same data, grouped: `{"wallets": [{wallet_id, acquired_week, fee_week, pay_cycle, weeks: [{week, txn_count, ...}]}]}`.
At most **500 wallets per request** (≈ 2.5 MB, under Vercel's 4.5 MB body limit,
https://vercel.com/docs/functions/limitations). Send larger files in chunks; the Score page does this.

Auth: `X-API-Key: <SCORE_API_KEY>` for upay backends, or `Authorization: Bearer <token>` for a signed-in
analyst or approver.

## What comes back

One result per wallet, **in request order**: `verdict` (`attributed` / `refused`), `cause`, `posterior` over the
five causes, top-8 `contributions`, `refusal_reasons`, `rule_baseline`, and the priced `remedy` (null if refused).
The response also carries `model_version`, `tau` and `delta`.

Refusals before the model (still first-class answers, never errors):
- no transaction anywhere in the window: "No transaction in the history, so there is no decline shape to read";
- last transaction under 3 weeks ago (the `src/rules` dormancy rule): "Not dormant: ...".

## Errors

| Status | When |
| --- | --- |
| 401 | missing or wrong API key / token |
| 403 | signed-in account has no WhyQuiet role |
| 422 | schema violation: bad ID, week outside 0..51 or before `acquired_week`, duplicate week or wallet, negative count, more than 500 wallets |
| 503 | model file missing, or Supabase down on the bearer-token path |
