> Optional operational adapter. This is a 2026-10-12 engineering workflow experiment, **not an addition to PEOS's frozen pre-2026-09-30 research corpus**. Adopt only when it reduces the risk or cost of a specific change. The project repository remains the source of truth for its state, release policy and domain rules.

# Forensic change loop — from a real defect to a trustworthy release claim

## Problem and scope

AI-assisted teams can produce a fix, tests, a clean diff and a green CI run while still being wrong about what the real system does, what inputs the build consumed, or whether the installed release contains the validated change. This adapter is intended for reproducible defects, legacy host integrations, analyzers, financial calculations, migrations and high-impact releases. It is **not** required for copy changes, cosmetic adjustments or every low-risk PR.

It complements, not replaces, PEOS [risk routing](../00-core/adaptive-workflow-router.md), [test strategy](../06-modules/quality-engineering/STAGE-15-TESTING.md), [delivery assurance](../06-modules/delivery-production/delivery-assurance/) and [work closure](../07-templates/WORK-CLOSURE.md). The one-page case record is [DEFECT-REGRESSION-EVIDENCE](../07-templates/DEFECT-REGRESSION-EVIDENCE.md).

## The loop

1. **Bound the claim.** State the user-visible failure and the invariant that must hold, the affected artifact/environment, who owns the behavior, business consequence, and the smallest successful outcome. Identify facts, hypotheses and unknowns separately.
2. **Reproduce before fixing when feasible.** Capture an executable reproducer with exact inputs, versions, source identity and observed output. A failed reproduction is not proof the report was invalid. State when the real host/environment is unavailable rather than inventing a result.
3. **Name the oracle and its limits.** Prefer an authoritative observable behavior: a real Office host/compiler for VBA parity, the domain-approved billing agreement and charge rules for Finance, a protocol reference for interoperability. A legacy system is a useful comparison target, not automatically the correct business rule. If two oracles conflict, hold the decision and escalate ownership.
4. **Prove the probe can detect the defect.** Run the regression check on the defective baseline and show **RED for the intended reason**. A test that passes unchanged on the broken implementation is not evidence. If red cannot be reproduced, mark the limitation explicitly and do not claim discriminating coverage.
5. **Make the narrowest justified change.** Preserve the project's boundaries, safety rules and update locality. No speculative refactoring, new global gate or new documentation framework is implied by finding a bug.
6. **Execute at the lowest trustworthy layer, then at the real boundary when required.** Require the check to turn GREEN against the fix, and run existing relevant regressions. For host behavior, separately observe the real UI/runtime; unit tests and CI alone do not demonstrate host parity. Use a disposable or synthetic fixture with process ownership, timeout, cleanup and a rollback procedure for stateful tools.
7. **Verify what the artifact actually consumed.** Record source SHA, dependency/companion SHA, build command, produced artifact digest and provenance. For cross-repository builds, verify actual compiler/bundler inputs, not just the declared pin or a guard returning PASS. For deployment, observe the promoted digest and runtime separately. Do not rebuild silently per environment.
8. **Close only the supported claim.** Link defect -> reproducer -> oracle -> RED -> code change -> GREEN -> actual-host observation (where necessary) -> artifact -> outcome. Preserve failed and skipped checks, uncertainty, remaining risk and the next action. Mark docs and decisions superseded instead of maintaining contradictory current-state snapshots.

## When to decline

- **Unknown oracle:** ask the rule owner; do not encode a guess as expected behavior.
- **Non-reproduced defect:** preserve an investigative finding, not a completed regression proof.
- **Protected/signed or production data:** no destructive mutation without the repository's authorization, backup/rollback and guardrails.
- **CI green but untested host boundary:** report TESTED / HOST UNVERIFIED.
- **Pin verified but build inputs unobserved:** report PROVENANCE PARTIAL; do not claim exact-input verification.
- **Production health unknown:** report DEPLOYED / HEALTH UNKNOWN, never SUCCESSFUL.

## Representative applications

| Local situation | Oracle | Discriminating evidence |
| --- | --- | --- |
| CRD Finance charge discrepancy | Agreed billing policy/version and reconciled domain examples, with Legacy as comparison evidence | Baseline discrepancy, approved calculation, RED/GREEN shadow case, policy/price provenance and accountable decision |
| Repository Intelligence Toolkit quality-gate defect | Independently constructed adversarial fixture and observed tool output | A deliberately invalid evidence sample rejected before and after the code change, plus a formerly accepted defect case that turns RED -> GREEN |
| Excel/VBA tooling | Live Excel/VBE compiler, document semantics and UI observation | Real workbook fixture, failing pre-fix result, code-level check, live host confirmation and intact workbook/signature policy |

## Adoption rule

Keep the local `AGENTS.md` and existing CI/test commands authoritative. For an R2–R4 defect, copy the template into the project's normal evidence location and add only the checks needed to demonstrate the invariant. Existing tests/gates should be extended, not duplicated. No new approval requirement is implied. Never impose a human GitHub reviewer solely because an external project does; review independence and approval are separate from artifact integrity and executable evidence.

## Source and limitations

Process ideas were adapted after inspecting public repositories and working agreements of WilliamSmithEdward: [xlide_vbide lessons](https://github.com/WilliamSmithEdward/xlide_vbide/blob/main/docs/lessons.md), [decisions](https://github.com/WilliamSmithEdward/xlide_vbide/blob/main/docs/decisions.md), [verify.ps1](https://github.com/WilliamSmithEdward/xlide_vbide/blob/main/tools/verify.ps1), [xlide_vscode CI](https://github.com/WilliamSmithEdward/xlide_vscode/blob/main/.github/workflows/ci.yml), and [xlide_mcp](https://github.com/WilliamSmithEdward/xlide_mcp). This adapter paraphrases observable methods; it does not claim that the author's private workflow, tests or code quality were independently audited. License and reuse of code require separate review; no third-party code was copied here.
