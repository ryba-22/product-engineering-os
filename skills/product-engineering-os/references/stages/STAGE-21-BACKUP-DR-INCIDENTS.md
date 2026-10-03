# Stage 21 — Backup / DR / incidents

**Module:** security-reliability  
**Gate:** G10  
**Evidence anchors:** EVD-DR-001, EVD-INC-001  
**Primary artifacts:** `07-templates/RESTORE-DRILL.md`, `07-templates/INCIDENT-RUNBOOK.md`

## Purpose
Ensure the system can recover from data loss, infrastructure failure and serious operational incidents with measured evidence rather than assumptions. Backup configuration is only an input; recovery capability is demonstrated by restore exercises and incident learning.

## Required inputs
Data ownership and persistence model, backup configuration, retention/encryption policy, RPO/RTO targets, deployment topology, external dependencies, SLOs/alerts, incident ownership and communication channels.

## Questions the Brain must answer
1. What data/state must be recoverable and to what point in time?
2. What RPO and RTO are required for each critical capability?
3. Where are backups stored and how are they protected from the same failure domain?
4. Can backup integrity be verified before an emergency?
5. Can application/schema/config versions be restored together?
6. Who declares and leads an incident?
7. What containment actions prevent further harm?
8. What evidence and follow-up are captured after recovery?

## Workflow
1. **Classify recoverable assets.** Data, files, configuration, secrets references and critical infrastructure definitions.
2. **Define recovery objectives.** Set RPO/RTO based on business consequence, not generic targets.
3. **Map backup mechanisms.** Frequency, retention, encryption, access, geographic/failure-domain separation and deletion protection.
4. **Document restore procedure.** Include prerequisites, version compatibility, dependency order and verification checks.
5. **Run isolated restore drills.** Measure usable recovery time and actual data point recovered.
6. **Test failure variants.** Accidental deletion, corrupted data, unavailable primary region/host, bad migration or credential loss as relevant.
7. **Define incident severity and command.** Trigger, owner, escalation, communication and decision log.
8. **Contain before optimizing.** Protect users/data, stop propagation and preserve evidence.
9. **Recover and verify.** Confirm business capability, not only process startup.
10. **Run blameless post-incident learning.** Convert causes and contributing conditions into tracked system/process actions.

## Decision rules
- A backup that has never been restored is not recovery evidence.
- RPO/RTO targets without measured drills remain assumptions.
- Rollback after data corruption may reintroduce bad state; restore/reconciliation plans must reflect cause.
- Incident timelines should distinguish observed facts from hypotheses.
- Root cause should not collapse complex contributing conditions into one human error.
- Corrective actions need owner, priority and closure evidence.

## Evidence standard
Recovery readiness requires successful restore results tied to backup timestamp, environment and measured RPO/RTO. Incident closure requires evidence that service/data integrity is restored and material follow-ups are tracked.

## Canonical outputs
Recovery policy; restore runbook; measured Restore Drill Record; incident runbook; incident timeline; impact assessment; postmortem; corrective-action register.

## Failure modes
Backup checkbox mentality; backups in same failure domain; untested encryption keys; restore docs requiring unavailable infrastructure; incident chat with no timeline; blame-based postmortem; action items that never close.

## Exit conditions
G10 recovery scope is satisfied when critical data/capabilities have exercised recovery within accepted objectives and incident response has explicit ownership, communication and learning loops.

## Handoff
Stage 24 consumes incident/recovery learning. Stage 25 stores durable lessons, supersedes obsolete runbooks and ensures remediation knowledge remains current.
