# Data / Persistence Brain

Use with `STAGE-14-DATABASE-PERSISTENCE.md`. Persistence design protects authoritative state, invariants and evolution under concurrency and production change.

## Start with ownership and invariants

Tables are storage structures, not domain boundaries. For each critical fact identify:
- authoritative owner/writer;
- readers;
- lifecycle;
- invariants;
- consistency requirement;
- retention/deletion needs.

Encode invariants in the database when the database can enforce them honestly: uniqueness, foreign keys, not-null/check constraints and transactional boundaries reduce race-prone application assumptions.

## Transaction and isolation

For each critical mutation ask which anomalies matter:
- lost update;
- write skew;
- duplicate insert;
- non-repeatable read;
- phantom;
- inconsistent multi-row transition.

Choose constraints, locking, optimistic versioning or higher isolation based on the invariant and workload. Do not rely on ORM defaults as a concurrency model.

Keep transactions bounded. External network calls inside a transaction extend lock time and still do not make the external system atomic with the database.

## Schema design

Normalize around data meaning and update consistency first, then denormalize where measured access paths justify it. Record the synchronization/invalidation cost introduced by duplicated data.

Indexes are workload artifacts. Document the query/order/selectivity they support and watch write/storage cost. Remove speculative indexes that do not serve real access paths.

## Migration rule

Applied migrations are immutable history. Correct them with a new migration.

For breaking changes prefer:
1. **expand** schema/API so old and new versions can coexist;
2. deploy compatible application code;
3. **migrate/backfill** in bounded, resumable batches;
4. switch reads/writes;
5. verify;
6. **contract** obsolete columns/constraints later.

Large backfills need progress, rate limits, pause/resume and failure recovery.

## Data corrections

Production corrections are audited operations, not ad hoc SQL folklore. Define target rows, invariant checks, dry-run/select evidence, transaction/batch plan and post-change verification.

## Retention and deletion

Retention is part of the model. Define whether deletion is hard, soft, anonymization or archival, and what linked/audit data must remain. Privacy requirements may conflict with audit/history needs and require explicit policy.

## Recovery compatibility

A database restore is usable only if schema, application version, configuration and external state remain compatible. Coordinate persistence changes with Stage 21 restore drills.

## Decision outputs

A material persistence decision should capture ownership, schema/invariant design, transaction/isolation semantics, migration path, workload assumptions, recovery implications and test plan. This gives Stage 15 and Stage 19 something concrete to verify rather than rediscovering database behavior during failure.
