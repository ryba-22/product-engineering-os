# Product Analytics Brain

## Start from meaning
Canonical chain: `OUTCOME → BEHAVIOR → SIGNAL → METRIC → EVENT/DATA SOURCE`.
Do not start from instrumentation or dashboards.

## Metric tree
Use a small outcome metric set plus drivers/inputs and guardrails. Measures may include task success, adoption, retention, satisfaction, cost, quality, error/friction and domain-specific outcomes. Select what answers the product question; do not force a universal framework.

## Event taxonomy
Events should describe stable product/domain behavior (`payment_match_confirmed`) rather than transient UI implementation (`green_button_clicked`) unless UI interaction itself is the research question. Define actor, object, timestamp, properties, source, identity/session semantics, version and privacy classification.

## Interpretation
Segment/cohort where relevant; inspect denominators and data completeness. A movement is a signal, not automatically a cause. Combine quantitative behavior with research/support/operational evidence.
