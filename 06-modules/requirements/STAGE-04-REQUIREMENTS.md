# Stage 04 — Requirements / specification

**Module:** requirements  
**Gate:** G3  
**Evidence anchors:** EVD-REQ-001, EVD-ARCH-001  
**Primary artifacts:** `07-templates/PRD.md`, `07-templates/TRACEABILITY.json`

## Purpose
Translate validated outcomes, user/domain evidence and constraints into a specification that can guide design, implementation and verification without erasing uncertainty. Requirements are a traceability bridge, not a transcript of stakeholder requests.

## Required inputs
Product Brief/PDR, discovery evidence, domain scenarios and invariants, known quality attributes, constraints, risk class and prior decisions.

## Questions the Brain must answer
1. Which behaviors are required to achieve the outcome?
2. Which business rules are confirmed and which remain hypotheses?
3. What are the main and exceptional scenarios?
4. What quality attributes materially affect success?
5. What failure and recovery behavior is required?
6. What security, privacy, data and accessibility constraints apply?
7. How will each material requirement be verified?
8. Which requirement links back to which evidence and decision?

## Workflow
1. **Start from outcomes and scenarios.** Do not start from a feature inventory.
2. **Write actor-centered behavior.** Describe observable capability, trigger, rule and result.
3. **Attach business invariants.** Keep domain rules distinct from UI or storage implementation.
4. **Write exception and recovery paths.** Include invalid input, conflict, stale state, dependency failure and partial completion when relevant.
5. **Elicit quality scenarios.** For performance, reliability, security, accessibility and operability specify stimulus, context, response and measurable threshold when material.
6. **Define acceptance criteria.** Criteria must be testable and map to the intended guarantee.
7. **Mark uncertainty.** A hypothesis is not promoted to a requirement because the document needs to look complete.
8. **Trace the chain.** Maintain `EVIDENCE → OUTCOME/NEED → REQUIREMENT → SCENARIO → ACCEPTANCE → TEST/OBSERVATION`.
9. **Review for contradictions and hidden design.** Remove accidental architecture unless it is a verified constraint or explicit decision.
10. **Baseline only what is decision-ready.** Keep open questions visible.

## Decision rules
- “System shall use technology X” belongs in requirements only when X is a true external constraint; otherwise it is an architecture decision.
- Acceptance criteria describe observable behavior or quality, not implementation steps.
- Non-functional requirements without context or threshold are aspirations, not testable requirements.
- A requirement with no evidence/outcome link should be challenged.
- A critical rule with no planned verification should not pass G3.
- Contradictory stakeholder requirements require an explicit trade-off decision, not silent wording compromise.

## Evidence standard
Each material requirement must link to evidence, a governing rule/constraint or an accepted decision. High-risk requirements need explicit verification and ownership. Unknowns remain visible with a plan to resolve them.

## Canonical outputs
PRD/specification; scenario set; functional requirements; business rules; quality scenarios; acceptance criteria; open-question register; traceability records.

## Failure modes
Feature wish-list PRD; mixing hypotheses with facts; ambiguous “fast / secure / intuitive” NFRs; happy-path-only acceptance; duplicate requirements with different wording; requirements that dictate internal implementation without justification.

## Exit conditions
G3 is satisfied when implementation/design teams can identify required outcomes and guarantees, testers can derive or confirm verification, architecture can see material quality drivers, and unresolved questions are explicitly owned.

## Handoff
Stage 05/06 receive domain and quality drivers. Stages 07–11 receive interaction/accessibility constraints. Stages 12–15 consume acceptance and traceability IDs rather than reinterpreting stakeholder requests.
