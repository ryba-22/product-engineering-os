# Backend / API Brain

Use with `STAGE-13-BACKEND-API.md`. Backend/API design defines authoritative behavior under validation, authorization, concurrency, retries and partial failure.

## API contract first

For every consequential operation define:

- actor and required capability;
- request schema and validation;
- resource/business preconditions;
- business invariants;
- authorization boundary;
- transaction scope;
- idempotency and retry behavior;
- concurrency/conflict behavior;
- response semantics;
- error categories/codes;
- side effects and timing;
- audit/telemetry;
- compatibility/versioning;
- performance expectations.

Use OpenAPI or another machine-readable schema where it improves shared understanding and verification, but keep domain semantics richer than the transport schema.

## Commands versus queries

Queries should not create hidden mutations. Commands express intent and may fail because the domain state changed. Avoid CRUD endpoints that expose internal storage semantics when the real operation is a business action such as approve, enroll, settle, schedule or cancel.

## Authorization

Check the capability against the authenticated actor and target resource/context. UI visibility is not security. Distinguish:
- authentication: who/what is calling;
- coarse role/capability;
- resource scope/ownership;
- state-dependent permission.

Log authorization-relevant decisions proportionally to risk without leaking secrets.

## Idempotency and retries

HTTP method idempotency is not the same as application-level duplicate protection. For retryable commands define:
- idempotency key or natural uniqueness;
- stored result/deduplication window;
- behavior while an earlier attempt is in progress;
- behavior after timeout where the caller does not know whether commit occurred.

External side effects after a database commit commonly need outbox/worker or another reconciliation pattern.

## Concurrency

Critical mutations need a deliberate strategy:
- unique/foreign-key/check constraints;
- optimistic versioning;
- row/advisory locks;
- serializable transaction;
- single-writer queue.

“Read, check, then write” without atomic enforcement is race-prone.

## Errors

Prefer stable machine-readable categories plus safe human-readable detail. Distinguish validation, authorization, not-found, conflict, rate/temporary dependency failure and unexpected server failure. Retryability should be explicit enough for clients/workers to act safely.

## Compatibility

Treat API/schema evolution as a consumer migration problem. Additive change is usually safer, but semantics can still break consumers. Contract tests and version/deprecation policy should protect material integrations.

## Sync versus async

Choose asynchronous processing when work is long-running, externally coupled or benefits from retry/isolation. The API must then expose durable job/state semantics rather than pretending the work completed synchronously.

## Dual writes

When one business action must affect multiple independent systems, design for failure and reconciliation. A distributed transaction may be unavailable or undesirable; the alternative must still define source of truth, retries, idempotency, ordering and observability.
