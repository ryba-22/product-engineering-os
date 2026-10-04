# Product Engineering OS — Operational Runbook

Product Engineering OS is the operating method that turns a product/engineering problem into a bounded, evidence-backed change and then checks whether the change produced the intended outcome.

`IMPLEMENTED ≠ TESTED ≠ VERIFIED ≠ DEPLOYED ≠ HEALTHY ≠ SUCCESSFUL`.

## WHEN

Use PEOS when:

- a product or engineering change needs an explicit lifecycle from problem to verified outcome;
- several specialist concerns must be routed without loading every module;
- evidence, decisions, acceptance criteria, delivery, production learning, or value need to remain connected;
- an AI-assisted workflow needs explicit gates rather than prompt-level confidence.

Do not use PEOS as the canonical repository for raw research corpora or project-specific business truth.

## INPUT

Bring:

- desired outcome and problem statement;
- scope and non-goals;
- constraints and architecture/product drivers;
- acceptance criteria or examples when known;
- current implementation/evidence;
- risk level and reversibility;
- unresolved assumptions.

## FLOW

1. State the outcome, scope, constraints, and acceptance criteria.
2. Classify risk using `00-core/risk-model.md`.
3. Route only to the modules required by `00-core/routing.md`.
4. Gather decision-critical evidence and stop research when it is unlikely to change the decision.
5. For material business behavior, define examples/counterexamples and an executable oracle before implementation.
6. Execute the smallest useful change; record decisions and verify the evidence required by the relevant gate.
7. Separate implementation/test/verification/deployment/health/value claims; do not collapse them.
8. For production work, compare expected and observed behavior and feed supported learning back into requirements, decisions, tests, evals, and reusable knowledge.

Runtime detail: `BRAIN.md`. Specialist depth lives in `06-modules/**/STAGE-*.md`.

## OUTPUT

A completed PEOS pass should leave:

- a bounded outcome and scope;
- selected modules/stages;
- evidence and decision records;
- acceptance/examples where applicable;
- implementation or experiment;
- verification evidence;
- release/health evidence when deployed;
- outcome status: supported value or `UNVERIFIED OUTCOME`;
- remaining blockers and next action.

## EVIDENCE

Claims are supported only by evidence appropriate to their state:

- implementation → code/diff;
- tested → executable test result;
- verified → acceptance/eval evidence;
- deployed → release evidence;
- healthy → production/operational evidence;
- successful → outcome/value evidence.

Structural validation:

`python3 scripts/validate.py`

`python3 scripts/audit_coverage.py`

`python3 scripts/audit_freshness.py`

## STOP

Stop analysis when additional information is unlikely to change the current decision.

Prefer a reversible experiment when uncertainty is cheaper to resolve through execution than more research.

Do not claim closure beyond the strongest evidence available.

## HANDOFF

- domain/archetype diagnostic → **Domain Archetype Atlas**;
- reusable DDD/architecture reasoning → **PMA**;
- UI/UX evidence/models/audit → **UI/UX Knowledge Corpus**;
- book evidence → **Book Knowledge Corpus**;
- implementation, project decisions, tests, production evidence → **project repository**;
- multi-lane Brain/Worker execution coordination → **ChatLOOP**.

Reusable project learning moves upstream only after provenance, scope, and falsification review.
