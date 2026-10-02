# Delivery Production Brain — module contract

**Lifecycle stages:** 18, 19  
**Primary gate:** G9  
**Decision records:** ODR

## Mission
Create reproducible delivery, release evidence, safe rollout and rollback/forward-fix operations.

## Inputs
Upstream evidence and decisions, explicit current outcome, risk class, project constraints, and existing artifacts. Do not re-research what is already current and sufficient.

## Canonical outputs
CI gates; artifact provenance; environment/migration policy; rollout/rollback/forward-fix plan; release evidence bundle.

## Decision behavior
Build and migration are separate decisions. Deploy exact verified artifacts. Capture release evidence automatically where possible.

## Exit rule
The module may declare its gate satisfied only when the gate's required evidence is present, unresolved decision-changing uncertainty is recorded, and downstream consumers can identify the canonical artifact/decision IDs.

## Package coverage and dependencies
- Contract: complete.
- Shared evidence/governance integration: complete.
- Deep corpus/workflows: Wave 4 implemented.

## Deep stage playbooks

- Stage 18: [STAGE-18-CI-CD](./STAGE-18-CI-CD.md)
- Stage 19: [STAGE-19-DEPLOYMENT-ROLLOUT](./STAGE-19-DEPLOYMENT-ROLLOUT.md)
