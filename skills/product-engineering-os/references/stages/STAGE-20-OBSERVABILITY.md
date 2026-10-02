# Stage 20 — Observability

**Module:** security-reliability  
**Gate:** G10  
**Evidence anchors:** EVD-OBS-001, EVD-REL-002  
**Primary artifacts:** `07-templates/SLO.md`, telemetry/alert contracts

## Purpose
Make system behavior explainable enough to detect user-impacting failure, diagnose causes and support reliability decisions. Observability starts from questions and service objectives, not from collecting every possible log.

## Required inputs
Critical user capabilities, architecture/runtime dependencies, release identifiers, known failure modes, performance budgets, incident history, data/privacy constraints and on-call/operational ownership.

## Questions the Brain must answer
1. What does “available and healthy” mean from the user/service perspective?
2. Which SLI measures that outcome?
3. What SLO/window is appropriate and why?
4. Which signals explain failures across service boundaries?
5. Can operators correlate a user/request/job across logs, metrics and traces?
6. Which conditions require an alert versus dashboard/exploration?
7. What data must never be emitted into telemetry?
8. Can a release be correlated with changes in errors/latency?

## Workflow
1. **Define user-facing capabilities and SLOs.** Start with reliability objectives that influence decisions.
2. **Define SLIs and measurement sources.** Specify numerator/denominator or latency distribution precisely.
3. **Instrument shared context.** Correlation IDs, service/version, operation and relevant domain identifiers without leaking sensitive data.
4. **Collect complementary signals.** Metrics for trends, traces for request paths, structured logs/events for detail.
5. **Instrument known failure modes.** Dependency errors, retries, queue backlog, conflicts, domain rejection and resource saturation.
6. **Define dashboards around questions.** Service health, release impact, dependency health and capacity.
7. **Define alerts around action.** Alert when a human decision/action is needed; avoid symptom duplication.
8. **Use error budgets/SLOs for prioritization.** Reliability data should affect delivery decisions.
9. **Test observability.** Trigger representative failures and verify signal discoverability.
10. **Review cardinality, retention and privacy cost.**

## Decision rules
- More logs are not automatically better observability.
- Alerts without an owner or response action are noise.
- Liveness alone is not user-visible availability.
- High-cardinality labels need deliberate cost/privacy review.
- SLOs are decision tools, not decorative dashboard targets.
- Telemetry must preserve release/version context to distinguish regression from ambient failure.

## Evidence standard
Critical capabilities need measured SLIs from production-relevant sources. Alerts and dashboards should be validated against real or simulated incidents rather than assumed useful.

## Canonical outputs
SLO document; telemetry schema; correlation conventions; dashboards; alert rules/runbooks; release annotations; observability test evidence; known blind spots.

## Failure modes
Log dumping; CPU alerts disconnected from user impact; no version tags; dashboards nobody uses; alerts on every transient error; sensitive payload logging; SLO chosen from aspiration with no service context.

## Exit conditions
G10 observability scope is satisfied when operators can detect and investigate material failures, SLOs have trustworthy measurements, and alerts correspond to actionable conditions.

## Handoff
Stage 21 uses the telemetry/runbooks during incidents and recovery. Stage 24 consumes operational evidence for product/system learning.
