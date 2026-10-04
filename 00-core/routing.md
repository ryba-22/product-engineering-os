# Routing protocol

Route work from the current outcome, missing evidence and risk. The OS is not a checklist that loads every Brain for every task. Each module owns a distinct question; route only when that question is decision-relevant.

| Question | Primary module |
|---|---|
| Why should this exist / what outcome matters? | product-strategy |
| What do users/operators actually need or do? | product-discovery |
| What business events, rules and boundaries exist? | domain |
| What behavior/quality must the system guarantee? | requirements |
| What structure best satisfies quality drivers? | system-architecture |
| How should the task/interface behave? | experience |
| How should frontend/API/data contracts be implemented? | software-engineering |
| How do we prove the important guarantees? | quality-engineering |
| What threats/reliability/recovery obligations exist? | security-reliability |
| How do we build/release the exact artifact safely? | delivery-production |
| Did the product produce the intended outcome? | product-intelligence |
| Is the knowledge current, scoped and traceable? | knowledge-governance |

## Routing rule

1. State the **current decision or outcome** in one sentence.
2. Classify risk R0–R4.
3. Inspect existing evidence and decisions before opening a new stage.
4. Identify the smallest unresolved question that can materially change the decision.
5. Route to the module that owns that question.
6. Load the matching `STAGE-XX-*.md` playbook, not only the module contract.
7. Add a second module only when its question is independently decision-relevant.
8. Return to orchestration when the stage exit condition is satisfied.

## Typical multi-module routes

A feature request with weak problem evidence may route `strategy → discovery`, not immediately to UI. A concurrency bug may route `domain → backend/API → persistence → testing`. A release regression may route `observability → testing/engineering → delivery`. A visually inconsistent table may route only to Experience unless behavior/state semantics are also wrong.

## Anti-overrouting

Do not load Architecture merely because code will be written. Do not load Discovery when current user evidence already answers the decision. Do not load Security as a generic ceremony for R0 copy changes. Do not run Product Analytics before a meaningful outcome/metric contract exists.

Each added module increases context and coordination cost. The burden is to justify the route.

## Re-routing triggers

Re-route when evidence exposes a different owner question. Examples:

- usability research reveals a domain-rule conflict → Domain;
- architecture review reveals an unverified latency assumption → Performance;
- API implementation reveals unclear authorization semantics → Requirements/Security;
- rollout reveals production-only failure → Observability/Resilience;
- outcome review disproves the original problem hypothesis → Strategy/Discovery.

## Closure discipline

A routed stage closes only when its exit criteria are satisfied or an explicit blocker is recorded. Do not keep the module “active” because more reading is possible. Do not silently carry unresolved questions into implementation; attach an owner and next route.

The canonical route is therefore dynamic: `OUTCOME → RISK → MISSING EVIDENCE → OWNER MODULE → STAGE PLAYBOOK → GATE → NEXT DECISION`.


## Operator entrypoint and execution profile

For new work, use operator-front-door.md before selecting a lane or stage when the operator has supplied only a problem/outcome. After R0-R4 classification, derive FAST / STANDARD / EVIDENCE_HEAVY from execution-profiles.md.

The profile changes evidence and verification burden; it does not bypass module ownership, hard constraints or executable guarantees.
