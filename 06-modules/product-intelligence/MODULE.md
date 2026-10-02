# Product Intelligence Brain — module contract

**Lifecycle stages:** 22, 23, 24  
**Primary gate:** G11  
**Decision records:** PDR

## Mission
Measure outcomes, run appropriate experiments and turn production feedback into the next evidence-backed iteration.

## Inputs
Upstream evidence and decisions, explicit current outcome, risk class, project constraints, and existing artifacts. Do not re-research what is already current and sufficient.

## Canonical outputs
Metric tree; event taxonomy; tracking plan; experiment/pilot plan; outcome review; learning record.

## Decision behavior
Start from outcome → behavior → signal → metric → event. Choose A/B only when causal controlled experimentation is the right evidence method.

## Exit rule
The module may declare its gate satisfied only when the gate's required evidence is present, unresolved decision-changing uncertainty is recorded, and downstream consumers can identify the canonical artifact/decision IDs.

## Package coverage and dependencies
- Contract: complete.
- Shared evidence/governance integration: complete.
- Deep corpus/workflows: Wave 5 implemented.
