# Stage 25 — Knowledge governance

**Module:** knowledge-governance  
**Gate:** continuous  
**Evidence anchors:** EVD-GOV-001, EVD-GOV-002  
**Primary systems:** source registry, evidence ledger, decision records, maturity/evals

## Purpose
Keep the Product Engineering OS and project knowledge trustworthy over time. Reusable guidance needs provenance, scope, lifecycle, conflict handling, freshness and explicit supersession; otherwise an expanding corpus becomes a pile of contradictory notes.

## Required inputs
Source registry, evidence ledger, decision records, stage outputs, eval results, external specialist assets, project overrides, incident/outcome learning and source/update dates.

## Questions the Brain must answer
1. Where did this rule or claim come from?
2. What scope/population/technology/version does it apply to?
3. How strong is the evidence and what are its limitations?
4. Is the source still current enough for the decision?
5. Does new evidence conflict with an active claim or decision?
6. Which record supersedes which and why?
7. Which knowledge belongs globally versus project-local override?
8. Can behavior be evaluated, not merely structural presence?

## Workflow
1. **Register sources.** Record authority tier, domain, URL/location, verification date and cutoff policy.
2. **Atomize evidence.** Store one inspectable claim per record with scope, strength, limitation and source IDs.
3. **Promote deliberately.** Candidate → Verified → Active only when provenance and scope are adequate.
4. **Record material decisions.** Link evidence, options, trade-offs, validation and revisit triggers.
5. **Handle conflicts explicitly.** Keep competing claims until scope/time/method resolves the difference.
6. **Supersede, do not erase.** Preserve history and link replacement records.
7. **Separate global from local.** Project constraints may override general guidance without rewriting the global corpus.
8. **Audit freshness.** Flag sources/claims whose age or version matters.
9. **Evaluate behavior.** Golden/adversarial evals must test decision quality and failure handling, not just keyword/file existence.
10. **Feed learning back.** Production outcomes and incidents can strengthen, narrow or invalidate prior guidance.

## Decision rules
- A source being authoritative does not make every claim universally applicable.
- A later publication date does not automatically supersede older evidence; scope and method matter.
- “Very strong” maturity requires demonstrated behavioral effectiveness, not only files, IDs and green structural tests.
- External specialist brains remain conditional until their exact asset/version is available and reviewed.
- Project-local evidence must not silently contaminate global defaults.
- Deleted history is not governance; use deprecation/supersession for material knowledge.

## Evidence standard
Every active reusable claim has provenance, scope, status, verification date and limitations. Material decision records have evidence links and observable revisit triggers. Behavioral maturity claims require executed eval evidence.

## Canonical outputs
Source registry; evidence ledger; decision graph; supersession links; freshness report; conflict register; project overrides; executed eval results; maturity report grounded in observed behavior.

## Failure modes
Link dump without atomic claims; stale source treated as current; duplicated contradictory rules; “verified” with no verification method; maturity declared from counts; external corpus claimed but unavailable; global rule changed to satisfy one project.

## Exit conditions
This stage never permanently closes. A governance cycle is complete when new/changed knowledge has provenance, status and scope; conflicts are recorded; superseded items are linked; freshness is evaluated; and any maturity claim states what was actually tested.

## Handoff
All stages consume Active evidence and decisions. Every stage returns new validated learning, failed assumptions and supersession candidates to governance.
