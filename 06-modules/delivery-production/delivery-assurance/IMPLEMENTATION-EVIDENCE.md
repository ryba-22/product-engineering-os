# DA-01 implementation checkpoint — 2026-10-08

**Tracking:** PEOS issue #14. **State:** IMPLEMENTED / LOCAL_VERIFICATION_PASS / INDEPENDENT_REVIEW_OPEN.

## Scope delivered

- Read-only workflow inspector for GitHub Actions: immutable action references, privileged `workflow_run` trust-boundary suspicion and external production-environment protection evidence.
- Versioned rule catalogue and release execution evidence JSON Schema.
- Release evidence evaluation: required CI checks, observed OCI digests, production approval, recovery proof freshness and runtime-health provenance.
- 36 new targeted tests, covering adversarial and positive cases. Advisory exit semantics prevent unreviewed blocking enforcement.
- No actions against production systems, APIs, financial data, provider messages or secrets.

## Local verification (PEOS worktree)

Base before change: `origin/main@cda6e5daa5e9311a841c5220bc80b1cca3e6d25e`.

- `python3 -m pytest tests -q`: **175 passed**, including 36 DA-01 test cases.
- `scripts/validate.py`: PASS.
- `scripts/audit_package_index.py`: PASS.
- `scripts/audit_coverage.py`, `audit_content_depth.py`, `audit_adversarial_run.py`, independent eval audits v1/v2/v3, `audit_freshness.py`: PASS.
- `python3 -m py_compile scripts/delivery_assurance.py`: PASS.
- `git diff --check`: PASS.

## Advisory observations

1. PEOS `.github/workflows/validate.yml`: `DA-GHA-001=FAIL` because `actions/checkout@v4` and `actions/setup-python@v5` use mutable version tags, not full action commit SHAs. This is **not** a finding of an actual compromised action.
2. CRD Finance local main at `217730140389880c575dcf368ef9bdfddb425c55` (one commit behind its local `origin/main` at the time): `.github/workflows/ci.yml` action references were pinned. `.github/workflows/deploy.yml` reported `DA-GHA-002=UNKNOWN` for `workflow_run` trust review and `DA-GHA-003=UNKNOWN` for external environment protection evidence. These are **missing verification**, not proof of vulnerability or incorrectly configured production.

## Risks / known limitations

- The Python validator checks supplied evidence records, not cryptographically authenticated CI events or actual registry/cluster contents. An `ELIGIBLE_FOR_REVIEW` record does not grant deployment permission.
- No GitHub Settings/Environment API adapter or OCI attestation verification exists yet; unavailable checks remain UNKNOWN.
- An external caller must provide authoritative expected CI gates and applicability. Self-declared `required:false` cannot waive production recovery, but a complete external policy engine is outside DA-01.
- The static workflow analysis is intentionally narrow and may report UNKNOWN for safe `workflow_run` variants. It does not substitute for a threat model.
- Full end-to-end real production/staging evidence was not gathered; no production verification claim.

## Next gate

Independent architecture/security/verification review of this PR, plus GitHub Actions CI result. Do not turn advisory findings into mandatory release blocks before baseline agreement and owner acceptance. Project-specific CRD Finance GO/NO-GO remains owned by its existing PRR/REL gates.

## VERIFY-01 remediation — 2026-10-08

**Task:** address [PR #15 VERIFY-01](https://github.com/ryba-22/product-engineering-os/pull/15) findings on the original branch. **State:** IMPLEMENTED / LOCAL_TESTS_PASS / EXTERNAL_REVIEW_OPEN.

### Corrective changes

- P0-1: positive release claims are no longer authenticated by self-supplied JSON. The CLI never supplies a trusted verifier; asserted `evidence_ref` values cannot become observed PASS.
- P0-2: externally supplied, independently controlled project policy specifies mandatory CI gates and required image names. The release record's own `required: false` flags do not weaken expectations. A missing required item stays UNKNOWN; contradictory/failed gates become FAIL.
- P0-3: duplicate gate/artifact IDs fail; an app-only release cannot satisfy a policy requiring worker/migrator.
- P1-1: configurable evidence max-age per CI/approval/runtime/recovery. An old runtime-health observation is no longer a current PASS.
- P1-2: duplicate YAML mapping keys, missing trigger, malformed jobs/steps are rejected. This is not full actionlint coverage.
- P1-3: workflow_run suspicion is job-scoped; unrelated secrets in other jobs no longer force FAIL, but complex cases remain UNKNOWN. Deploy-like jobs without explicit environment produce UNKNOWN.
- Regression: 25 VERIFY-01 tests plus 2 follow-up edge cases added to the original 36 targeted tests.

### Verification evidence

- Isolated local baseline: original PR SHA `f180612a8a612a8de4ac225bcc8eb94a21392f45`.
- After remediation: **202/202 pytest PASS**, including **63 Delivery Assurance tests**.
- `scripts/validate.py`, `audit_package_index.py`: PASS.
- Prior full-scope regression at 200 tests: coverage/content-depth/adversarial run/independent eval audits v1-v3/freshness PASS (two extra isolated tests added since).
- Advisory run against PEOS workflow: identifies unpinned action tags, without changing deployment settings.
- Advisory run against existing local CRD Finance working copy: CI full-SHA pinning PASS, `workflow_run` and production environment verification UNKNOWN. This copy is **not** an authoritative current production audit.

### Known boundary / residual risks

There is no authenticated GitHub environment, OCI registry, signed provenance, required-check inventory, or runtime-health adapter yet. Consequently, **the public CLI deliberately cannot produce production release eligibility from asserted evidence alone**. `policy_verified=True` and in-process `verifier` are hooks for a future trusted adapter, currently used only by synthetic test doubles. Even with a future adapter, project-level independent operator/financial GO gates remain separate.

No CRD Finance code, staging, production, secrets, migrations, data, or SMS have been mutated.

**Next:** new exact SHA + GitHub CI verification; independent security/architecture review on final diff; no enforcement and no production merge via this task.
