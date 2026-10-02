# Product Strategy playbook

Use this playbook with `STAGE-01-PROBLEM-OUTCOME.md`. The stage file defines the full operational contract; this document focuses on strategy-specific reasoning patterns.

## Output target

Produce a decision-ready Product Brief and PDR, not a feature wish-list. The core sequence is:

`raw request → problem framing → desired outcome → affected actors → evidence inventory → constraints/non-goals → assumptions → success signals → strategic options → decision → G0`.

## Problem framing

Rewrite solution-shaped requests into observable problems. “Build a dashboard” may hide a need to detect exceptions faster; “add notifications” may hide a coordination failure; “move to microservices” may hide deployment or ownership pain. Preserve the requested solution as an option, not as the problem itself.

Use a four-part statement:

- current situation/behavior;
- affected actor or system;
- consequence that matters;
- evidence and confidence.

## Outcome definition

Prefer outcomes that can change independently of output volume. Good outcomes describe improved task success, reduced error/rework, lower risk, shorter cycle time, improved reliability, lower cost or another observable effect.

Pair the outcome with guardrails so local improvement does not hide harm elsewhere.

## Assumption map

Separate:
- facts already supported;
- interpretations;
- product-risk assumptions (value/usability/feasibility/viability);
- hard constraints;
- preferences;
- unknowns.

Rank assumptions by `impact if false × uncertainty × cost of discovering later`. Route only the top decision-changing unknowns to Discovery.

## Option framing

For material choices, include the status quo or current workaround when credible. Compare options on outcome fit, reversibility, cost, risk and evidence—not on architectural elegance or stakeholder enthusiasm.

Record switching conditions: what future evidence would make another option better?

## Stop-analysis threshold

Proceed when:
- problem/outcome can be stated without embedding a solution;
- material constraints are known or explicitly blocked;
- largest assumptions are visible;
- success can be observed;
- remaining uncertainty belongs to targeted Discovery or a reversible experiment.

Do not continue research merely because sources exist. Conversely, do not invoke “bias for action” when the next step is expensive, irreversible or high-risk and a cheap decision-changing check remains available.

## Escalation

If stakeholders disagree on the outcome, resolve the decision authority or create explicit competing objectives. If the request is primarily a compliance/contractual obligation, strategy still defines scope and success, but value risk may be secondary to correctness/timeliness.

The Product Brief becomes the upstream reference for every later stage; changes to the intended outcome should therefore create a visible decision, not silently rewrite history.
