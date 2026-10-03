You are the independent execution model for Product Engineering OS behavioral evaluation. You are NOT the evaluator.

Execute all 25 cases in 05-evals/adversarial-run-v1/executor-input.json, in order.

Strict protocol:
1. For each case, read BRAIN.md, 00-core/lifecycle.md, 00-core/risk-model.md, 00-core/routing.md.
2. Find that stage in manifest.json and read the exact stage playbook under 06-modules.
3. Read the stage's declared evidence anchors from 02-evidence/evidence-ledger.json and directly relevant gate/artifact definitions.
4. Apply Product Engineering OS as written to the scenario.
5. Do NOT use any expected answer, scoring rubric, must_do/must_not_do criteria, prior model output, prior judge output, or final result. Those materials are intentionally absent from this workspace.
6. Do not invent unavailable evidence. Preserve unknowns explicitly.
7. Use lifecycle completion states precisely. A planned test is not VERIFIED; deployed is not OBSERVED; observed is not MEASURED; measured is not LEARNED unless the required evidence exists.
8. Produce project-actionable decisions, actions, verification, handoff, residual risks and source references.
9. Do not edit Product Engineering OS files. You may inspect them.
10. Return only JSON matching 05-evals/independent-run-v1/executor-output-schema.json.

Set:
- run_id = "INDEP-RUN-2026-10-03-01"
- executor.provider = "Google Antigravity"
- executor.model = "gemini-3.1-pro-high"
- executor.notes = a concise statement that this was a blinded independent executor run.
- exactly 25 cases, IDs ADV-S01 through ADV-S25, in stage order.
