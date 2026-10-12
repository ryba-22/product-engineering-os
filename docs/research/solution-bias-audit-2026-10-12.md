# Solution Bias Audit — selected cross-project evidence

**Date:** 2026-10-12  
**Status:** Evidence-limited, representative audit of available project sources. Not a complete historical/production effectiveness study.  
**Purpose:** detect unsupported defaults in AI-assisted recommendations, distinguish them from justified reuse, and route a proportionate decision method into the existing PEOS operating system.

## Finding

**HYPOTHESIS:** the most consequential recurring risk is *recommendation anchoring*: choosing a familiar UI component, architectural mechanism or governance procedure before defining the task and testing alternatives. This was observed as a risk in earlier assistant proposals and process discussions, not proven as the cause of every implemented design.

**FACT:** PEOS already requires evidence, trade-off evaluation, proportional risk controls and stop-analysis. The missing emphasis was an explicit bias diagnostic across UX, domain, architecture and process, including the **zero option**, falsification and critical multi-perspective challenge. Creating a separate framework would itself risk accidental complexity.

## Evidence map

| ID | Project / observed source | What evidence establishes | Classification and verdict |
|---|---|---|---|
| SB-01 | [LINKI README](https://github.com/ryba-22/LINKI/blob/main/README.md), [AGENTS](https://github.com/ryba-22/LINKI/blob/main/AGENTS.md) | A private, offline searchable catalog with `data/links.json` as source of truth. Prior assistant conversations floated richer detail/backend/monitoring ideas; their necessity was not established. | **HYPOTHESIS — unexamined default.** KEEP CURRENT SOLUTION; experiment before adding more state/services. |
| SB-02 | [CRD Finance Task 3](https://github.com/ryba-22/CRD-Finance/blob/main/docs/ui/implementation/TASK_3_PUPIL_UNITS_COMPOSITION.md), [Task 3B](https://github.com/ryba-22/CRD-Finance/blob/main/docs/ui/implementation/TASK_3B_QUEUE_SELECTION_STATE.md) | Queue selection is URL-owned and authorization-scoped; desktop modal Drawer was replaced by a nonmodal Inspector; mobile uses full-screen detail. Documented browser/accessibility contracts justify key constraints. | **FACT — justified reuse candidate**, not proof of bias. KEEP CURRENT SOLUTION pending task-based operator evidence. |
| SB-03 | [CRD Finance issue #258](https://github.com/ryba-22/CRD-Finance/issues/258), [PR #276](https://github.com/ryba-22/CRD-Finance/pull/276), [PR #280](https://github.com/ryba-22/CRD-Finance/pull/280) | Reviewer/evidence rules were repeatedly debated; the owner waived unavailable GitHub reviewers for specific work, while keeping separate safety/release concerns. Issue status text and GitHub state diverged at inspection. | **HYPOTHESIS — accidental process complexity** in parts; do not label all R3/R4 controls unnecessary. RECOMMEND WITH CONDITIONS: reuse risk-specific existing gates. |
| SB-04 | [WieniawskiApp PR #70](https://github.com/ryba-22/WieniawskiApp/pull/70) | Changing allocation could also change the source requirement; review corrected write ownership without schema migration. Separate endpoint alone had not separated responsibility. | **FACT — problem-led domain correction.** KEEP the requirement/entitlement boundary. |
| SB-05 | [WieniawskiApp PR #77](https://github.com/ryba-22/WieniawskiApp/pull/77) | Urgent formal-application MVP deliberately separates submission from enrollment and financial charge; DB/security/E2E remained unverified at inspection. | **FACT — justified scope reduction.** VERIFY BEFORE RELEASE; do not enlarge scope by default. |
| SB-06 | [Excel Workbook Analyzer](https://github.com/ryba-22/excel_audit/blob/main/README.md) | Local, standard-library analyzer explicitly avoids modifying originals and documents heuristics and format limits. | **FACT — simplicity counterexample.** KEEP CURRENT APPROACH without an evidenced need for services. |
| SB-07 | [Harmonogramy](https://github.com/ryba-22/harmonogramy) | Repo discovered; relevant root docs were unavailable on inspection. User decisions establish domain constraints, not implementation evidence. | **INSUFFICIENT EVIDENCE** to attribute recommendation bias. |
| SB-08 | [Engineering Knowledge Hub routing](https://github.com/ryba-22/engineering-knowledge-hub/blob/main/docs/ROUTING.md), [PEOS protocol](../06-modules/system-architecture/DECISION-PROTOCOL.md) | Reusable methods belong in PEOS; UX research and product-specific decisions remain with their owners. Existing decision standards already cover alternatives and risks. | **FACT — existing safeguard.** Extend PEOS instead of duplicating governance. |

**Evidence discipline:** repository/PR text proves a recorded decision or stated result, not necessarily deployment, operational success, user benefit or causation by AI bias. An issue description labeled OPEN while GitHub reports CLOSED is a source-conflict flag, not a reason to choose one silently. No actual named team member approved this audit; the "SZTAB" perspectives below are analytical lenses.

## Alternative evaluation — not a universal ranking

### A. Reviewing many records

**Problem:** operators need to understand or compare details, with possible repeated selection and return.

| Option | When credible | Main downside |
|---|---|---|
| 0 — Improve the table row / no new view | Detail demands are small and brief | May become too dense |
| Inline expansion | Local inspection while maintaining row position | Reflow, weak comparison across many rows |
| Dedicated detail page | Deep reading/editing, shareable destination | Navigation/context switching |
| Modal | Short, isolated consequential task | Blocks collection scanning |
| Nonmodal master-detail / Inspector | Frequent record-to-record inspection | Width, keyboard/focus/mobile state complexity |

**Verdict:** No universal preferred component. In CRD Finance existing URL/authorization/focus contracts make the current Inspector credible; verify actual operator task efficiency before reworking it. In LINKI, retain simple list/search until interaction evidence changes the decision.

### B. Recoverable long-running operation

Compare **(0) remove/simplify the long operation; synchronous step with checkpoint; database job + worker; message broker; workflow engine**. Differentiate retry/idempotency, transactional boundaries, scale, operational maturity, failure recovery and team ownership. A queue is warranted by buffering/decoupling requirements, not because "asynchronous" sounds sophisticated. Do not require 5 options where only 2 are plausible.

### C. More process gates

Compare **(0) existing controls unchanged; improve existing tests/evidence; focused risk-specific review; new enforceable gate**. Evaluate escaped defect, false-positive cost, ownership, availability of reviewers, ability to enforce and verification of actual runtime consequences.

**Verdict:** Don't create a new mandatory approval layer in PEOS. Strengthen a project-specific control only for a named risk which current controls cannot adequately manage.

## Multi-perspective challenge

- **Product/domain perspective (analytical):** Is the actual user outcome improved; is the work solving a symptom; what must remain invariant?
- **Architecture/engineering perspective (analytical):** Are ownership, consistency, recovery, coupling and locality of change proportionate; which smaller option could work?
- **UX/interaction perspective (analytical):** Does the flow support real scanning, comparison, error recovery, navigation and accessibility; does a shared pattern obscure differing tasks?
- **Security/operations perspective when applicable:** Does the proposed option satisfy the existing release/privacy/safety boundary without inventing an unrelated gate?

These are review **perspectives**, not signatures or completed independent reviews by the people sometimes associated with them.

## Decision / permanent contract

**RECOMMEND WITH CONDITIONS:** Keep PEOS as canonical owner; add [Research-first solution selection](../../00-core/research-first-decisions.md) as a short cross-domain rule; link from `AGENTS.md`, the existing decision record and architecture protocol. No new governance framework, mandatory reviewer, CI gate or product refactor. New research must be proportional to decision risk and stop once another source is unlikely to change the selection.

**Validation:** apply to a sample of actual R2+ decisions; check zero option, rejected alternatives, trade-offs, falsification and process overhead. If the rule is ignored or creates ceremony, revise based on observed decisions rather than duplicating standards.

## Limitations and scope

This audit inspected a *sample* of connected repository artifacts and prior conversation evidence. No exhaustive history, deep operational metrics, live user observation, independent usability experiment or complete Harmonogramy implementation review was done. Evidence of repeated implementation is not proof of an unjustified recommendation; passed checks are not evidence of business value. Cross-project outputs remain guidance, not automatic retroactive judgments of released systems.

**STOP:** Documentation-only. No product UI/code changes, financial actions, release, new architecture initiatives, or mandatory project-level reviews.
