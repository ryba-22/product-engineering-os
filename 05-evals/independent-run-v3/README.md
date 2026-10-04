# Independent Eval Run v3 — unseen distribution

`INDEP-RUN-2026-10-05-03` tests Product Engineering OS on 12 new, multi-axis holdout cases rather than replaying the frozen v1/v2 stage scenarios.

The cases deliberately combine concerns that were previously evaluated mostly in isolation: money + unknown external side effects + retry, UI selection + pagination + concurrency, semantic migration + mixed versions, temporal data repair + ambiguity, AI capability + PII + credentials, aggregate product success + segment harm, and similar combinations.

The executor was Anthropic Claude Opus 5.5 through Claude Code CLI in three fresh batches. Its runtime contained the PEOS files and `executor-input.json`, but not the judge rubric, judge prompts/results or expected answers. The judge ran afterwards through GitHub Copilot CLI using model routing `auto`; the CLI silent mode did not expose the concrete selected model, so the evidence records that limitation rather than inventing a model identity.

Result: **12/12 PASS, 0 hard failures, average 9.0/10**. PASS required score >= 8 and no hard failure.

This is evidence of generalization beyond the frozen v1/v2 scenarios, not proof of universal engineering competence. The set is still authored and bounded, and should be replaced or supplemented periodically with new holdouts after material runtime changes.

## Evidence inventory and rerun policy

`executor-input.json` is the blinded case set. `judge-rubric.json` is the frozen post-execution scoring contract. `executor-raw-*.json` and `judge-raw-*.txt` preserve batch-level raw evidence; the canonical merged results are `executor-results.json` and `judge-results.json`. `run-manifest.json` binds the four critical artifacts with SHA-256 hashes and records the runtime commit and isolation method.

Do not raise the maturity claim by rerunning these same 12 cases. A future v4 should introduce a new holdout distribution after material PEOS changes, ideally with independently authored cases or production-derived mutations. Replaying v3 is useful only for regression, not for new generalization evidence.
