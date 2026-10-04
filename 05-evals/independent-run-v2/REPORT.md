# Independent behavioral validation v2 — Product Engineering OS v1.2

Run: INDEP-RUN-2026-10-04-02
Final runtime commit: bb22c203248040ee0b4c5c799f87846dd8d4762b
Suite: 28 frozen scenarios = 25 lifecycle regression cases + 3 v1.2 loop-closure cases
Executor: Anthropic Claude Opus 5.5 via Claude Code CLI
Judge: OpenAI GPT-6 Luna via GitHub Copilot CLI
Final: 28/28 PASS, 0 hard failures, average 9.57/10

## Why this run exists

Product Engineering OS v1.2 changed the runtime contract after the v1 independent benchmark. The new contract made three behaviors first-class: pre-implementation ATDD / Example Mapping, AI data/model/tool capability governance, and the Production Learning Loop that compares expected versus observed production behavior and propagates learning back into model/tests/evals/knowledge. Reusing the old v1 result would therefore have overstated evidence.

The v2 executor received blinded scenarios plus the Product Engineering OS runtime/playbooks/templates. It did not receive must-do criteria, must-not-do criteria, expected answers, scores or prior judge results. The judge received the frozen criteria only after executor outputs existed. The executor and judge used distinct model providers and execution systems.

## Round 1 — failure preserved, not hidden

Round 1 produced 26/28 PASS with hard failures on ADV-S04 and ADV-S18.

ADV-S04 exposed a requirements-modeling defect: a plausible retry policy and telephone-number normalization behavior had been promoted from unresolved assumptions into decision-ready examples. The remediation strengthened Stage 04 and the ATDD / Example Mapping playbook: a concrete example is not evidence for missing policy; unresolved normalization/equivalence/retry semantics remain OPEN/HYPOTHESIS and cannot be baselined at G3.

ADV-S18 exposed a lifecycle-state evidence defect: the executor upgraded deployed to staging into staging healthy without supplied runtime health evidence. Stage 18 now states explicitly that deployed to staging is not the same as staging healthy; health requires its own smoke/SLO/telemetry evidence.

The frozen scenarios and judge criteria were not changed.

## Round 2 — targeted frozen regression

After remediation, fresh blinded executor and judge sessions reran only the same two failed cases:

- ADV-S04: 9/10, PASS, no hard failure.
- ADV-S18: 9/10, PASS, no hard failure.

The canonical final result therefore contains the original round-1 results for the 26 cases that already passed and the round-2 results for the two remediated cases.

## v1.2 loop-closure cases

The three new v1.2 behaviors all pass:

- V2-LC-ATDD: 9/10.
- V2-LC-AIGOV: 10/10.
- V2-LC-PROD: 10/10.

Passing criticism is not discarded. Judge-noted omissions remain in weakness-backlog.json; a pass is not treated as a claim of perfection.

## Claim and boundary

This run supports the scoped status independently-behaviorally-validated-v2 for this frozen Product Engineering OS v1.2 runtime on these 28 scenarios. It does not prove universal product-engineering competence, correctness on unseen distributions, or production correctness of downstream products.

The evidence chain preserves the failed first round, the exact remediation, the targeted rerun, executor/judge provenance, frozen input/rubric hashes and final canonical result. The maturity claim is therefore based on executed behavioral evidence rather than file presence or self-assessment.
