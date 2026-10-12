# Product Engineering OS — agent working agreement

Read [BRAIN.md](BRAIN.md), [RUNBOOK.md](RUNBOOK.md) and the *relevant* stage playbook before material changes. This repository is a reusable operating method, **not** the authority for any adopting project's business facts, architecture, access policy, CI, secrets or production state.

## Before acting

For nontrivial product, UX, domain, architecture, technology or engineering-process recommendations, apply [Research-first solution selection](00-core/research-first-decisions.md) within the existing PEOS route: clarify the problem, evidence/drivers, credible alternatives (including no change), trade-offs, critical perspectives and verdict. Keep low-risk choices lightweight. An AI perspective is not a real person's approval.

1. Preserve the user's original outcome, scope, constraints and STOP. Inspect the current repository evidence and overlapping PRs first; do not create a second framework for a capability already present.
2. Distinguish FACT / HYPOTHESIS / ASSUMPTION / DECISION / OPEN QUESTION. Record decision-changing uncertainty rather than fabricating evidence or expanding research indefinitely.
3. Route proportionally to risk. Use the smallest relevant template and executable check. Do not impose release gates, independent reviewers, new layers or extensive documents on unrelated work.
4. For changes in this PEOS repository, respect the `2026-09-30` research-corpus cutoff. A later external example may inform a clearly identified **operational adapter**, but must not silently become historical evidence in the frozen source registry.

## When repairing a real defect

Use [Forensic change loop](08-adapters/forensic-change-loop.md) and [Defect-to-regression evidence](07-templates/DEFECT-REGRESSION-EVIDENCE.md) for material reproducible failures. State the invariant and oracle; reproduce the defect; prove the regression detects the broken baseline (RED); implement a bounded fix; observe GREEN and the necessary host/integration behavior. An assertion, a passed test or an AI report is not its own oracle. If RED cannot be observed, report that limitation.

For integrations with legacy applications, never confuse a test double with a real host. For cross-repository/release work, verify what inputs the build **actually consumed**, the emitted artifact digest and the exact candidate under test. If any link is missing, report PARTIAL / UNVERIFIED rather than PASS.

## Evidence, safety and closure

- Do not mutate production data, protected files, signed artifacts, secrets, deployment state or release tags without task-specific authorization. Use disposable fixtures, explicit ownership, timeouts and cleanup for live tests.
- Existing project-level `AGENTS.md`, domain decisions, quality gates, owner permissions and runbooks supersede generic examples when adopting PEOS.
- Keep `DECIDED / IMPLEMENTED / TESTED / VERIFIED / DEPLOYED / HEALTHY / SUCCESSFUL` separate; cite execution result, exact SHA and artifact for each supported claim.
- Update or supersede affected durable documentation; do not create competing 'current state' files. Use [WORK-CLOSURE](07-templates/WORK-CLOSURE.md), including `NO_DOC_DELTA` when warranted.
- No evidence without provenance. No new work solely because the last review found a possible improvement.

## Validation for this repository

Run the existing package/contract validation workflow (not a new parallel gate): `python scripts/validate.py`, `python scripts/audit_package_index.py` and the applicable unit tests. CI's `.github/workflows/validate.yml` is the complete check. A local script not run must not be described as PASS.
