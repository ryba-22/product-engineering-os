# ATDD / Example Mapping

Use this guide when a material business behavior, policy, invariant or exception is about to move from discovery into implementation. The purpose is not to create more specification prose. The purpose is to make the business rule falsifiable before code exists and to preserve the same example as executable evidence later.

## Core model

Treat these as different things:

`rule ≠ example ≠ implementation ≠ test result`

A rule states what must remain true. An example demonstrates the rule under concrete conditions. Implementation is one mechanism that may satisfy the rule. A passing test is evidence about one executable example, not proof that the business model is universally correct.

Use Example Mapping as the default discovery structure for material behavior:

`capability/story → rules → examples/counterexamples → open questions`

Then preserve traceability:

`EVIDENCE → RULE → EXAMPLE → ACCEPTANCE → TEST/EVAL → PRODUCTION OBSERVATION`

The same example should travel through the lifecycle whenever practical instead of being rewritten independently by analyst, developer, tester and evaluator.

## Workflow

1. **Name the business capability or decision.** State the observable outcome, not the UI action or implementation technique.
2. **Extract rules.** Identify policies, invariants, eligibility conditions, calculations, state transitions, ownership and temporal rules.
3. **Write the smallest representative example.** Use concrete actors, values, dates/states and expected result.
4. **Add boundary and counterexamples.** Ask what happens immediately before/after a threshold, with missing data, duplicate commands, stale state, partial failure or conflicting facts.
5. **Mark uncertainty before writing the expected result.** If participants disagree, or if the `Then` depends on an unresolved policy such as identity/normalization equivalence, retry classification, eligibility edge behavior, temporal semantics or exception handling, record an open question or hypothesis instead of choosing an answer. An example may expose missing policy; it must not manufacture it.
6. **Choose the executable layer.** Domain rules should usually be exercised below the UI; integration behavior at the boundary; user workflow only where the interaction itself is the guarantee.
7. **Create a stable example ID.** Reference that ID from acceptance criteria, fixtures/tests and evals.
8. **Freeze only decision-ready behavior.** Examples that depend on unresolved business questions remain non-blocking hypotheses unless risk requires resolution before implementation.
9. **Execute after implementation.** Record actual test/eval evidence against the original example; do not rewrite the expected outcome to match the implementation.
10. **Carry the example into production learning.** When a real trace resembles or contradicts the example, link the observation back to the rule/example ID.

## Example shape

A useful business example contains:

- **Context/Given:** relevant state and facts;
- **Trigger/When:** command, event or decision point;
- **Expected/Then:** observable outcome and invariant;
- **Counterexample:** behavior that must not occur;
- **Questions:** facts still needed to decide;
- **Oracle:** how correctness will be observed;
- **Example ID / source links:** provenance and traceability.

Do not require Gherkin syntax. Structured prose, tables or executable fixtures are valid if semantics remain explicit.

## Decision rules

- A material business rule without at least one representative example should not pass G3 unless equivalent evidence already exists.
- A complex rule with only happy-path examples is not decision-ready.
- A scenario that specifies database tables, framework classes or UI widgets is usually leaking implementation into business acceptance.
- A test generated after implementation can verify code, but it does not replace pre-implementation agreement on expected behavior.
- A concrete-looking example is not evidence for a missing business rule. If deduplication depends on an unconfirmed normalization rule, or recovery behavior depends on an unconfirmed retry policy, keep the expected result `OPEN/HYPOTHESIS` and do not baseline it as acceptance.
- Technical resilience defaults such as transient/permanent retry classification belong to architecture/operations unless the business requirement or external constraint establishes an observable guarantee. Requirements must not promote such defaults into business policy by assumption.
- If an example reveals disagreement about vocabulary or ownership, route back to Domain Discovery rather than polishing acceptance wording.
- If a rule is probabilistic, heuristic or human-judgment based, define observable decision boundaries and escalation/review evidence instead of pretending the rule is deterministic.

## Example as executable contract

Executable does not mean every example must become a browser test. It means there is a reproducible oracle capable of deciding whether the implemented behavior matches the agreed example at the lowest trustworthy layer.

For a high-risk behavior, preserve both positive and negative executable evidence. Where production data is needed to validate semantics, mark the pre-release example as `VERIFIED-IN-TEST` rather than `PROVEN-IN-REALITY`.

## Failure modes

Specification-by-prose only; examples written after code merely to document it; UI-specific scenarios for domain rules; no counterexamples; examples with ambiguous dates or actors; filling an unknown policy with a plausible normalization/retry/default rule; tests that silently change expected values; treating a passing fixture as proof that the domain model is complete; duplicated scenarios with no stable IDs.

## Exit evidence

The ATDD slice is ready when material rules have representative examples, important boundaries/negative cases exist, open questions are explicit, the verification layer is chosen, and example IDs link forward to acceptance/test/eval evidence.
