# Release Engineering / rollout

Use with `STAGE-19-DEPLOYMENT-ROLLOUT.md`. Release engineering controls exposure and proves post-deployment health.

## Release state machine

`CANDIDATE → VERIFIED → RELEASE-READY → DEPLOYING → DEPLOYED → HEALTH-CHECKED → STABLE`

Each transition needs its own evidence. Do not collapse “deployment command returned success” into “system is healthy.”

## Strategy selection

Choose by risk, blast radius, reversibility and telemetry maturity:

- **immediate:** low-risk, easily reversible;
- **rolling:** capacity permits mixed versions and compatibility is proven;
- **blue/green:** fast traffic switch useful and state/data compatibility supports it;
- **canary:** representative partial exposure can reveal regression;
- **feature flag:** useful for behavior exposure, but does not undo migrations/background side effects.

State why the strategy fits the change.

## Pre-release checks

Confirm:
- exact artifact digest/source;
- required gates;
- migration/config readiness;
- capacity;
- backup/recovery prerequisites;
- feature flag/default state;
- smoke checks;
- health/SLO signals;
- rollback or forward-fix path;
- owner/escalation.

## Rollout decisions

Define pause/rollback thresholds before exposure when possible. Watch:
- errors;
- latency;
- saturation;
- dependency health;
- queue/job failures;
- domain-specific rejection/failure rates;
- support/operational anomalies.

A canary must receive representative traffic. “No errors in 10 requests” is weak evidence for a broad release.

## Database and irreversible effects

Rollback may not be safe after schema/data transformation or external messages/payments. Use compatibility sequencing and forward-fix/reconciliation where needed. Feature flags do not erase side effects that already occurred.

## Release Evidence Bundle

Record:
- artifact/version/digest;
- environment;
- gate results;
- migration/config state;
- rollout strategy;
- exposure timeline;
- smoke results;
- telemetry snapshot;
- operator decisions;
- rollback/forward-fix status;
- stable-state declaration.

## Completion

“Stable” means the intended exposure has been reached and health remained acceptable for a relevant observation window. It still does not mean the product outcome succeeded; Product Intelligence measures that later.
