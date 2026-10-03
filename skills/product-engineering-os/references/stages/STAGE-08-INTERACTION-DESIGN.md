# Stage 08 — Interaction design

**Module:** experience  
**Gate:** G5  
**Evidence anchors:** EVD-UX-003, EVD-UX-004  
**Primary outputs:** interaction contracts, state transitions, UDRs

## Purpose
Define how each consequential interaction behaves over time: trigger, feedback, validation, pending state, success, failure, cancellation, conflict and recovery. Components are implementation adapters to behavior, not the source of the behavior.

## Required inputs
UX architecture, scenarios, domain/state transitions, permissions, accessibility requirements, latency/dependency expectations and existing interaction conventions.

## Questions the Brain must answer
1. What user intent starts the interaction?
2. What state can change and who owns it?
3. What immediate feedback is required?
4. What can fail locally, remotely or concurrently?
5. Can the action be cancelled, retried or undone?
6. What happens when data becomes stale during the interaction?
7. Which validation belongs before submit and which only the server can decide?
8. What focus/keyboard behavior accompanies each state change?

## Workflow
1. **Write the interaction as a state machine.** Name idle, editing, validating, submitting, success, failure, stale/conflict and recovery states as applicable.
2. **Separate local intent from authoritative result.** Optimistic UI is allowed only when reconciliation is defined.
3. **Define validation layers.** Client feedback improves speed; authoritative business/security validation remains server-side.
4. **Specify latency behavior.** Decide when to show inline progress, skeleton, pending marker, disabled action or background completion.
5. **Specify error semantics.** Tell the user what failed, what remains saved, what they can do next and whether retry is safe.
6. **Design concurrency/conflict handling.** Choose refresh, merge, reject or explicit overwrite based on data risk.
7. **Define cancellation/undo.** Prefer reversible operations where practical; do not fake undo after irreversible external side effects.
8. **Define keyboard/focus behavior with the interaction.**
9. **Choose components only after semantics.** Verify that library primitives support required states and accessibility.
10. **Test realistic transitions.** Include double-submit, slow dependency, expired permission and stale entity where relevant.

## Decision rules
- Spinner-only feedback is insufficient when users need to know which operation is pending.
- Disabling a submit button is not an idempotency guarantee.
- Toasts are poor containers for errors that require corrective action or must remain discoverable.
- A confirmation dialog is justified by consequence, not by developer anxiety.
- Optimistic updates need rollback/reconciliation and a clear source of truth.
- Library component behavior may be overridden or replaced when it conflicts with the required semantic contract.

## Evidence standard
Interaction choices should trace to task risk, domain semantics, known latency/concurrency behavior, accessibility requirements or validated conventions. Novel interactions need stronger usability evidence than familiar patterns.

## Canonical outputs
Interaction/state contract; validation/error model; pending/retry/cancel/undo behavior; conflict strategy; focus/keyboard expectations; component semantics; UDR for material choices.

## Failure modes
Component-first design; success-only prototypes; global toast for every failure; silent retry loops; hidden stale data; accidental double-submit; irreversible actions disguised as reversible; focus loss after async updates.

## Exit conditions
A workflow is interaction-complete when a developer and tester can enumerate its states and transitions, users have a recovery path for material failures, and accessibility behavior is not left unspecified.

## Handoff
Stage 09 validates accessibility mechanics. Stage 12 implements the state contract. Stage 15 derives interaction tests from the same transitions.
