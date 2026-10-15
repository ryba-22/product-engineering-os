# ChatGPT execution checkpoint — per-work-item template

> Use only where an existing project issue, PR, audit ledger or status record does not already carry this information. Link the canonical source; do not create a parallel task queue. This is evidence to review, not a self-certifying approval.

## Identity and source snapshot

- Work-item / canonical task URL:
- Global outcome / DoD contract URL:
- Risk and authorized scope / STOP:
- Checkpoint ID / attempt / previous verified checkpoint:
- Repository, branch, inspected SHA, checked at (timezone):
- Executor / actual reviewer(s):
- Environment, source facts or artifact digest:

## The checkpoint

- Why this checkpoint is necessary for the global objective:
- Intended smallest verifiable result:
- Work performed / changed paths:
- Side effects / external operation IDs / idempotency evidence:
- Failed or ambiguous operations and reconciliation:

## Review (checkpoint-specific)

- Exit conditions:
- Executed checks + command, input SHA/environment, result, evidence:
- Skipped checks (NOT_RUN) and why:
- Contradicting evidence / possible regression:
- Reviewer provenance (self-review is not independent review):
- Verdict: VERIFIED / FAILED / BLOCKED / UNVERIFIED
- Reason:

## Evaluate the whole objective

| DoD criterion ID | Evidence / missing evidence | Met? |
| --- | --- | --- |
| AC-01 | | YES / NO / UNVERIFIED |

- DoD met in full? YES / NO
- Applicable Documentation Closure Gate: PASS / FAIL / NOT_YET_APPLICABLE
- Remaining risks / decisions / blockers:
- Retry safety: safe to replay / reconcile first / forbidden pending approval

## Decision and restart contract

- Execution status: RUNNING / PAUSED / BLOCKED / DONE
- If not DONE, next checkpoint + why it is critical path:
- Dependency or missing authorization:
- Exact next source/ref/SHA to refresh (do not assume unchanged):
- Exact resume command:
- If DONE, verified acceptance evidence and closure location:

**Invariant:** `DONE` requires the entire agreed DoD and applicable closure evidence. `VERIFIED` here describes only this checkpoint. `PAUSED` must be restartable; `BLOCKED` must name the dependency.
