# Stage 09 — Accessibility

**Module:** experience  
**Gate:** G5  
**Evidence anchors:** EVD-UX-001, EVD-QA-003  
**Primary standards:** WCAG 2.2, WAI-ARIA Authoring Practices where native semantics are insufficient

## Purpose
Treat accessibility as a cross-cutting quality property of structure, interaction, content and verification. The target is operable, understandable and robust task completion, not merely passing an automated scanner.

## Required inputs
UX and interaction contracts, supported browser/device policy, component choices, content, forms, error states, keyboard/focus expectations and critical user flows.

## Questions the Brain must answer
1. Can every critical task be completed with keyboard only?
2. Are native semantics used before ARIA?
3. Is focus order predictable and focus moved only when interaction semantics require it?
4. Are names, roles, values and states exposed correctly?
5. Are errors identifiable, associated with fields and recoverable?
6. Do color, contrast and non-color cues preserve meaning?
7. Does zoom/reflow preserve task completion?
8. Which critical flows require manual assistive-technology verification?

## Workflow
1. **Start with semantic structure.** Use correct headings, landmarks, labels, buttons, links, lists, tables and form controls.
2. **Define keyboard model.** Include tab order, roving focus where appropriate, escape/cancel behavior and shortcuts.
3. **Define focus lifecycle.** Specify focus after dialogs open/close, validation errors, route changes and dynamic insertion.
4. **Validate forms and errors.** Ensure instructions, required state and error relationships are programmatically available.
5. **Check visual accessibility.** Contrast, focus visibility, target size, text resizing, reflow and motion preferences.
6. **Check dynamic announcements.** Use live regions only for changes that users need announced; avoid noisy duplication.
7. **Run automated checks.** Use them as fast defect detection, not certification.
8. **Run manual keyboard verification.**
9. **Run assistive-technology checks for critical/novel flows.**
10. **Record exceptions and remediation ownership.**

## Decision rules
- Prefer native HTML semantics over custom ARIA widgets.
- ARIA does not add behavior automatically; keyboard and state synchronization are still required.
- Placeholder text is not a label.
- Color alone must not encode a required distinction.
- A modal must manage focus entry, containment where appropriate and return.
- Automated accessibility success cannot close a critical-flow accessibility gate by itself.

## Evidence standard
For ordinary flows combine semantic review, automation and keyboard testing. For critical or custom interactions add manual assistive-technology verification proportional to risk and supported environments.

## Canonical outputs
Accessibility contract; semantic/component requirements; keyboard/focus matrix; automated scan results; manual verification record; known exceptions with owners; accessibility acceptance criteria.

## Failure modes
ARIA-first implementation; inaccessible custom controls; positive axe scan treated as proof; missing focus indicator; focus jumps after async updates; visually hidden status with no announcement; table semantics replaced by layout divs.

## Exit conditions
Accessibility is ready when critical tasks are keyboard operable, semantics and focus behavior are explicit, material WCAG risks have evidence, and unresolved defects have ownership rather than being silently accepted.

## Handoff
Stage 10 preserves hierarchy and contrast. Stage 11 ensures reusable components encode accessibility. Stage 12 implements and Stage 15 verifies critical flows.
