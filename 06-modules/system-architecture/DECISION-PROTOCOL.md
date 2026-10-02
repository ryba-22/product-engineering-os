# System Architecture Brain — decision protocol

## Core question
What system structure best satisfies the known business capabilities and quality attributes with the least irreversible complexity?

## Runtime
1. Load product outcome, domain boundaries, requirements and risk class.
2. Extract architecture drivers: scale, latency, availability, consistency, security, auditability, changeability, operability, cost, team constraints and integration needs.
3. Convert vague NFRs into measurable quality-attribute scenarios.
4. Identify hard constraints and failure modes before choosing patterns.
5. Generate at least one simple baseline architecture and only add distributed/specialized mechanisms when a named force requires them.
6. Compare options on consequences and switching conditions, not fashion.
7. Record material decisions in ADRs.
8. Define architecture fitness functions or verification hooks for properties that can regress.
9. Revisit when an observable trigger invalidates an assumption.

## Architecture-inflation guard
Microservices, CQRS, event sourcing, Kafka/queues, distributed caches, service meshes and multi-region designs are not maturity badges. They require explicit problem forces and an explanation of why a simpler architecture is insufficient.

## Failure analysis prompts
For each cross-boundary workflow ask: what if the caller retries, times out, crashes after commit, receives a duplicate, executes concurrently, observes stale data, or loses a dependency? Decide whether the response is retry, idempotency, locking, compensation, queueing, outbox, rejection or operator recovery.
