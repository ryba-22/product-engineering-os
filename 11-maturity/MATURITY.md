# Coverage, depth and behavioral validation

Product Engineering OS uses three different claims and does not collapse them:

1. **Structural coverage** — required files, IDs, schemas, evidence links, gates and integration references exist.
2. **Deep structural coverage** — every lifecycle stage also has a substantive stage-specific playbook with decision questions, workflow, decision rules, evidence standard, canonical outputs, failure modes, exit conditions and handoff.
3. **Behavioral effectiveness** — the runtime has been executed against representative/adversarial cases and the results have been independently or repeatably assessed.

As of v1.2, all 25 lifecycle stages are **deep-structural**. The stage playbooks are validated for minimum depth and required operational sections. This is materially stronger than the earlier skeleton-only coverage.

This still does **not** prove general behavioral effectiveness. Existing golden evals are specifications unless accompanied by executed results. The worked idempotent-enrollment example is self-assessed, not an independent benchmark.

The maturity report must therefore never use a green structural test as proof that the Brain made a good real-world decision. Behavioral claims require executed evidence with version, inputs, outputs, evaluator and limitations.

Optional specialist corpora remain conditional until the exact assets are supplied, versioned and reviewed. The bundled stage playbooks provide native fallback depth so Domain and Experience stages no longer depend only on crosswalk files.

Run `python scripts/validate.py`, `python scripts/audit_coverage.py`, `python scripts/audit_freshness.py` and `pytest` before a release.

## Executed adversarial evidence — 2026-10-03

Run ADV-RUN-2026-10-03-01 executed one realistic adversarial scenario for each of the 25 lifecycle stages. The initial result was 24/25: Stage 15 incorrectly claimed VERIFIED after designing a test strategy without executed test evidence. The stage playbook, golden evals and regression tests were changed, then the same frozen Stage-15 scenario was rerun. Final result: 25/25.

This upgrades the package from depth-only evidence to executed self-assessed behavioral evidence for those scenarios. It does not upgrade the package to an independent benchmark: executor and judge were separate passes of the same GPT-5.6 Sol session. See 05-evals/adversarial-run-v1/REPORT.md and final-results.json.

## Independent behavioral validation — 2026-10-03

Run `INDEP-RUN-2026-10-03-01` reused the exact frozen 25 adversarial lifecycle scenarios. The executor was **Google Gemini 3.1 Pro (High)** and saw blinded scenario inputs plus the Product Engineering OS runtime/playbooks/evidence, but not `must_do`, `must_not_do`, scoring criteria or prior self-assessed results. A distinct **Anthropic Claude Opus 4.6 (Thinking)** judge scored the independent outputs against the frozen rubric without access to prior self-assessed answers/judgments.

Result: **25/25 passed**, **0 hard failures**, average **9.12/10**. The judge still identified explicit coverage gaps in a number of passing answers; these are preserved in `05-evals/independent-run-v1/weakness-backlog.json` rather than hidden by the pass result.

This supports the scoped maturity status **`independently-behaviorally-validated-v1` for these 25 frozen scenarios**. It does not establish universal Product Engineering competence, production correctness, or performance on unseen distributions. Future maturity claims require additional unseen/adversarial sets and periodic revalidation after material corpus/runtime changes.

## Loop-closure extension — 2026-10-04

v1.2 materially changes the runtime contract in three areas: pre-implementation ATDD/Example Mapping, expected-vs-observed production learning with propagation into model/test/eval/knowledge, and explicit AI data/model/tool capability governance.

Structural evidence now exists through updated G3/G8/G10/G11 gates, focused playbooks, templates, runtime instructions and new golden eval specifications. This is sufficient to call the extension **structurally implemented**.

At the point the v1.2 structure was introduced, the prior `INDEP-RUN-2026-10-03-01` was not sufficient to validate the new runtime contract. That evidence boundary was preserved until a fresh blinded run was executed; the result is recorded below rather than back-projecting the v1 score onto v1.2.

## Independent behavioral validation v2 — 2026-10-04

Run `INDEP-RUN-2026-10-04-02` evaluates Product Engineering OS v1.2 on **28 frozen scenarios**: the 25 lifecycle regression cases plus three focused loop-closure cases for ATDD / Example Mapping, AI data/model/tool capability governance and expected-vs-observed Production Learning / Definition of Value.

The blinded executor was **Anthropic Claude Opus 5.5 via Claude Code CLI**. The independent judge was **OpenAI GPT-6 Luna via GitHub Copilot CLI**. The executor did not receive judge criteria or prior results; the judge criteria were introduced only after executor outputs existed.

Round 1 produced **26/28 PASS** and deliberately preserved two hard failures:
- **ADV-S04** — unresolved normalization/retry semantics were promoted into decision-ready requirements/examples;
- **ADV-S18** — staging deployment was incorrectly upgraded to staging health without runtime health evidence.

The runtime/playbooks were hardened while the frozen scenarios and judge rubric remained unchanged. Fresh independent sessions reran only those same two failed cases. Both passed at 9/10.

Final result: **28/28 PASS, 0 hard failures, average 9.57/10**. Focused v1.2 cases scored ATDD 9/10, AI governance 10/10 and Production Learning 10/10. The first-round failures, remediation, round-2 outputs, provenance and weakness backlog remain stored under `05-evals/independent-run-v2/`.

This supports the scoped maturity status **`independently-behaviorally-validated-v2`** for the frozen 28-case suite. It does not prove universal product-engineering competence, correctness on unseen distributions, or production correctness of downstream systems. Material future runtime changes reopen the need for revalidation.


## Unseen-distribution behavioral validation v3 — 2026-10-05

Run `INDEP-RUN-2026-10-05-03` adds **12 previously unused multi-axis holdout cases**. Unlike v1/v2, the cases combine concerns such as financial side-effect uncertainty + retry + callback, UI bulk selection + pagination + concurrency, semantic migration + mixed versions, ambiguous temporal data repair, AI PII + tool/credential capability, and aggregate success + segment harm.

The blinded executor was **Anthropic Claude Opus 5.5 via Claude Code CLI** in three fresh batches. Its runtime explicitly excluded the judge rubric and results. The independent judge ran afterwards through **GitHub Copilot CLI with `auto` model routing**. The concrete model selected by that routing mode was not surfaced by silent CLI output; the evidence records this limitation instead of claiming an identity.

Result: **12/12 PASS, 0 hard failures, average 9.0/10**. The input, frozen rubric, raw batch outputs, canonical executor/judge results, provenance and SHA-256 manifest live under `05-evals/independent-run-v3/`.

This supports the scoped maturity status **`unseen-distribution-behaviorally-validated-v3` for this 12-case holdout**. It improves generalization evidence beyond the frozen v1/v2 distribution, but does not establish universal competence or production correctness. Material routing/control-loop/governance changes require a fresh holdout rather than replaying v3 as the only proof.
