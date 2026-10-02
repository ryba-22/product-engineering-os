# Backend / API Brain

## API contract first
For each operation define: actor/capability, request schema, invariants/validation, authorization boundary, transaction scope, idempotency/retry semantics, response/error model, concurrency semantics, side effects, audit/telemetry and compatibility policy.

## HTTP guidance
Use HTTP semantics intentionally. Safe/idempotent method properties do not automatically make business effects safe to retry; document application-level idempotency for consequential operations. Prefer a consistent machine-readable error contract such as RFC 9457 where applicable.

## Sync vs async
Choose synchronous request/response when the caller needs a bounded immediate result and the work can meet latency/reliability expectations. Choose background/asynchronous work when execution is long-running, dependency-sensitive, retryable, scheduled or intentionally decoupled. Async introduces status, retry, duplicate, ordering and operator-recovery contracts that must be explicit.

## Dual writes
When one business action updates the database and triggers an external message/side effect, treat it as a consistency problem. Consider transactional outbox or another explicit coordination design rather than `commit; then hope publish succeeds`.
