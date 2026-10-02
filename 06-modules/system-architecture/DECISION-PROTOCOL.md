# System Architecture Brain — decision protocol

Use with `STAGE-06-SYSTEM-ARCHITECTURE.md`. Architecture decisions are justified by business capabilities, quality scenarios and failure consequences, not by pattern preference.

## Core question

What system structure satisfies the known outcomes and quality attributes with the least irreversible complexity?

## Decision preparation

Before comparing architectures, write:

- business capability and domain ownership involved;
- architecture-driving quality scenarios;
- workload/scale assumptions and their confidence;
- data consistency/concurrency requirements;
- external dependencies and failure domains;
- operational constraints;
- security/privacy boundaries;
- migration/legacy constraints;
- risk class R0–R4.

If these are unknown, do not invent precision. State switching thresholds and route targeted evidence.

## Option generation

For a material decision generate at least:
1. the simplest credible option;
2. the leading alternative;
3. optionally a structurally different option when the trade-off space is unclear.

Compare options on:
- correctness/invariant fit;
- coupling and change autonomy;
- latency/performance;
- availability/resilience;
- security/trust boundaries;
- deployability/operability;
- data consistency;
- cost;
- migration/recovery;
- cognitive complexity.

Avoid weighted score theater when the weights are arbitrary. Use narrative trade-offs plus hard constraints and disqualifiers.

## Runtime and failure analysis

Architecture is incomplete until important runtime paths and failure paths are described. For critical interactions ask:

- what happens on timeout?
- what happens on duplicate delivery?
- what happens on partial success?
- what happens when one dependency is stale/unavailable?
- what happens during deployment/version skew?
- what happens under concurrent mutation?
- what happens when recovery/rollback starts?

A component that improves one quality while creating another failure mode must make that trade explicit.

## Architecture-inflation guard

Reject additional services, queues, caches, replicas, orchestration platforms or data stores unless they satisfy a named driver better than the simpler option.

Microservices are justified by independently valuable deployment/ownership/scaling/failure-boundary needs, not by system size aesthetics. Queues are justified by decoupling, buffering or workflow semantics that tolerate asynchronous completion. Caches are justified by measured or strongly evidenced latency/load needs and a defined invalidation model.

## Reversibility

Prefer choices that preserve future options:
- modular boundaries before network boundaries;
- explicit interfaces before duplicated data;
- adapters around legacy/vendor dependencies;
- expand/contract migration paths;
- feature flags only when they do not hide irreversible side effects.

For irreversible choices, increase evidence and review burden.

## ADR contract

A significant ADR records:
- context and driver;
- decision;
- alternatives considered;
- accepted trade-offs;
- assumptions;
- validation evidence;
- consequences;
- observable revisit trigger.

“Because it is best practice” is not an acceptable rationale.

## Stop-analysis gate

Stop comparing architectures when one option satisfies hard constraints and quality drivers with acceptable risk, alternatives have explicit switching conditions, and remaining uncertainty is cheaper to resolve by a reversible implementation slice or measurement.

## Failure analysis prompts

Use these before G4:
- Which single dependency failure can stop the user outcome?
- Which hidden state can diverge?
- Which retry can duplicate an external effect?
- Which migration can strand old/new versions?
- Which resource can saturate first?
- Which operator action can cause broad blast radius?
- Which architectural assumption has never been measured?

The resulting risks feed Quality, Security, Performance, Delivery and Observability.
