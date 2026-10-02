# Stage 02 — User / Product Discovery

**Module:** product-discovery  
**Gate:** G1  
**Evidence anchors:** EVD-PROD-001, EVD-PROD-004  
**Primary artifact:** `07-templates/RESEARCH-PLAN.md`

## Purpose
Reduce the product risks that can still change the decision. Discovery is not a mandatory interview phase and not a search for confirmation. It is a deliberate evidence loop that explains current behavior, unmet needs, constraints and opportunity space before committing to a solution.

## Required inputs
Product Brief, outcome target, current evidence inventory, risk class, known user/operator segments, current workflow or workaround, available analytics/support evidence and decision deadline.

## Questions the Brain must answer
1. Who actually performs or experiences the relevant work?
2. What are they trying to accomplish in context?
3. What do they do today, including workarounds and failure recovery?
4. Which pains, delays, errors or unmet outcomes are observed rather than merely reported?
5. Which assumptions can change the product decision?
6. What is the cheapest valid method for testing each important assumption?
7. Which findings are segment-specific and which are broadly supported?
8. What evidence would make us abandon or reshape the opportunity?

## Workflow
1. **Translate risks into research questions.** Each question must have a clear decision it can affect.
2. **Reuse existing evidence.** Review support contacts, analytics, logs, prior research, domain interviews and operational notes before recruiting new participants.
3. **Choose the method from the uncertainty.** Use contextual observation for real workflow, interviews for motivations and history, usability work for interaction risk, analytics for prevalence/behavior, pilots for operational feasibility, and experiments where causal inference is needed.
4. **Define participants and scope.** State inclusion/exclusion, segment, context and recruitment bias.
5. **Collect evidence without leading.** Prefer past behavior and demonstrated workflow over hypothetical preference.
6. **Synthesize explicitly.** Preserve `observation → interpretation → confidence → scope → decision implication`.
7. **Map opportunities.** Connect desired outcome to opportunities, candidate solutions and critical assumptions. Do not jump directly from quote to feature.
8. **Triangulate material claims.** Combine sources when consequence or uncertainty warrants it.
9. **Update the PDR.** Record changed assumptions, confidence and next decision.
10. **Stop when the decision can move.** Do not research merely because more participants or sources are available.

## Decision rules
- One participant is evidence about that participant, not proof of market-wide need.
- Stated preference is weaker than observed behavior for workflow claims.
- “Users asked for feature X” must be decomposed into the goal/problem behind the request.
- Research method choice is driven by the unknown; interviews are not the default for every unknown.
- If a remaining uncertainty is cheaper to resolve with a reversible prototype or pilot, hand it forward rather than extending research.
- Contradictory evidence is recorded and scoped; it is not averaged away.

## Evidence standard
Material claims should identify source, participant/context or dataset, recency, confidence, scope and limitations. Claims used to justify irreversible/high-risk work require stronger triangulation than claims supporting a reversible experiment.

## Canonical outputs
Research Plan; evidence synthesis; opportunity/risk map; updated assumption register; prototype/pilot or experiment recommendation; decision-changing findings linked to evidence IDs.

## Failure modes
Confirmation interviews; asking users to design the solution; treating anecdotes as prevalence; research without a decision owner; collecting quotes without synthesis; excluding operators or edge segments that materially affect the workflow; continuing until “saturation” without defining what decision saturation means.

## Exit conditions
G1 is satisfied when material value/usability uncertainties are sufficiently reduced, deliberately deferred to a cheaper test, or explicitly accepted according to risk. Downstream teams can distinguish confirmed needs from hypotheses.

## Handoff
Stage 03 receives domain language and observed business events. Stage 04 receives validated needs, scenarios and constraints. Candidate solutions remain candidates until later design/architecture decisions.
