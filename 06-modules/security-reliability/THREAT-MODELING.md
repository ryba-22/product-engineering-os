# Threat Modeling Brain

Use with `STAGE-16-SECURITY.md`. Threat modeling is a repeatable design activity that ties protected outcomes and trust boundaries to security requirements and verification.

## Scope

Name:
- system/change version;
- protected assets/outcomes;
- actors and privilege levels;
- entry points;
- trust boundaries;
- data flows/stores;
- external dependencies;
- administrative/build/deployment paths.

A diagram without version/scope quickly becomes misleading.

## Workflow

1. **Identify assets/outcomes.** Data confidentiality, transaction integrity, service availability, identity/account safety, business operations.
2. **Map actors and privileges.** Anonymous, authenticated, privileged operator, service identity, third party, compromised insider/account.
3. **Map trust boundaries and data flows.**
4. **Generate threats/abuse cases.** Use STRIDE or another structure as a prompt, not as a checkbox.
5. **Prioritize.** Consequence × plausibility/exposure × detectability; align with R0–R4.
6. **Turn threats into requirements.**
7. **Map controls.** Prevention, detection, containment and recovery.
8. **Plan verification.**
9. **Record residual risk and owner.**
10. **Revisit on material architecture/identity/data-flow change.**

## Abuse-case prompts

Ask:
- Can an actor access another tenant/user/object by changing an ID?
- Can privilege be retained after role/session change?
- Can replay/retry duplicate a sensitive action?
- Can untrusted input reach interpreter/query/template/path contexts?
- Can secrets leak through logs, errors, client bundles or build artifacts?
- Can rate/automation exhaust a costly resource?
- Can a third party or dependency compromise the trust chain?
- Can an operator/admin action bypass ordinary controls without audit?

## Controls

Controls should be explicit and testable: authentication, resource-level authorization, input validation, output encoding, CSRF/replay protection, secure secret storage/rotation, encryption, rate limits, dependency verification, audit, segmentation, backups and incident response.

Defense in depth is valuable when layers fail independently; duplicated checks that share the same flaw are not independent protection.

## Hard rules

- Authentication ≠ authorization.
- UI hiding ≠ authorization.
- Encryption ≠ access control.
- Validation ≠ output encoding.
- Dependency scan success ≠ supply-chain trust.
- A pentest does not replace design-time threat modeling.

## Output

The Threat Model must leave downstream teams with concrete security requirements, control owners, verification methods and residual risks—not only a list of possible attacks.
