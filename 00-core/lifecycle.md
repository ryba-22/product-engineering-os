# 25-stage lifecycle

The lifecycle is not a waterfall. Stages can loop, run in parallel when independent, or be skipped when current evidence already satisfies the stage exit criteria. Skipping requires evidence, not convenience.

| # | Stage | Primary module | Canonical exit evidence |
|---:|---|---|---|
| 1 | Problem / idea / business goal | product-strategy | decision-ready Product Brief / PDR |
| 2 | User / Product Discovery | product-discovery | decision-changing user/product evidence |
| 3 | Domain Discovery | domain | shared domain language, rules, hotspots |
| 4 | Requirements / specification | requirements | traceable scenarios/acceptance/quality requirements |
| 5 | Domain Architecture | domain | ownership, invariants and context decisions |
| 6 | System Architecture | system-architecture | architecture drivers, ADRs, failure model |
| 7 | UX Architecture | experience | task/navigation/state architecture |
| 8 | Interaction design | experience | interaction state/recovery contract |
| 9 | Accessibility | experience | semantic/keyboard/focus verification contract |
| 10 | Visual UI | experience | hierarchy/density/token decisions |
| 11 | Design System | experience | reusable pattern/component governance |
| 12 | Frontend implementation | software-engineering | implemented state/feature contracts |
| 13 | Backend / API | software-engineering | authoritative command/query/API contracts |
| 14 | Database / persistence | software-engineering | invariant-safe persistence/migration plan |
| 15 | Testing | quality-engineering | risk-based verification evidence |
| 16 | Security | security-reliability | threat/control/residual-risk evidence |
| 17 | Performance | quality-engineering | budget/workload/performance evidence |
| 18 | CI/CD | delivery-production | immutable candidate + provenance/gates |
| 19 | Deployment / rollout | delivery-production | stable rollout/health evidence |
| 20 | Observability | security-reliability | SLO/telemetry/alert capability |
| 21 | Backup / DR / incidents | security-reliability | measured recovery + incident readiness |
| 22 | Product analytics | product-intelligence | trusted metric/event contracts |
| 23 | Experimentation | product-intelligence | trustworthy decision experiment/pilot |
| 24 | Feedback → next iteration | product-intelligence | outcome review and next decision |
| 25 | Knowledge governance | knowledge-governance | provenance/freshness/supersession/evals |

## State semantics

`UNKNOWN → EXPLORED → DECIDED → IMPLEMENTED → VERIFIED → RELEASED → OBSERVED → MEASURED → LEARNED`

These are evidence states, not project-phase labels.

- **UNKNOWN:** material question has no trustworthy answer yet.
- **EXPLORED:** options/evidence exist but no binding decision has been made.
- **DECIDED:** a material choice and its rationale/constraints are explicit.
- **IMPLEMENTED:** code/config/artifact reflects the decision.
- **VERIFIED:** the relevant guarantee has been tested or otherwise checked.
- **RELEASED:** the verified artifact reached the target environment/exposure.
- **OBSERVED:** production/runtime behavior has been inspected with trustworthy telemetry.
- **MEASURED:** outcome/guardrail data is available for the intended population/time window.
- **LEARNED:** evidence changed or confirmed the model/decision and has been fed back into governance/next iteration.

The OS must not collapse these states. Implementation does not imply verification; deployment does not imply health; health does not imply product success.

## How stages are selected

Start from the current outcome and risk. Route only stages that own unresolved decision-changing questions. A bug may begin at Stage 15 or 20 rather than Stage 1. A small visual correction may use Stage 10 and 12 only. A new product initiative may traverse many stages.

For each selected stage load its `STAGE-XX-*.md` playbook, evidence anchors, relevant template and gate.

## Skip rule

A stage can be skipped when:
1. equivalent current evidence already exists;
2. the evidence is scoped to this decision/context;
3. downstream consumers can locate it;
4. no new risk/constraint invalidates it.

“Done on a previous project” is not enough unless the assumptions still hold.

## Parallel rule

Parallelize only when outputs do not depend on unresolved decisions from another branch. Examples:
- accessibility review can run with visual refinement once interaction semantics are stable;
- API and frontend implementation can run in parallel against a frozen contract;
- performance/security verification can run in parallel after the relevant architecture is sufficiently stable.

Do not parallelize contradictory design/architecture alternatives into separate implementations unless the comparison itself is the deliberate experiment.

## Loop rule

Later evidence can reopen earlier stages:
- usability finding can reopen Requirements;
- concurrency defect can reopen Domain Architecture;
- rollout failure can reopen System Architecture;
- product outcome failure can reopen Strategy/Discovery.

Reopening is not failure of the lifecycle. It is the expected feedback mechanism.

## Completion rule

A lifecycle task is complete when its declared outcome has reached the required evidence state, unresolved risks are explicit, and the next owner/action is known. “No more analysis ideas” is not completion.
