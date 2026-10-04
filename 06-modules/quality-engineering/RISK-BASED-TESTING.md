# Quality Engineering Brain — risk-based testing

Use with `STAGE-15-TESTING.md`. The test strategy exists to produce evidence for important guarantees, not to maximize the number of tests or conform to a fixed pyramid.

## Risk inventory

For each feature/change identify:
- critical user/business outcomes;
- invariants;
- likely failure modes;
- consequence;
- detectability;
- boundaries/dependencies involved;
- reversibility.

Prioritize cases where consequence is high and failure may be silent.

## Verification budget

Allocate human review by semantic risk, not diff size. Mechanical/cosmetic work can rely heavily on agents and automated checks. Business invariants, ownership boundaries, concurrency/idempotency semantics, authorization/privacy boundaries and consequential residual-risk acceptance require explicit human review. For each material risk record what can be delegated, what remains human-owned, the required evidence layer and known blind spots.

## Evidence layer selection

Choose the lowest layer that can honestly exercise the failure mechanism.

| Guarantee | Preferred evidence |
|---|---|
| pure rule/transformation | unit/property test |
| domain invariant | domain/application test + DB constraint where applicable |
| API schema/error contract | contract/integration test |
| transaction/concurrency | integration test against real DB semantics |
| migration/backfill | migration test on representative data |
| browser workflow | targeted E2E/browser test |
| accessibility interaction | automation + manual keyboard/AT for critical/custom flows |
| deployment/health | release smoke + production telemetry |
| performance | defined workload/budget test |

Do not use a lower layer when it mocks away the behavior being proven.

## Adversarial cases

Happy-path tests are insufficient for consequential state changes. Consider:
- duplicate/retry requests;
- concurrent updates;
- stale version;
- partial dependency failure;
- timeout ambiguity;
- clock/time-zone/day-boundary logic;
- permission change mid-flow;
- corrupted/missing data;
- migration mixed-version window;
- external provider accepts request but response is lost.

Each adversarial test should link to a real risk or invariant.

## Test oracle

A test needs an independent observable that distinguishes correct from incorrect behavior. Avoid assertions that simply mirror implementation details. Prefer business state, durable event, contract response or externally visible effect.

## Flakiness

Flaky evidence is weak evidence. Track owner, failure rate and root cause. Quarantine only temporarily with an expiry/issue. Do not normalize rerunning until green.

## Regression strategy

When a production defect occurs:
1. identify the violated guarantee;
2. add the cheapest reliable oracle that would detect it;
3. fix the implementation;
4. prove the new test fails before/without the fix when practical;
5. keep higher-layer coverage only where the failure required it.

## Environment fidelity

Not every test needs production parity, but the environment must preserve the semantics under test. Concurrency needs the real DB isolation/constraints. Browser behavior needs supported browsers. Performance needs representative workload/data. Restore needs realistic backup artifacts.

## Exit contract

For each material risk record:
- evidence layer;
- exact test/check;
- artifact/version/environment;
- pass criteria;
- known blind spots;
- residual risk/acceptance owner.

A green suite means the declared guarantees were exercised, not that all possible failures are impossible.
