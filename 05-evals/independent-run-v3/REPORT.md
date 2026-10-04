# Independent Eval v3 Report

## Result

- run: `INDEP-RUN-2026-10-05-03`
- distribution: 12 previously unused multi-axis holdouts
- executor: Anthropic Claude Opus 5.5 / Claude Code CLI
- judge: GitHub Copilot CLI / `auto` model routing (concrete selected model not surfaced)
- PASS: 12/12
- hard failures: 0
- average score: 9.0/10

## What changed versus v2

v2 proved repeatability on the frozen lifecycle suite plus three loop-closure cases. v3 changes the distribution: it evaluates combined failure modes and conflicting signals instead of one stage at a time.

## Covered mutation axes

Financial side-effect uncertainty, retries and callbacks; stale bulk selection and concurrency; semantic migration with mixed versions; segment-concentrated automation risk; DST/time ambiguity in repairs; ambiguous external notification delivery; AI data/capability governance; performance architecture pressure without measurement; low-volume contaminated experimentation; source/context contradiction; build provenance plus migration; and aggregate success masking segment harm.

## Interpretation

The PEOS method generalized across this holdout without a hard failure. The evidence supports a scoped claim: **unseen-distribution-behaviorally-validated-v3 for this 12-case holdout**.

It does not prove production correctness, all future task distributions, or specialist correctness in every domain. Revalidation is required after material changes to routing, control-loop, governance or stage playbooks.

## Evidence controls

The judge criteria were frozen before the executor run, but the executor operated against a temporary PEOS runtime copy from which the entire v3 judge material was excluded. Raw executor responses are retained even where formatting differed between batches. Canonicalization removed only response wrappers/code fences; it did not alter case content.

The judge evaluated the completed executor outputs against per-case criteria and global hard-failure rules. No remediation round was needed. Unlike v2, no PEOS files were changed in response to this run before scoring completed.

## Revalidation rule

This holdout now becomes known test material. It may be replayed as regression evidence, but a future claim of improved generalization requires new cases. New holdouts should change combinations, domains, ambiguity patterns or production-derived failure modes rather than paraphrasing the same scenarios.
