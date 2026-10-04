# Production Learning Loop

Production is not only the place where already-correct software runs. It is an evidence source that can falsify product, domain, requirement and operational assumptions. Use this loop to turn real traces, telemetry, incidents, support workarounds and operator overrides into deliberate model updates.

## Core model

Keep these separate:

`expected behavior ≠ observed behavior ≠ explanation ≠ decision`

An anomaly is evidence of a delta. It is not automatically a code bug. The mismatch can come from an implementation defect, a wrong domain assumption, incomplete requirements, data quality, instrumentation error, a new population/context, operator behavior or a previously unknown business exception.

The minimum loop is:

`EXPECTED → OBSERVED → DELTA → CLASSIFY → LEARN → PROPAGATE → RE-VERIFY`

and not merely:

`alert → patch → close ticket`

## Preconditions

Before interpreting production behavior, establish enough provenance to know:
- deployed version/configuration/feature flag;
- affected population, tenant/account/cohort and time window;
- whether the observation is a single trace or aggregate signal;
- instrumentation quality and known missingness/duplication;
- links to the original outcome, rule/example, decision or release when available.

If exposure or instrumentation is unknown, confidence must be reduced rather than inferred.

## Learning workflow

1. **Reopen the expectation.** Name the outcome, invariant, policy, acceptance example, SLO or assumption that predicted behavior.
2. **Capture the observation.** Preserve the smallest useful production trace or aggregate evidence with time/version/scope.
3. **Describe the delta without explanation.** State what differs from expectation.
4. **Classify the mismatch.** Use one or more categories:
   - implementation defect;
   - domain-model gap or unknown rule;
   - stale/incorrect requirement;
   - data-quality/source-of-truth problem;
   - instrumentation defect;
   - operator/workflow friction;
   - expected exception not represented in the model;
   - new population/context or changed environment;
   - security/reliability incident;
   - outcome hypothesis falsified;
   - unresolved.
5. **Estimate consequence and recurrence.** One surprising trace can be highly material; frequency alone is not priority.
6. **Choose the next evidence action.** Reproduce, query additional traces, interview operators/users, inspect data lineage, run an experiment, or make a bounded code correction.
7. **Update the model only when evidence supports it.** Preserve old evidence and record supersession rather than rewriting history.
8. **Propagate learning.** Identify all affected artifacts: domain model/rules, Example Map, requirements, ADR/UDR/PDR, tests, golden/adversarial evals, knowledge records, dashboards/alerts, runbooks.
9. **Re-verify.** Execute the changed examples/tests/evals and, where required, observe the next production cycle.
10. **Close only when the learning has an owner and destination.** A ticket fix with no model/knowledge propagation is an incomplete learning loop when the underlying assumption changed.

## Production observations as domain evidence

Manual overrides, repeated operator corrections, recurring support explanations and reconciliation differences deserve special attention. They often indicate one of three conditions: the software implementation is wrong, the explicit model is incomplete, or real work uses a policy the system has not represented.

Do not automatically automate the workaround. First ask what business decision the workaround is making and who owns that decision.

A useful diagnostic question is:

> What did the human know or decide here that the system did not?

That answer may expose a missing policy, exception, temporal rule, source-of-truth boundary or authority model.

## Propagation contract

For every material learning record, explicitly mark each downstream artifact as:
- `NO_CHANGE` — reviewed and unaffected;
- `UPDATE_REQUIRED` — owner/action identified;
- `SUPERSEDE` — current artifact is no longer valid;
- `NEW_EVAL` — create regression/adversarial coverage;
- `UNKNOWN` — impact still under investigation.

This makes “we learned something” auditable. Durable learning must reach Stage 25 rather than remain only in an incident, chat or issue tracker.

## Definition of Value

A release can be `HEALTHY` without being `SUCCESSFUL`. The Production Learning Loop therefore distinguishes:
- **Definition of Released:** intended artifact/version reached the environment;
- **Definition of Live:** the release is exposed and operationally healthy for the intended population;
- **Definition of Value:** outcome evidence shows enough intended value, within guardrails, to support continuing the decision.

If value cannot yet be measured, record `UNVERIFIED OUTCOME`; do not infer success from deployment or usage alone.

## Failure modes

Ship-and-forget; dashboard-only observability; treating every mismatch as a code defect; changing acceptance criteria after seeing production; closing incidents without updating tests/evals; capturing raw logs without scope/version; accumulating “lessons learned” notes with no supersession path; automating operator workarounds before understanding their decision logic.

## Closure evidence

The loop is closed for a material delta when expectation and observation are linked, the mismatch is classified with explicit confidence, affected artifacts are reviewed, required model/test/eval/knowledge updates are completed or owned, and re-verification or a planned production observation is recorded.
