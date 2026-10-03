# Experimentation Brain

Use with `STAGE-23-EXPERIMENTATION.md`. Experimentation selects the cheapest valid evidence method for a decision-changing uncertainty and protects against false causal certainty.

## Choose the evidence method first

Possible methods include interview/observation, prototype/usability test, concierge/fake-door test, operational pilot, shadow mode, staged rollout, quasi-experiment, controlled A/B experiment or production measurement.

Use A/B only when:
- causal attribution matters;
- eligible traffic/time is sufficient;
- assignment can remain stable;
- outcomes/guardrails are measurable;
- contamination/interference is acceptable;
- ethical/operational risk is acceptable;
- instrumentation is trustworthy.

A usability defect visible in five task sessions usually does not need an A/B test. A legal/security requirement is not a preference experiment.

## Experiment contract

Before launch define:
- decision to be made;
- hypothesis/mechanism;
- unit of assignment;
- eligibility and trigger;
- control/treatment;
- primary metric;
- guardrails;
- minimum practically important effect;
- power/sample assumptions when applicable;
- duration/stopping rule;
- trustworthiness checks;
- analysis plan;
- rollout/rollback action.

## Assignment and exposure

Randomization unit should match interference risk. Account-level behavior may require account-level assignment; session assignment can contaminate learning/experience.

Log assignment separately from actual exposure when users may never encounter the treatment.

## Trustworthiness gates

Before interpreting outcomes check:
- Sample Ratio Mismatch;
- exposure counts/balance;
- invariant/A-A-like diagnostics where useful;
- missing/duplicate outcome events;
- eligibility consistency;
- implementation/version skew.

SRM is not “another metric.” It is a warning that the experiment machinery or assumptions may be broken.

## Analysis discipline

Estimate effect and uncertainty, not only p-values. Statistical significance can accompany trivial product impact. Lack of significance does not prove equivalence unless designed for it.

Avoid:
- optional stopping from repeated peeking;
- switching primary metrics post hoc;
- testing many segments until one looks positive;
- excluding inconvenient users after assignment;
- interpreting exploratory subgroups as confirmed.

Sequential methods are valid when preplanned and statistically appropriate.

## Product decision

Experiment completion requires a decision:
- ship/expand;
- do not ship;
- iterate;
- gather different evidence;
- stop because the uncertainty was not worth further cost.

Record what remains uncertain and whether the result generalizes beyond the tested population/time/product version.

The goal is not to “win experiments.” It is to reduce uncertainty without fooling the product team.
