# Resilience, DR and Incidents

## Recovery engineering
For stateful systems define RPO, RTO, backup mechanism, retention, access/encryption, restore procedure, isolated validation and application compatibility. A backup is `CONFIGURED` until a restore drill produces evidence.

## Dependency failure
For material dependencies define timeout, retry/backoff, circuit/bulkhead or queueing behavior only where needed; also define operator-visible degraded mode and recovery/replay semantics.

## Incident response
Declare incident owner/commander, impact, timeline, containment, communication, evidence capture and recovery criteria. Preserve logs/correlation IDs without copying sensitive payloads unnecessarily.

## Postmortem
Record impact, detection, contributing conditions, timeline, what worked/failed, causal/system factors and owned follow-ups. Avoid blame; the purpose is improved reliability and reduced recurrence.
