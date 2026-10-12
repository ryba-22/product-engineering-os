# Defect to Regression — Evidence Record

Use for a material reproducible defect or a high-risk behavioral change. Do not fill fields with invented evidence. N/A needs a reason. A completed template is **not** an executed verification gate.

## Scope and identity
- Work item / owner:
- Problem and user-visible consequence:
- Boundary / invariant:
- Risk and rollback or recovery:
- Repository / base SHA / proposed SHA:
- Affected host / environment / versions:
- Source of truth for the behavior:
- FACT (observed):
- HYPOTHESIS (falsifiable):
- OPEN QUESTION (decision-changing):

## Before the fix — reproducer
- Minimal reproducible fixture and sanitized inputs:
- Exact invocation / preconditions:
- Actual output / failure and evidence location:
- Expected output and oracle (who/what authorizes it):
- Oracle limitations or conflicts:
- Regression test ID and path:
- RED run: command, exit/status, timestamp, exact baseline SHA and evidence:
- Does the failure prove the intended defect, rather than a broken harness?:

## Change and verification
- Smallest implemented change / diff:
- GREEN run: command, exit/status, timestamp, exact HEAD SHA and evidence:
- Relevant existing regressions and outcomes:
- Negative/adversarial case:
- Real host or integration check (if required), observable result and proof:
- Skipped, failed or unavailable checks (do not collapse into PASS):
- If live host is unavailable, report HOST UNVERIFIED:

## Release/input proof (only if claiming release qualification)
- Source SHA and dependency/companion pin(s):
- Actual build inputs observed (manifest/metafile/log/check):
- Artifact digest and provenance evidence:
- Exact artifact tested:
- Exact artifact deployed/promoted (if any):
- Runtime health evidence (if any):
- Any unresolved source/artifact mismatch:

## Verdict and learning
- Claim supported: DECIDED / IMPLEMENTED / TESTED / VERIFIED / DEPLOYED / HEALTHY / SUCCESSFUL (name the highest **proven** state only):
- Confidence limits and residual risks:
- Root cause / rejected hypotheses:
- Contract/test or documentation updated:
- Canonical status/decision updated or NO_DOC_DELTA (reason):
- Next owner / action / STOP condition:
