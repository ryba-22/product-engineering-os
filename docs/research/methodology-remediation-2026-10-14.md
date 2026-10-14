# Methodology remediation — executed audit, 2026-10-14

**Status:** PARTIALLY VERIFIED, evidence-bounded.
**Owner:** Product Engineering OS (method and evaluation); ChatLOOP (execution telemetry).
**Goal:** prevent process inflation, rubber-stamp AI review and unmeasured claims of productivity improvement, without introducing another governance layer.

## Baselines and source limits

- PEOS: `origin/main` at `1b82299` (2026-10-14 checkout); `python3 -m pytest tests -q` → **202 passed** (Python 3.10, 10.31 s).
- ChatLOOP: `origin/main` at `b4ccf2e`; `python3.12 -m unittest discover -s tests -v` → **99 passed** (110.833 s).
- The ChatLOOP change on a separate audit branch adds a read-only projection of `.ai-loop/events.jsonl` and four isolated tests (4/4 PASS). This provides an observation method, not historical data.
- The inspected clean ChatLOOP checkout had no `.ai-loop/events.jsonl`; **there is no real ready-to-accept cycle-time baseline** from it. There must be no imputation of zero duration.
- A separate, non-public review of 52 recently merged PRs across three repositories collected PR creation/merge intervals. That interval begins *after* unknown parts of discovery and coding; it is neither task lead time nor AI/human effort. It cannot be used to compare PEOS variants. Private PR metadata is intentionally excluded from this public document.
- The independent PEOS holdout eval v3 has 12/12 PASS, but tests agent decisions on curated cases, not the cost or product outcomes of three execution workflows.

## Six control probes

| Probe | Executed oracle | Result | Limit |
| --- | --- | --- | --- |
| T1 — proportionate workflow | `tests/test_workflow_router.py::test_simple_ui_change_stays_small` | PASS | Routing outcome tested; actual agent usage not sampled |
| T2 — independent review | ChatLOOP `ReviewProvenanceTests.test_r3_requires_strong_separation_or_approved_exception` | MECHANISM PASS | Different harness/model is not independent domain truth or behavioral verification |
| T3 — scope drift | ChatLOOP `FindingsAndExplorationTests.test_scope_extension_forces_replan_and_new_task_revision` | PASS | Protects protocol use, not all conversations outside ChatLOOP |
| T4 — safe recovery | ChatLOOP `RecoveryCheckpointTests.test_checkpoint_is_reachable_and_exact_resume_is_idempotency_guarded` | PASS | Does not prove a production provider's external side effects |
| T5 — falsifiable knowledge | `tests/test_source_delta.py::test_detector_never_infers_semantic_classification_and_traces_blast_radius` | PASS | Human-owned semantic interpretation still required |
| T6 — outcome claims | `tests/test_loop_closure.py::test_quality_gates_enforce_loop_closure` and `test_delivery_does_not_infer_health_from_deployment` | CONTRACT PASS | Production outcome samples are still missing |

Focused PEOS probes: **4/4 PASS**. Focused ChatLOOP probes: **3/3 PASS**. These overlap with the full suites above; do not add their counts as distinct tests.

## Remediation decision (keep controls, measure effects)

1. **KEEP** existing R0–R4 risk router, stop-analysis, goal control, evidence-state distinctions, Source Delta Pipeline and ChatLOOP scope/recovery gates. Do not duplicate them in a new framework.
2. **ADOPT** a read-only ChatLOOP cycle-time projection. It must preserve missingness and identify wall time including queue/review waits; it does *not* collect AI cost, human effort or success outcomes.
3. **CHALLENGE** the use of cross-harness reviewers as proof of semantic correctness. R3/R4 review must still use independently grounded test or domain evidence, and real authority for consequential decisions.
4. **HOLD** any claim that the full methodology is faster/cheaper/better than simpler variants. No comparable A/B/C real-task assignment, cost data, human minutes or escaped-defect baseline was available for this audit.

## Small real-task comparison — experiment contract (not yet executed)

Candidate study: **18 comparable R0–R2 tasks**, balanced across low-risk UI, backend bugfix and bounded business-workflow implementation. Assign six each to: A (basic agent + requirement/tests), B (minimal PEOS routing and contracts), C (risk-proportionate complete PEOS/ChatLOOP with relevant knowledge). Do not replay the same task after observing the answer. Pre-commit independent expected behavior and risk class before assignment. Keep model/tool baseline comparable, and record confounders.

Required per task: task ID and repository SHA, class/risk, assigned arm, first accepted scope, start/end timestamps, actual human minutes, observed agent expense or **unknown**, number of review/rework loops, verified outcome evidence, escaped defects during a declared observation interval, and whether task was reopened.

Primary comparison: **total cost to verified outcome** *with quality and safety as guardrails*. Separate developer effort from wall-clock delay. Publish denominators and missingness by arm, avoid winner claims from a small sample and allow `INCONCLUSIVE`.

**Study admission:** no complete assignment and no validated work/cost records today. Running the experiment requires genuinely comparable tasks and operators; fabricated synthetic completions or historical PR-open intervals are not substitutes.

## Closure, rollback and STOP

- **Done in this execution:** inspected existing gates, ran real tests and captured their evidence, implemented a minimal read-only measurement entrypoint, documented data limits and baseline.
- **Open:** actual A/B/C execution and independently measured production/value improvement. This is a remaining evidence gap, not a defect proven in existing controls.
- **No new gate, new source of truth, required reviewer or repository** is introduced.
- Reassess instrument usefulness after at least three real ChatLOOP tasks with complete lifecycle events. Remove or simplify the projection if it does not help find a decision-changing bottleneck.
- Stop research/expansion until observed failed controls, unexpected rework or measured workflow costs justify a specific next change.
