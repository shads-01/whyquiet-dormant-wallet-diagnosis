# SPEC: Boundary Transparency ("what would change this verdict")

This spec proposes surfacing each wallet's distance from the refusal boundary on the Wallet Detail screen so that refusal and attribution read as measured, auditable decisions instead of opaque verdicts.

**Execution order:** Wave 1 — parallel-safe. **File ownership:** `web/src/Wallet.tsx`, `web/e2e/wallet.spec.ts` only. This spec must NOT touch `scripts/`, `web/src/Evidence.tsx`, or `web/public/seed.json` (owned by other specs running in parallel).

## Verified facts (pre-checked 2026-10-07, seed 42)

- `web/public/seed.json` → `meta.tau = 0.8`, `meta.delta = 0.1` exist.
- Every wallet object has `posterior` (dict of all 5 cause probabilities) and `refusal_reasons` (already string sentences with numbers).
- Everything needed is client-side computable. No export changes, no API changes, no new fields.

## Goals

1. Refusal panel gains a "What would change this verdict" block: the wallet's top-1 probability and top-2 margin rendered against the tau and delta bars (e.g., "Top cause: 0.45 — needs ≥ 0.80"; "Margin: 0.24 — needs ≥ 0.10"), so the analyst sees exactly how far the wallet is from attribution.
2. Attributed wallets whose top-2 margin < 0.15 (ASSUMED threshold, shown as a badge) or top-1 probability < 0.90 (ASSUMED) display a boundary notice: "Near the refusal boundary — a small change in the decline shape would flip this verdict to refused."
3. Both blocks are read-only by construction: no button, control, or affordance may imply the operator can override a verdict (refusals are terminal, D13).

## Non-Goals

- No third verdict (no "monitor" state), no changes to `src/model/train.py::decide` or the tau/delta values.
- No threshold retuning and no re-export of seed.json.
- No changes to the Queue screen or Evidence page.

## Constraints

**Compatibility** — seed.json is read-only for this spec; `meta.tau`/`meta.delta` are the single source of threshold values (no hard-coded 0.8/0.1 in components).
**Performance** — client-side computation over a 5-key dict; no measurable render cost.
**Security/Compliance** — no override affordance (D13); no new data exposure (all values already shipped).
**Operational** — English-only operator copy (D13b); responsive at 375px; follows existing panel patterns and ASSUMED badge styling in `web/src/design/`.

## Acceptance Criteria

1. Given a refused wallet in seed.json, when its detail page renders, then the refusal panel shows the wallet's actual top-1 probability and margin numerically against the tau/delta bars taken from `meta` — not hard-coded values.
2. Given an attributed wallet with top-2 margin < 0.15, when its detail page renders, then a boundary badge is visible; given one with margin ≥ 0.15, no badge appears.
3. Given both panel variants, when inspected, then neither contains any button or control acting on the verdict.
4. Given `make e2e`, when wallet specs run, then prior assertions pass unchanged and at least one new assertion covers the boundary block rendering real numbers.
5. Given `make check`, when run, then ruff/pyright/tsc/oxlint are clean.

## Open Questions

1. Badge thresholds 0.15 / 0.90 are ASSUMED — user may want them tuned after seeing real wallets; impact if wrong: purely cosmetic (badge shows too often/too rarely).
2. Who knows the visual design intent: Shads — the block must read as explanation, not as doubt-spreading; show it to the user before polishing.
