# Memory ↔ Knowledge Base Contract

## Purpose

Conversation memory, agent summaries and recalled project context are useful because they reduce repeated discovery. They are not durable evidence by themselves. This contract defines when remembered context may guide work, when it must be verified, how conflicts are resolved and how useful learning becomes canonical knowledge.

The core boundary is:

`memory ≠ evidence`
`recollection ≠ project state`
`context ≠ canonical knowledge`

Memory is an **index and continuity mechanism**. The knowledge base and project repositories are the **auditable decision surface**.

## Memory classes

- **CURRENT_INPUT** — information explicitly stated by the user in the current interaction.
- **SESSION_CONTEXT** — facts and decisions visible in the current working session.
- **RETRIEVED_MEMORY** — remembered or retrieved context from earlier interactions.
- **AGENT_SUMMARY** — a compressed handoff produced by an agent or workflow.

Compression can remove qualifiers, dates, scope and uncertainty. A summary is therefore not automatically equivalent to the evidence it summarizes.

## Claim classes

### User intent
Current explicit user intent, preference and requested scope may be used directly for that intent. A repository must not override what the user is currently asking for.

This exception is narrow: “I want X” can be authoritative for intent; “production is currently on version X” is still a project fact and must be verified when consequential. Decision-ready intent is **not** authorization to execute a consequential action and does not bypass capability, approval or security controls.

### Project or system fact
Examples: current branch, deployed SHA, database schema, production behavior, open incident, current configuration. Prefer the most current inspectable project/runtime evidence. Memory may tell the agent **where to look**, not what to declare as current truth.

### Project decision
A remembered decision should resolve to the durable decision record, issue, accepted specification, code contract or other canonical project artifact before it is relied on materially. If no artifact exists, the decision is remembered context and must be labeled as such.

### Reusable guidance
Reusable rules, methods and heuristics belong in governed knowledge. A remembered rule does not become Active guidance through repetition. Promotion requires provenance, scope, verification and the normal knowledge lifecycle.

### Historical context
Low-risk historical context may be used as context when it is clearly non-decision-making. If it changes a current decision, it stops being “just context” and requires corroboration.

## Canonical precedence

Precedence depends on the kind of claim rather than one global ranking.

| Claim | Preferred authority |
|---|---|
| current user intent/scope | latest explicit current user input |
| current runtime/system state | direct runtime/data evidence |
| current implementation | project repository at the relevant ref |
| accepted project decision | project decision record/specification |
| reusable engineering guidance | Active governed knowledge + supporting evidence |
| historical recollection | durable historical artifacts, then memory as labeled context |

A newer memory or newer document does not automatically supersede a stronger scoped source. Scope, authority, time and evidence quality still matter.

## Decision algorithm

For every decision-relevant remembered claim:

1. Classify the claim and risk.
2. Ask whether it is current intent or an objective/project fact.
3. Resolve canonical references when they exist.
4. Compare memory with canonical evidence.
5. Use one of five outcomes:
   - **DECISION_READY** — current intent, or corroborated by canonical evidence.
   - **CONTEXT_ONLY** — useful orientation, but not admissible as the basis of a decision.
   - **VERIFY_REQUIRED** — verification is required before material use.
   - **BLOCKED** — an unresolved conflict or high-risk unsupported claim prevents progression.
   - **PROMOTION_REQUIRED** — useful remembered knowledge should be made durable before reuse as policy.
6. Record conflict rather than silently picking the convenient version.
7. Continue only to the lifecycle state supported by evidence.

## Risk rule

For R3/R4 work, or work involving money, identity/authorization, production data mutation, irreversible migration, external contracts, security or recovery guarantees, unsupported remembered project facts fail closed. The correct state is **BLOCKED**, not “probably correct.”

For lower-risk work, unsupported memory may be **VERIFY_REQUIRED** or **CONTEXT_ONLY**, depending on whether it affects the decision.

## Conflict protocol

When memory conflicts with canonical evidence:

1. preserve the remembered claim as context;
2. prefer current inspectable evidence for current-state claims;
3. verify that the apparent conflict is not a scope/date/environment mismatch;
4. if the canonical artifact is stale, update it through its normal owner and lifecycle rather than treating memory as a silent override;
5. if the user explicitly corrects intent or scope, apply the correction to intent immediately, while independently verifying any attached objective fact;
6. for material unresolved conflicts, stop at **BLOCKED**.

Absence from memory is never evidence that something does not exist. Likewise, a remembered item missing from the repository is not proof that the repository is wrong.

## Promotion from memory to knowledge

Promotion is an explicit write path:

`MEMORY → CLAIM → PROVENANCE → SCOPE → VERIFICATION → DURABLE ARTIFACT → GOVERNANCE`

For project-local truth, the target is normally the project repository: decision record, contract, test, runbook, evidence or code. For reusable cross-project guidance, the target is the appropriate knowledge repository and its lifecycle.

A **USER_INTENT** record may be persisted as a project-local instruction or decision input, but no USER_INTENT record—current, retrieved or summarized—can directly become global reusable knowledge. Promotion to the Knowledge Base requires a **separate claim** classified for reusable guidance and corroborated by canonical evidence, with declared scope and provenance.

For a Knowledge Base promotion, whether the candidate changes existing Active guidance is itself required evidence. If `changes_active_guidance` has not been assessed, the promotion remains `PENDING_EVIDENCE`; it cannot reach owner review. If it is true, `source_delta_required=true` and the Source Delta Pipeline is mandatory before the Active guidance can change.

Promotion must not manufacture provenance. If the original evidence cannot be recovered, preserve the claim as a hypothesis or operational note until independently verified.

If promotion changes existing Active reusable guidance, the **Source Delta Pipeline** applies before supersession or promotion.

## Corrections and forgetting

Correcting or forgetting conversational memory does not mutate project repositories or governed knowledge automatically. Durable knowledge must be changed through its own owner and evidence path. Conversely, changing a repository does not guarantee every remembered summary has already refreshed.

The safe model is explicit reconciliation, not assumed synchronization.

## Machine guard

`machine/memory-knowledge-policy.json` defines protected rules and statuses.
`01-governance/memory-knowledge.schema.json` defines the claim record.
`scripts/memory_knowledge_guard.py` validates a claim and returns the admissibility status.

Example:

```bash
python3 scripts/memory_knowledge_guard.py check claim.json
```

The guard is deliberately conservative. It enforces **structural admissibility from the declared claim classification**; it does not resolve a canonical reference or prove that the referenced evidence semantically supports the claim. A declared `SUPPORTS` relation is therefore an explicit assessment that remains auditable, not automated proof.

The output separates claim use from execution authority: `action_authorized` is always `false`. Promotion has its own machine gate (`NOT_REQUESTED`, `BLOCKED`, `PENDING_EVIDENCE`, `READY_FOR_OWNER_REVIEW`) and requires declared scope plus provenance before it can reach owner review. A blocked claim is never instructed to persist.

Promotion decisions are inspectable as data, not only prose: the output exposes `promotion_scope`, `promotion_provenance_refs`, `missing_promotion_inputs` and `source_delta_required` (`true`, `false` or `UNKNOWN`). `UNKNOWN` blocks Knowledge Base promotion at `PENDING_EVIDENCE`.

CLI exit codes are fail-closed: `0` only when the claim is `DECISION_READY` **and**, if promotion was requested, its promotion gate is `READY_FOR_OWNER_REVIEW`; `3` for every valid but non-ready claim or promotion state, including `CONTEXT_ONLY` and `PENDING_EVIDENCE`; `2` for an invalid record. None of these codes authorizes a consequential tool action.

JSON with duplicate object keys is invalid rather than parser-dependent. Canonical references are also restricted to declared canonical URI classes; conversational provenance may be recorded as provenance, but a `chat://` pointer is not canonical support.

## Closure

The boundary is working when an agent can answer three questions for every material remembered claim:

1. **What exactly is remembered?**
2. **What durable evidence confirms or contradicts it?**
3. **What is the strongest lifecycle state we may claim now?**

Memory provides continuity. Canonical knowledge provides accountability.
