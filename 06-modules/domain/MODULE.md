# Domain Brain — module contract

**Lifecycle stages:** 3, 5  
**Primary gate:** G2  
**Decision records:** ADR

## Mission
Discover domain language, events, rules, boundaries and tactical models from traceable evidence.

## Inputs
Upstream evidence and decisions, explicit current outcome, risk class, project constraints, and existing artifacts. Do not re-research what is already current and sufficient.

## Canonical outputs
Evidence Bank; glossary; Event Storming; Context Map; aggregate hypotheses.

## Decision behavior
Use a supplied, verified domain specialist when available; otherwise follow the bundled Domain contract and document unresolved questions. Never derive contexts directly from tables/screens.

## Exit rule
The module may declare its gate satisfied only when the gate's required evidence is present, unresolved decision-changing uncertainty is recorded, and downstream consumers can identify the canonical artifact/decision IDs.

## Package coverage and dependencies
- Contract: complete.
- Shared evidence/governance integration: complete.
- Deep corpus/workflows: adopt existing mature asset.

## Standalone operation
Specialist brains are optional integrations, not bundled dependencies. If unavailable, use this contract, the bundled evidence ledger, templates and quality gates. Record unresolved domain or experience questions explicitly; request targeted evidence when required. Do not claim access to an external corpus or equivalent specialist depth.
