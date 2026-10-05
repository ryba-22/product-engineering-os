# Boundary Evidence Review — candidate operationalization

Status: **candidate / not active runtime guidance**

Source trigger: DevStyle / Domain Drivers public demo published 2026-10-05:
https://youtu.be/Bbk-M96Rghc

## Why this is not being promoted directly

The current PEOS corpus target is 2026-09-30. This source is newer than the frozen corpus target, so its ideas must not silently rewrite active Stage 05/06 guidance.

The reusable synthesis belongs upstream in PMA. PEOS should adopt only the operational contract after an explicit Source Delta assessment and a focused evaluation.

## Proposed capability

Add a **Boundary Evidence Review** for material domain/architecture boundaries.

The review should answer a narrower question than “is this architecture good?”:

> What actually crosses this candidate boundary, how strong are those dependencies, which of them are correctness-relevant, and would an alternative boundary reduce the material coupling under current drivers?

## Candidate workflow

1. Define candidate boundary and membership A/B.
2. Gather inspectable evidence: code, schema, data, runtime, tests, contracts and domain knowledge.
3. Identify ambiguous ownership/shared concepts.
4. Require a human semantic gate before scoring.
5. Inventory every crossing.
6. Classify crossings at least across:
   - operation/API semantics;
   - types/meaning;
   - ordering/transaction protocol;
   - cross-boundary invariants;
   - wiring/injection;
   - free conventions;
   - shared storage;
   - shared mutable runtime state.
7. Record source references for every material crossing.
8. Separate structural, semantic, temporal and consistency coupling.
9. Rank strongest offenders.
10. Search for correctness holes, not only architectural smells.
11. Compare a competing model/boundary where the decision is material.
12. Record decision, falsifiers and revisit triggers.

## Candidate artifact

Add `07-templates/BOUNDARY-EVIDENCE-CARD.md` only after source-delta/eval approval.

Required fields should include:
- boundary and membership;
- ownership;
- evidence sources;
- semantic ambiguities and human gate;
- crossing inventory;
- transaction/temporal/identity coupling;
- cross-boundary invariants;
- shared storage/state;
- ranked offenders;
- optional heuristic score/profile;
- correctness risks;
- counter-hypothesis;
- decision and revisit triggers.

## Scoring constraint

Any numerical score must be explicitly labeled **heuristic**.

The demonstrated formula:

```text
cost = strength_rank × log₂(1 + degree)
```

must not become a universal PEOS quality metric without independent justification.

Prefer:
- offender ranking;
- profile by coupling class;
- before/after comparison;
- candidate A vs candidate B under the same method.

Avoid:
- cross-system leaderboard scores;
- “lower total means better architecture” without driver analysis.

## Proposed PEOS placement

- Stage 05 Domain Architecture: primary semantic/ownership boundary review.
- Stage 06 System Architecture: consume the profile for runtime, consistency and deployment trade-offs.
- Architecture fitness functions: only executable constraints that can be derived without collapsing semantic judgment into a static dependency rule.

## Required validation before promotion

1. Source Delta classification for the post-cutoff source.
2. At least one positive eval: boundary looks clean statically but leaks through transaction/timing/invariant.
3. At least one negative/adversarial eval: strong coupling is legitimate because a true invariant requires one consistency boundary.
4. At least one ambiguity eval: Shared Kernel vs boundary crossing requires human confirmation.
5. Demonstrate that the method does not equate package separation with autonomy.
6. Demonstrate that a total score never overrides correctness or domain ownership.

## Handoff

Canonical conceptual synthesis: PMA `Boundary Coupling Evidence`.

Project-specific consumers should store actual boundary evidence and decisions in their own repositories.
