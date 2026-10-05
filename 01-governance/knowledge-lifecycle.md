# Knowledge lifecycle

Every source, evidence claim, reusable rule, pattern and decision has an independent lifecycle:

`Candidate → Verified → Active → Superseded → Deprecated → Archived`

The lifecycle prevents the corpus from becoming a flat collection where newer notes silently overwrite older decisions.

## Candidate

A Candidate may be useful but is not yet trusted for consequential decisions. Record provenance, scope, date/version and why it was added. Candidate claims may guide investigation but should not be presented as established policy.

## Verified

Promote to Verified when the source/claim has been checked for identity, scope and fidelity. Verification does not mean universal truth; limitations and population/technology/version boundaries remain part of the record.

## Active

Active means the item is currently approved for its declared scope. Promotion requires:

- traceable source/provenance;
- explicit scope and material limitations;
- no unresolved contradiction that invalidates the intended use;
- current-enough verification for the decision;
- owner or governance path when the rule is operationally significant.

## Superseded

Use Superseded when a newer record intentionally replaces the item. Preserve the old record and link both directions: what supersedes it, why, and from which date/version/scope. Never erase history merely to keep the corpus “clean.”

A newer publication date alone is insufficient. Supersession depends on scope, authority, evidence quality and compatibility.

## Deprecated

Deprecated items are still understandable and may remain in historical projects, but new work should not adopt them. Record migration guidance or the preferred replacement when one exists.

## Archived

Archived items are retained for provenance but excluded from normal routing. Archiving is appropriate when the item is no longer operationally useful and no active decision depends on it.

## Conflict protocol

When two credible claims conflict:

1. keep both records;
2. compare scope, population, version, method and authority;
3. identify whether the disagreement is real or contextual;
4. narrow each claim if both are valid in different contexts;
5. create a decision record if the project must choose under unresolved uncertainty;
6. do not manufacture consensus.

## Source delta gate

A new, changed, removed or materially re-verified source must pass the [Source Delta Pipeline](source-delta-pipeline.md) before it can silently change Active guidance. The detector traces structural change and downstream evidence impact, but semantic classification remains explicit: `SUPPORT`, `SCOPE`, `EXTEND`, `CHALLENGE`, `FALSIFY` or `NO_MATERIAL_CHANGE`.

Until affected live evidence has been reviewed and the delta record reaches `READY`, promotion or supersession remains blocked. `CHALLENGE` and `FALSIFY` preserve the existing record and require an explicit resolution path rather than mutation-by-overwrite.

## Memory ingress

Conversation memory, agent summaries and remembered project context are not an additional lifecycle state. They enter governance as retrieval hints or Candidate claims until corroborated. Current explicit user intent is authoritative for requested intent/scope, but attached objective project facts still require verification when decision-relevant.

Use the [Memory ↔ Knowledge Base Contract](memory-knowledge-contract.md) to classify remembered claims. R3/R4 decisions fail closed when a remembered project fact lacks canonical evidence. Promotion into durable project or reusable knowledge requires provenance, scope and verification; promotion that changes Active reusable guidance also passes the Source Delta Pipeline.

## Project overrides

Global guidance and project-local decisions are separate layers. A project may override an Active global rule because of a concrete constraint, but the override must name scope, rationale and revisit trigger. It must not mutate the global rule for every future project.

## Freshness

Freshness is risk-sensitive. Standards/versioned APIs, security guidance, vendor behavior and fast-moving platform rules may require more frequent verification than stable conceptual methods. `verified_at` records when the source/claim was checked; it does not imply new claims after a frozen corpus cutoff were imported.

## Promotion and behavioral evidence

File presence or a successful schema check can support structural validity only. Promotion of behavioral guidance should be informed by executed evals, worked examples, production outcomes or other evidence appropriate to the claim.

Stage 25 governs this process continuously.
