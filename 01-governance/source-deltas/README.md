# Source Delta Reports

This directory stores committed Source Delta assessment reports for changes that alter the source registry or evidence ledger. A report is durable evidence that a specific knowledge-state transition was detected, inspected and deliberately classified before Active guidance was changed.

## Required sequence

1. Make and commit the source/evidence change.
2. Detect the delta against the intended base commit:

       python3 scripts/source_delta.py detect \
         --base-ref origin/main \
         --head-ref HEAD \
         --output 01-governance/source-deltas/SDL-YYYY-MM-DD-NN.json

3. Inspect the actual old/new source content. Metadata, publication date and prestige are insufficient to classify meaning.
4. Apply one assessment per changed source until every record is READY. Record the reviewed evidence IDs, rationale, downstream actions and resolution.
5. Validate the report:

       python3 scripts/source_delta.py validate \
         --report 01-governance/source-deltas/SDL-YYYY-MM-DD-NN.json \
         --require-ready

6. Commit the READY report separately.

The detector resolves branch names to concrete commit SHAs observed at assessment time. The authorization boundary is the baseline/candidate source-registry and evidence-ledger hashes plus the detected source/evidence structure. A later documentation-only commit does not invalidate the assessment; a later registry/evidence change does. The recorded commit SHAs are fully re-verified when those commits remain reachable; after a squash merge they may become informational, while CI independently re-detects the current base→head knowledge state before accepting the report.

## What READY means

READY is not a claim that the new source is universally correct. It means the specific source/evidence delta has enough governance evidence to proceed:

- its semantic relationship to existing guidance was explicitly classified;
- every affected claim that was Active or Verified before or after the change was reviewed;
- high-risk deltas have at least one substantive downstream action; a decision record may supplement but never replace that action;
- removed sources cannot be disguised as SUPPORT or EXTEND, and live-source removals cannot close as a rejected/no-op CHALLENGE;
- FALSIFY/supersession keeps historical provenance and names replacement evidence that exists in the candidate ledger;
- the structural facts in the report still match the registry/evidence state that CI sees.

A report stays BLOCKED when any of those conditions is absent.

## CI gate

For pull requests, CI compares the real PR base SHA to the PR branch head SHA. For pushes to non-default branches, it compares the merge-base with the default branch to the pushed head, so the documented two-commit knowledge-change + READY-report workflow remains valid across successive pushes. For pushes to the default branch, it compares the event's previous SHA to the pushed head. Full Git history is fetched so those states can be inspected.

If no source/evidence delta exists, the gate passes. If a delta exists, CI requires a committed READY report whose source/evidence hashes, candidate evidence-ID set and immutable source/evidence change fields match the current candidate state. This means a branch cannot change a source, quietly remove its citation, and then pass only because the final evidence ledger no longer points at it: the detector compares both baseline and head ledgers. `downstream_refs` is retained as review evidence but is not used as the later authorization key.

The report directory is excluded from downstream-reference discovery so committing the report does not create a self-reference. This also supports the normal two-commit workflow: one commit changes knowledge, the next records the assessment.

Squash merge can change Git commit identity while preserving the exact registry/evidence state. The CI gate therefore re-detects the current base→head delta and matches the committed report by knowledge hashes and immutable source/evidence fields rather than requiring the original branch head SHA to remain reachable forever. `downstream_refs` remains a review-time snapshot and is deliberately not part of this later authorization key; new consumers are governed by their own code/document change rather than silently changing the meaning of the already-reviewed source delta.

## Report naming and scope

Use a stable name such as SDL-YYYY-MM-DD-NN.json. One report may contain multiple changed sources when they belong to one reviewed knowledge transition. Do not combine unrelated research waves merely to reduce file count.

If a later source/evidence edit changes the hashes, candidate evidence-ID set or immutable source/evidence change fields, rerun detection and review. A docs/code-only consumer change may change the current downstream reference set without invalidating the already-reviewed knowledge delta. Do not edit detected fields by hand to make an old report fit a new state.

## Failure modes

Do not:

- infer SUPPORT or FALSIFY from changed dates, authority tier or title alone;
- mark a delta READY while live affected evidence is unreviewed;
- remove the source and its evidence citation in the same commit to hide impact;
- reuse a report whose hashes describe another knowledge state;
- change event, risk, before/after snapshots or affected-evidence fields manually;
- treat a project-local exception as justification to rewrite global knowledge;
- delete the superseded record merely because a replacement exists.

When the source itself cannot be inspected, keep the delta BLOCKED and record the missing evidence. When a source changes externally at the same URL but the repository has no changed revision signal, this pipeline cannot discover it automatically; re-verification must update inspectable source metadata so a delta is created.

## Verification

A useful local closure sequence is:

    python3 scripts/source_delta.py validate \
      --report 01-governance/source-deltas/SDL-YYYY-MM-DD-NN.json \
      --require-ready

    python3 scripts/source_delta.py gate \
      --base-ref origin/main \
      --head-ref HEAD

Then run the normal PEOS validation suite. Source Delta evidence complements freshness and behavioral evals; it does not replace either.
