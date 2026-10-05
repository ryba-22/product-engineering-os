# AI-SDLC execution crosswalk

## Purpose

This adapter note defines how Product Engineering OS (PEOS) relates to the external
[AI-SDLC](https://github.com/ai-sdlc-framework/ai-sdlc) framework without transferring
PEOS ownership to an external runtime.

Reviewed upstream: `ai-sdlc-framework/ai-sdlc@64680f7482b79c7dffc7becab8f347a8ba2a81a9`
on 2026-10-06.

## Boundary

```text
PEOS = method / risk / evidence burden / specialist routing / quality gates
ChatLOOP = task admission / coordination / lane lifecycle / execution provenance / recovery
AI-SDLC = optional external execution implementation behind an adapter
project repo = code / tests / decisions / production evidence
```

This is intentionally not a source-of-truth inversion:

`external runtime != product/domain authority`

An AI-SDLC task may execute a PEOS/ChatLOOP contract, but it does not redefine the
business rule, architecture driver, acceptance oracle or risk classification.

## Concept mapping

| PEOS concept | ChatLOOP / execution concept | AI-SDLC analogue | Rule |
|---|---|---|---|
| R0–R4 risk | per-task execution/review burden | complexity/autonomy routing | PEOS risk wins; no automatic autonomy promotion |
| quality gate | admission/review requirement | QualityGate / DoR | gate must name evidence and owner |
| executable examples / AC | TASK contract | DoR acceptance rubric | structural readiness does not prove semantic correctness |
| AI capability matrix | executable role/tool authority | AgentRole / AutonomyPolicy | capabilities and approvals win over persona labels |
| independent verification | Brain/reviewer provenance | cross-harness reviewers | require proportionally to risk |
| production learning | new task/evidence/decision | emergent issue / exploration | finding does not silently become current-task scope |
| evidence ledger | task/review/runtime provenance | attestations / event log | content-address first; sign only with a defined trust model |
| critical path | lane dependency DAG | task dependency graph | hard dependencies are machine-checked |
| recovery evidence | checkpoint / reachable commit | quarantine/checkpoint/recovery | preserve inspectable work before destructive cleanup |

## Adoption policy

### Use directly as ideas/contracts

- deterministic-first admission checks;
- explicit readiness separate from prioritization/value;
- task dependency graph;
- isolated worktree execution;
- append-only event/audit history;
- emergent finding capture and triage;
- exploration as a different work contract;
- checkpoint/recovery;
- independent reviewer provenance;
- operator projections derived from canonical state.

### Use only behind a bounded experiment

- AI-SDLC orchestrator/spawners;
- automatic PR/merge paths;
- DSSE signing;
- spec-kit bridge;
- full operator TUI.

A pilot must keep PEOS risk/gate decisions and ChatLOOP lifecycle externally inspectable.
Success is lower recovery/coordination cost with equivalent or stronger evidence, not merely
“the pipeline ran autonomously”.

### Do not import as PEOS policy

- autonomy levels that grant authority from historical model performance alone;
- one fixed reviewer fan-out for every risk class;
- a Kubernetes-style resource model without a local lifecycle need;
- compliance posture labels without executable controls/evidence.

## Decision rule

Prefer adapting a mechanism when it strengthens one of these invariants:

1. no execution before the task contract is ready for its mode;
2. accepted task meaning cannot change silently after admission;
3. executor cannot approve its own consequential work;
4. state transitions and decisions can be reconstructed;
5. interruptions preserve enough evidence to resume or recover;
6. parallel work cannot silently invalidate another lane's assumptions;
7. authority comes from explicit capability/approval policy, not agent naming.

If an upstream feature does not strengthen a local invariant, reduce a measured failure mode,
or lower recovery cost, it is not adopted merely because AI-SDLC contains it.

## Source-governance note

This adapter note is an integration crosswalk, not an Active PEOS evidence claim.
If AI-SDLC is promoted into the PEOS source registry/evidence ledger, that change must go through
the normal Source Delta Pipeline and classify the semantic impact explicitly.
