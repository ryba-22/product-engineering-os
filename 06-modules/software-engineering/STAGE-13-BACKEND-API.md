# Stage 13 — Backend / API

**Module:** software-engineering  
**Gate:** G6  
**Evidence anchors:** EVD-API-001, EVD-API-003  
**Primary artifacts:** `07-templates/API-CONTRACT.md`, OpenAPI where useful

## Purpose
Implement application commands and queries with explicit authorization, invariants, transaction scope, retry semantics and failure contracts. API design is not just route naming; it is the executable boundary between callers and authoritative business behavior.

## Required inputs
Domain ownership/invariants, requirements and scenarios, actor/capability model, persistence constraints, integration dependencies, concurrency risks, audit requirements and expected workload.

## Questions the Brain must answer
1. Who is authorized to perform the operation?
2. What invariants must hold before and after it?
3. Which validation is syntactic, referential or business-semantic?
4. What is the transaction boundary?
5. What happens on retry, duplicate delivery or timeout ambiguity?
6. Which conflicts can occur concurrently?
7. Which side effects may occur only after commit?
8. What error information is safe and useful to expose?

## Workflow
1. **Define operation semantics.** Actor, intent, input, preconditions, invariant changes and result.
2. **Define authorization at the business capability boundary.** Do not rely only on UI visibility.
3. **Define validation layers.** Reject malformed input early, then evaluate authoritative rules in the domain/application layer.
4. **Choose transaction scope.** Keep critical invariant mutations atomic where required.
5. **Define idempotency/retry.** Distinguish HTTP method semantics from application-level deduplication.
6. **Define concurrency strategy.** Use constraints, optimistic versioning, locking or serialized processing based on the invariant.
7. **Separate external side effects from database commit.** Use outbox or equivalent when atomicity across systems is impossible.
8. **Define error contract.** Stable codes/categories, safe messages, retryability and conflict semantics.
9. **Specify audit/telemetry.** Capture actor, decision/result and correlation context proportionally to risk.
10. **Publish machine-readable contracts where beneficial.** Verify compatibility for consumers.

## Decision rules
- Disabling duplicate clicks on the frontend does not make a command retry-safe.
- GET must not mutate state merely because the framework permits it.
- A 2xx response does not prove downstream side effects succeeded unless the contract says synchronous completion.
- Authorization is checked for the requested capability and resource, not inferred from possession of an object ID.
- Cross-system dual writes need explicit failure/reconciliation design.
- Database uniqueness can be part of idempotency/invariant enforcement when it matches domain semantics.

## Evidence standard
Critical API guarantees should have contract/integration tests and, for concurrency or retry behavior, adversarial cases. Machine-readable schemas should match runtime behavior rather than exist as stale documentation.

## Canonical outputs
API/command contract; authorization matrix; validation rules; transaction/idempotency/concurrency policy; error model; OpenAPI/schema; audit/telemetry contract; integration tests.

## Failure modes
CRUD-shaped APIs around tables; hidden business rules in controllers; inconsistent error payloads; retry-unsafe POSTs; external calls inside unbounded transactions; trusting client authorization; race conditions patched with “check then insert”.

## Exit conditions
The backend scope passes G6 when authoritative behavior and failure semantics are explicit, material invariants are enforced under concurrency/retry, and consumers can depend on a verified contract.

## Handoff
Stage 14 implements persistence guarantees. Stage 15 verifies contracts and adversarial behavior. Stage 20 receives telemetry/correlation requirements.
