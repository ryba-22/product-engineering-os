# Release Engineering / rollout

## Release state machine
`CANDIDATE → VERIFIED → RELEASE-READY → DEPLOYING → DEPLOYED → HEALTH-CHECKED → STABLE`

Each transition requires its own evidence.

## Strategy selection
Use direct rollout for low-risk/reversible changes. Use staged/canary/shadow/blue-green or feature-controlled exposure only when blast-radius reduction or comparative evidence justifies added complexity.

## Release Evidence Bundle
At minimum: artifact/source identity, gate results, migration status, configuration/environment identity, rollout plan, smoke/health results, critical telemetry snapshot, known risks, operator/owner and recovery action.

## Rollback rule
Application rollback is only safe when compatible with current data/schema/external effects. Prefer forward-fix for irreversible data history; never assume down-migration is a generic recovery mechanism.
