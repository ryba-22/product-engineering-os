# Knowledge Governance Brain — module contract

**Lifecycle stages:** 25  
**Primary gate:** continuous  
**Decision records:** all

## Mission
Keep sources, evidence, decisions, patterns and evals fresh, attributable, conflict-aware and supersedable.

## Inputs
Upstream evidence and decisions, explicit current outcome, risk class, project constraints, and existing artifacts. Do not re-research what is already current and sufficient.

## Canonical outputs
Source registry; evidence ledger; decision registry; supersession graph; freshness queue; eval regression report.

## Decision behavior
Preserve provenance, scope and conflicts. Newer evidence does not automatically supersede stronger scoped evidence.

## Exit rule
The module may declare its gate satisfied only when the gate's required evidence is present, unresolved decision-changing uncertainty is recorded, and downstream consumers can identify the canonical artifact/decision IDs.

## Current maturity in v0.1
- Contract: complete.
- Shared evidence/governance integration: complete.
- Deep corpus/workflows: Wave 1 implemented.
