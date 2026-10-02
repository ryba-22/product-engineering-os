# Stage 01 — Problem / idea / business goal

**Module:** product-strategy  
**Gate:** G0  
**Evidence anchors:** EVD-PROD-002, EVD-PROD-003  
**Primary artifact:** `07-templates/PRODUCT-BRIEF.md`

## Purpose
Convert a request, idea or proposed feature into a decision-ready problem and outcome definition without smuggling the proposed solution into the problem statement. This stage exists to decide what improvement matters, for whom, under which constraints, and how success could be observed before Discovery or architecture work starts.

## Required inputs
Use what already exists before asking for more: requester intent, current product/service behavior, business objective, known users or operators, current metrics, constraints, prior decisions and known deadlines. Mark missing facts as unknown instead of filling them from intuition.

## Questions the Brain must answer
1. What observable problem or opportunity exists today?
2. Who experiences it or depends on its resolution?
3. What outcome should change if the work succeeds?
4. What evidence currently supports the problem statement?
5. Which of value, usability, feasibility and viability risks are material now?
6. Which constraints are hard, negotiable or merely assumed?
7. What is explicitly out of scope?
8. Which success signals would falsify the claim that the work helped?

## Workflow
1. **Separate request from need.** Rewrite “build X” as the underlying behavior, friction, risk or business outcome. Keep the requested solution as one candidate option.
2. **Inventory evidence.** Link observations, analytics, support cases, operational workarounds, prior research and stakeholder commitments. Give each claim a confidence level.
3. **Map affected actors.** Distinguish direct users, operators, approvers, maintainers and people affected indirectly.
4. **Define outcome.** Express success as a measurable or observable change in behavior, quality, cost, risk or service performance.
5. **Surface constraints and non-goals.** Include legal, contractual, technical, timing, data and organizational constraints. Do not promote preferences into hard constraints.
6. **Identify material product risks.** State which risks can invalidate the initiative and which can safely wait for later stages.
7. **Generate strategic options.** Include “do nothing / keep current workaround” when credible. State switching conditions rather than pretending certainty.
8. **Create the PDR/Product Brief.** Record the chosen framing, trade-offs, open questions and evidence IDs.
9. **Apply stop-analysis.** Move forward when further strategy analysis is less valuable than targeted Discovery.

## Decision rules
- A problem statement that names a specific UI, architecture or vendor as mandatory is invalid unless that choice is a verified hard constraint.
- A metric is useful only if it represents the intended outcome; output counts such as “screens shipped” or “features delivered” are not outcome evidence.
- A reversible, low-risk initiative can proceed with weaker evidence than a costly, irreversible or safety-relevant initiative.
- If stakeholders disagree about the desired outcome, do not route to implementation. Resolve or explicitly record the conflict first.
- If the main uncertainty is “do users actually have this problem?”, route it to Stage 02 rather than extending desk analysis.

## Evidence standard
The stage needs enough evidence to justify the existence and intended direction of the work, not proof of the solution. Preserve the chain `claim → evidence → confidence → decision implication`. Separate observed facts from interpretations and hypotheses.

## Canonical outputs
A completed Product Brief; outcome statement; actor/stakeholder map; constraints and non-goals; assumption/risk list; initial success signals; PDR or explicit no-go/defer decision.

## Failure modes
Solution-first framing; vanity metrics; unbounded stakeholder wish-list; treating a deadline as evidence of user value; hidden assumptions presented as facts; researching indefinitely after the decision is already reversible and bounded.

## Exit conditions
G0 is satisfied when the problem and desired outcome can be stated without embedding the preferred solution, material constraints and risks are visible, success can be observed, and remaining decision-changing uncertainty has a named owner in the next stage.

## Handoff
Stage 02 receives the Product Brief plus unresolved value/usability questions. Stage 04 may receive already-confirmed constraints, but hypotheses must remain labeled as hypotheses.
