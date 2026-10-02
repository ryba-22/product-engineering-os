# Stage 10 — Visual UI

**Module:** experience  
**Gate:** G5  
**Evidence anchors:** EVD-UI-001, EVD-UI-002  
**Primary outputs:** visual hierarchy rules, density/layout decisions, visual UDRs

## Purpose
Turn information architecture and interaction behavior into a coherent visual system that improves comprehension, prioritization and perceived quality. Visual design is functional: hierarchy, spacing, typography, color and depth tell users what matters and what belongs together.

## Required inputs
UX architecture, interaction contracts, accessibility constraints, real content/data density, brand constraints, design-system primitives and representative viewport targets.

## Questions the Brain must answer
1. What information deserves primary, secondary and supporting emphasis?
2. Which relationships should be expressed by spacing before borders or containers?
3. What density matches the work: scanning, comparing, editing or reading?
4. Which typography scale supports hierarchy without excessive variation?
5. What colors carry semantic meaning and what alternatives exist without color?
6. Which surfaces need depth/elevation and why?
7. How does the visual structure transform across widths?
8. Does the screen remain understandable with realistic long/empty/error content?

## Workflow
1. **Design from hierarchy.** Rank information and actions before styling individual components.
2. **Establish constrained scales.** Reuse a small set of spacing, type, radius and depth tokens.
3. **Use proximity first.** Group related information with spacing and alignment; add containers only when they clarify boundaries.
4. **Set density intentionally.** Enterprise comparison/worklist screens may be dense; reading and decision pages need breathing room.
5. **Define action emphasis.** One visual primary action per decision context unless the task truly has peers.
6. **Apply semantic color.** Status/error/success/warning usage must be consistent and accessible.
7. **Handle edge content.** Test long names, zero data, large counts, validation, disabled states and localization expansion.
8. **Review wide and narrow screens.** Avoid both cramped mobile layouts and wasteful ultra-wide whitespace.
9. **Compare against existing product language.** Reuse established patterns when they still fit.
10. **Record visual decisions that affect reusable rules.**

## Decision rules
- Visual hierarchy should be achieved primarily through size, weight, spacing and placement before adding color or boxes.
- Repetition should become a token/pattern rather than hand-tuned per screen.
- More whitespace is not automatically more professional; density must match task frequency and information comparison needs.
- Decorative gradients, shadows or oversized cards need a functional reason in utilitarian workflows.
- Empty states should explain what the state means and the next useful action when one exists.
- Tables should remain tables when row/column comparison is the task.

## Evidence standard
Visual decisions derive from task structure, accessibility constraints, established product conventions and realistic content. Aesthetic preference alone is not evidence for a consequential layout change.

## Canonical outputs
Hierarchy map; spacing/type/color/depth rules; density decision; responsive visual behavior; empty/error visual treatment; token requests; visual UDRs and review screenshots.

## Failure modes
Card-everything design; arbitrary spacing; too many font sizes; color as the only status cue; desktop canvas with narrow content stranded in the center; hiding information to make screenshots look cleaner; design-system token drift.

## Exit conditions
Visual UI is ready when hierarchy is immediately legible, repeated decisions use consistent tokens, realistic states fit without collapse, accessibility constraints remain satisfied and implementation can reproduce the design without per-screen invention.

## Handoff
Stage 11 decides what becomes reusable design-system policy. Stage 12 receives tokens, layout rules and state visuals alongside interaction semantics.
