# Secure SDLC

Security spans governance, design, implementation, verification and operations.

## Minimum lifecycle controls proportional to risk
- tracked security requirements and decisions;
- threat modeling for material changes;
- authenticated identity and server-side authorization;
- least privilege and secret handling;
- dependency/vulnerability and secret scanning;
- secure build/release provenance where justified;
- security-focused code/architecture review;
- requirements-driven tests (e.g. ASVS-derived where applicable);
- logging/audit without leaking secrets/PII;
- incident/vulnerability handling and credential rotation;
- production edge/network/config verification.

## Supply-chain rule
A successful source scan does not prove the deployed artifact. Preserve the link from reviewed source/commit through build artifact to deployment; record provenance/attestation where the threat model warrants it.
