# Stage 05 — Domain Architecture

**Module:** domain  
**Gate:** G2  
**Evidence anchors:** EVD-DOM-002, EVD-DOM-003  
**Primary decision system:** Domain Brain / DDD adapter plus this playbook

## Purpose
Turn the exploratory domain model into explicit ownership boundaries and tactical consistency rules without allowing persistence schemas or framework conventions to dictate the domain. This stage hardens only the boundaries supported by business language, invariants and change behavior.

## Required inputs
Domain Discovery event map, glossary, invariants, candidate contexts, temporal rules, actor/authority model, current integration constraints and relevant requirements.

## Questions the Brain must answer
1. Which capability owns each business decision and mutation?
2. Which invariants require a single consistency boundary?
3. Which concepts belong together because they change and are reasoned about together?
4. Where can eventual consistency safely replace atomic consistency?
5. What information crosses boundaries and in what semantic form?
6. Which contexts are upstream/downstream and where are translation layers required?
7. Which aggregates/entities/value objects are justified by invariant ownership?
8. Which boundaries are still provisional and what evidence would change them?

## Workflow
1. **Re-test candidate contexts.** Use real scenarios and exceptions, not abstract nouns.
2. **Assign mutation ownership.** Every critical state transition must have one authoritative owner.
3. **Map invariants to consistency and enforcement.** For every material invariant name its semantic owner, authoritative source of truth, atomic/eventual/reconciled consistency need, enforcement layers, violation detection, evidence and recovery path. Use `00-core/engineering-control-loop.md` for the cross-cutting contract.
4. **Model concurrency windows.** For critical mutations identify competing writers, stale-read/lost-update risk, retries/duplicates, partial failure and the mechanism that protects the named guarantee.
5. **Define context relationships.** Record published language, translation, dependency direction and tolerated coupling.
5. **Design aggregates from invariants.** Keep them as small as possible while protecting required consistency.
6. **Model identity and lifecycle.** Separate stable identity from mutable attributes and define valid transitions.
7. **Model temporal semantics.** Specify effective time, event time, scheduling and historical correction where business rules depend on time.
8. **Challenge with change scenarios.** Ask how likely policy, workflow and reporting changes propagate across boundaries.
9. **Record domain ADRs.** Include rejected alternatives and switching triggers.
10. **Expose integration debt.** Legacy tables or shared databases may be constraints, but they do not erase logical ownership.

## Decision rules
- An aggregate is not “all objects needed on one screen”; it protects invariants within a transactional boundary.
- Shared database access does not imply shared domain ownership.
- Cross-context writes require explicit authority; avoid two modules independently mutating the same business fact.
- If a boundary creates constant synchronous chatter for one invariant, reconsider the split.
- Eventual consistency requires defined user/business consequences, reconciliation and observability.
- Legacy structure may force an adapter, but should not become the target domain model by default.

## Evidence standard
Boundary decisions should cite scenarios, invariants, language distinctions, ownership and change coupling. Tactical patterns are justified only after strategic boundaries are credible.

## Canonical outputs
Context map; ownership map; aggregate/invariant model; integration contracts at the semantic level; consistency choices; temporal model; domain ADRs; boundary risks.

## Failure modes
Table-per-aggregate thinking; microservice-per-context by reflex; giant aggregate for convenience; shared mutation authority; events used as CRUD replication; ignoring correction/history semantics; mistaking current code package boundaries for domain boundaries.

## Exit conditions
G2 is satisfied for architecture when critical business facts have explicit owners, invariants map to consistency boundaries, context relationships are explainable, and unresolved boundary hypotheses are named with switching evidence.

## Handoff
Stage 06 receives capabilities, ownership and quality implications. Stages 13–14 receive semantic contracts and invariants but decide transport/storage separately.
