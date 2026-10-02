# Stage 19 — Deployment / rollout

**Module:** delivery-production  
**Gate:** G9  
**Evidence anchors:** EVD-DEL-002, EVD-OPS-001  
**Primary artifact:** `07-templates/RELEASE-EVIDENCE.md`

## Purpose
Move a verified artifact into production through a controlled state machine that limits blast radius and proves health after exposure. “Deployed” is an intermediate state, not evidence that the release is healthy or successful.

## Required inputs
Immutable release candidate, release evidence, migration/config plan, rollback or forward-fix strategy, SLO/health signals, feature-flag/canary capability where available and incident escalation path.

## Questions the Brain must answer
1. What is the blast radius of the first exposure?
2. Which health signals must remain within limits?
3. Which migrations/config changes are coupled to the release?
4. Is rollback safe after data/schema side effects?
5. When should rollout pause automatically or manually?
6. What smoke checks prove the critical path works?
7. How long must the release be observed before increasing exposure?
8. Who owns go/no-go and incident escalation?

## Workflow
1. **Verify release identity.** Artifact digest, source SHA and environment target.
2. **Check preconditions.** Capacity, backups/recovery prerequisites, migrations, config and dependency readiness.
3. **Choose rollout strategy.** Immediate for low-risk/reversible changes; staged/canary/feature flag for higher uncertainty or blast radius.
4. **Apply compatible data/config changes** in the planned order.
5. **Deploy initial scope.**
6. **Run smoke/contract checks.** Verify critical availability and business path.
7. **Observe telemetry.** Error rate, latency, saturation, domain failures and support signals as relevant.
8. **Decide continue/pause/rollback/forward-fix** from predefined thresholds.
9. **Expand exposure deliberately.**
10. **Record final release state and evidence.** Continue monitoring after “100%” because some failures emerge only over time.

## Decision rules
- Rollback is not automatically safe after irreversible data changes.
- Canary success needs comparable traffic/behavior; a canary receiving no representative workload is weak evidence.
- Feature flag off is not equivalent to rollback when migrations or background side effects already occurred.
- Health checks must test meaningful dependencies, not only process liveness.
- Manual verification should be explicit evidence, not an undocumented chat message.
- Rollout completion requires health evidence; product success belongs to later analytics/feedback stages.

## Evidence standard
Release evidence ties exact artifact, environment, migration/config state, rollout timestamps, smoke checks, health metrics and operator decisions together.

## Canonical outputs
Release Evidence Bundle; rollout log; migration/config status; smoke results; telemetry snapshot; go/no-go decisions; rollback/forward-fix record; stable-state declaration.

## Failure modes
Big-bang by default; “deploy succeeded” treated as health; no rollback threshold; canary without representative traffic; irreversible migration before application compatibility; manual config drift; alert storm with no release correlation.

## Exit conditions
G9 is satisfied when the intended exposure is reached, critical health checks remain within thresholds for the required observation window, and rollback/forward-fix posture is known.

## Handoff
Stage 20 owns continuous operational health. Stage 22–24 determine whether the release changed product outcomes as intended.
