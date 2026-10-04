# Adaptive Workflow Router

The router chooses the **smallest sufficient workflow** for a task. It does not replace engineering judgement; it makes the first routing decision explicit, repeatable and auditable.

## Input contract

Provide a one-sentence task/outcome, affected surfaces, known business/data/security consequences, production-degradation status, whether stored data/external contracts/user-visible behavior change, and the important unknowns.

If evidence is missing, classify conservatively and route to the stage that can remove the uncertainty.

## Task classes

| Class | Use when | Default route |
|---|---|---|
| BUG | Existing behavior violates an accepted contract | 15 → relevant implementation stage |
| FEATURE | New user/business behavior is requested | 01/02 as needed → 04 → implementation → 15 |
| REFACTOR | Internal structure changes without intended behavior change | relevant implementation stage → 15 |
| DOMAIN_DISCOVERY | Meaning, ownership, lifecycle, policy or boundary is unclear | 03 → 04/05 as needed |
| UI_UX | Interaction, information architecture or visual behavior is primary | 07/08/09/10/11 as needed → 12 → 15 |
| PERFORMANCE | Latency, throughput, resource or scale target is primary | 17 → implementation → 15/20 |
| MIGRATION | Schema/data/system transition changes persisted state or compatibility | 04/06/14 → 15 → 19/20/21 |
| RESEARCH | Decision-critical evidence is missing and code is not yet justified | owning module discovery/research only |
| INCIDENT | Production is degraded or unsafe now | 20/21 → relevant owner → 15/19 |
| DATA_REPAIR | Existing production data must be corrected | 04/14 → 15/20; require auditability |
| PRODUCTION_LEARNING | Compare expected and observed production behavior | 20/22/24/25 |

## Risk escalation

Use R0–R4. Escalate when work changes money, identity, authorization, production data, external contracts, cross-system coordination, concurrency/retry/idempotency, or can create irreversible/hard-to-detect harm. Never lower risk because implementation appears small.

## Minimal-routing algorithm

1. Classify the task.
2. Classify risk R0–R4.
3. Add mandatory concerns from task facts.
4. Remove stages whose decision is already backed by current evidence.
5. Preserve stages required by risk, compatibility, recovery or verification.
6. Return the ordered route, required evidence and stop condition.
7. Re-route when new evidence changes task class, risk or owner.

The router MUST explain both why a stage is included and why obvious stages are intentionally skipped.

## Mandatory concern overlays

- `money_or_critical_business_rule` → Domain/Requirements + Testing.
- `identity_or_authorization` → Requirements + Security + Testing.
- `production_data_mutation` → Requirements + Persistence + Testing + Observability + recovery evidence.
- `external_contract_change` → Requirements + implementation + Testing + compatibility decision.
- `concurrency_retry_idempotency` → Domain/Requirements + implementation + Testing.
- `production_degraded` → Observability/Incident first.
- `user_visible_interaction` → Experience + Frontend as applicable.
- `unknown_problem_or_outcome` → Problem/Outcome or Discovery before implementation.

## Output contract

A routing decision contains `task_class`, `risk`, ordered `stages`, reasons, important skipped stages, required evidence, stop condition and reroute triggers.

Machine-readable defaults live in `machine/workflow-router.json`. `scripts/route_work.py` validates a task descriptor and produces a deterministic baseline route.

## Stop condition

Routing is complete when the next owner has a bounded question, required evidence is known, and no additional stage can materially change the current decision.

`TASK → CLASS → RISK → CONCERNS → MINIMAL ROUTE → EVIDENCE → RE-ROUTE OR CLOSE`
