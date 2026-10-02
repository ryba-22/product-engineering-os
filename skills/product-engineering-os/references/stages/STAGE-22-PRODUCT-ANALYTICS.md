# Stage 22 — Product analytics

**Module:** product-intelligence  
**Gate:** G11  
**Evidence anchors:** EVD-AN-001, EVD-AN-003  
**Primary artifacts:** `07-templates/METRIC-TREE.md`, `07-templates/TRACKING-PLAN.md`

## Purpose
Measure whether the product is producing the intended outcomes and provide behavioral evidence for decisions. Analytics starts from product purpose and decision questions, then works backward to metrics and events; it does not start from whatever instrumentation is easiest to collect.

## Required inputs
Product outcome/PDR, user behaviors that indicate value, release exposure, critical workflows, data/privacy constraints, operational metrics and known research findings.

## Questions the Brain must answer
1. What outcome should change if the product is working?
2. Which user behavior is a credible leading or direct signal of that outcome?
3. Which metric measures the behavior without distorting it?
4. What denominator, cohort, time window and segmentation are required?
5. Which guardrail metrics detect harmful side effects?
6. What events/properties are actually needed to compute the metric?
7. How will identity, sessions and anonymous/authenticated transitions work?
8. Which qualitative evidence is needed to explain observed movement?

## Workflow
1. **Build the metric tree.** `purpose → outcome → behavior → signal → metric → event/data source`.
2. **Define metric contracts.** Formula, denominator, cohort/window, exclusions, owner and interpretation limits.
3. **Choose guardrails.** Reliability, quality, accessibility, support burden, cost or other unintended effects.
4. **Design event taxonomy.** Behavior-first names and stable semantic meaning.
5. **Specify properties minimally.** Collect only attributes needed for decisions and permitted by privacy policy.
6. **Define identity/session semantics.** Avoid accidental double counting or cohort drift.
7. **Instrument and validate.** Confirm events fire once at the correct semantic moment with correct properties.
8. **Check data quality.** Missingness, duplication, late arrival, bot/internal traffic and version drift.
9. **Create decision views.** Dashboards/queries answer named questions rather than accumulate charts.
10. **Pair metrics with research.** Analytics shows what/how much; qualitative evidence helps explain why.

## Decision rules
- A metric without an explicit decision or outcome link is a candidate for removal.
- Event names should describe meaningful product behavior, not DOM clicks when the behavior can be represented directly.
- “Active user” requires a product-specific value behavior definition.
- Percentages require visible denominator and cohort semantics.
- Instrumentation changes are versioned; historical comparability must be considered.
- Correlation in analytics does not establish causal impact.

## Evidence standard
Metric claims must specify population/cohort, time period, formula and data-quality caveats. Outcome interpretation should combine operational/product data and research where causal explanation matters.

## Canonical outputs
Metric Tree; metric contracts; Tracking Plan; event/property schema; data-quality checks; outcome dashboard/queries; instrumentation version history.

## Failure modes
Tracking everything; click-level taxonomy with no product meaning; vanity MAU; denominator drift; event duplication; identity stitching assumptions; dashboards with no action; interpreting correlation as experiment.

## Exit conditions
G11 analytics scope is satisfied when priority outcomes and guardrails are computable from validated data, metric semantics are explicit, and decision owners know how to interpret the measures.

## Handoff
Stage 23 uses trusted metrics for experiments. Stage 24 compares intended versus observed outcomes and feeds learning back into strategy/discovery.
