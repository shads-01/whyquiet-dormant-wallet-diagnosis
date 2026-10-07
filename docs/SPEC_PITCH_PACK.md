# SPEC: Pitch Pack (demo story cards, hardest-question rehearsal, headline)

This spec proposes a demo-story and defense pack so that all three team members can deliver the same sharp, number-backed narrative — especially the adversarial moments judges probe.

**Execution order:** Wave 1 — parallel-safe. Final numbers refresh happens AFTER all code specs ship (see "Second pass" below). **File ownership:** `docs/PITCH_PACK.md`, `docs/DEMO_STORY.md` only. Must NOT touch code, seed.json, or README (other specs own those).

## Verified facts (pre-checked 2026-10-07)

- Judges scored Innovation 8.33/10; comments praised refusal + governance. The gap reads as credibility, not concept.
- Verified numbers available for the pitch: forced-choice error 49.1% among refused vs 13.5% among attributed; enrichment 1.91×; B macro-F1 0.864, refusal 21.7% B vs 9.3% A-test; multi-seed spread 0.847–0.886 (D33); routed economics +15.02M BDT central @ 4% (D56).
- Existing pitch assets: `docs/IMPACT_SLIDE_COPY.md`, `docs/PILOT_PROTOCOL.md`, `docs/report.md`, README results block.
- The mandated honesty sentence (A3) and the caveat wording for refusal validity are fixed strings — use verbatim.

## Goals

1. `docs/DEMO_STORY.md` exists with: (a) the 3-beat demo script (queue → attributed wallet → refused wallet → Evidence), timed ≤ 8 minutes, with one "judge asks to see a refusal" moment engineered in; (b) **3 adversarial story cards** — hand-picked wallets from seed.json where the model is wrong, near the boundary, or refuses something that looks obvious — each with what to say about it; (c) speaker split so any of the 3 members can run any beat.
2. `docs/PITCH_PACK.md` exists with: (a) the hardest-question rehearsal — "You learned your simulator" answered with the 4-number defense chain (A3 sentence → population C table → flip rate → refusal audit), each slot marked `TBD` until its producing spec ships; (b) headline sentence candidates built on the audit, e.g. *"The only MFS churn tool that publishes its own refusal error rate"*; (c) the 3 numbers every member must memorize.
3. Adversarial story cards reference real wallet IDs from seed.json (executor picks them by inspecting the data — wrong predictions are visible in the confusion matrix and low-margin attributed wallets via `posterior`).

## Non-Goals

- No final numbers in pass 1 — every slot that depends on a not-yet-shipped spec is marked `TBD: <spec name>`; a second pass fills them after Wave 3.
- No slide deck rebuild, no video recording, no changes to existing docs (`report.md`, README) — those are touched by the code specs that change the numbers.
- No new feature claims that aren't shipped.

## Constraints

**Compatibility** — story cards must only reference wallets that exist in the CURRENT seed.json; if a later re-export changes IDs, the second pass re-verifies card IDs (make this a checklist item).
**Security/Compliance** — every number used must be traceable to a seed.json field or a DECISIONS.md entry; ASSUMED figures are labelled ASSUMED in the copy (D5). The A3-mandated sentence appears verbatim wherever synthetic-data claims are made.
**Operational** — the demo script must work offline from seed.json (D6); no step may depend on the write path or network.

## Acceptance Criteria

1. Given `docs/DEMO_STORY.md`, when any team member reads it cold, then they can run the full demo in ≤ 8 minutes (rehearsed once before sign-off).
2. Given the 3 adversarial cards, when each wallet ID is looked up in seed.json, then the wallet exists and exhibits the claimed property (verdict/margin/cause checked programmatically).
3. Given `docs/PITCH_PACK.md`, when the hardest-question section is read, then every `TBD` slot names the spec that fills it and no number is stated that lacks a source.
4. Given the pack, when read, then ASSUMED figures are labelled and the A3 sentence appears verbatim at least once.

## Open Questions

1. Which 3 adversarial stories are most persuasive — who decides: Shads after picking candidate wallets; impact if wrong: a weak card wastes 90 seconds of demo time.
2. Whether the demo should show the cost-sweep UI (if SPEC_METRIC_DEPTH ships it) in the main beat or keep it as a judge-question answer — who decides: user at rehearsal.
