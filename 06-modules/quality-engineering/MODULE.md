# Quality Engineering Brain — module contract

**Lifecycle stages:** 15, 17  
**Primary gate:** G7  
**Decision records:** TDR

## Mission
Design risk-based verification and performance evidence at the lowest trustworthy layer.

## Inputs
Upstream evidence and decisions, explicit current outcome, risk class, project constraints, and existing artifacts. Do not re-research what is already current and sufficient.

## Canonical outputs
Risk map; test strategy; contract/invariant/property/integration/concurrency/E2E plans; performance budgets.

## Decision behavior
Choose the lowest layer that can honestly prove the risk, then add integration/runtime evidence where needed. Tests are guarantees, not counts.

## Exit rule
The module may declare its gate satisfied only when the gate's required evidence is present, unresolved decision-changing uncertainty is recorded, and downstream consumers can identify the canonical artifact/decision IDs.

## Package coverage and dependencies
- Contract: complete.
- Shared evidence/governance integration: complete.
- Deep corpus/workflows: Wave 3 implemented.

## Deep stage playbooks

- Stage 15: [STAGE-15-TESTING](./STAGE-15-TESTING.md)
- Stage 17: [STAGE-17-PERFORMANCE](./STAGE-17-PERFORMANCE.md)
