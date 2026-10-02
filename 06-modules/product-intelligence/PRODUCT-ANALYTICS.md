# Product Analytics Brain

Use with `STAGE-22-PRODUCT-ANALYTICS.md`. Product analytics turns product purpose and behavior into trustworthy measurement contracts.

## Start from meaning

Canonical chain:

`OUTCOME → BEHAVIOR → SIGNAL → METRIC → EVENT/DATA SOURCE`

Do not start from instrumentation, vendor dashboards or existing events. Existing data may constrain what can be measured now, but it should not redefine the desired outcome.

## Metric tree

Use a small set:
- primary outcome metric(s);
- driver/input metrics that explain movement;
- guardrails that detect harm;
- diagnostic metrics for investigation.

Possible dimensions include task success, adoption, retention, satisfaction, cost, quality, error/friction, reliability and domain-specific outcomes. Select only what answers the decision.

For every metric define:
- formula;
- numerator/denominator;
- eligible population;
- cohort/window;
- exclusions;
- data source;
- owner;
- interpretation limit.

“Conversion improved 10%” is incomplete without baseline, denominator, period and population.

## Event taxonomy

Events should describe stable product/domain behavior such as `enrollment_submitted` rather than transient implementation details such as `green_button_clicked`, unless the UI interaction itself is under study.

Define:
- event semantic meaning;
- actor/object;
- trigger moment;
- required properties;
- identity/session behavior;
- source;
- version;
- privacy classification;
- metric consumers.

Avoid sending every field “just in case.” Instrumentation has privacy, quality and maintenance cost.

## Identity and sessions

Be explicit about anonymous/authenticated transitions, account/user/device relationships, shared accounts and cross-device behavior. Identity stitching assumptions can distort retention/funnel metrics.

## Data quality

Monitor:
- missing/duplicate events;
- impossible order;
- schema/property drift;
- delayed arrival;
- bot/internal/test traffic;
- client clock issues;
- version adoption;
- broken denominators.

Metrics built from untrusted instrumentation should be labeled degraded rather than silently reported.

## Segmentation and cohorts

Use segmentation when product behavior differs by meaningful context: role, institution, plan, device, lifecycle stage, geography or other permitted dimension. Avoid slicing until a random pattern looks interesting.

Cohorts should preserve the time/eligibility logic needed to interpret behavior.

## Interpretation

Analytics reveals behavior and magnitude, not automatically cause. Pair it with experiments for causal questions and with research/support/operational evidence to understand mechanism.

A dashboard is not the output. The output is a trustworthy measurement system that supports named decisions and can survive instrumentation evolution.
