# Stage 16 — Security

**Module:** security-reliability  
**Gate:** G8  
**Evidence anchors:** EVD-SEC-003, EVD-SEC-004  
**Primary artifact:** `07-templates/THREAT-MODEL.md`

## Purpose
Integrate security into design and delivery by making assets, trust boundaries, attacker goals, abuse cases and controls explicit. Security is a lifecycle property: requirements, design, implementation, verification, release and operations all contribute evidence.

## Required inputs
Architecture views, data flows, actor/permission model, data classification, external dependencies, deployment model, API/persistence contracts, regulatory constraints and operational access paths.

## Questions the Brain must answer
1. What assets or outcomes require protection?
2. Which actors and systems cross trust boundaries?
3. What attacker or misuse capabilities are realistic?
4. How can confidentiality, integrity, availability or authorization fail?
5. Which controls prevent, detect or contain each material threat?
6. Where are credentials/secrets created, stored, rotated and revoked?
7. Which dependency/supply-chain risks matter?
8. What security evidence is required before release?

## Workflow
1. **Scope the model.** Tie it to a concrete architecture/version and protected outcomes.
2. **Map data flows and trust boundaries.** Include users, services, data stores, third parties, admin paths and build/deploy systems.
3. **Identify threats and abuse cases.** Use a structured method where helpful, then adapt to domain-specific misuse.
4. **Prioritize by consequence and plausibility.** Avoid equal treatment of cosmetic and material risks.
5. **Convert threats into security requirements.** Ownership, authentication, authorization, validation, secrets, encryption, audit, rate controls and recovery as applicable.
6. **Map controls to layers.** Prefer prevention plus detection/containment for high-impact scenarios.
7. **Verify design assumptions.** Ensure API, persistence and deployment choices actually implement the control.
8. **Plan security testing.** Static/dependency checks, contract tests, abuse cases and targeted manual review based on risk.
9. **Track residual risk.** Acceptance needs owner and rationale.
10. **Revisit on material change.** New trust boundary, identity model, sensitive data or external integration reopens the model.

## Decision rules
- Authentication is not authorization.
- Hiding an action in the UI is not access control.
- Input validation does not replace authorization or output encoding.
- Secrets never belong in source, logs or client bundles.
- Third-party libraries and build provenance are part of the threat surface.
- “Internal only” lowers some exposure but does not eliminate misuse, compromised credentials or data leakage risks.

## Evidence standard
Material threats need a traceable requirement/control and verification method. High-risk residual issues need explicit acceptance or blocking status rather than a vague “known risk” note.

## Canonical outputs
Threat Model; security requirements; control map; abuse cases; dependency/supply-chain policy; security test plan/results; residual-risk register; security ADR/SDR.

## Failure modes
Checklist-only security; pentest-at-the-end mindset; missing authorization boundaries; logging sensitive data; stale threat model; false trust in internal networks; dependency scanning with no remediation ownership.

## Exit conditions
G8 security scope is satisfied when material threats have implemented and verified controls or explicitly accepted residual risk, and release/operations know what must remain observable.

## Handoff
Stage 18 enforces security gates in CI where appropriate. Stage 19 preserves secure configuration. Stage 20 monitors relevant signals. Stage 21 incorporates security incidents into response plans.
