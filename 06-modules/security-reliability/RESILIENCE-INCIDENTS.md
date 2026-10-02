# Resilience, DR and Incidents

Use with `STAGE-21-BACKUP-DR-INCIDENTS.md`. Reliability planning connects recovery objectives, dependency failure behavior and incident learning.

## Recovery engineering

For each stateful capability define:
- RPO;
- RTO;
- backup/snapshot mechanism;
- frequency and retention;
- encryption/key dependency;
- access control;
- failure-domain separation;
- restore steps;
- application/schema/config compatibility;
- post-restore verification.

A configured backup job is not recovery evidence. Run isolated restore drills and measure actual usable recovery.

## Dependency failure

For each critical dependency decide:
- timeout;
- retry count/backoff/jitter;
- circuit/bulkhead behavior where useful;
- queue/buffer limits;
- degraded mode;
- fallback source;
- idempotency;
- operator signal;
- reconciliation after recovery.

Retries can amplify overload. Fallbacks can serve stale/incorrect data. Each resilience mechanism needs semantics, not just a library setting.

## Incident response

Define severity by user/data/business impact. A runbook should state:
- trigger and declaration authority;
- incident commander/owner;
- immediate safety/data protection actions;
- communication/escalation;
- evidence preservation;
- containment;
- recovery;
- verification;
- decision log.

During an incident separate observed facts from hypotheses. Update the shared timeline as understanding changes.

## Recovery verification

Do not close because processes are “up.” Verify critical user/business capability, data integrity, queues/background jobs, integrations and SLO/telemetry recovery.

## Postmortem

Use a blameless system perspective:
- impact;
- detection;
- timeline;
- contributing conditions;
- what went well/poorly;
- why safeguards did not prevent/detect earlier;
- corrective actions.

Avoid one-word “root cause: human error.” Human action occurs inside a system of permissions, tooling, procedures, feedback and incentives.

## Corrective action quality

Actions should change the system: automation, guardrail, test, ownership, observability, architecture or procedure. “Be more careful” is weak unless paired with a concrete control.

Track owner, priority, due/revisit condition and closure evidence. Feed lessons into evidence/decision governance so the same knowledge is not rediscovered in the next incident.
