# Stage 15 — Testing

**Module:** quality-engineering  
**Gate:** G7  
**Evidence anchors:** EVD-QA-001, EVD-QA-002  
**Primary artifact:** `07-templates/TEST-STRATEGY.md`

## Purpose
Produce trustworthy evidence for the product/system guarantees that matter most. Test strategy starts from risk, invariants and contracts; it does not optimize for test counts, a fashionable pyramid or maximum browser automation.

## Required inputs
Requirements/acceptance criteria, domain invariants, architecture failure modes, interaction states, API/persistence contracts, security/performance risks, migration plan and release risk.

## Questions the Brain must answer
1. What could fail and what would the consequence be?
2. Which guarantees can be proven cheaply at unit/property/contract level?
3. Which boundaries require integration tests?
4. Which critical workflows require browser/end-to-end evidence?
5. Which concurrency, retry, migration and recovery cases are adversarial?
6. Which tests are deterministic enough for CI?
7. Which checks require production-like infrastructure or manual validation?
8. What evidence is required to close the release gate?

## Workflow
1. **Build a risk inventory.** Rank failure by consequence, likelihood and detectability.
2. **Map each risk to an oracle.** Define what observable result proves or falsifies the guarantee.
3. **Choose the lowest trustworthy layer.** Prefer fast deterministic tests when they prove the same property.
4. **Add contract tests at boundaries.** Verify schemas, error semantics and provider/consumer expectations.
5. **Test stateful/adversarial behavior.** Retries, duplicate commands, stale versions, partial failure, time boundaries and race conditions.
6. **Test migrations/data changes.** Include compatibility, backfill and representative volume when material.
7. **Use browser tests for integrated critical journeys.** Keep them focused on contracts that lower layers cannot prove.
8. **Include accessibility/manual checks.** Automation does not replace keyboard/AT verification for critical flows.
9. **Control flakiness.** A flaky test is unreliable evidence and needs ownership.
10. **Record residual risk.** Passing tests do not prove untested properties.

## Decision rules
- Code coverage is diagnostic, not evidence that important risks are tested.
- A browser test should not duplicate dozens of lower-level cases merely because it resembles the user journey.
- Mock-heavy tests cannot prove integration behavior they bypass.
- Production bugs should create or strengthen the cheapest regression oracle that would have detected them.
- A test that cannot fail for the intended defect is not meaningful evidence.
- Release criteria must distinguish implemented, tested, verified and production-observed states.

## Evidence standard
High-risk guarantees need independent, repeatable evidence at the layer that exercises the relevant failure mechanism. Test results should identify environment and version/artifact.

## Canonical outputs
Risk-based Test Strategy; risk→test matrix; automated tests; manual verification records; migration/concurrency cases; known gaps; release evidence links.

## Failure modes
Test-count vanity; all-E2E strategy; snapshot tests with no semantic oracle; mocks proving mocks; ignored flaky suite; no negative/adversarial cases; assuming CI green means production healthy.

## Exit conditions
G7 is satisfied when material risks have trustworthy verification or an explicit accepted residual risk, failures are diagnosable, and evidence can be tied to the exact change/artifact.

## Handoff
Stages 16–17 add specialist verification. Stage 18 consumes deterministic gates. Stage 19 uses release evidence rather than branch state.
