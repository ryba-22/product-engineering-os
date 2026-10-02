# Stage 12 — Frontend implementation

**Module:** software-engineering  
**Gate:** G6  
**Evidence anchors:** EVD-FE-001, EVD-FE-002  
**Primary decision system:** `FRONTEND-ARCHITECTURE.md`

## Purpose
Implement the experience contract with explicit state ownership, predictable data flow and maintainable boundaries. Frontend architecture should preserve domain and interaction semantics rather than recreate them as ad hoc component state.

## Required inputs
UX/interaction/accessibility contracts, design-system primitives, API contracts, permission model, performance expectations, error/recovery behavior and acceptance criteria.

## Questions the Brain must answer
1. What is the source of truth for each piece of state?
2. Which values can be derived instead of stored?
3. What state belongs to URL, server cache, form, component or application scope?
4. Which transitions are user events versus synchronization effects?
5. How are stale, pending, optimistic and failed states represented?
6. Where do feature boundaries align with product/domain ownership?
7. Which rendering or loading strategy fits the task?
8. What can be tested below the browser layer?

## Workflow
1. **Map state before components.** Classify authoritative server state, URL state, local interaction state, form state and derived values.
2. **Define ownership/lifetime.** Keep state as local as possible while preserving a single source of truth.
3. **Model async transitions explicitly.** Pending, error, stale, retry and cancellation are first-class states.
4. **Separate events from effects.** User-triggered logic runs from events/actions; effects synchronize with external systems.
5. **Align feature boundaries.** Group code around coherent capabilities/workflows rather than file type alone.
6. **Implement API contracts.** Keep validation/error semantics consistent with backend authority.
7. **Preserve accessibility.** Use semantic primitives and implement focus/keyboard requirements from Stage 09.
8. **Manage performance deliberately.** Avoid speculative memoization; measure expensive work and network/render bottlenecks.
9. **Test logic at the lowest trustworthy layer.** Use unit/contract/component tests for local guarantees and browser tests for integrated flows.
10. **Review drift.** Compare implementation against UDRs and design-system contracts.

## Decision rules
- Do not duplicate server truth into local state without a clear synchronization reason.
- Derived values should remain derived unless caching has measured value.
- Effects are not a replacement for event handlers or ordinary computation.
- URL-visible filters/search/pagination should usually be URL-addressable when shareability/back-navigation matters.
- Optimistic UI needs reconciliation and failure behavior.
- Global state requires a cross-feature ownership need; convenience is not enough.

## Evidence standard
Implementation choices should point to interaction contracts, state semantics, performance evidence or maintainability constraints. Framework idioms are defaults, not proof that a pattern fits the product.

## Canonical outputs
Feature/state architecture; implemented UI states; typed client/API boundaries; accessibility behavior; frontend tests; performance notes; implementation ADRs where material.

## Failure modes
Duplicated state; effect chains; prop drilling solved with premature global stores; data fetching in arbitrary leaf components; business rules copied into UI; route state that cannot be shared/restored; loading and error behavior invented during coding.

## Exit conditions
G6 frontend scope is satisfied when the implemented flow matches interaction/state contracts, state ownership is explicit, key logic is verified below or at the browser layer as appropriate, and no material UX/accessibility rule is silently dropped.

## Handoff
Stage 15 receives risk/contract tests. Stage 17 receives measurable frontend budgets where relevant. Stages 18–20 receive build/runtime telemetry requirements.
