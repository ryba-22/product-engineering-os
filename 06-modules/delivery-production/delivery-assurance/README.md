# Delivery Assurance — DA-01 (advisory prototype)

Tracking: [PEOS #14](https://github.com/ryba-22/product-engineering-os/issues/14). Scope: portable, read-only, *non-authoritative* workflow and release-claim evaluation. This package **never approves or blocks an actual deployment**. Projects own runtime and final go/no-go.

## Ownership and trust boundary

- Engineering Knowledge Hub routes source knowledge; PEOS owns rule/eval semantics; a project owns its release policy, real CI and operational evidence.
- `release-evidence.schema.json` defines **untrusted assertions** about one candidate release, not cryptographically authenticated observations.
- `project-policy.schema.json` defines **expected** required CI gates, artifact names and evidence freshness. It is a separate input and cannot be weakened by a release record's own `required: false` flags or missing artifact entries.
- A JSON policy loaded via CLI is not authenticated merely because it resides in a file. A consuming integration must pin/review its exact identity (e.g. approved main SHA or protected configuration) *outside* the release input.
- `assess_release(..., policy=..., policy_verified=True, verifier=...)` exists for a **trusted in-process integration only**. The `verifier` callable must cross an authenticated GitHub/registry/runtime boundary and compare immutable identities. It is not currently implemented. Any self-supplied or fake verifier invalidates real-world safety claims.
- The CLI intentionally offers **no** flag to self-declare policy authentication or external evidence verification. Without such evidence its positive claims become `UNKNOWN`, not `PASS`.

A passed local test using a deliberately trusted mock verifier proves **evaluation branching only**, not the security of an external adapter.

## Commands

```bash
python scripts/delivery_assurance.py workflows .github/workflows/validate.yml
python scripts/delivery_assurance.py release path/to/release-evidence.json \
  --policy 06-modules/delivery-production/delivery-assurance/project-policy.example.json \
  --as-of 2026-10-08T13:00:00Z
python -m pytest tests/test_delivery_assurance.py -q
```

The example policy is **synthetic**. It does not encode or authorize CRD Finance production requirements. Provide a real, separately reviewed project policy before interpreting project findings.

Output: JSON `mode: ADVISORY`, `verdict`, `findings[]`. Semantic failures are present in JSON but currently exit 0 so no accidental CI enforcement occurs.

## Results

- `PASS`: requirement observed within *a trusted evidence boundary*. Local static checks can PASS for an unambiguous YAML property. Self-reported runtime evidence cannot.
- `FAIL`: contradiction, expired evidence, failed gate, duplicate identity or structural defect.
- `UNKNOWN`: absent or unauthenticated policy/evidence, unobservable environment approval, or insufficient static trust-boundary analysis.
- `NOT_APPLICABLE`: justified scope exclusion, never a substitute for a required gate.
- `WAIVED`: accepted only when owner/scope/rationale/expiry and independently authenticated waiver are present; never auto-PASS.

Aggregate precedence: `BLOCKED > UNVERIFIED > REVIEW_REQUIRED > ELIGIBLE_FOR_REVIEW`. The last status is **still not** a production GO decision.

## Static workflow inspection

The parser uses string-valued GitHub-compatible YAML loading and rejects duplicate mapping keys. Missing `on` triggers and invalid jobs/steps cannot produce a positive verdict. This is **not** full `actionlint` or GitHub runtime evaluation.

`DA-GHA-001`: full commit SHA for external uses references (but no verification of the SHA's owner). `DA-GHA-002`: cautious, job-scoped suspicion of `workflow_run` upstream checkout combined with same-job secrets; unrelated jobs do not prove exposure, while complex cross-job flows remain UNKNOWN. `DA-GHA-003`: production or dynamic Environment declarations require external GitHub settings evidence; deploy-like jobs with no declared environment also remain UNKNOWN rather than claiming an approval control is inapplicable. YAML alone cannot prove reviewer enforcement.

## Release-claim inspection

`DA-REL-006`: separately trusted project policy must be verified before review eligibility.

`DA-REL-001`: policy-required checks cannot disappear via `required:false`; missing evidence is UNKNOWN and actual failures are FAIL.

`DA-REL-002`: the policy determines required image names (including workers/migrators where appropriate); duplicates fail; matching strings without independently observed digests remain UNKNOWN. A source commit SHA does not replace an OCI digest.

`DA-REL-003`: production approval must have current independently verified evidence. `DA-REL-004`: recovery proof must be current under both project policy and its own validity window. `DA-REL-005`: post-deploy health requires current runtime observation; an old CI run is not production health.

## Adversarial acceptance / limitations

`tests/test_delivery_assurance.py` includes the VERIFY-01 reproductions: fabricated evidence refs; self-weakened required gates; missing/duplicate artifacts; expired or ancient runtime and recovery; missing/duplicate YAML triggers; privileged checkout with unrelated vs same-job secrets; dynamic environment; unverified waivers.

**Explicit non-goals:** self-deploying a release, creating release permits, reading GitHub secrets or host credentials, accessing financial production, inspecting live GitHub Environment settings, registry digest attestations, or protected configuration. Adapter implementation and independent threat model review remain follow-up work.

CRD Finance retains its independent REL #97/#102 and PRR #198 gates and production NO-GO decisions.
