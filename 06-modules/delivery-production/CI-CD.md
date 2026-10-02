# Delivery Engineering — CI/CD

## Goal
Move one immutable, attributable change through repeatable gates. CI/CD is evidence production, not only automation.

## Default gate chain
Dependency install/lock verification → formatting/lint/typecheck → unit/domain tests → integration/DB tests → security/supply-chain checks → build → migration validation → E2E/smoke → artifact/provenance capture → deploy authorization.

Not every project needs every step, but removing a gate requires a risk-based reason.

## Principles
- build once; promote the same artifact;
- keep production secrets out of source/build logs;
- separate application build from production data migration;
- fail closed on required gates;
- preserve exact commit, dependency lock, build identity and artifact digest where feasible;
- treat flaky required gates as defects, not as reasons to ignore failures;
- measure delivery performance over time, not by one heroic release.
