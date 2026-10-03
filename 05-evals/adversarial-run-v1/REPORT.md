# Adversarial behavioral run — 25/25 lifecycle stages

**Run:** ADV-RUN-2026-10-03-01  
**Date:** 2026-10-03  
**System:** Product Engineering OS v1.1 / deep-brain-pass-2026-10-03

## Result

Initial pass: **24/25**. One hard failure occurred in **ADV-S15 (Testing)**.

After remediation and a targeted rerun: **25/25 pass**, final average **10.00/10**.

The failed case was valuable: the Brain designed the correct real-database concurrency test strategy, but incorrectly labeled the state **VERIFIED** before any test had actually executed. Stage 15 was changed so test plans/cases remain **DECIDED / UNVERIFIED** until executed evidence exists. Golden eval `EV-S15-STATE` and a regression test were added.

## Method

The 25 realistic adversarial scenarios were frozen before execution. The executor input omitted `must_do`, `must_not_do` and scoring criteria.

Each case was executed against:
- `BRAIN.md`
- core lifecycle/risk/routing rules
- the exact matching `STAGE-XX` playbook
- its evidence anchors and relevant gate/artifact contract

The judge pass scored: decision correctness (4), evidence/scope (2), risk/constraints (1), execution closure (1), verification (1), traceability (1). Passing required at least 8/10 and no hard failure.

**Limitation:** executor and judge were two passes of the same GPT-5.6 Sol session. An external Codex executor was attempted but unavailable because its local usage quota was exhausted. This is therefore reproducible **self-assessed behavioral evidence**, not an independent benchmark.

## Stage results
| Stage | Case | Score | Result | Capability demonstrated |
|---:|---|---:|---|---|
| 01 | ADV-S01 | 10/10 | PASS | Resisted solution-first dashboard framing |
| 02 | ADV-S02 | 10/10 | PASS | Detected confirmation/sampling bias |
| 03 | ADV-S03 | 10/10 | PASS | Preserved temporal/domain ambiguity instead of inheriting schema truth |
| 04 | ADV-S04 | 10/10 | PASS | Specified billing-SMS behavior without leaking architecture into requirements |
| 05 | ADV-S05 | 10/10 | PASS | Kept Legacy/Finance mutation ownership separate |
| 06 | ADV-S06 | 10/10 | PASS | Rejected microservice/Kafka/Kubernetes architecture inflation |
| 07 | ADV-S07 | 10/10 | PASS | Designed dense worklist + durable URL state + mobile transformation |
| 08 | ADV-S08 | 10/10 | PASS | Handled stale concurrent editing as a recoverable conflict |
| 09 | ADV-S09 | 10/10 | PASS | Rejected axe-only accessibility completion |
| 10 | ADV-S10 | 10/10 | PASS | Favored operator comparison density over decorative card/whitespace pressure |
| 11 | ADV-S11 | 10/10 | PASS | Rejected premature Core design-system promotion |
| 12 | ADV-S12 | 10/10 | PASS | Removed duplicated URL/local React state and effect synchronization |
| 13 | ADV-S13 | 10/10 | PASS | Rejected state mutation through GET and defined safe command semantics |
| 14 | ADV-S14 | 10/10 | PASS | Rejected fabricated midnight history in DATE→datetime migration |
| 15 | ADV-S15 | 10/10 | PASS after rerun | Required real-DB concurrency evidence and corrected lifecycle overclaim |
| 16 | ADV-S16 | 10/10 | PASS | Detected resource-level authorization/IDOR risk despite hidden UI |
| 17 | ADV-S17 | 10/10 | PASS | Refused speculative index/buffer tuning without workload evidence |
| 18 | ADV-S18 | 10/10 | PASS | Required immutable artifact provenance instead of production rebuild |
| 19 | ADV-S19 | 10/10 | PASS | Separated green CI/staging from safe data-affecting rollout |
| 20 | ADV-S20 | 10/10 | PASS | Made outbox/notification state machine observable and actionable |
| 21 | ADV-S21 | 10/10 | PASS | Rejected backup-status-as-restore-evidence |
| 22 | ADV-S22 | 10/10 | PASS | Built semantic outcome analytics instead of click/MAU vanity metrics |
| 23 | ADV-S23 | 10/10 | PASS | Rejected underpowered contaminated A/B test |
| 24 | ADV-S24 | 10/10 | PASS | Separated release health from product outcome learning |
| 25 | ADV-S25 | 10/10 | PASS | Preserved provenance and explicit supersession under newer-source pressure |

## Round-1 defect and remediation

**ADV-S15 — Testing** was the only initial failure. The Brain correctly required a real-database concurrency/retry test, but then set `completion_state=VERIFIED`. That contradicted the OS rule `IMPLEMENTED ≠ VERIFIED` because no test execution evidence existed.

Remediation:
1. Added a completion-state guard to Stage 15.
2. Added `EV-S15-STATE` to golden evals.
3. Added a regression test that requires the guard.
4. Reran only ADV-S15 with the same frozen scenario.
5. The rerun scored 10/10 with `DECIDED / UNVERIFIED` until the real test executes.

## What this run proves — and what it does not

It shows that v1.1 can produce policy-compliant, evidence-scoped decisions on these 25 adversarial scenarios and that the eval loop detected and converted one behavioral defect into a durable regression guard.

It does **not** prove universal Product Engineering competence, production correctness, or independent model agreement. A stronger maturity level requires blind execution by another model/session and ideally human/expert review for high-risk stages such as security, migrations, recovery and experimentation.
