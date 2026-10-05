# Stage 24 — Feedback → next iteration

**Module:** product-intelligence  
**Gate:** G11  
**Evidence anchors:** EVD-FB-001, EVD-FB-002  
**Primary artifacts:** `07-templates/OUTCOME-REVIEW.md`, `07-templates/PRODUCTION-LEARNING-RECORD.md`
**Supporting playbook:** `PRODUCTION-LEARNING-LOOP.md`

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
6. Where does observed production behavior differ from the expected rule/example/mechanism?
7. Is each material delta an implementation defect, domain/requirement gap, data/instrumentation issue, operator-workflow signal, new context or falsified outcome hypothesis?
8. Which assumptions were confirmed, weakened or falsified?
9. What new opportunities/problems emerged?
10. Should the next action be iterate, expand, revert, retire or research?

## Workflow
1. **Reopen the original outcome and assumptions.** Do not redefine success after seeing results.
2. **Confirm exposure.** Know who actually received the change and for how long.
3. **Review outcome and driver metrics.** Include confidence/limitations and relevant segments.
4. **Review guardrails and operations.** Errors, support burden, reliability, performance, accessibility and cost.
5. **Integrate qualitative evidence.** Research, support contacts and observed workarounds explain mechanisms.
6. **Compare expected vs observed.** Link production evidence to the originating outcome, invariant, rule/example, SLO or decision when possible.
7. **Classify material deltas before fixing.** Distinguish implementation defects from domain/requirement gaps, data/instrumentation issues, operator workarounds, new context and falsified outcome hypotheses.
8. **Update opportunity map/assumptions.** Preserve contradictory evidence.
9. **Decide next action.** Continue, expand, iterate, rollback, retire or investigate.
10. **Propagate learning.** Review affected domain model/rules, Example Maps, decisions, tests, golden/adversarial evals, observability/runbooks and durable knowledge; mark each NO_CHANGE/UPDATE_REQUIRED/SUPERSEDE/NEW_EVAL/UNKNOWN.
11. **Re-verify changed contracts.** Execute the updated example/test/eval and plan the next production observation when reality is part of the oracle.
12. **Route only unresolved questions.** Feed the smallest next loop into Strategy, Discovery or another stage.

## Decision rules
- No change in top-line metric does not imply no learning; inspect exposure, drivers and data quality before interpreting.
- Improved usage can coexist with worse reliability/support burden; guardrails matter.
- A post-release correlation is not automatically causal.
- Successful local behavior may fail at broader rollout because population/context changed.
- A feature with no meaningful outcome and ongoing maintenance cost is a retirement candidate.
- Lessons from incidents/support should update product and engineering models, not live only in tickets.
- A repeated manual override is potential domain evidence; ask what the human knew or decided before automating the workaround.
- A release may be HEALTHY while the product outcome remains UNVERIFIED; success requires Definition of Value evidence.

## Evidence standard
Outcome review states population, period, exposure, metrics, qualitative sources, limitations and comparison to the original target. Conclusions are scoped to evidence rather than universalized.

For material production claims, create a machine-readable Production Evidence Record compatible with `machine/production-evidence.schema.json` and validate it with `python3 scripts/production_evidence.py <record.json> --check`. A `SUCCESS_SUPPORTED` result requires outcome evidence, a met target, passing guardrails, usable instrumentation and no known segment harm.

## Canonical outputs
Outcome Review; Production Learning Record for material deltas; machine-readable Production Evidence Record when the claim is material; derived value status; updated assumption/opportunity/domain model; propagation status across examples/tests/evals/knowledge; retirement/iteration decision; new evidence records; next-stage routing.

## Failure modes
Ship-and-forget; redefining success post hoc; analytics-only review; ignoring low-adoption segments; treating support volume as mere noise; never retiring weak features; endless iteration with no explicit outcome.

## Exit conditions
G11 feedback scope is satisfied when the team can state what changed, compare expected vs observed behavior, classify material deltas, propagate assumption changes to affected model/test/eval/knowledge artifacts, record Definition of Value status, and name the next deliberate action tied to evidence.

## Handoff
Stage 01 receives new strategic problems/outcomes; Stage 02 receives unresolved user questions; Stage 25 receives durable knowledge and supersession updates.
