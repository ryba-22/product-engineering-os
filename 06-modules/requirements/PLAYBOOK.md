# Requirements playbook

Use with `STAGE-04-REQUIREMENTS.md`. Requirements translate evidence and decisions into verifiable behavior without pretending every unknown is settled.

## Canonical traceability chain

`EVIDENCE → OUTCOME/NEED → REQUIREMENT → SCENARIO → ACCEPTANCE CRITERION → TEST/OBSERVATION → RELEASE/OUTCOME EVIDENCE`

A link may be many-to-many, but every material requirement should have a reason to exist and a planned way to verify it.

## Functional requirement pattern

State:
- actor/capability;
- trigger/precondition;
- required behavior;
- business rule/invariant;
- resulting observable state;
- failure/recovery behavior where material.

Avoid implementation unless it is a real external constraint or already accepted architecture decision.

## Scenario set

For each critical workflow include:
- normal success;
- invalid input or failed precondition;
- permission denied;
- missing/empty data;
- dependency failure/timeout;
- concurrent/stale state where relevant;
- retry/duplicate behavior for commands;
- cancellation/partial completion;
- historical/time-boundary behavior when rules depend on time.

This turns “requirements” from prose into a testable state space.

## Quality attribute scenarios

Replace words like “fast”, “secure”, “reliable” or “accessible” with context and response. A useful quality scenario identifies stimulus/source, environment, affected artifact/capability, expected response and measurable response measure.

Not every requirement needs a number, but a material architecture-driving quality does.

## Acceptance criteria

Acceptance criteria prove user/system behavior, not internal implementation steps. Prefer observable outcomes and invariants. Separate:
- deterministic automated criteria;
- environment-dependent performance/reliability criteria;
- manual accessibility/usability checks;
- exploratory hypotheses that are not release gates.

## Uncertainty handling

Label open questions and assumptions. Do not convert “we think” into “shall” for the sake of a complete PRD. If implementation cannot proceed without the answer, assign an owner and blocking status. If the decision is reversible, state the temporary assumption and revisit trigger.

## Change control

Requirements may evolve, but material changes after architecture/implementation starts should update traceability and affected decisions/tests. Silent edits destroy provenance.

## Exit rule

G3 closes when design/engineering/test can identify required behavior and quality, trace it upstream, derive verification, and distinguish confirmed constraints from unresolved hypotheses.
