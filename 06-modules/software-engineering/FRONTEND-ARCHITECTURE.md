# Frontend Architecture

## Decision hierarchy
1. User workflow/state contract from Experience.
2. Source of truth for each piece of state.
3. Ownership and lifetime: component/local, feature, URL/navigation, server/cache, persistent client storage.
4. Async/error/recovery behavior.
5. Component boundaries and dependency direction.
6. Framework/library adapter last.

## Rules
- Avoid duplicated or contradictory state; derive values when possible.
- URL state is preferred for shareable/navigable filters/selections where browser semantics matter.
- Server state is not copied into client state without a reason; define cache invalidation/refresh semantics.
- Effects synchronize with external systems; they are not a generic replacement for derived data or event handlers.
- Shared UI standardizes behavior and semantics, not domain meaning.
- Optimistic UI requires a rollback/reconciliation contract and must be proportional to consequence.

## Required contract for consequential workflows
State owner, initial/loading/empty/error/stale/pending/success/conflict states, mutation idempotency assumptions, retry behavior, navigation semantics, and telemetry hooks.
