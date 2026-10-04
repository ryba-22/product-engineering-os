# Engineering Control Loop

This contract turns important product/domain/architecture decisions into explicit guarantees before implementation. It is cross-cutting: it does not replace Domain, Requirements, Architecture, Quality or Product Intelligence. It binds their outputs into one decision/verification loop.

Use it by default for R2–R4 changes and for any change involving money, identity, authorization, critical data mutation, external side effects, cross-system coordination, concurrency, retries, migrations or hard-to-detect failure. For R0–R1 use only the relevant parts.

## Governing distinctions

- fact != hypothesis != assumption != decision
- invariant != implementation check
- data source != source of truth
- atomic consistency != eventual consistency
- implementation != verification
- provider contract != consumer guarantee
- agent capability != agent permission
- cheap generation != cheap verification

The goal is not more process. The goal is to prevent the team or an AI agent from implementing a model that has not earned the right to become code.

## 1. Falsification / unknown-unknown pass

Before proposing implementation, attempt to disprove the current model.

Record:
- FACTS: directly supported by code, data, policy, production evidence or authoritative domain evidence;
- HYPOTHESES: plausible explanations that still need discriminating evidence;
- ASSUMPTIONS: temporary beliefs accepted for progress;
- OPEN QUESTIONS: unresolved facts that can change a decision;
- COUNTER-MODELS: at least one credible alternative explanation/model for R2+ work;
- DISCONFIRMING PROBES: concrete questions, examples or measurements that could falsify the leading model.

Ask explicitly:
- What would make the current model wrong?
- Which exception or second use case breaks it?
- Which hidden temporal, authority or ownership rule have we assumed?
- Which failure mode is absent from the happy path?
- Are we solving the problem, or compensating for a bad model one layer lower?

Do not extend research indefinitely. The stop-analysis gate still applies.

## 2. Invariant + consistency + enforcement map

For each material invariant record:

| Field | Meaning |
| --- | --- |
| Invariant | What must remain true across valid state transitions |
| Owner | One capability/context responsible for the business decision |
| Source of truth | Authoritative business fact/state |
| Consistency | Atomic, monotonic, eventual, reconciled, or explicitly weaker |
| Enforcement | Domain/application/DB/API/integration/UI locations that enforce or protect it |
| Evidence | Scenario/test/constraint/runtime signal proving the guarantee |
| Detection | How violation or divergence becomes visible |
| Recovery | Retry, compensation, reconciliation, rollback or manual repair |
| Revisit trigger | Evidence that would invalidate the current placement |

Rules:
- An invariant may be defended in multiple layers, but it has one semantic owner.
- UI validation is never sufficient protection for a business invariant.
- DB constraints are valuable when they express storage-level truths, but persistence must not silently become the domain owner.
- Eventual consistency is a business/UX/recovery decision, not a synonym for “we use events”.
- If no enforcement point can honestly protect the invariant, the model or boundary is not ready.

## 3. Concurrency and failure model

For critical mutations, describe the competing actors and failure window before implementation.

Check:
- simultaneous commands on the same business fact;
- stale reads / lost updates;
- duplicate delivery or retry;
- timeout after an external side effect;
- partial success across boundaries;
- out-of-order messages/events;
- version skew during rollout;
- recovery after process crash;
- reconciliation when sources diverge.

Record the chosen mechanism where applicable: optimistic/pessimistic locking, unique constraint, idempotency key, deduplication, transactional boundary, outbox/inbox, compare-and-swap/version, compensating action, reconciliation job or explicit manual recovery.

Do not select a mechanism because it is fashionable. Select it because it protects a named guarantee under a named failure mode.

## 4. Verification budget

Human attention is scarce. Allocate it by semantic risk, not by line count.

Default ownership:

| Work | Default verification ownership |
| --- | --- |
| cosmetic/mechanical refactor | agent/automation + focused review |
| generated CRUD/plumbing | automated contract/integration checks + spot review |
| data migration or persistence semantics | human design review + representative data evidence |
| concurrency/retry/idempotency | human-owned model + integration/runtime evidence |
| business invariant/policy | human-owned decision + executable examples |
| bounded-context/ownership boundary | human-owned |
| authorization/security/privacy boundary | human-owned + independent/specialist evidence when risk requires |
| production outcome interpretation | human-owned; AI may analyze evidence but not redefine success |

The AI may generate options, tests and evidence collection. It must not silently decide semantics whose failure changes money, rights, ownership, safety, privacy or irreversible effects.

For every material risk, name:
- required evidence layer;
- human review depth;
- what can be delegated;
- what cannot be delegated;
- residual blind spots.

## 5. Architecture economics / complexity investment

Before adding architecture or expensive AI/tooling, classify the need:

- COMMODITY: prefer buying/reusing/managed capability unless a constraint prevents it;
- DIFFERENTIATOR: invest when it creates product/domain advantage;
- DETERMINISTIC CORE: prefer ordinary code/rules when correctness must be reproducible;
- PROBABILISTIC ASSISTANCE: use AI where ambiguity/tolerance exists and verification is affordable;
- ESCALATED MODEL: use a more capable/costly model only when expected error reduction justifies the cost;
- IRREVERSIBLE COMPLEXITY: demand stronger evidence and a switching/rollback story.

Ask: what named driver becomes better because this complexity exists? If none, reject it.

## 6. Consumer-oriented contract check

At system boundaries, provider correctness is insufficient when consumers depend on stronger semantics.

For each important contract record:
- consumer and job-to-be-done;
- provider output;
- semantic guarantee the consumer actually relies on;
- compatibility/versioning rule;
- negative/error behavior;
- test/evidence owned by the consumer side;
- fallback/recovery when the provider is unavailable or changes.

Use consumer-driven contract testing where it exercises real consumer expectations. Do not use it as ceremony for internal calls with no meaningful compatibility risk.

## 7. Implementation gate

Implementation may begin when the relevant parts of this loop are explicit enough that:
- the problem/outcome and risk are known;
- material invariants have owners and consistency choices;
- critical concurrency/failure modes have a handling strategy;
- human-owned decisions are separated from delegable work;
- additional complexity has a named driver;
- important cross-system consumer guarantees are visible;
- remaining uncertainty is consciously accepted, experimentally bounded or cheaper to resolve in execution.

For R3/R4, unresolved gaps in these areas are blockers unless an explicit acceptance authority records the risk.

## 8. Production learning closure

After release, compare the expected mechanism with production evidence.

If telemetry, incidents, support cases, user behavior or reconciliation expose a mismatch:
1. identify the violated/incorrect assumption, invariant, contract or failure model;
2. update the model and executable evidence first;
3. supersede the affected decision when necessary;
4. change implementation;
5. verify and observe again.

Production is evidence about the model, not merely a place where code runs.
