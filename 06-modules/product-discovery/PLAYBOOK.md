# Product Discovery playbook

Use with `STAGE-02-DISCOVERY.md`. Discovery is a decision-oriented evidence loop, not a fixed sequence of interviews, surveys and prototypes.

## Start from the uncertainty

Write each research question as: “We need to know **X** because it would change **decision Y**.” If no realistic answer can change a decision, the research is probably unnecessary.

Common uncertainty types and suitable methods:

| Unknown | Strong first methods |
|---|---|
| Current workflow/context | contextual observation, workflow reconstruction, interviews about recent behavior |
| Prevalence/frequency | analytics, logs, survey with careful sampling |
| Comprehension/usability | prototype or usability task |
| Motivation/decision drivers | interviews, field observation, support/sales evidence |
| Operational feasibility | pilot, shadow run, service simulation |
| Causal product effect | controlled experiment when assumptions allow |
| Domain rule | authoritative policy + domain expert scenarios, not preference research |

## Participant and evidence scope

Define who counts as relevant and why. Include operators/admins when they carry hidden work. Look for edge segments when their failure consequence is high even if they are uncommon.

Record recruitment/source bias. “Five users said…” is incomplete without who they were, what context they represented and how they were selected.

## Interview discipline

Ask for concrete recent examples before hypothetical preference. Reconstruct trigger, steps, tools, decisions, workarounds, failures and consequences. Avoid presenting the preferred solution early. Distinguish observed behavior from a participant’s explanation and from the researcher’s interpretation.

## Synthesis

Preserve the chain:

`observation → interpretation/hypothesis → confidence → scope → decision implication`.

Cluster evidence around opportunities/problems, not desired features. Contradictory observations remain visible until segment/context explains them or more evidence resolves them.

## Triangulation

Triangulate when the decision consequence warrants it. Qualitative evidence explains mechanism/context; quantitative evidence estimates scale/distribution; operational evidence reveals feasibility and workarounds. Different methods answer different questions and should not be averaged into fake certainty.

## Opportunity mapping

Connect desired outcome → opportunities → candidate solutions → assumptions/tests. Multiple solutions may address one opportunity. One requested feature may address several different opportunities and should be decomposed.

## Stop rule

Discovery ends when material product risks are sufficiently reduced for the current reversible decision, explicitly accepted, or cheaper to test in a prototype/pilot/production slice. “More participants are available” is not a reason to continue.

Every output must preserve unknowns. Discovery that produces only polished themes and loses uncertainty is weaker than a smaller synthesis with explicit confidence and decision consequences.
