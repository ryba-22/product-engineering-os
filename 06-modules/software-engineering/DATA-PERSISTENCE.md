# Data / Persistence Brain

## Start with ownership and invariants
Tables are storage, not domain boundaries. Define which module owns mutation authority, which invariants must hold transactionally, and which projections are read-only or eventually consistent.

## Decision areas
- entity/value representation and normalization;
- identifiers and uniqueness;
- temporal/effective-date modeling;
- money/precision and units;
- transactions and isolation;
- optimistic/pessimistic concurrency;
- constraints as defense in depth;
- indexes from real query patterns;
- audit/history and deletion/retention;
- import/reconciliation semantics;
- migration compatibility and rollout;
- backup/restore and data recovery.

## Migration rule
Treat schema/data migrations as production operations. Do not edit an already-applied migration. Prefer expand/migrate/contract or other compatibility-safe sequencing when code and schema versions may overlap. A rollback plan must account for persisted data, not only application binaries.
