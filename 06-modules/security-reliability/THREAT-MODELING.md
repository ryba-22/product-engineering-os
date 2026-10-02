# Threat Modeling Brain

Threat modeling is a design activity, not a final penetration-test substitute.

## Workflow
1. Define protected outcomes/assets and trust boundaries.
2. Diagram relevant data/control flows and external dependencies.
3. Identify actors, privileges and abuse/misuse cases.
4. Enumerate threats against confidentiality, integrity, availability, authorization, auditability and privacy as applicable.
5. Prioritize by consequence, exploitability/exposure and detectability; avoid fake precision.
6. Choose prevention, detection, recovery or explicit acceptance.
7. Link mitigations to requirements, tests, telemetry and owners.
8. Revisit on architecture/data/privilege/integration changes.

## Hard rule
Client-side checks are not authorization. Security boundaries must be enforced at a trusted server/data boundary.
