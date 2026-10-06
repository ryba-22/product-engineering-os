# Implementation Task

## Identity

- **ID:**
- **Title:**
- **Class:** DISCOVERY / DECISION / IMPLEMENTATION / VERIFICATION / RELEASE / REMEDIATION
- **Risk:** R0 / R1 / R2 / R3 / R4
- **State:** DRAFT / REFINEMENT / DECISION_READY / DECIDED / READY_FOR_IMPLEMENTATION / IMPLEMENTING / IMPLEMENTED / VERIFIED / CLOSED
- **Execution owner:**
- **Semantic reviewer:**
- **Verification owner:**
- **Business/product acceptance:**
- **Blocked by:**

## Why / problem

### Current undesirable behavior

### Why it matters

### Evidence / current-state anchors

- FACT:
- DECISION:
- HYPOTHESIS:
- OPEN QUESTION:

## Intended outcome

After this task, the observable system/user/business state is:

## Frozen contract

### Invariants / policies / ownership

### Source of truth

### State/lifecycle rules

### Security/privacy/authorization constraints

### Compatibility/temporal constraints

## Scope

### IN SCOPE

### OUT OF SCOPE / NON-GOALS

## Expected implementation approach

- **REQUIRED:**
- **PREFERRED:**
- **OPTIONAL:**
- **FORBIDDEN:**

### Expected change surfaces

### Migration/backfill/compatibility strategy

## Failure / retry / recovery contract

| Scenario | Required behavior | Evidence |
| --- | --- | --- |
| Invalid input | | |
| Duplicate/replay | | |
| Partial failure | | |
| Concurrent/stale write | | |
| Crash after durable write | | |
| Dependency/provider outage | | |
| Correction/reversal | | |
| Migration rollback/backfill | | |

## Examples / adversarial scenarios

### EX-01 — happy path

**Given**
**When**
**Then**

### EX-02 — boundary/conflict

**Given**
**When**
**Then**

### EX-03 — failure/retry

**Given**
**When**
**Then**

## Acceptance criteria

- [ ] AC-01 —
- [ ] AC-02 —
- [ ] AC-03 —

## Verification plan

- **Unit/domain:**
- **Persistence/PostgreSQL:**
- **HTTP/query boundary:**
- **Browser/runtime:**
- **Security/privacy negative cases:**
- **Concurrency/replay:**
- **Migration/backfill:**
- **Provider/external:**
- **Performance/query plan:**
- **Manual evidence:**

## READY_FOR_IMPLEMENTATION

- [ ] R1 problem + outcome unambiguous
- [ ] R2 required decisions frozen/linked
- [ ] R3 scope + non-goals explicit
- [ ] R4 blocking dependencies satisfied
- [ ] R5 invariants/policies/ownership stated
- [ ] R6 acceptance oracle known
- [ ] R7 failure/retry/recovery explicit
- [ ] R8 verification can prove the claim
- [ ] R9 owners/escalation path named
- [ ] R10 closure conditions explicit

If any box is false:

`NOT_READY_FOR_IMPLEMENTATION: <reason>`

## Stop-and-escalate triggers specific to this task

-

## Closure contract

The task can be called `CLOSED` only when:

- [ ] implementation/decision artifact exists at canonical SHA/location
- [ ] all acceptance criteria have evidence
- [ ] required independent verification/review passed
- [ ] no hidden blocker remains
- [ ] follow-ups are recorded separately
- [ ] current-state/roadmap/decision/evidence/runbook docs updated or `NO_DOC_DELTA`
- [ ] Documentation Closure Gate = PASS

### Required closure evidence

- Canonical SHA/artifact:
- Test/runtime evidence:
- Documentation to update:
- Residual risks:
- Next owner/action:
