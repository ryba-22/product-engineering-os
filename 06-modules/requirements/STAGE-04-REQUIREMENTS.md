# Stage 04 — Requirements / specification

**Module:** requirements  
**Gate:** G3  
**Evidence anchors:** EVD-REQ-001, EVD-ARCH-001  
**Primary artifacts:** `07-templates/PRD.md`, `07-templates/TRACEABILITY.json`, `07-templates/EXAMPLE-MAP.md`
**Supporting playbook:** `ATDD-EXAMPLE-MAPPING.md`

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
7. Which concrete examples and counterexamples make each material business rule falsifiable before implementation?
8. How will each material requirement be verified at the lowest trustworthy executable layer?
9. Which requirement/example links back to which evidence and decision?

## Workflow
1. **Start from outcomes and scenarios.** Do not start from a feature inventory.
2. **Write actor-centered behavior.** Describe observable capability, trigger, rule and result.
3. **Attach business invariants.** Keep domain rules distinct from UI or storage implementation.
4. **Write exception and recovery paths.** Include invalid input, conflict, stale state, dependency failure and partial completion when relevant.
5. **Elicit quality scenarios.** For performance, reliability, security, accessibility and operability specify stimulus, context, response and measurable threshold when material.
6. **Run Example Mapping for material business behavior.** Bind rule IDs to concrete examples, boundary/counterexamples, open questions and an executable oracle before implementation.
7. **Define acceptance criteria from the examples.** Criteria must be testable and map to the intended guarantee without leaking accidental implementation.
8. **Mark uncertainty.** A hypothesis is not promoted to a requirement because the document needs to look complete.
9. **Trace the chain.** Maintain `EVIDENCE → OUTCOME/NEED → REQUIREMENT/RULE → EXAMPLE → ACCEPTANCE → TEST/EVAL → PRODUCTION OBSERVATION`.
10. **Review for contradictions and hidden design.** Remove accidental architecture unless it is a verified constraint or explicit decision.
11. **Baseline only what is decision-ready.** Keep open questions visible.

## Decision rules
- “System shall use technology X” belongs in requirements only when X is a true external constraint; otherwise it is an architecture decision.
- Acceptance criteria describe observable behavior or quality, not implementation steps.
- Non-functional requirements without context or threshold are aspirations, not testable requirements.
- A requirement with no evidence/outcome link should be challenged.
- A critical rule with no planned verification should not pass G3.
- A material business rule with no representative pre-implementation example/counterexample should not pass G3 unless equivalent current evidence already exists.
- Tests written after implementation do not retroactively prove that the expected business behavior was agreed before implementation.
- Example Mapping does not authorize invention. If an example's expected result depends on an unresolved normalization/equivalence rule, retry policy, eligibility edge case, temporal rule or exception policy, keep that result explicitly open/hypothetical and do not baseline it at G3.
- Do not turn a plausible technical default (for example retrying transient failures) into a confirmed business requirement without evidence or an explicit external constraint.
- Contradictory stakeholder requirements require an explicit trade-off decision, not silent wording compromise.

## Evidence standard
Each material requirement must link to evidence, a governing rule/constraint or an accepted decision. The evidence must support the semantic detail being baselined: a source that establishes deduplication does not automatically establish normalization equivalence, and a requirement to handle failures does not automatically establish retry classification. High-risk requirements need explicit verification and ownership. Unknowns remain visible with a plan to resolve them.

## Canonical outputs
PRD/specification; Example Map with stable rule/example IDs; scenario set; functional requirements; business rules; quality scenarios; acceptance criteria; open-question register; traceability records.

## Failure modes
Feature wish-list PRD; mixing hypotheses with facts; ambiguous “fast / secure / intuitive” NFRs; happy-path-only acceptance; duplicate requirements with different wording; requirements that dictate internal implementation without justification.

## Exit conditions
G3 is satisfied when implementation/design teams can identify required outcomes and guarantees, material business rules have representative executable examples/counterexamples or equivalent evidence, testers can identify the oracle/verification layer, architecture can see material quality drivers, and unresolved questions are explicitly owned.

## Handoff
Stage 05/06 receive domain and quality drivers. Stages 07–11 receive interaction/accessibility constraints. Stages 12–15 consume acceptance and traceability IDs rather than reinterpreting stakeholder requests.
