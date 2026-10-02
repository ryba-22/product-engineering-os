# Continuous Feedback / Learning Loop

Use with `STAGE-24-FEEDBACK-NEXT-ITERATION.md`. Feedback is the mechanism that prevents the lifecycle from ending at release.

## Inputs

Combine:
- product analytics;
- user research;
- support/contact reasons;
- operational workarounds;
- search/log data;
- errors/incidents;
- sales/implementation feedback;
- accessibility findings;
- delivery/reliability signals;
- experiment/pilot results;
- cost/capacity signals.

No single source is the product truth.

## Loop

1. **Reopen the intended outcome.** Use the original PDR rather than redefining success after seeing data.
2. **Confirm exposure.** Know who received the change, when and under which version/flag.
3. **Ingest evidence with provenance and scope.**
4. **Cluster signals around outcomes/problems, not requested features.**
5. **Separate observation from interpretation and hypothesis.**
6. **Compare expected mechanism with observed mechanism.**
7. **Update opportunity/problem model and confidence.**
8. **Choose the highest-value uncertainty or friction on the current outcome.**
9. **Run the cheapest valid discovery/experiment/implementation slice.**
10. **Measure outcome and guardrails.**
11. **Record learning and supersede decisions if needed.**
12. **Repeat only while the outcome remains worth pursuing.**

## Signal triage

Classify incoming signals:
- **incident/critical defect:** route immediately to Restorative mode;
- **repeated friction:** candidate opportunity;
- **one-off request:** evidence point, not backlog commitment;
- **metric regression:** validate instrumentation/exposure before causal story;
- **successful outcome with rising cost/risk:** guardrail problem;
- **low-use feature:** inspect need, discoverability and maintenance cost before assuming awareness issue.

## Opportunity promotion

A signal becomes a promoted opportunity when it:
- links to a desired outcome;
- has enough evidence for its consequence;
- names affected population/context;
- has a decision horizon;
- is not already explained by a known incident or instrumentation defect.

Avoid backlog-as-graveyard. Large backlogs often store unresolved decisions, not value.

## Learning record

Record:
- what changed;
- what was expected;
- what was observed;
- evidence and limitations;
- which assumption/decision changed;
- what was superseded;
- next action and owner.

Feed durable learning to Stage 25 so future work reuses it.

## Stop rule

Stop iterating when the outcome is achieved enough, the opportunity is no longer material, marginal improvement is too expensive, or evidence shows the original problem/solution framing should be abandoned.

Continuous discovery does not mean continuous motion. It means continuous ability to learn and deliberately change course.
