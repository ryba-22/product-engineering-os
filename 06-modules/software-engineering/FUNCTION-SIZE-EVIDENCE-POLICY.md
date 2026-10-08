# Function size as evidence — not a proxy for domain correctness

**Status:** reusable engineering policy (adoption requires an explicit project-level gate).
**Owner modules:** Software Engineering (implementation) + Quality Engineering (verification).
**Applies to:** refactors and review of functions with substantial logic or side effects, especially financial commands, queue handlers and transaction orchestration.

## Contract

A SLOC cap is a _signal of potential excessive responsibility_, not a universal readability metric. Never declare a refactor safe because a function became shorter or because CI became green. A 90-line coordinator can be clearer than fragmented single-line wrappers.

| Function kind                        | Typical design target | Default gate                                                                        |
| ------------------------------------ | --------------------- | ----------------------------------------------------------------------------------- |
| Domain decision / policy / validator | ~30–50 SLOC           | 80 SLOC                                                                             |
| Infrastructure/data adapter          | ~40–60 SLOC           | 80 SLOC                                                                             |
| Transaction/workflow orchestrator    | ~60–80 SLOC           | 80 SLOC                                                                             |
| Experimental proof code              | Context dependent     | Explicit lifecycle and independent review; do not auto-delete if tests depend on it |

**80 SLOC is a proposed project default**, not an OS-wide enforced override of established repositories. For an existing project, retain its current thresholds/baseline while refactoring and change the gate only through an explicit design decision.

## Refactor rather than suppress when

- The function mixes validation, planning, mutation, persistence, audit and recovery.
- A function both discovers resources and locks/mutates them, making ordering non-obvious.
- Critical financial effects depend on implicit optional payloads or control-flow shortcuts.
- The function has independent failure modes and policies whose tests can be separated.

Extract named **domain phases with stable input/output contracts**: e.g. validate reviewed intent → verify source facts and OCC → inspect target Charges → apply atomic delta/audit → check postconditions. Keep one transaction owner and do not move lock acquisition behind Facts load.

Do **not** use forwarding wrappers, remove checks, widen size baselines, delete a tested prototype or silently relax business rules solely to satisfy a numeric target.

## Evidence required for a meaningful refactor

1. Pin the prechange commit, failing threshold and exact function names; identify source-of-truth invariants and error codes.
2. Map which functions own authorization, idempotency, lock order, audit, money conservation, retries and recovery.
3. Compare before/after public API/payload/error contracts, authorization and SQL transaction boundaries.
4. Test deterministic domain invariants, negative cases and persistence. Add native PostgreSQL concurrency/retry tests for multi-connection claims; a PGlite PASS is not PostgreSQL concurrency evidence.
5. Run format, lint, typecheck, size gate and full relevant CI on the **exact refactor commit**. Inspect skipped tests.
6. Require an independent reviewer for consequential behavior; keep incomplete business policy and migration evidence as separate blockers.
7. Record side effects, deployment state, changes to thresholds/exclusions and explicit remaining risks.

### Exception policy (e.g. 82–120 SLOC orchestrator)

Never automatically raise a global cap from 80 to 120. A **narrow per-function exception** can be accepted only when it improves cognitive clarity and all of the following are true:

- The function is a clear coordinator with relatively linear control flow, and meaningful extraction would obscure atomicity or ordering.
- No independent business policy, error handling or side effect is hidden inside a long branch.
- A decision record identifies the precise symbol/path, actual SLOC, why the exception is safer, owner and re-review condition.
- Static policy enforces the exception precisely rather than exempting an entire folder.
- Contract, rollback, retry and authorization tests (where relevant) pass; an independent reviewer signs off.

A 120 SLOC upper band is **exceptional guidance**, not a new global default. Projects may keep a lower bound. Exception evidence must not be inferred from CI alone.

## Example: CRD Finance CP4.2-S

[Issue #195](https://github.com/ryba-22/CRD-Finance/issues/195) exposed seven 80-SLOC violations spanning atomic correction, matching guards, deterministic locking, transaction coordinator and a tested design prototype. The preferred remedy is responsibility-based decomposition with the existing **80 SLOC** cap unchanged, while proving old/new money effects, no implicit allocation, Credit/LegalEntity policy, fail-closed `targets=[]`, audit/command replay and PostgreSQL concurrency in separate evidence layers.

**Scope warning:** visual mockups, a passing size gate or test counts do not authorize a production financial operation or deployment.
