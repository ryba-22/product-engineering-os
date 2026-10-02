# Stage 11 — Design System

**Module:** experience  
**Gate:** G5  
**Evidence anchors:** EVD-UX-005, EVD-GOV-001  
**Primary outputs:** pattern inventory, token/component contracts, promotion decisions

## Purpose
Govern reusable interface decisions so teams stop reinventing stable patterns without turning every local solution into a global component. A design system is a managed product of semantics, behavior, accessibility and migration policy, not merely a component gallery.

## Required inputs
Repeated UI patterns, interaction contracts, accessibility requirements, visual tokens, existing component library, usage evidence, ownership model and known product variants.

## Questions the Brain must answer
1. Which decisions recur often enough to justify reuse?
2. Is the pattern semantically stable across contexts or only visually similar?
3. What behavior and accessibility guarantees belong to the reusable primitive?
4. Which parts are tokens, primitives, composed patterns or application-specific workflows?
5. Who owns changes, deprecation and migration?
6. What variants are justified by real use cases?
7. What would break if the pattern were promoted too early?
8. Which local exceptions should remain local?

## Workflow
1. **Inventory repeated decisions.** Group by semantics and behavior, not screenshot resemblance.
2. **Classify scope.** Use Local → Extended → Core based on actual reuse and stability.
3. **Define contract.** Specify purpose, supported states, behavior, accessibility, content constraints and extension points.
4. **Separate token from component.** Put visual constants in tokens; do not create components for every styling combination.
5. **Validate variants.** Each variant needs a distinct use case; remove cosmetic duplication.
6. **Test composition.** Ensure primitives can combine without conflicting state, focus or spacing assumptions.
7. **Define ownership.** Assign maintainer, review path and release/version policy.
8. **Define migration.** Promotion or breaking change needs adoption steps, compatibility window and deprecation signal.
9. **Document examples and anti-examples.** Show when not to use the pattern.
10. **Measure reuse and exceptions.** Frequent overrides are evidence of a wrong abstraction.

## Decision rules
- Similar appearance does not prove shared semantics.
- A Core component must carry stronger accessibility and regression guarantees than a Local pattern.
- Reusable components should encode stable behavior, not product-specific business rules.
- Escape hatches are allowed but tracked; repeated escape-hatch use triggers contract review.
- Promotion requires evidence of reuse and semantic stability, not senior preference.
- Deprecation must be explicit; silent replacement creates hidden divergence.

## Evidence standard
Promotion decisions cite real usages, failure history, accessibility evidence and migration cost. Provenance and lifecycle metadata are part of the knowledge asset.

## Canonical outputs
Pattern catalog; token definitions; component contracts; scope tier; owner; usage guidance; accessibility states; migration/deprecation notes; UDRs.

## Failure modes
Component zoo; globalizing one-off screens; copy-paste forks; style-only components with no semantic contract; breaking changes with no migration; design-system team becoming approval bottleneck; inaccessible primitives replicated everywhere.

## Exit conditions
A reusable pattern is ready when its semantics, states, accessibility and ownership are stable enough for its declared scope, and consumers know when to use or avoid it.

## Handoff
Stage 12 consumes implementation-ready component contracts. Stage 25 governs provenance, lifecycle and supersession of shared design knowledge.
