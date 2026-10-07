# SPEC: Repo & Ops Hygiene (LICENSE, rotation runbook, Supabase ping)

This spec proposes closing the repo's known operational risks (missing LICENSE, unrotatable-in-a-crisis demo passwords, silent Supabase free-tier pause) so that demo day cannot be ruined by any of them.

**Execution order:** Wave 1 — parallel-safe. **File ownership:** `LICENSE`, `Makefile`, `docs/OPS_RUNBOOK.md`, `README.md` (license badge line only). Must NOT touch `web/`, `scripts/evaluate.py`, `scripts/export_seed.py`, or `src/` (owned by parallel specs).

## Verified facts (pre-checked 2026-10-07)

- No LICENSE file exists (STATE open item; deliberate but undecided).
- Demo passwords are public by design (D42: `DEMO_PASSWORDS` in `web/src/App.tsx`); rows written to the live DB are permanent (delete blocked by triggers). Rotation path exists: `supabase/seed_demo_users.py` + editing `DEMO_PASSWORDS` + redeploy — but it is undocumented.
- Supabase free tier pauses after 7 days idle (STATE open item). The UI already renders a 503 "Write path offline" banner (D40/D41); there is no quick way to check wake-state from the laptop.
- `.env` holds `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` (D36/D37).

## Goals

1. A LICENSE file exists at repo root. License choice: **MIT, unless the user says otherwise** (see Open Questions).
2. `docs/OPS_RUNBOOK.md` exists with three tested, copy-paste procedures: (a) rotate demo passwords end-to-end (Supabase users + `DEMO_PASSWORDS` + redeploy), (b) wake/check the Supabase project before a demo, (c) verify the 503 offline banner appears when the DB is unreachable.
3. A `make ping` target (≤ 5 lines) curls the Supabase REST root with the service key from `.env` and prints OK/paused — so pre-demo checking is one command.

## Non-Goals

- Do NOT rotate the passwords now — judges may already use the current ones; rotation happens via the runbook immediately before final judging.
- No changes to auth code, no new dependencies, no cron/scheduled pinging infra (YAGNI — a manual `make ping` before each demo suffices at this scale).
- No change to the 503 banner behavior or to `src/api/`.

## Constraints

**Compatibility** — `make ping` must work on Windows bash (the team's environment) using only curl + the existing `.env`; no Python runtime requirement.
**Security/Compliance** — the runbook must never print or store the service key in docs; commands read it from `.env` (D36 pattern). Rotation procedure must not log old passwords.
**Operational** — every runbook command must have been executed successfully by the spec author before the spec is marked done; untested commands are the failure mode of runbooks.
**Compliance** — LICENSE must not conflict with the public-repo hackathon context (attribution to team members; no CLA files needed).

## Acceptance Criteria

1. Given the repo root, when listing files, then `LICENSE` exists and README references it.
2. Given `docs/OPS_RUNBOOK.md`, when following procedure (a) verbatim on a test user, then the new password authenticates on the live site and the old one does not.
3. Given `make ping`, when run against the live project, then it prints an unambiguous OK or PAUSED result and exits 0/1 respectively.
4. Given the runbook, when read, then it contains no secrets and no untested commands (author executed each one).
5. Given `make check`, when run, then it stays green (Makefile change is additive).

## Open Questions

1. License choice (MIT vs Apache-2.0 vs none-for-competition-reasons) — who decides: user; impact if wrong: trivial to swap a text file later.
2. Whether the runbook's rotation procedure needs a Supabase dashboard step (deleting demo users may require dashboard UI if the service-key script can't) — who knows: whoever runs `supabase/seed_demo_users.py`; verify during execution.
