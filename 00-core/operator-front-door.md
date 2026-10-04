# Operator front door

The operator should be able to start from a problem statement without knowing the repository topology or lifecycle stage in advance.

Canonical routing:

problem/outcome -> current evidence -> project constitution -> risk -> missing decision-changing evidence -> owner module -> execution profile -> workflow/lane topology -> verification matrix

## Intake contract

Capture:
- desired outcome / problem;
- target product/repository if known;
- constraints and non-goals;
- known evidence or prior decision IDs;
- external effects (money, messages, identity, data mutation, deployment);
- reversibility and detectability;
- urgency only as a scheduling input, never as evidence.

## Front-door algorithm

1. Inspect the actual repository/worktree and prior decisions before classifying the request.
2. Read an approved Project Constitution if present. If none exists, run local constitution discovery and keep findings as candidates.
3. Classify R0-R4 using risk-model.md.
4. Select FAST / STANDARD / EVIDENCE_HEAVY using execution-profiles.md.
5. Apply the stop-analysis gate: identify only unknowns capable of changing the decision, risk class, safety boundary or expected outcome.
6. Route to the minimum sufficient PEOS modules/stage playbooks.
7. Determine whether work can remain one lane or requires independent lanes/dependencies.
8. Create a task contract containing risk, execution profile, applicable constitution rules, acceptance evidence and required verification dimensions.
9. After implementation, resolve the Verification Matrix before claiming the declared lifecycle boundary.

## No implicit standards

Repository frequency is evidence of an observed convention, not authorization. If discovered project rules conflict, the conflict remains explicit until a responsible owner resolves it.

## No implicit lane guessing

A front door may propose a lane topology, but runtime execution still requires explicit lane ownership and canonical state. Ergonomics must not weaken source-of-truth rules.
