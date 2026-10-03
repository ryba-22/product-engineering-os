# Independent Eval Run v1

Goal: rerun the same frozen 25 adversarial lifecycle scenarios with a model that did not produce the original self-assessed results, then score those outputs with a third distinct model or a human judge.

## Independence protocol

- Executor sees only `executor-input.json` from the frozen adversarial run plus Product Engineering OS runtime/stage playbooks/evidence anchors/gates.
- Executor must not read scenario `must_do` / `must_not_do`, prior executor outputs, prior judge outputs, or final self-assessed results.
- Judge sees frozen scenario criteria plus the independent executor output and relevant Product Engineering OS rules.
- Judge must not read prior self-assessed executor/judge outputs.
- Promotion to `independently-behaviorally-validated` requires 25/25 pass, no hard failures, and provenance identifying a distinct executor and judge.

## Planned models

- Independent executor: Google Antigravity model, target `gemini-3.1-pro-high`.
- Independent judge: a third distinct model, target `claude-sonnet-4-6` through Antigravity if available on the authenticated account.
- Human judge sheet is included as a fallback/secondary review surface.

## Current state

The harness, frozen hashes, judge rubric, output schemas and human judge sheet are prepared. Model execution begins only after external-model authentication is complete and available models are confirmed with `agy models`.

## Evidence boundaries

This run is deliberately stronger than the earlier self-assessment but narrower than a universal capability claim. The executor is allowed to use the Product Engineering OS runtime, stage playbooks, declared evidence anchors, gates and templates because those are the system being evaluated. It is not allowed to see the frozen `must_do`, `must_not_do`, judge scores, expected behavior or previous model answers. The judge receives those frozen criteria only after the executor output exists.

The scenarios themselves remain unchanged from the prior adversarial run. Their SHA-256 hashes are stored in `run-manifest.json`, so later edits to wording cannot silently turn the benchmark into an easier test. Outputs are stored separately for executor and judge batches, with model/provider provenance and token/runtime metadata.

## Promotion rule and limitations

A run may promote the maturity claim only when all 25 stages pass the frozen threshold, no hard failure remains, and executor and judge provenance demonstrate distinct models. Passing does not erase judge criticism: partial omissions in otherwise passing answers are retained in `weakness-backlog.json` so the corpus can improve without post-hoc changing the benchmark.

`independently-behaviorally-validated-v1` therefore means: this exact version of the OS produced independently executed and independently judged acceptable behavior on these 25 frozen scenarios. It does **not** mean every future Product Engineering problem is solved correctly, nor that production correctness has been proven. New unseen eval sets, specialist review for high-risk areas and revalidation after material runtime/corpus changes remain necessary.

## Stored artifacts

- `run-manifest.json` — frozen hashes, provenance, models and final maturity claim.
- `executor-results.json` / `executor-provenance.json` — merged independent execution and run metadata.
- `judge-rubric.json` — frozen criteria hidden from the executor.
- `judge-results.json` / `judge-provenance.json` — merged independent scoring and run metadata.
- `weakness-backlog.json` — judge-identified omissions retained after the pass.
- `REPORT.md` — human-readable result and per-stage scores.
- `HUMAN-JUDGE-SHEET.md` — optional human review surface for a later fourth-party check.
