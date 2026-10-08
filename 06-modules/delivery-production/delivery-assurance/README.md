# Delivery Assurance — DA-01 (advisory pilot)

Tracking: [PEOS #14](https://github.com/ryba-22/product-engineering-os/issues/14).

## Why

PEOS G8/G9/G10 contain release and production requirements, but text policy alone is not evidence that any real workflow or release satisfied them. DA-01 turns a deliberately narrow subset into machine-evaluable checks. It **does not authorize a release**, access production, or mutate repositories.

## Ownership

- Engineering Knowledge Hub owns source/provenance routing.
- Product Engineering OS owns reusable rule semantics, rule catalogue, test fixtures and evaluation.
- Each project owns its CI/runtime configuration, release evidence, exceptions and final go/no-go decisions.
- CRD Finance retains independent financial-correctness/operational-pilot gates and existing REL/PRR issues.

## CLI usage

From the repository root:

```bash
python scripts/delivery_assurance.py workflows .github/workflows/validate.yml
python scripts/delivery_assurance.py release path/to/release-evidence.json --as-of 2026-10-08T13:00:00Z
python -m pytest tests/test_delivery_assurance.py -q
```

Output is a machine-readable JSON object: `mode: ADVISORY`, `verdict`, `findings[]`. Process exit is zero for semantic FAIL (to prevent early enforcement); malformed invocation or unrecoverable program bugs are not silently handled.

## Meaning of statuses

- `PASS`: observed in the permitted evidence boundary;
- `FAIL`: contradiction with a declared rule;
- `UNKNOWN`: evidence missing or outside the inspector's trusted scope;
- `NOT_APPLICABLE`: the scenario is outside the declared scope;
- `WAIVED`: explicit owner, scope, reason and expiry; remains review-required, never PASS.

Overall verdict: `BLOCKED` if any FAIL, otherwise `UNVERIFIED` if any UNKNOWN, otherwise `REVIEW_REQUIRED` if any WAIVED, otherwise `ELIGIBLE_FOR_REVIEW`. None is a deployment command or production go decision.

## Static vs runtime boundary

`workflows` parses local YAML using PyYAML BaseLoader (so GitHub's `on` key is not interpreted as a YAML 1.1 boolean). It checks full-SHA `uses` references, a narrow unsafe `workflow_run` combination, and whether production approval needs external inspection. A `workflow_run` without a known dangerous pattern stays UNKNOWN rather than being categorically rejected. A declared `environment: production` also stays UNKNOWN: protected reviewers are GitHub settings, not YAML proof. The tool does not fetch or inspect settings, secrets, external action ownership or upstream artifacts.

`release` consumes a project-supplied record defined by `release-evidence.schema.json`. It checks mandatory CI checks, app/worker/migrator digest identity, approval evidence, recovery freshness, and observed production health separately. A PASS field without evidence references and timestamps becomes UNKNOWN. Expired recovery proof becomes FAIL. Waivers need explicit scope/owner/expiry and never elevate release eligibility.

The source of a release's financial/domain truth remains the project, not PEOS. A green workflow does not prove reconciled money or provider delivery.

## Adversarial acceptance

`tests/test_delivery_assurance.py` includes positive and negative cases: mutable action tag, production environment missing API proof, privileged upstream checkout with secrets, skipped gate, digest mismatch, missing approval, stale restore evidence, false runtime-health inference, malformed waiver and malformed metadata.

## Boundaries / follow-ups

1. No enforcement wiring before independent review. The existing `.github/workflows/validate.yml` already runs pytest, so tests execute in CI when PR runs.
2. Add real GitHub-environment and OCI registry adapters in separate implementation tasks. Until then they MUST remain UNKNOWN, not fabricated.
3. Validate receipt of observations from live CI/runtime against known immutable identifiers; avoid trusting self-declared JSON as cryptographic proof.
4. Treat the rule set as pilot coverage, not an exhaustive security proof. Reassess severity, exception expiry and parsing limits before adopting it as a blocking gate.
5. No changes to CRD Finance production, secrets, deployment or GO/NO-GO policy are authorized by this package.
