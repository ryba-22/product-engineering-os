# Architecture fitness functions

A fitness function is an executable or inspectable constraint that detects architecture drift early enough to act. Use fitness functions for properties important enough to protect continuously and stable enough to test meaningfully.

## What belongs here

Good candidates include:

- dependency direction between modules;
- forbidden cross-boundary database access;
- API/schema compatibility;
- latency or bundle-size budgets;
- maximum dependency cycles;
- security policies;
- migration compatibility rules;
- availability/error-budget conditions;
- required telemetry/provenance;
- accessibility invariants in shared components.

Do not automate every preference. Automation creates maintenance cost and can freeze a weak architecture rule.

## Contract

Each fitness function should state:

- **property:** what architecture quality is being protected;
- **scope:** components/services/repos/environments affected;
- **mechanism:** static analysis, test, policy, metric or manual inspection;
- **threshold:** pass/fail/warn condition;
- **cadence:** commit, CI, release, scheduled or production;
- **owner:** who maintains the rule and handles failures;
- **escape path:** how a justified exception is recorded;
- **revisit trigger:** what change could make the function obsolete.

## Examples

### Dependency direction
Property: domain/application code must not import infrastructure/UI modules.
Mechanism: static dependency graph in CI.
Failure: block merge or require an explicit architecture exception.

### API compatibility
Property: a released consumer contract must not be broken unintentionally.
Mechanism: schema diff / contract tests against the previous released version.
Failure: block unless version/migration decision exists.

### Performance budget
Property: critical interaction p95 remains below the accepted threshold under defined workload.
Mechanism: reproducible performance test or production SLO.
Failure: block or require explicit risk acceptance depending on stability of the test.

### Data ownership
Property: only the owning module writes a critical table/entity.
Mechanism: repository query/linter, database permissions or audit telemetry.
Failure: report architectural drift and require an ADR.

## Design rules

- Protect a user/business quality, not a diagram aesthetic.
- Prefer binary rules for true invariants; use warning/trend for noisy metrics.
- Keep the oracle independent enough that implementation cannot trivially “test itself.”
- Avoid brittle text/filename rules when semantic analysis is available.
- Exceptions are time-bounded and visible.
- A fitness function without an owner will decay into ignored noise.

## Evolution

Fitness functions evolve with architecture. When a boundary is intentionally changed, update the ADR and the function together. When the function repeatedly fails for valid changes, either the rule is wrong, the threshold is wrong or the architecture is fighting its own desired evolution.

A green fitness suite means declared architecture constraints currently hold. It does not prove the architecture is globally optimal or behaviorally successful.
