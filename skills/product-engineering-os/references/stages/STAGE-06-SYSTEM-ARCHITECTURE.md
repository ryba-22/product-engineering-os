# Stage 06 — System Architecture

**Module:** system-architecture  
**Gate:** G4  
**Evidence anchors:** EVD-ARCH-004, EVD-ARCH-005  
**Primary artifacts:** architecture drivers, ADRs, fitness functions

## Purpose
Choose the least irreversible system structure that satisfies known business capabilities and quality requirements. Architecture exists to manage consequential trade-offs and failure modes, not to maximize novelty, distributed components or diagram count.

## Required inputs
Product outcome, domain boundaries and ownership, requirements, quality scenarios, risk class, scale/workload assumptions, integration constraints, security/privacy needs, operational constraints and known legacy dependencies.

## Questions the Brain must answer
1. Which quality attributes are materially architecture-driving?
2. What failure modes have unacceptable consequences?
3. Which boundaries must remain independently changeable or deployable?
4. Where is strong consistency required and where can coordination be relaxed?
5. Which external dependencies dominate availability, latency or recovery risk?
6. What is the simplest structure that meets the known constraints?
7. Which choices are reversible and which create long-lived migration cost?
8. What measurable fitness functions can detect architectural drift?

## Workflow
1. **Extract architecture drivers.** Turn vague qualities into scenarios: stimulus, environment, response and measurable response measure.
2. **Map domain capabilities and dependencies.** Preserve domain ownership; do not let deployment topology redefine the model without evidence.
3. **Model important failure modes.** Include dependency timeout, partial failure, concurrency, duplicate delivery, stale data, deploy mismatch and operator error where relevant.
4. **Generate at least two plausible structures for material decisions.** Include a simpler option.
5. **Compare trade-offs explicitly.** Evaluate complexity, coupling, reliability, performance, operability, security, cost and migration effort.
6. **Choose reversibility deliberately.** Prefer modular structure and clear interfaces before distributed deployment when scale/autonomy does not require distribution.
7. **Define runtime and deployment views.** Keep logical ownership, runtime collaboration and infrastructure topology distinct.
8. **Record ADRs.** State context, decision, alternatives, consequences and revisit triggers.
9. **Define fitness functions.** Automate or inspect constraints that matter enough to protect continuously.
10. **Challenge architecture inflation.** Remove components with no architecture driver.

## Decision rules
- “Industry standard” is not an architecture driver.
- A service boundary needs stronger justification than a code-module boundary because it adds network, deployment and operational failure modes.
- Shared persistence across logical owners is debt to be made explicit, not proof that the owners are the same.
- Caches, queues and replicas add consistency/recovery questions; they are not free performance switches.
- Every irreversible choice should have stronger evidence than an equivalent reversible choice.
- If expected scale fits a simple design with margin, complexity must be justified by another quality attribute.

## Evidence standard
Material choices must trace to quality scenarios, domain constraints or measured workload/failure evidence. Estimates must be labeled as estimates and paired with switching thresholds.

## Canonical outputs
Architecture Drivers; context/building-block/runtime/deployment views; ADRs; dependency/failure map; consistency model; capacity assumptions; fitness functions; migration constraints and unresolved risks.

## Failure modes
Microservices by aspiration; queue/cache by reflex; architecture from vendor diagram; mixing logical and deployment boundaries; undocumented single points of failure; speculative scale; no rollback/migration path; ADRs that record only the chosen option.

## Exit conditions
G4 is satisfied when downstream engineering can implement without inventing architecture, material quality attributes have explicit handling, major failure modes are understood, and significant choices have evidence plus revisit conditions.

## Handoff
Stages 12–14 receive implementation boundaries and contracts. Stages 15–21 receive the guarantees, risks and failure modes that must be verified and observed.
