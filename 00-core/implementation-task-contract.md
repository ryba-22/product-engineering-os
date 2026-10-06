# Implementation Task Contract v1

**Status:** ACTIVE
**Purpose:** define when a project task is sufficiently explicit to be handed to an executor without forcing that executor to invent product, domain, architecture, or acceptance semantics.

A task is an **execution contract**, not a reminder, title, or feature wish.

The task must make it possible for a competent executor to answer, before changing code:

1. **What problem am I solving?**
2. **Why does it matter?**
3. **What observable outcome is expected?**
4. **Which decisions and constraints are already frozen?**
5. **What is in scope and explicitly out of scope?**
6. **How should I approach the change without inventing missing semantics?**
7. **What can fail, and what behavior is required under failure/retry/recovery?**
8. **How will we prove the task is correct?**
9. **Who decides if ambiguity appears?**
10. **What exact evidence allows the task to be called CLOSED?**

## 1. Task classes

Every material task declares one primary class:

- **DISCOVERY** — resolve an unknown that materially affects a decision.
- **DECISION** — compare/falsify alternatives and freeze a contract.
- **IMPLEMENTATION** — change the system under already-frozen semantics.
- **VERIFICATION** — independently test a claim or guarantee.
- **RELEASE / OPERATIONS** — deploy, migrate, recover, observe, or operate.
- **REMEDIATION** — correct a known defect while preserving or explicitly revising the governing contract.

Do not write an IMPLEMENTATION task when the real work is still DECISION work.

A downstream implementation task may exist before its dependency closes, but it must remain **BLOCKED / NOT READY** and must not invent the missing contract.

## 2. Task lifecycle

Use these states:

```text
DRAFT
  ↓
REFINEMENT
  ↓
DECISION_READY        (for discovery/decision work)
  ↓
DECIDED               (required upstream semantics frozen)
  ↓
READY_FOR_IMPLEMENTATION
  ↓
IMPLEMENTING
  ↓
IMPLEMENTED
  ↓
VERIFIED
  ↓
INTEGRATED / RELEASED / HEALTHY   (when applicable)
  ↓
DOCUMENTATION_CLOSURE
  ↓
CLOSED
```

Not every task traverses every state, but no state may be inferred from a later-sounding label.

Examples:

- a DECISION task can close after its accepted decision/evidence and documentation closure;
- an IMPLEMENTATION task cannot be `READY_FOR_IMPLEMENTATION` while a required business/domain decision is still open;
- green unit tests do not imply `VERIFIED`;
- merged code does not imply `CLOSED`.

## 3. Mandatory task anatomy

For R2–R4 work, every task MUST contain the sections below. R0/R1 may compress them, but the semantics still apply.

### A. Identity

Record:

- task ID and descriptive title;
- task class;
- risk R0–R4;
- state;
- execution owner;
- semantic reviewer where applicable;
- verification owner;
- business/product acceptance owner where applicable;
- dependencies / blocked-by relationships.

### B. Why / problem

State the current undesirable condition, not the proposed implementation.

Include:

- what happens today;
- why that is wrong, costly, risky, or limiting;
- affected actor/workflow/system boundary;
- relevant evidence or current implementation anchors.

Bad:

> Add PaymentComponent.

Good:

> A single bank transfer may contain tuition and a non-tuition amount. Today the whole CUSTOMER_PAYMENT transaction becomes one Payment, which can incorrectly turn the non-tuition remainder into tuition Credit.

### C. Outcome

Describe the observable end state.

Prefer:

> After the change, a 180 PLN bank transaction can be represented as 150 PLN entering the tuition settlement ledger and 30 PLN remaining categorized outside that ledger, while the original bank transaction stays immutable.

Avoid:

> Create table X and component Y.

Implementation details may be constraints or guidance, but they are not the outcome.

### D. Current state and evidence

Give the executor enough verified context to avoid archaeology from zero.

Include the narrowest useful anchors:

- relevant types/tables/commands/routes;
- current invariant/policy;
- existing tests/evidence;
- known historical behavior;
- canonical documents/ADR/UDR;
- current SHA/branch when state drift matters.

Mark statements as FACT / DECISION / HYPOTHESIS / OPEN QUESTION when ambiguity would change implementation.

### E. Frozen contract

List semantics the executor MUST preserve.

Examples:

- invariants;
- policies;
- source-of-truth ownership;
- state transitions;
- authorization boundaries;
- temporal semantics;
- idempotency requirements;
- immutable provenance;
- external-provider semantics;
- compatibility requirements.

If a required semantic rule is not frozen, the task is not implementation-ready.

### F. Scope

Explicitly state:

**IN SCOPE**
- capabilities and affected boundaries.

**OUT OF SCOPE / NON-GOALS**
- tempting adjacent changes;
- future-domain extensions;
- refactors not required for correctness.

A good non-goal prevents accidental redesign.

### G. Expected implementation approach

Give enough guidance that the executor understands the intended architecture and blast-radius strategy, without pretending uncertain design is already decided.

Include when known:

- preferred change boundary;
- expected write/read path;
- migration strategy;
- reuse vs new abstraction;
- expected compatibility layer;
- files/modules likely involved;
- sequencing constraints.

Use these labels:

- **REQUIRED** — chosen by an accepted decision/constraint.
- **PREFERRED** — expected approach; deviation requires explanation.
- **OPTIONAL** — implementation detail owned by executor.
- **FORBIDDEN** — known unsafe/incorrect approach.

If the exact approach is the unresolved question, create/finish a DECISION task first.

### H. Failure, retry, recovery, and concurrency contract

For any consequential mutation or external side effect, specify applicable scenarios:

- invalid input;
- partial failure;
- duplicate/replay;
- retry after ambiguous outcome;
- concurrent execution;
- stale data/version conflict;
- dependency/provider outage;
- crash after persistence but before response;
- correction/reversal;
- rollback/backfill/migration recovery.

If a scenario is irrelevant, say why. Do not leave consequential failure behavior implicit.

### I. Examples and adversarial scenarios

Material business behavior requires concrete examples/counterexamples.

Use stable IDs when useful.

At minimum include:

- happy path;
- boundary case;
- conflict/ambiguity;
- failure/retry;
- negative authorization/privacy case when relevant;
- migration/backward-compatibility case when relevant.

Expected results must come from accepted rules/evidence. If an expected result is unresolved, mark it OPEN and block implementation rather than inventing an oracle.

### J. Acceptance criteria

Acceptance criteria must be **observable and falsifiable**.

Each criterion should answer:

> What must be demonstrably true for this task to be accepted?

Prefer guarantees:

- no duplicate Payment is created when the same command is replayed;
- a PARENT cannot read a different FinanceAccount via direct URL/query manipulation;
- the source bank amount equals the sum of persisted interpreted parts;
- a provider timeout with unknown outcome does not trigger an unconditional resend.

Avoid:

- “works correctly”;
- “handle edge cases”;
- “UI looks good”;
- “tests added”.

Tests are evidence for an acceptance criterion, not usually the criterion itself.

### K. Verification plan

Define the **lowest trustworthy verification layer** and any higher layer required by risk.

Specify:

- unit/domain contract tests;
- persistence/PostgreSQL integration;
- concurrency/replay tests;
- HTTP/query boundary tests;
- browser/runtime tests;
- migration/backfill evidence;
- provider sandbox/real-provider evidence;
- performance/query-plan evidence;
- security/privacy negative tests;
- manual evidence only where automation is insufficient.

Name concrete commands or suites when already known.

### L. Closure contract

State exactly what must exist before `CLOSED`.

A material task normally requires:

1. intended implementation/decision artifact exists;
2. acceptance criteria have evidence;
3. required independent review/verification passed;
4. no hidden unresolved blocker remains;
5. canonical branch/SHA/artifact identity is recorded;
6. follow-up work is explicitly separated instead of silently omitted;
7. current-state/roadmap/decision/evidence/runbook documentation is updated or `NO_DOC_DELTA` is justified;
8. Documentation Closure Gate = PASS.

If production health is part of the declared task outcome, closure additionally requires production evidence. Otherwise report the strongest achieved state instead of overstating closure.

## 4. READY_FOR_IMPLEMENTATION gate

An IMPLEMENTATION task is READY only when all hard gates are true.

### Hard gates

- **R1 Why:** problem and intended outcome are unambiguous.
- **R2 Authority:** business/domain/architecture decisions needed for implementation are frozen and linked.
- **R3 Scope:** in-scope and non-goals are explicit.
- **R4 Dependencies:** blocking tasks/decisions are CLOSED or explicitly satisfied by current evidence.
- **R5 Invariants:** material invariants/policies/ownership boundaries are stated.
- **R6 Oracle:** acceptance criteria and material scenario outcomes are known.
- **R7 Failure contract:** consequential failure/retry/recovery behavior is explicit.
- **R8 Verification:** evidence plan is capable of proving the claim.
- **R9 Ownership:** executor, reviewer/verifier, and decision escalation path are named.
- **R10 Closure:** the exact conditions for CLOSED are stated.

If any hard gate is false, state:

`NOT_READY_FOR_IMPLEMENTATION: <missing decision/evidence>`

Do not compensate for a missing hard gate with a high numeric score.

## 5. Task quality heuristic — 3C + 7G

Use this quick review before handoff.

### 3C — context

- **Cause** — do we know why the task exists?
- **Contract** — do we know the rules it must preserve/change?
- **Consequence** — do we know what observable outcome proves value/correctness?

### 7G — execution guarantees

- **Grounding** — current-state evidence is linked.
- **Guardrails** — scope/non-goals and forbidden shortcuts are explicit.
- **Graph** — dependencies and upstream/downstream relationships are clear.
- **Graceful failure** — retry/recovery/concurrency/partial failure are addressed.
- **Golden examples** — happy/adversarial scenarios define behavior.
- **Gate evidence** — verification is specified before implementation.
- **Good closure** — acceptance + documentation closure define DONE.

A task failing any 3C item is not ready for handoff.
A material R3/R4 task should satisfy all 7G items.

## 6. Executor start protocol

Before changing code, the execution owner must:

1. recover canonical repo/branch/SHA and inspect working-tree drift;
2. read the task contract and linked decisions/evidence;
3. verify blocking dependencies are actually satisfied;
4. inspect the current implementation at the named anchors;
5. identify any contradiction between task and code/reality;
6. stop and escalate if implementing would require a new business rule, invariant, policy, ownership decision, or unsafe migration assumption.

The executor owns implementation detail **inside** the frozen contract.
The executor does not silently become product/domain authority because the task was vague.

## 7. Stop-and-escalate triggers

Implementation MUST pause when any of these appears:

- required expected behavior is not defined;
- code contradicts a supposedly frozen invariant;
- migration requires reinterpretation of historical data;
- a new cross-boundary side effect appears;
- an authorization/privacy consequence was not modeled;
- retry/idempotency semantics are unknown for a consequential operation;
- external provider behavior needed for correctness is unverified;
- fulfilling the task requires broadening scope beyond the stated outcome;
- acceptance can only be met by changing the governing business/domain decision.

Escalate to the appropriate decision owner and update the task before continuing.

## 8. Anti-patterns

A task is not implementation-ready when it is primarily:

- a title: “add categories”;
- a solution with no problem: “create PaymentComponent”;
- a wish list with no priority/boundary;
- a copy of chat discussion with no frozen decisions;
- a file-by-file coding recipe that hides unresolved semantics;
- “implement and test” with no acceptance oracle;
- “handle errors” with no failure contract;
- “follow existing behavior” when existing behavior is precisely what is disputed;
- “done when PR merged”;
- a parent task that delegates all semantics to child tasks without a shared contract.

## 9. Relationship to closure

Task readiness and task closure are symmetrical:

```text
GOOD TASK INPUT
= problem + frozen contract + scope + examples + oracle + verification plan

GOOD TASK OUTPUT
= implementation/decision + evidence + integration state + residual risks + synchronized docs
```

The task contract defines what the executor is authorized to change.
Documentation Closure proves what actually changed and what state the project is now in.
