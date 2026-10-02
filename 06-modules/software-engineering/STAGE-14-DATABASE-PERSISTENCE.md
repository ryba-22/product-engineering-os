# Stage 14 — Database / persistence

**Module:** software-engineering  
**Gate:** G6  
**Evidence anchors:** EVD-DATA-001, EVD-DATA-002  
**Primary artifact:** `07-templates/DATA-CHANGE-PLAN.md`

## Purpose
Persist authoritative state so domain invariants, concurrency guarantees, migrations and recovery behavior remain explicit. Tables serve the model; they do not define domain boundaries by themselves.

## Required inputs
Domain ownership and invariants, command transaction boundaries, expected read/write workload, retention/privacy requirements, migration constraints, legacy compatibility and recovery objectives.

## Questions the Brain must answer
1. Which data is authoritative and who owns mutation?
2. Which invariants belong in schema constraints as well as application logic?
3. What isolation/concurrency anomalies matter?
4. What indexes are required by measured or expected access paths?
5. How will schema changes remain compatible during rollout?
6. How will backfills be bounded and observable?
7. What rollback/forward-fix path exists if migration behavior fails?
8. What data lifecycle, retention and deletion rules apply?

## Workflow
1. **Map data to ownership.** Identify authoritative writer and readers for each business fact.
2. **Encode durable invariants.** Use constraints/keys where the database can honestly enforce them.
3. **Choose transaction/isolation behavior.** Analyze races around critical mutations rather than assuming default isolation is enough.
4. **Design access paths.** Index from real query/workload needs; estimate cardinality and growth.
5. **Plan migration compatibility.** Prefer expand → migrate/backfill → switch reads/writes → contract for breaking changes.
6. **Make backfills resumable.** Batch, checkpoint, rate-limit and record progress for large changes.
7. **Protect deployments.** Applied migrations are immutable; corrections are new migrations.
8. **Plan failure handling.** State whether rollback is safe or forward-fix is required.
9. **Validate production-like scale.** Test locking/runtime impact for material migrations.
10. **Link backup/recovery.** Schema and application versions must remain restorable together.

## Decision rules
- Application “check then insert” cannot replace a database uniqueness constraint for a critical uniqueness invariant.
- Denormalization is justified by workload and consistency trade-offs, not by fear of joins.
- A nullable column added for rollout compatibility still needs a plan for final invariant enforcement.
- Long-running migrations and backfills are operational changes and need telemetry.
- Deleting a migration already applied to an environment destroys provenance.
- Shared physical storage does not grant every module write authority.

## Evidence standard
Critical persistence choices should cite invariants, concurrency analysis, query/workload evidence and migration/recovery constraints. Performance claims need plans or measurements appropriate to expected scale.

## Canonical outputs
Persistence contract; schema/invariants; indexing rationale; transaction/isolation policy; migration plan; backfill plan; retention rules; data tests; recovery compatibility notes.

## Failure modes
Table-driven domain design; missing constraints; race-prone check-then-write; destructive migration in one step; unbounded backfill; speculative indexes; ORM defaults treated as concurrency design; rollback promised where data transformation is irreversible.

## Exit conditions
Persistence passes G6 when authoritative ownership and invariants are enforceable, critical races are addressed, schema evolution has a compatible operational plan, and recovery implications are known.

## Handoff
Stage 15 tests invariants/migrations. Stage 17 validates performance where material. Stage 19 executes migration/rollout. Stage 21 validates restore compatibility.
