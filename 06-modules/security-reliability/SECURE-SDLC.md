# Secure SDLC

Security spans governance, requirements, design, implementation, verification, delivery and operations. The controls below scale with R0–R4 risk; they are not a mandatory ceremony for every typo change.

## Requirements and ownership

For material changes define:
- data/security classification;
- authentication and authorization requirements;
- sensitive operations;
- logging/audit requirements;
- privacy/retention constraints;
- third-party trust;
- recovery/incident implications.

Assign an owner for unresolved security risk.

## Design controls

Use threat modeling when new trust boundaries, privileged operations, sensitive data, external integrations or high-impact flows appear. Record security architecture decisions and abuse cases. Prefer secure defaults and least privilege.

## Implementation controls

- centralize/standardize authorization where practical;
- validate untrusted input at boundaries;
- encode/escape for output context;
- parameterize database queries;
- handle secrets outside source/client artifacts;
- use safe crypto/platform libraries rather than custom algorithms;
- protect idempotency/retry for sensitive state changes;
- avoid sensitive data in logs/errors;
- minimize privileges for service identities.

## Dependency and supply chain

Lock/pin dependencies where appropriate, scan known vulnerabilities, review material new dependencies, keep provenance from source to artifact, protect CI credentials and avoid executing untrusted build inputs with broad secrets.

Vulnerability count alone is not a decision. Evaluate exploitability, exposure, compensating controls and update risk.

## Verification

Use the layer that matches the threat:
- unit/property tests for validation/authorization helpers;
- integration tests for resource-level access and data boundaries;
- static/dependency checks;
- dynamic/abuse-case testing;
- targeted manual security review for R3/R4 or novel surfaces;
- release configuration/provenance checks.

Security tests should include negative cases: unauthorized actor, wrong tenant/resource, expired/revoked credential, replay/duplicate, malformed input and dependency failure.

## Release

Ensure security-critical migrations/configuration and secrets are present, least privilege remains intact and rollback/forward-fix is known. Do not expose debug endpoints or verbose sensitive errors.

## Operations

Monitor authentication/authorization anomalies, abusive traffic, secret/certificate expiry and security-relevant provider failures. Maintain incident response and postmortem paths.

## Exception policy

A failed security control may be temporarily accepted only with scope, owner, rationale, mitigation and expiry/revisit trigger. Silent exceptions are policy erosion.

The goal is traceability from threat → requirement → control → verification → production signal.
