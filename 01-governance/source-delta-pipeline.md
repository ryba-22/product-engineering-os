# Source Delta Pipeline

The Source Delta Pipeline turns a new, changed, removed or re-verified source into an explicit knowledge-governance decision. It prevents publication date, prestige or a metadata refresh from silently rewriting active guidance.

## WHEN

Run this pipeline whenever a registered source is added, removed, materially changed, re-verified after a meaningful upstream revision, or found to conflict with an active claim. Also run it when a source change is discovered through research, production learning, an incident, a standards/vendor update or a corpus refresh.

A successful freshness check alone is not a semantic delta assessment.

## INPUT

Minimum inputs:

- baseline and candidate source registry;
- baseline and candidate evidence ledger;
- the actual old/new source content or inspectable source notes when semantic meaning may have changed;
- downstream project context for consequential decisions.

The detector can identify registry changes and impacted evidence. It cannot infer semantic truth from metadata, so semantic classification remains an explicit assessment.

## FLOW

1. Detect. Compare source records plus source-registry/evidence-ledger metadata and emit ADDED, REMOVED or CHANGED events with immutable input hashes. Registry-level metadata uses the reserved `SOURCE-REGISTRY` delta; unattributed ledger-only changes use `EVIDENCE-LEDGER`.
2. Trace impact. Resolve every evidence claim that cites the source and locate downstream contracts/consumers that reference those evidence IDs. Evals remain visible; raw executor/judge result artifacts are excluded as noise.
3. Inspect content. Compare the actual old/new source meaning, scope, population, technology/version, method and authority. Do not classify from title/date/prestige alone.
4. Classify the semantic delta. Use exactly one:
   - SUPPORT — materially reinforces an existing claim without changing its scope;
   - SCOPE — narrows or qualifies where an existing claim is valid;
   - EXTEND — adds a compatible claim, context or applicability;
   - CHALLENGE — creates unresolved tension requiring review before continued use;
   - FALSIFY — provides sufficient scoped evidence that an existing claim should not remain active as stated;
   - NO_MATERIAL_CHANGE — inspected change does not alter operational meaning.
5. Assess downstream impact. Review all affected active/verified evidence and any decisions, tests, evals or playbooks that consume it.
6. Resolve deliberately. Record rationale, reviewed evidence IDs and downstream actions. CHALLENGE and FALSIFY never auto-promote or auto-delete old knowledge.
7. Promote/supersede. Change lifecycle state only after the delta record is READY. Preserve old records and explicit replacement links.
8. Revalidate behavior. If the changed knowledge affects a behavioral maturity claim, routing rule, gate or consequential project policy, run the smallest relevant eval before closure.

## OUTPUT

Canonical output is a Source Delta Report conforming to 01-governance/source-delta.schema.json. A report contains observed baseline/head commit SHAs, SHA-256 hashes of both source registries and evidence ledgers, the candidate evidence-ID/status set, changed-source records, a point-in-time downstream blast-radius snapshot, semantic assessment and a BLOCKED/READY promotion gate.

READY reports that authorize a repository source/evidence change are committed under 01-governance/source-deltas/. CI compares the actual base→head knowledge state and requires a matching READY report whenever a delta exists. A report commit may follow the source/evidence commit because the report is bound to the unchanged registry/evidence hashes rather than to documentation-only commit identity.

UNASSESSED is a detector state, not a semantic conclusion.

## EVIDENCE

A delta can be READY only when:

- semantic classification is explicit;
- rationale names the actual source/content comparison;
- all affected active or verified evidence claims were reviewed;
- classification/resolution is allowed by policy;
- SCOPE, CHALLENGE and FALSIFY have concrete downstream actions;
- FALSIFY resolved by supersession names replacement evidence that exists in the candidate evidence ledger; an optional decision record must resolve to a concrete file;
- removed sources supporting live evidence are not closed as no-op;
- input hashes remain intact.

The machine policy is machine/source-delta-policy.json.

## STOP

Stop and keep the delta BLOCKED when source content is unavailable, applicability is unclear, affected evidence has not been reviewed, or the team cannot distinguish contextual disagreement from contradiction.

Do not manufacture consensus and do not change active global knowledge to satisfy one project-local constraint.

The pipeline is change-triggered, not a crawler: if an external page changes at the same URL and no registry/evidence metadata changes, CI cannot discover that fact by itself. Re-verification must update an inspectable registry revision signal such as verified_at (and a source version/fingerprint when the corpus records one), which then creates the delta to assess.

## HANDOFF

- SUPPORT / NO_MATERIAL_CHANGE: freshness/evidence governance may close with retained provenance.
- SCOPE / EXTEND: update or add atomic evidence and re-check consumers.
- CHALLENGE: hand off to a decision record or targeted research/eval; active guidance remains visibly challenged.
- FALSIFY: create explicit supersession/deprecation plus downstream migration/revalidation.
- Project-local disagreement: create a scoped project override rather than mutating the global rule.

## CLI

Detect registry/evidence deltas between Git refs after committing the candidate knowledge change:

    python3 scripts/source_delta.py detect --base-ref origin/main --head-ref HEAD --output 01-governance/source-deltas/SDL-YYYY-MM-DD-NN.json

The detector resolves both refs to immutable commit SHAs. Inspect the actual source content, then apply reviewed assessments to the report. An assessment file contains source_id plus classification, rationale, reviewed_evidence_ids, downstream_actions, resolution and any replacement_evidence_ids / decision_record required by policy.

Validate closure readiness before committing the report:

    python3 scripts/source_delta.py validate --report 01-governance/source-deltas/SDL-YYYY-MM-DD-NN.json --require-ready

CI then enforces the same base→head contract through:

    python3 scripts/source_delta.py gate --base-ref BASE_SHA --head-ref HEAD_SHA

See 01-governance/source-deltas/README.md for the two-commit evidence workflow.

The detector deliberately fails to assign SUPPORT/SCOPE/EXTEND/CHALLENGE/FALSIFY by itself. That is the safety boundary between structural diffing and semantic judgment.
