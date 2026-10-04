# Stage 03 — Domain Discovery

**Module:** domain  
**Gate:** G2  
**Evidence anchors:** EVD-DOM-001, EVD-DOM-002  
**Primary decision system:** Domain Brain / Event Storming adapter plus this playbook

## Purpose
Build a shared, evidence-backed model of the business domain before software structure hardens assumptions. The goal is not to produce fashionable DDD diagrams; it is to understand language, events, rules, ownership, time and invariants well enough to expose ambiguity and candidate boundaries.

## Required inputs
Validated product outcomes and scenarios, domain experts or authoritative operational sources, existing process documentation, current system behavior, known data/state transitions and prior domain decisions.

## Questions the Brain must answer
1. What business events actually occur and in what order?
2. Which commands, policies, actors and external systems cause or react to them?
3. Which terms have conflicting meanings across contexts?
4. Which rules must always hold?
5. Which rules depend on time, status, prior events or authority?
6. Who owns each decision and mutation?
7. Where do workarounds reveal missing concepts or incorrect boundaries?
8. Which candidate boundaries reduce language collision and change coupling?

## Workflow
1. **Collect concrete scenarios.** Start from real cases, including exceptions and failed flows.
2. **Build the event timeline.** Capture domain events in business language, not table or screen names.
3. **Add commands and actors.** Identify who intends each change and what authority is required.
4. **Add policies and reactions.** Make automatic rules and downstream consequences explicit.
5. **Mark hotspots.** Record disagreements, missing facts, temporal ambiguity, duplicate concepts and manual workarounds.
6. **Extract invariants.** Phrase them as conditions that must remain true across transitions.
7. **Build the ubiquitous language.** Define terms with examples and counterexamples.
8. **Compare candidate boundaries.** Challenge them using language cohesion, invariant ownership, temporal rules, data ownership, change coupling and operational autonomy.
9. **Separate evidence from hypothesis.** Proposed context boundaries remain hypotheses until challenged by scenarios.
10. **Run a falsification pass.** Name a credible counter-model and at least one scenario, exception or observation that could disprove the leading model or reveal an unknown unknown.
11. **Record open domain questions.** Do not “resolve” uncertainty through implementation convenience.

## Decision rules
- Database tables, menu sections and organizational charts are evidence inputs, not automatic bounded contexts.
- A shared noun with different rules or lifecycle may indicate different concepts despite identical labels.
- An invariant that needs atomic enforcement is a strong boundary signal.
- Frequent coordinated change across proposed boundaries is evidence against premature separation.
- Temporal rules must name the relevant business time and transition; “same day” is insufficient when ordering matters.
- If two domain experts disagree, record the competing models and discriminating scenarios rather than selecting by authority alone.

## Evidence standard
Every material domain rule should point to a scenario, authoritative policy, observed workflow or verified expert decision. Hypotheses must remain labeled. Important temporal and ownership rules require at least one concrete example and one edge case.

## Canonical outputs
Event map; glossary; actor/capability map; rule and invariant catalog; hotspot list; candidate bounded contexts with rationale; unresolved domain questions; domain decision records.

## Failure modes
Screen-driven modeling; table-driven aggregates; noun extraction without behavior; ignoring exceptions; treating current software bugs as business rules; collapsing conflicting meanings into one global model; skipping time and authority.

## Exit conditions
Stage 03 can hand off when the team can explain the main business flow and exceptions in shared language, material invariants are explicit, and candidate boundaries have evidence-based reasons and known uncertainties.

## Handoff
Stage 04 receives verified business rules and scenarios. Stage 05 receives candidate boundaries, invariant ownership and hotspots for architectural hardening.
