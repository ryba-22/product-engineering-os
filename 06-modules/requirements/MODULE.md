# Requirements Brain — module contract

**Lifecycle stages:** 4  
**Primary gate:** G3  
**Decision records:** PDR/TDR

## Mission
Translate validated outcomes and domain evidence into traceable requirements, scenarios, NFRs and acceptance criteria.

## Inputs
Upstream evidence and decisions, explicit current outcome, risk class, project constraints, and existing artifacts. Do not re-research what is already current and sufficient.

## Canonical outputs
Product brief; PRD; NFR quality scenarios; scenarios; acceptance criteria; traceability matrix.

## Decision behavior
Every material requirement should trace to evidence/outcome and forward to verification. Avoid implementation detail unless it is a real constraint.

## Exit rule
The module may declare its gate satisfied only when the gate's required evidence is present, unresolved decision-changing uncertainty is recorded, and downstream consumers can identify the canonical artifact/decision IDs.

## Current maturity in v0.1
- Contract: complete.
- Shared evidence/governance integration: complete.
- Deep corpus/workflows: Wave 1 implemented.
