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
