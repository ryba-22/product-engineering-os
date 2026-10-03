# Stage 24 — Feedback → next iteration

**Module:** product-intelligence  
**Gate:** G11  
**Evidence anchors:** EVD-FB-001, EVD-FB-002  
**Primary artifact:** `07-templates/OUTCOME-REVIEW.md`

## Purpose
Close the product-development loop by comparing intended outcomes with observed product, user and operational evidence, then deciding what to continue, change, retire or investigate next. Shipping is not the terminal state.

## Required inputs
Original PDR/outcome, release exposure and date, product metrics, SLO/reliability evidence, experiment results, user research/support themes, incidents/workarounds, cost/operational signals and known residual risks.

## Questions the Brain must answer
1. Did the intended outcome change for the intended population?
2. Which leading drivers moved and which did not?
3. Did guardrails, reliability or accessibility regress?
4. What qualitative evidence explains the observed behavior?
5. Which segments benefited or were harmed differently?
6. Which assumptions were confirmed, weakened or falsified?
7. What new opportunities/problems emerged?
8. Should the next action be iterate, expand, revert, retire or research?

## Workflow
1. **Reopen the original outcome and assumptions.** Do not redefine success after seeing results.
2. **Confirm exposure.** Know who actually received the change and for how long.
3. **Review outcome and driver metrics.** Include confidence/limitations and relevant segments.
4. **Review guardrails and operations.** Errors, support burden, reliability, performance, accessibility and cost.
5. **Integrate qualitative evidence.** Research, support contacts and observed workarounds explain mechanisms.
6. **Compare with expected mechanism.** Ask whether the change worked for the reason predicted.
7. **Update opportunity map/assumptions.** Preserve contradictory evidence.
8. **Decide next action.** Continue, expand, iterate, rollback, retire or investigate.
9. **Record learning as durable evidence.** Link it to prior PDR/ADR/UDR and affected patterns.
10. **Route only unresolved questions.** Feed the smallest next loop into Strategy, Discovery or another stage.

## Decision rules
- No change in top-line metric does not imply no learning; inspect exposure, drivers and data quality before interpreting.
- Improved usage can coexist with worse reliability/support burden; guardrails matter.
- A post-release correlation is not automatically causal.
- Successful local behavior may fail at broader rollout because population/context changed.
- A feature with no meaningful outcome and ongoing maintenance cost is a retirement candidate.
- Lessons from incidents/support should update product and engineering models, not live only in tickets.

## Evidence standard
Outcome review states population, period, exposure, metrics, qualitative sources, limitations and comparison to the original target. Conclusions are scoped to evidence rather than universalized.

## Canonical outputs
Outcome Review; updated assumption/opportunity map; product/system learning; retirement/iteration decision; new evidence records; next-stage routing.

## Failure modes
Ship-and-forget; redefining success post hoc; analytics-only review; ignoring low-adoption segments; treating support volume as mere noise; never retiring weak features; endless iteration with no explicit outcome.

## Exit conditions
G11 feedback scope is satisfied when the team can state what changed, what remains uncertain, what was learned, and the next deliberate action tied to evidence.

## Handoff
Stage 01 receives new strategic problems/outcomes; Stage 02 receives unresolved user questions; Stage 25 receives durable knowledge and supersession updates.
