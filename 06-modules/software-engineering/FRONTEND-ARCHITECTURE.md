# Frontend Architecture

Use with `STAGE-12-FRONTEND-IMPLEMENTATION.md`. The frontend should preserve product/domain semantics while keeping state ownership and asynchronous behavior understandable.

## Decision hierarchy

1. User workflow and state contract from Experience.
2. Authoritative source of truth for each piece of data.
3. Ownership and lifetime: URL / server cache / form / local component / application scope.
4. Feature/module boundaries.
5. Rendering/data-fetch strategy.
6. Component composition and design-system adapters.
7. Performance optimizations based on evidence.

Framework primitives come after these decisions.

## State taxonomy

### Server state
Authoritative remote data with freshness, loading, error, retry and invalidation semantics. Use a consistent cache/query layer when complexity warrants it.

### URL state
Search, filters, sort, page, selected object or view mode belong in the URL when navigation, shareability, refresh or back/forward behavior should preserve them.

### Form state
Transient edits, validation and dirty/submitting status. Keep draft semantics explicit: unsaved local draft is not server truth.

### Local UI state
Open/closed, focus, temporary selection, disclosure and interaction state. Keep local unless another feature genuinely owns/needs it.

### Derived state
Compute from authoritative inputs when cheap and deterministic. Avoid storing duplicate values that can drift.

## Async state

Every remote interaction should have defined:
- initial/loading behavior;
- refresh/stale behavior;
- submitting/pending behavior;
- retry and cancellation;
- empty state;
- error and recovery;
- conflict/version mismatch;
- optimistic update rollback/reconciliation when used.

Do not hide material pending state behind a generic spinner or toast.

## Effects

Effects synchronize React/UI state with external systems such as network subscriptions, timers or imperative APIs. They should not be the default tool for:
- deriving render values;
- responding to button clicks;
- copying props into state;
- chaining ordinary business logic.

Prefer explicit events/actions and derived computation.

## Feature boundaries

Organize around coherent product capabilities/workflows. Shared UI primitives belong in the design system; feature-specific business components stay near the feature. Avoid a global “components/utils/hooks” dump that erases ownership.

## Error boundaries and recovery

Distinguish:
- expected domain/validation errors;
- authorization/not-found;
- transient dependency/network failures;
- rendering/programming faults.

Each category has a different recovery and telemetry path.

## Performance

Measure before broad memoization. Common risks include over-fetching, duplicate requests, huge client bundles, rendering large tables without virtualization when needed, unnecessary global state subscriptions and blocking work on the main thread.

## Verification

Use:
- unit/property tests for pure state/business helpers;
- component tests for local interaction/semantics;
- contract tests around API adapters;
- browser tests for integrated critical journeys;
- manual accessibility validation for critical/custom interactions.

The goal is predictable behavior under real state transitions, not merely “components render.”
