# Stage 07 — UX Architecture

**Module:** experience  
**Gate:** G5  
**Evidence anchors:** EVD-UX-002, EVD-UX-003  
**Primary decision system:** Experience Brain and verified UI Brain integrations when supplied

## Purpose
Define how users move through the product, where state and decisions are exposed, and how the interface supports real tasks across happy paths, interruptions and recovery. UX architecture precedes visual styling and component selection.

## Required inputs
Validated user scenarios, domain concepts, requirements, actor/permission model, information constraints, device/context constraints, risk class and existing product navigation patterns.

## Questions the Brain must answer
1. What are the user’s highest-value tasks and decision points?
2. What information must be visible together to complete each task?
3. Which objects, workflows or statuses deserve first-class navigation?
4. Where can users safely pause, resume, back out or recover?
5. Which states are transient, persisted, stale, conflicting or externally controlled?
6. How does the structure adapt across desktop/mobile or constrained contexts?
7. Which actions are destructive, consequential or permission-sensitive?
8. What information architecture reduces switching and hidden state?

## Workflow
1. **Model task flows before screens.** Capture trigger, goal, decisions, required information and end state.
2. **Identify product objects and worklists.** Use domain/user language rather than implementation entities where they differ.
3. **Design navigation around frequency and consequence.** Separate global areas, local object context and transient tasks.
4. **Define state visibility.** Users must be able to tell what exists, what changed, what is pending and what requires action.
5. **Specify non-happy paths.** Loading, empty, partial, error, stale, conflict, permission denied, timeout and recovery states are part of the architecture.
6. **Define adaptive transformations.** Mobile is not desktop squeezed narrower; decide what reorders, collapses, becomes a card or moves behind progressive disclosure.
7. **Model cross-flow continuity.** Preserve filters, context, drafts or return paths when the task requires it.
8. **Review consequence and reversibility.** Add confirmation only where error cost and reversibility justify friction.
9. **Record UDRs for consequential structure.**
10. **Validate with representative tasks.** Use realistic data density and edge conditions.

## Decision rules
- A page should exist because it supports a coherent task/object context, not because a backend resource exists.
- Navigation labels use user/domain language; internal architecture names require translation when they are not user concepts.
- Hidden state that materially changes an action must be surfaced.
- Dense enterprise workflows can favor tables/worklists when comparison and batch action matter; cards are not automatically more usable.
- Responsive behavior is a transformation decision, not a CSS breakpoint afterthought.
- If a workflow cannot explain its error/conflict recovery, it is not design-complete.

## Evidence standard
Task architecture should trace to observed workflows, validated scenarios or explicit operational requirements. Pattern choice may reuse established product conventions when they fit the same task and constraints.

## Canonical outputs
Context-of-use summary; information architecture; task/workflow map; screen/archetype map; state/recovery matrix; responsive/adaptive rules; UDRs; unresolved usability risks.

## Failure modes
Sitemap from database entities; mobile as compressed desktop; modal chains; dashboard-first design with no decisions; hidden pending states; destructive actions without consequence model; happy-path-only flows.

## Exit conditions
The UX architecture is ready when critical tasks have a coherent path, state and recovery are visible, adaptive behavior is explicit, and interaction design can proceed without inventing product structure.

## Handoff
Stages 08–11 refine interactions, accessibility, visual hierarchy and reusable patterns. Stage 12 receives explicit workflow/state contracts rather than screenshots alone.
