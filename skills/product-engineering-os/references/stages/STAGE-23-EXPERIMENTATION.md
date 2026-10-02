# Stage 23 — Experimentation

**Module:** product-intelligence  
**Gate:** G11  
**Evidence anchors:** EVD-EXP-001, EVD-EXP-003  
**Primary artifact:** `07-templates/EXPERIMENT-PLAN.md`

## Purpose
Choose and run the smallest trustworthy test that can resolve a decision-changing uncertainty. Randomized experiments are one method among several; use them when causal attribution matters and randomization/instrumentation assumptions can be satisfied.

## Required inputs
Explicit decision and uncertainty, candidate intervention, target population, trustworthy metric contracts, eligibility/trigger logic, operational constraints, expected effect size or practical threshold and risk/ethics/privacy constraints.

## Questions the Brain must answer
1. What decision changes based on the result?
2. Is causal attribution necessary or would a cheaper method answer the question?
3. What is the unit of assignment and exposure?
4. Who is eligible and when are they triggered?
5. What primary outcome and guardrails are defined before analysis?
6. What minimum practically important effect matters?
7. What contamination, interference or novelty risks exist?
8. How will assignment/instrumentation trustworthiness be checked?

## Workflow
1. **State decision and hypothesis.** Avoid “test feature X” without a decision threshold.
2. **Choose evidence method.** Interview/prototype/pilot/quasi-experiment/A-B based on uncertainty and feasibility.
3. **Define population and trigger.** Eligibility must be reproducible.
4. **Define assignment.** User/account/session/object level according to interference and product behavior.
5. **Predefine outcomes.** Primary metric, guardrails, analysis window and practical decision threshold.
6. **Estimate duration/sample needs** when statistical inference is used, including baseline variability and expected traffic.
7. **Validate instrumentation before launch.**
8. **Run trustworthiness checks.** Sample Ratio Mismatch, exposure balance, event completeness and invariant metrics.
9. **Analyze without metric fishing.** Separate prespecified results from exploratory findings.
10. **Make the decision.** Ship, stop, iterate or gather different evidence; record uncertainty that remains.

## Decision rules
- Do not A/B test when a usability defect can be observed directly or a policy/legal requirement determines the outcome.
- A statistically significant trivial effect may be practically irrelevant.
- No significant difference does not prove equivalence unless the design supports that conclusion.
- SRM invalidates ordinary interpretation until diagnosed.
- Repeated peeking and optional stopping need appropriate sequential methods or fixed analysis discipline.
- Segment findings discovered after the fact are exploratory until replicated or otherwise supported.

## Evidence standard
Experiment conclusions identify assignment unit, population, dates, exposure, primary metric, guardrails, trustworthiness checks and uncertainty interval/effect estimate as appropriate.

## Canonical outputs
Experiment/Pilot Plan; randomization/exposure contract; instrumentation checks; SRM/invariant results; analysis; decision record; follow-up questions.

## Failure modes
Experiment for every decision; testing without enough traffic; changing primary metric mid-run; SRM ignored; exposure logging after outcome; novelty/learning effects ignored; shipping because p<0.05 despite harm guardrail.

## Exit conditions
G11 experimentation scope is satisfied when the chosen evidence method validly addresses the decision, trustworthiness checks pass, and the result is translated into an explicit action or next uncertainty.

## Handoff
Stage 24 integrates experiment results with analytics, research, support and operational evidence rather than treating one experiment as permanent truth.
