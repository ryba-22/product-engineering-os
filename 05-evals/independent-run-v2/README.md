# Independent Eval Run v2 — Product Engineering OS v1.2

INDEP-RUN-2026-10-04-02 independently revalidates the 25 lifecycle stages after the v1.2 runtime change and adds three focused cases for the new loop-closure contracts: ATDD / Example Mapping, AI data/model/tool capability governance, and expected-vs-observed Production Learning with Definition of Value.

The executor was Anthropic Claude Opus 5.5 through Claude Code CLI. It received the blinded scenarios plus the frozen Product Engineering OS runtime/playbooks/templates, but not judge criteria, expected answers, scores or prior results. The independent judge was OpenAI GPT-6 Luna through GitHub Copilot CLI. Judge criteria were supplied only after executor output existed.

Round 1 produced 26/28 passes. Two hard failures were preserved as evidence rather than hidden: Stage 04 invented unresolved normalization/retry policy, and Stage 18 inferred staging health from deployment. The OS runtime/playbooks were corrected without changing the frozen scenarios or judge criteria. Fresh independent sessions then reran only those same failed scenarios. Both passed.

Final result: 28/28 PASS, 0 hard failures, average 9.57/10. The three v1.2-focused cases scored ATDD=9/10, AI governance=10/10, Production Learning=10/10.

Promotion requires more than the aggregate score. run-manifest.json freezes input/rubric hashes, runtime commits and model provenance. executor-results-round1.json and judge-results-round1.json preserve the failed first round. executor-results-round2.json and judge-results-round2.json preserve the targeted remediation evidence. Canonical executor-results.json and judge-results.json contain the final merged 28-case result. weakness-backlog.json retains judge criticism for passing cases.

The supported maturity claim is independently-behaviorally-validated-v2 scoped to these 28 frozen scenarios. This is not a universal benchmark and does not prove correctness on unseen product-engineering work or production correctness of downstream systems.
