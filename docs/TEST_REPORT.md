# End-to-end test report (2026-10-04)

First run on `main` at `d75d445`; re-checked after Arko's `599818d` and `9335ddb`, the fresh deploy and
CI/CD (PR #6, merged) and Arko's open items (PR #7, open). Owners follow the directory split in
[plans/README.md](plans/README.md): **Shads** = `web/**`, **Hrittika** = data/model, **Arko** = `src/rules`,
`src/api`, `api/`, `supabase/`, `README.md`, `Makefile`, `vercel.json`, deploy.

Status key: **OPEN** · **DONE** (merged to `main`) · **PR #7** (fixed, waiting for review and merge).

## 1. What passed

| Check | Result |
| --- | --- |
| `ruff check` | passed |
| `pyright` | 0 errors |
| `pytest -q` | 88 passed on `d75d445`; **105 passed** on PR #7 |
| OpenAPI and `schema.d.ts` in sync | no drift (PR #7 regenerates both after removing the stub endpoints) |
| `tsc -b`, `oxlint`, `vite build` | passed (bundle 714 kB, over the 500 kB warning) |
| Playwright e2e | 27 / 27 passed (also on PR #7) |
| `seed.json` integrity (400 wallets, 100 refused, IDs, posteriors sum to 1, numbers match README) | passed |
| Write path against the new Supabase project | 11 / 11 checks passed: login, wrong password 401, wrong role 403, propose, same wallets again 409, export before approval 409, unknown batch 404, approve, approve again 409, export, anon key sees nothing |
| **Live site** (`scripts/verify_deploy.py`) | old site FAIL; **PASS** on https://whyquiet.vercel.app |
| CI/CD | `ci.yml` green on `main`; `deploy.yml` deployed `4dfa7b9` and its live check passed |

`make` is not installed on Windows, so each `make check` step was run by hand.

## 2. Bugs (most serious first)

| # | Owner | Status | Problem | Example / proof | Fix |
| --- | --- | --- | --- | --- | --- |
| 1 | **Arko** (Task 5, deploy) | **DONE** (Hrittika, D37, PR #6) | The live Vercel site was the hour-0 placeholder. | Home page said "Operator console placeholder"; `/seed.json` and `/api/batches` returned 404. | Fresh Vercel project `whyquiet` at https://whyquiet.vercel.app. |
| 1b | **Arko** (Tasks 3 and 5) | **DONE** (Hrittika, D37, PR #6) | The batches migration was never applied and the demo accounts never created, though STATE.md and README said so. | `GET /api/batches` returned 500 "Could not find the table 'public.batch_summaries'". The UI hid it behind "write path offline". | Fresh Supabase project `grflsfhkcatoxpjeszxh` with both migrations and both demo accounts. |
| 2 | **Shads** (Task 4) | OPEN | Sign-in is fake. `handleLoginSubmit` in `web/src/App.tsx` never calls `login()` from `api.ts`. It waits 400 ms and saves the role button you clicked. | Signed in as approver with password `••••••••`; no request to `/api/auth/login`. No token is stored, so every write call gets 401. | Call `login(email, password)` from `api.ts`, use the role the server returns, show the error `detail` on failure. |
| 3 | **Shads** (Task 4) | OPEN | The Batches page hides every API failure and pretends it worked. `proposeBatch`, `decideBatch` and `exportBatch` each sit in a `catch {}` that builds a fake local result (`web/src/Batches.tsx`). | "Batch BATCH-4821 successfully proposed!" appears although the API returned 401. Real 409 and 403 errors never reach the screen. | Fall back only on 503 (write path offline); otherwise show `err.message`. |
| 4 | **Shads** | OPEN | Exported campaign file can contain the wrong wallets. The export fallback fills `wallet_ids` from the cause in the dropdown, not the batch's cause. | Select "Fee Shock", then download an approved Job Exit batch: the file lists Fee Shock wallets. | Remove the fallback or filter by `batch.cause`. |
| 5 | **Shads** | OPEN | Self-approval guard never fires on real batches. UI compares `user.email === b.proposed_by`, but the API returns a user UUID. | Works only on the hard-coded sample batches. | Store `user_id` from the login response (after #2) and compare `user.user_id === b.proposed_by`. |
| 6 | **Shads** | OPEN | Fake sample batches are shown as if real when the batch list is empty. | IDs like `BATCH-8910` are not UUIDs (approve returns 422); codes like `REM-JOB-01` fail the DB check `^[a-z][a-z0-9_]{1,63}$`. | Show an empty state; use sample batches only in offline (503) mode, labelled as sample. |
| 7 | **Arko** (`Makefile`) | **DONE** (Hrittika, D36, PR #6) | `make dev` started the API on 8000 while Vite forwards `/api` to 8008, so every local API call failed. | Header showed "API down". | Makefile, README and the 5 agent instruction files use port 8008. |
| 8 | **Shads** (Task 3) | OPEN | Money chart Y axis shows "৳0.0M" on every tick (`web/src/Evidence.tsx:403` divides by 1,000,000; values are in thousands). | All four ticks read ৳0.0M. | Use `formatBDT(val)`, or divide by 1000 and show `k`. |
| 9 | **Shads** | OPEN | Table shows fractional people, e.g. "84.41" recovered users. | Evidence money table, 4% row. | Round for display, or label the column "expected". |
| 10 | **Arko** (Task 6) | **PR #7** (Hrittika, D40) | The hour-0 stub endpoints `/api/triage`, `/profile`, `/explain`, `/refuse` returned the same hard-coded answer for any input, had no auth or validation, and `/api/triage` let anyone write audit rows. | `POST /api/triage {"wallet_id":"anything at all"}` returned "attributed: job_exit" at 0.30, which the 0.80 refusal bar forbids. The Queue quick lookup called `/api/triage` and showed "evaluated via live Cause Desk model" for it. | Removed with their models and example data. Side effects listed in section 4. |
| 11 | **Arko** (`src/api/auth.py`, from `599818d`) | **PR #7** (Hrittika, D40) | `except Exception` in `current_user` turned a Supabase outage into **401 "Invalid or expired token"**; the contract says 503. | A paused free-tier project would look like a bad login instead of showing the offline banner. | One app-level handler maps network errors and auth 5xx to 503 "Write path offline"; tests cover auth and DB outages. |

## 3. Missing or out of date

| # | Owner | Status | What | Fix |
| --- | --- | --- | --- | --- |
| 12 | **Arko** | **DONE** (Hrittika, D36, PR #6) | `.env` was never loaded. | `uv run --env-file .env ...` (built into uv, no new dependency, not loaded during `pytest`). Local `.env` now holds the new project's keys, DB password and demo passwords. |
| 13 | **Shads** (Task 4/5) | OPEN | No test covers the real write path; the e2e batch tests only exercise the fake fallback, so they pass although login is fake. | Add an e2e that mocks `/api/*` with `page.route` and checks login calls the API and 401/403/409 are shown. |
| 14 | **Shads + Arko** (Task 5) | OPEN | Full flow on prod through the website (analyst proposes, approver approves, download) not possible until #2 and #3 are fixed. The API flow is verified (section 1). | Do it after #2, #3. |
| 15 | **Shads** (Task 6) | OPEN | `docs/demo-script.md` does not exist. | Write it (3 minutes, wallet IDs picked, honesty lines verbatim). |
| 16 | **Arko** (`README.md`) | **DONE** (D36, D37, D38) | README had the wrong port, the old URL and a deploy-guide link to a path on one laptop. | Fixed. |
| 17 | **All** (`docs/STATE.md`) | **DONE** (D37) | STATE.md pointed at the old deployment. | Points at the new Vercel and Supabase projects. |
| 18 | **Hrittika** | OPEN | `docs/superpowers/` (datagen spec and plan) is committed to git, against our rule to keep those docs local. | `git rm --cached -r docs/superpowers` and add it to `.gitignore`. |
| 18b | **Shads** | OPEN | After PR #7 the Queue quick lookup still calls the removed `/api/triage`, so each lookup makes one 404 request before falling back to `seed.json`. Unknown IDs show "No anomalous lockups detected", which the model never said. | Delete the `fetch("/api/triage")` block in `web/src/Queue.tsx`; for an ID not in the seed, show "not in this sample". |
| 19 | **Shads** (minor) | OPEN | JS bundle is 714 kB (Vite warns above 500 kB). | Optional: lazy-load the Evidence page (Recharts) with `import()`. |
| 20 | **Team decision** (Arko owns `money.py`) | OPEN | Not a code bug: at the base 4% recovery rate the model earns less than the simple rule (৳4,560 vs ৳9,300); it wins only at 8%. README says so honestly, but judges will ask. | Agree on the answer for the demo script. |
| 21 | **Hrittika** (with PR #7) | OPEN | The stack line in `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `OPENCODE.md` and `.agents/rules/00-project.md` says "Postgres via Supabase (triage audit log)". After PR #7 nothing writes to `triage_audit_log`; the database holds the batches and their audit log. | Change it to "Postgres via Supabase (remedy batches + audit log)". |
| 22 | **Hrittika** | OPEN | Uncommitted edits to `.env.example` (not from this review) document `LOCAL_STORE_DIR`, which PR #7 removes. | Drop that line before committing them. |
| 23 | **Hrittika** | OPEN | The `VERCEL_TOKEN` GitHub secret (created in the Vercel dashboard) expires; when it does, `deploy.yml` fails with "missing token value" and nothing deploys. The free Supabase project pauses after 7 days without use. | Note the token's expiry date; open the site before demo day. |

## 4. Side effects of PR #7 (removing the stubs and the catch-all)

Nothing below breaks a test or a screen. Listed so reviewers know what changed besides the fixes.

| What changed | Before | After | Judgement |
| --- | --- | --- | --- |
| Queue quick lookup | Called `/api/triage`, ignored the answer, showed "evaluated via live Cause Desk model". | Gets 404, falls back to `seed.json` (the real model output). | Better; leaves one wasted request (#18b). |
| `triage_audit_log` table | Written by every public `/api/triage` call. | Nothing writes to it. Table kept (no DB change). | Intended: `docs/system-design.md` says public viewers "cannot ... write to audit logs"; `docs/database-schema.md` says the table "is not part of this design". Stale doc line: #21. |
| Odd Supabase auth replies (e.g. a non-JSON error body, `AuthUnknownError`) | 401 "Invalid or expired token" (catch-all). | 500. Outages (network errors, 5xx) are 503. | 500 is more honest (not the user's fault), but it is a change. |
| `/api/health` `store` field | `"local"` if the Supabase settings were present but creating the client failed. | `"supabase"` whenever both settings are present. | Reports configuration only; it never tested the connection. |
| Tests | `test_triage_contract`, `test_refuse_is_first_class` checked the stubs' hard-coded answers. | Removed with the stubs. Real refusal is still tested on the model (`tests/test_model.py`, e.g. `test_decide_refuses_uniform_posterior_with_both_reasons`). | No coverage lost. |
| `LOCAL_STORE_DIR` env var | Folder for the local triage JSONL file. | Not read anywhere. | See #22. |

## 5. Review of Arko's commits

### `599818d` "harden API input validation"
Good: rejects a blank bearer token, strips whitespace-only decision notes (422), adds tests for bad wallet IDs, bad auth headers and rule edge cases.

| Status | Issue |
| --- | --- |
| OPEN (process) | Pushed straight to `main` with no pull request. Team rule: one feature per branch, reviewed. |
| **PR #7** | Introduced #11 (outage reported as 401). |
| **PR #7** | Deleted `test_money_table_refusals_cost_zero`, the only test tying refusal to money. Restored. |
| **PR #7** | No `docs/DECISIONS.md` entry. Recorded as D39. |
| Note | `test_full_workflow_consistency` only checks that the fake returns what the test told it to; the added `#` comments mostly repeat function names. |

### `9335ddb` "deployment"
Good: `docs/DEPLOYMENT.md`, slim runtime `requirements.txt`, `make deploy`, the `deploy.yml` idea.

| Status | Issue |
| --- | --- |
| OPEN (process) | Also pushed straight to `main`; its first run failed (no `VERCEL_TOKEN` secret). |
| **DONE** (D38) | `.vercelignore` did not exclude `.env`, so `make deploy` from a laptop would upload secrets. Now an allowlist. |
| **DONE** (D38) | Health check ran against the per-deployment URL, which Vercel's deployment protection answers with a login redirect. Now checks https://whyquiet.vercel.app. |
| **DONE** (D38) | The workflow re-ran the whole suite already run by `ci.yml` and passed with the write path offline on every push. Now it waits for CI and checks strictly. |
| **DONE** (D38) | README linked the deploy guide as `file:///media/arkosaha/...`. Now relative. |
| **DONE** | Both of us used D35; Arko keeps D35, Hrittika's entries are D36-D38. |

## 6. Suggested order

1. **Hrittika:** review and merge PR #7 (merging deploys automatically), with #21 and #22; then #18.
2. **Shads:** #2, #3, #5, #6 together (one branch), then #18b, #4, #8, #9, #13, #15.
3. **Shads + Arko:** #14 on prod once #2 and #3 land.
4. **Team:** #20 answer for the demo script; process rule: no direct pushes to `main`.

## 7. How to test by hand (Windows, no `make`)

### Automated checks
```bash
uv run ruff check src tests datagen scripts api
uv run pyright
uv run pytest -q
cd web && npx tsc -b --noEmit && npx oxlint src e2e && npx vite build && npx playwright test
```

### Run the app (two terminals, API on port 8008)
```bash
uv run --env-file .env uvicorn src.api.main:app --port 8008
cd web && npm run dev
```
Open http://localhost:5173. Without Supabase keys in `.env`, the header shows "API ok" and Batches shows the "write path offline" banner; that is expected.

> **Careful:** your `.env` points at the **production** Supabase project. Batches and audit rows cannot be deleted (database triggers block it), so every batch you propose locally appears on the live site for good. For throwaway tests, use a separate Supabase project.

### Read screens (no login needed)
- **Queue:** header badge says "API ok", no yellow "Sample data mode" banner, 400 wallets (100 refused). Search and filters work; searching nonsense shows an empty state. Quick lookup of a wallet from the list opens it.
- **Wallet:** click a row. The 26-week chart shades the silent weeks. Attributed wallets show the remedy in English and Bengali; refused wallets show the reasons. Try `#/w/W-ZZZZZZ` for the not-found state.
- **Evidence:** headline macro-F1 86.4% with rule baseline 8.2% and shuffled control 16.2% beside it. Fairness table present. The 1% / 4% / 8% toggle changes the money table.
- **Both:** toggle dark mode, and narrow the window to phone width.

### Write path (through the API until #2 and #3 are fixed)
Demo passwords are in your `.env`. Open http://localhost:8008/api/docs (or https://whyquiet.vercel.app/api/docs) and run, in order:
- `POST /api/auth/login` as analyst → copy the token.
- `POST /api/batches` with the token → 200.
- Same request again → **409** (wallet already in an open batch).
- Log in as approver, approve the batch → 200.
- Approve with the analyst token → **403**.
- `GET /api/batches/{id}/export` → the wallets you proposed.

### Live site
```bash
uv run --no-project --with httpx python scripts/verify_deploy.py https://whyquiet.vercel.app
```
Prints `PASS` (checked 2026-10-04). Every merge to `main` runs CI, then `deploy.yml` deploys and runs this same check.
