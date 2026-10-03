# Security Reliability Brain — module contract

**Lifecycle stages:** 16, 20, 21  
**Primary gate:** G8/G10  
**Decision records:** SDR/ODR

## Mission
Integrate secure SDLC, threat modeling, reliability, observability, DR and incident readiness.

## Inputs
Upstream evidence and decisions, explicit current outcome, risk class, project constraints, and existing artifacts. Do not re-research what is already current and sufficient.

## Canonical outputs
Threat model; security requirements; SLO/SLI; telemetry contract; DR/incident runbooks; restore evidence.

## Decision behavior
Security is lifecycle-wide. Reliability targets are user-facing decisions. Configuration without exercised recovery is not verified.

## Exit rule
The module may declare its gate satisfied only when the gate's required evidence is present, unresolved decision-changing uncertainty is recorded, and downstream consumers can identify the canonical artifact/decision IDs.

## Package coverage and dependencies
- Contract: complete.
- Shared evidence/governance integration: complete.
- Deep corpus/workflows: Wave 3–4 implemented.

## Deep stage playbooks

- Stage 16: [STAGE-16-SECURITY](./STAGE-16-SECURITY.md)
- Stage 20: [STAGE-20-OBSERVABILITY](./STAGE-20-OBSERVABILITY.md)
- Stage 21: [STAGE-21-BACKUP-DR-INCIDENTS](./STAGE-21-BACKUP-DR-INCIDENTS.md)
