# Coverage, depth and behavioral validation

Product Engineering OS uses three different claims and does not collapse them:

1. **Structural coverage** — required files, IDs, schemas, evidence links, gates and integration references exist.
2. **Deep structural coverage** — every lifecycle stage also has a substantive stage-specific playbook with decision questions, workflow, decision rules, evidence standard, canonical outputs, failure modes, exit conditions and handoff.
3. **Behavioral effectiveness** — the runtime has been executed against representative/adversarial cases and the results have been independently or repeatably assessed.

As of v1.1, all 25 lifecycle stages are **deep-structural**. The stage playbooks are validated for minimum depth and required operational sections. This is materially stronger than the earlier skeleton-only coverage.

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

## Independent replication — 2026-10-03

Run `INDEP-REPL-2026-10-03-01` repeated the same frozen 25 scenarios with fresh independent sessions and a different execution shape: **Google Antigravity / Gemini 3.1 Pro High** executed all 25 cases in one blinded run, then **Anthropic Claude Code / Claude Opus 4.6** judged the outputs in a separate first-party session.

Result: **25/25 passed**, **0 hard failures**, average **9.16/10**. The replication judge was more granular than the original run: it recorded 44 omitted secondary `must_do` details across 24 passing answers, with zero material `must_not_do` violations. Per-stage scores matched the original independent run exactly on 15/25 stages; mean absolute score delta was 0.44.

This strengthens **repeatability** of `independently-behaviorally-validated-v1` for the frozen scenario set. It does not create unseen-distribution evidence and therefore does not justify a broader maturity label. The next maturity increase should use an unseen holdout/mutation set and specialist human review for selected R3–R4 stages.
