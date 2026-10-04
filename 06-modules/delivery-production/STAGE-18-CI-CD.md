# Stage 18 — CI/CD

**Module:** delivery-production  
**Gate:** G9  
**Evidence anchors:** EVD-DEL-001, EVD-DEL-003  
**Primary decision system:** `CI-CD.md`

## Purpose
Turn source changes into reproducible, attributable artifacts through automated evidence-producing gates. CI/CD is not just deployment automation; it is the mechanism that ties a release to code, dependencies, tests, security checks, migrations and provenance.

## Required inputs
Source repository, build definition, test/security/performance gates, dependency lock state, migration artifacts, environment configuration model, release policy and artifact registry.

## Questions the Brain must answer
1. Can the same source/dependency state produce the same release artifact?
2. Which checks are blocking versus advisory and why?
3. What exact commit/configuration produced the artifact?
4. Are secrets/config separated from build output?
5. Are dependencies and build provenance inspectable?
6. How are migrations coordinated with application rollout?
7. What evidence is retained for release decisions?
8. Which release-state claims are directly observed and which are only inferred from deployment, branch, artifact or pipeline state?
9. What happens when a gate is flaky or infrastructure fails?

## Workflow
1. **Define pipeline stages.** Lint/static → unit/contract → integration → security/dependency → build → artifact verification → release candidate.
2. **Pin/lock dependencies and build tooling** where reproducibility matters.
3. **Build once, promote the same artifact.** Avoid rebuilding different bytes per environment unless explicitly required and attributable.
4. **Attach provenance.** Source SHA, build ID, dependency metadata and artifact digest.
5. **Run deterministic gates early.** Expensive environment tests come later but before release where required.
6. **Handle migrations explicitly.** Define compatibility order and failure behavior.
7. **Separate configuration and secrets.** Validate required config without exposing secret values.
8. **Persist gate results.** A release decision should reference evidence, not a memory that “CI was green.”
9. **Treat flakiness as pipeline debt.** Quarantine only with owner and expiry.
10. **Measure delivery flow.** Track lead/throughput and instability in context rather than optimizing a single metric.

## Decision rules
- A branch name is not release provenance.
- Rebuilding on production can invalidate previously tested artifact evidence.
- “Allow failure” requires rationale and visible residual risk.
- Flaky tests are not neutral; they erode trust and eventually get ignored.
- Manual approval is useful only when the approver receives decision-relevant evidence.
- `deployed to staging ≠ staging healthy`; artifact presence, deployment completion or container/process liveness must not be promoted to health evidence unless the relevant smoke/SLO/telemetry observation actually exists.
- Do not upgrade a scenario statement or pipeline state into a stronger lifecycle claim. Say `DEPLOYED/UNVERIFIED HEALTH` when deployment is known but health evidence is absent.
- CI credentials should have least privilege and short-lived scope where practical.

## Evidence standard
Each release candidate should be traceable to immutable source/artifact identifiers and gate results. Evidence must distinguish skipped, failed, retried and passed checks. Claims about staging/production health require their own observed evidence; a successful build, push or deployment event is evidence of that earlier state only, not of runtime health.

## Canonical outputs
Pipeline definition; artifact/provenance record; gate matrix; test/security results; migration sequencing; release candidate metadata; delivery metrics.

## Failure modes
Build-per-environment drift; mutable artifacts; secret leakage in logs; ignored flaky tests; manual undocumented hotfix; deployment scripts outside version control; green pipeline with skipped critical tests; inferring `HEALTHY` from `DEPLOYED` or from an artifact/pipeline status without runtime evidence.

## Exit conditions
G9 CI/CD scope is satisfied when an exact artifact has reproducible provenance, required gates have trustworthy results, and deployment can consume that artifact without changing its tested contents.

## Handoff
Stage 19 receives the release candidate and Release Evidence Bundle. Stage 20 receives build/deploy version identifiers for telemetry correlation.
