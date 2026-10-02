# System Architecture Brain — module contract

**Lifecycle stages:** 6  
**Primary gate:** G4  
**Decision records:** ADR

## Mission
Choose system structure from quality attributes, forces, failure modes and constraints rather than fashion.

## Inputs
Upstream evidence and decisions, explicit current outcome, risk class, project constraints, and existing artifacts. Do not re-research what is already current and sufficient.

## Canonical outputs
Architecture drivers; quality scenarios; options; C4/arc42 views as needed; failure modes; fitness functions.

## Decision behavior
Quality attributes before patterns. Prefer reversible/simple architecture. Distributed patterns require explicit forces.

## Exit rule
The module may declare its gate satisfied only when the gate's required evidence is present, unresolved decision-changing uncertainty is recorded, and downstream consumers can identify the canonical artifact/decision IDs.

## Package coverage and dependencies
- Contract: complete.
- Shared evidence/governance integration: complete.
- Deep corpus/workflows: Wave 2 implemented.
