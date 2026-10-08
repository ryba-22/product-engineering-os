# Software Engineering Brain — module contract

**Lifecycle stages:** 12, 13, 14  
**Primary gate:** G6  
**Decision records:** ADR/DDR

## Mission

Turn architecture and interaction contracts into maintainable frontend, backend/API and persistence implementations.

## Inputs

Upstream evidence and decisions, explicit current outcome, risk class, project constraints, and existing artifacts. Do not re-research what is already current and sufficient.

## Canonical outputs

Frontend state/ownership contract; API contract; persistence contract; migration plan; implementation plan.

## Decision behavior

Keep domain semantics above technical adapters. Define idempotency, validation, error, concurrency and data ownership explicitly when material.

## Exit rule

The module may declare its gate satisfied only when the gate's required evidence is present, unresolved decision-changing uncertainty is recorded, and downstream consumers can identify the canonical artifact/decision IDs.

## Package coverage and dependencies

- Contract: complete.
- Shared evidence/governance integration: complete.
- Deep corpus/workflows: Wave 2 implemented.

## Deep stage playbooks

- Stage 12: [STAGE-12-FRONTEND-IMPLEMENTATION](./STAGE-12-FRONTEND-IMPLEMENTATION.md)
- Stage 13: [STAGE-13-BACKEND-API](./STAGE-13-BACKEND-API.md)
- Stage 14: [STAGE-14-DATABASE-PERSISTENCE](./STAGE-14-DATABASE-PERSISTENCE.md)

## Cross-stage implementation quality

- [Function size as evidence](./FUNCTION-SIZE-EVIDENCE-POLICY.md) — coherent decomposition, reviewable per-function exceptions, and preserved domain/transaction semantics.
