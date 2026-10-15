> Optional operational adapter (2026-10-15). This is an execution/resumption contract for interactive ChatGPT and ChatGPT Work, not a claim that this repository installs an autonomous agent, modifies ChatGPT settings, or schedules future turns. Adopting projects retain ownership of their state, DoD, permissions and source of truth.

# ChatGPT UI — checkpoint execution and recovery loop

## The problem

A user repeatedly says "continue, review, are you done, if not find the next checkpoint." A conversational model can follow the sequence in one response but may stop at a plausible-looking partial completion, repeat an external effect after losing its acknowledgement, confuse a green check with the overall outcome, or lose state when the conversation ends.

**Logical loop != durable execution. Checkpoint verified != objective completed. Implementation != evidence of intended outcome.**

This adapter adds a bounded, resumable decision protocol using existing Product Engineering OS readiness, evidence, risk and Documentation Closure contracts. It does not replace [BRAIN](../BRAIN.md), [RUNBOOK](../RUNBOOK.md), [Implementation Task Contract](../00-core/implementation-task-contract.md), or [Work Closure](../07-templates/WORK-CLOSURE.md).

## Applicability

Use for a long-running, user-authorized task with multiple dependent checkpoints, especially engineering research, implementation, repository reviews and release preparation. Skip for simple answers and atomic edits. A ChatGPT UI turn is a **bounded execution attempt**; ChatGPT Work may sustain a longer attempt, but neither is guaranteed to initiate the next turn after the session ends. To resume later, the operator must invoke it again or provide an actual scheduler/orchestrator with explicit permissions.

Prefer an existing project-specific checkpoint, issue, PR, audit ledger, state file or worktree note. **Do not introduce a second global progress/priority source.** A new per-work-item record is allowed only when no canonical durable artifact exists and must link to the existing backlog.

## Inputs — before starting

1. User outcome, scope, explicit exclusions, risk and authorization boundaries.
2. **Definition of Done (DoD):** finite, observable acceptance criteria for the *whole objective*, not a count of checkpoints. Use a project task contract when one exists; do not invent business outcomes or approvals.
3. Current repository/branch/SHA and timestamp, canonical task/priority documents, open issues/PRs and test/runtime evidence when relevant.
4. Last **verified** checkpoint with evidence; unreviewed prose from earlier sessions is a lead, not a verified state.
5. Available tools and their actual authority, including data/provider restrictions and any explicit STOP or approval gates.

If the DoD cannot yet be derived without inventing a material decision, execute a **discovery/decision** checkpoint first, not speculative implementation.

## State model

Checkpoint review outcomes:
- `VERIFIED`: evidence supports this checkpoint's exit conditions. It does not imply the global DoD.
- `FAILED`: the review falsified its exit conditions; repair this checkpoint.
- `BLOCKED`: missing authority, external dependency, decision or necessary oracle.
- `UNVERIFIED`: a claim exists but relevant review/evidence was not executed.

Execution-attempt outcomes:
- `RUNNING`: the next checkpoint is currently being worked on.
- `PAUSED`: the attempt stopped due to UI/tool/time/context limits; persisted state permits another turn.
- `BLOCKED`: progress requires an external input or approval; never pretend to have it.
- `DONE`: **all global acceptance criteria** are supported by evidence, applicable closure gate passed and remaining limitations are recorded.

Never infer `DONE` from `VERIFIED`, `MERGED`, `TESTED`, a progress count, or a green CI check. For R2–R4 work observe the existing PEOS Implementation Task readiness and Documentation Closure gates. Do not convert `BLOCKED` into a loop that repeatedly reissues the same unsuccessful action.

## Algorithm — one or many checkpoints per execution attempt

```text
BOOTSTRAP:
  inspect actual project state and canonical sources; reconcile earlier claims
  freeze the objective's DoD and task-specific authorization/STOP
LOOP:
  1 CONTINUE  choose the first justified unverified item on the critical path;
              execute the smallest useful, permitted checkpoint
  2a REVIEW   inspect actual artifacts and errors; execute relevant checks;
              record negative/skipped checks and evidence identity
              if FAILED: repair same checkpoint; review again (bounded retries)
              if BLOCKED: record blocker and stop
  2b EVALUATE compare *whole objective* to its DoD and current evidence;
              test whether new results falsify the plan or require a decision
              if full DoD + closure gate supported: record DONE; stop
  3a NEXT     identify next dependency / acceptance gap; persist the verified
              checkpoint and exact resume instructions; go to 1
              if no meaningful progress or session limit: record PAUSED; stop
  3b DONE     write final supported outcome, provenance and residual risks
```

**Review checklist (risk-proportionate):** Is the proposed artifact actually present? Did the check execute on the expected SHA/environment/inputs? Did the test discriminate wrong behavior? Are domain invariants, privacy, idempotency and regressions preserved? Is the result demonstrable beyond an assistant claim? Are failing and skipped checks recorded? Did the checkpoint reduce the remaining DoD gap?

**Stop rules:** Stop on explicit user STOP, unavailable permission/decision/oracle, irreversible operation without authorization, two unchanged repair attempts, no material progress, or host execution limits. A stop due to limits is `PAUSED`, never `DONE`. Don't create endless "NEXT" checkpoints solely to keep the loop alive.

## Durable checkpoint contract

Use the existing project location. For new records start from [CHATGPT-CHECKPOINT](../07-templates/CHATGPT-CHECKPOINT.md). Include:

- work-item and objective/DoD reference; checkpoint ID, attempt and predecessor;
- canonical repository, exact branch/SHA/source snapshot and evidence timestamp;
- what changed and any side effect, including command/provider IDs;
- review verdict and actual checks (PASS/FAIL/NOT_RUN), independent reviewer *only if actually independent*;
- global DoD verdict per criterion, remaining gaps, blockers and retry safety;
- next checkpoint with dependencies, or explicit DONE/PAUSED/BLOCKED and exact resume step.

Save the record in a durable repo artifact/issue/PR **before** treating the checkpoint as recoverable. Chat text alone is not the durable checkpoint. Never store credentials, personal data or private runtime tokens.

## Retry and replay safety

On resume read the canonical target **again**, including remote side effects, not just the checkpoint file. A crash can occur after a write but before its response. In that case a missing success message does **not** justify repeating a payment, message, migration, deployment or GitHub write. Correlate using operation ID, idempotency key or recorded target SHA; investigate unknown outcomes; fail closed where safe replay cannot be established. Separate approval to plan from approval to execute consequential mutations.

Concurrent edits require compare-and-swap/version preconditions or a human conflict-resolution step. Never overwrite a newer checkpoint or successful outcome with a stale attempt.

## ChatGPT UI invocation (copy into the task conversation)

> Continue the current task using the repository's ChatGPT checkpoint loop and its existing AGENTS/RUNBOOK/DoD. First verify the real state and the last accepted checkpoint. Then repeatedly CONTINUE -> REVIEW -> EVALUATE -> NEXT until the **whole objective** is DONE, a real blocker is found, or this execution attempt reaches its limit. Repair failed checkpoints before progressing. Persist each verified checkpoint at the project's canonical location. Do not request permission merely to continue; do require authorization for consequential actions. Distinguish VERIFIED checkpoint, DONE objective, BLOCKED and PAUSED. On PAUSED, provide the exact work-item, SHA, evidence and next action to resume. Never claim the UI will automatically start a future session.

In ChatGPT Work, select Work mode in the interface and submit the invocation with access to the relevant repository/apps. That mode selection and connector authorization are actions in the product UI; this repository cannot set them by commit.

## Acceptance / falsification scenarios

1. Three locally green checkpoints but missing production acceptance -> global `PAUSED` or `BLOCKED`, **not DONE**.
2. Review detects a regression -> `FAILED` and bounded repair of the same checkpoint, **not NEXT**.
3. Tool returned no acknowledgement after an external mutation -> reconcile provider/target state, **no blind retry**.
4. A stale checkpoint disagrees with the canonical task/commit -> use current evidence, record conflict, **never overwrite silently**.
5. All agreed acceptance criteria plus applicable closure gates have evidence -> `DONE` with links and residual risk; don't invent more tasks.

## Evaluation of this adapter

Use it on one real, non-destructive project work item. Measure: false DONE count, duplicate side effects, manual repeated-context effort, actual time to resume, and whether every accepted checkpoint has verifiable evidence. Compare with unstructured "continue" prompts. Structural correctness of this document **does not** prove behavioral success in ChatGPT Work.
