# Independent Behavioral Validation — Replication Run

Run: INDEP-REPL-2026-10-03-01
Validated runtime: c775a1772ab24f90c9cda4093460bd81fa1caa65
Frozen scenario set: the same 25 cases used by INDEP-RUN-2026-10-03-01

## Result

25/25 PASS, 0 hard failures, deterministic average 9.16/10.

Score distribution: {8: 5, 9: 11, 10: 9}. The independent judge recorded 44 omitted frozen must_do details across 24/25 passing answers, and 0 material must_not_do violations.

The Claude judge model reported average_score=9.12 in its summary, but its 25 case totals sum to 229. A deterministic normalization therefore corrects only that arithmetic field to 9.16; the exact model output is preserved in judge-model-output.json and no case judgment was changed.

This is a replication, not a new/unseen benchmark. It tests repeatability on the same frozen scenarios using fresh sessions and a different execution shape.

## Independence chain

- Executor: Google Antigravity / Gemini 3.1 Pro High, one fresh blinded session for all 25 cases.
- Judge: Anthropic Claude Code / Claude Opus 4.6, separate authenticated first-party session.
- Executor workspace physically excluded the rubric, expected criteria, prior executor/judge answers and prior final results.
- Judge workspace contained the frozen rubric and fresh executor output, but physically excluded prior self-assessed answers/judgments.

## Comparison with Independent Run v1

- Independent v1: 25/25, avg 9.12/10, 0 hard failures.
- Replication: 25/25, avg 9.16/10, 0 hard failures.
- Exact per-stage score agreement: 15/25.
- Mean absolute per-stage score delta: 0.44.
- Both runs pass every stage; differing omission lists show judge sensitivity rather than identical templated grading.

| Stage | Case | v1 | Replication | Delta | Replication missing criteria |
|---:|---|---:|---:|---:|---:|
| 01 | ADV-S01 | 9 | 9 | +0 | 3 |
| 02 | ADV-S02 | 9 | 8 | -1 | 2 |
| 03 | ADV-S03 | 9 | 8 | -1 | 2 |
| 04 | ADV-S04 | 9 | 9 | +0 | 2 |
| 05 | ADV-S05 | 9 | 9 | +0 | 2 |
| 06 | ADV-S06 | 8 | 9 | +1 | 2 |
| 07 | ADV-S07 | 9 | 8 | -1 | 2 |
| 08 | ADV-S08 | 9 | 9 | +0 | 2 |
| 09 | ADV-S09 | 10 | 10 | +0 | 1 |
| 10 | ADV-S10 | 8 | 8 | +0 | 2 |
| 11 | ADV-S11 | 9 | 9 | +0 | 2 |
| 12 | ADV-S12 | 9 | 10 | +1 | 1 |
| 13 | ADV-S13 | 8 | 10 | +2 | 2 |
| 14 | ADV-S14 | 9 | 10 | +1 | 2 |
| 15 | ADV-S15 | 10 | 10 | +0 | 0 |
| 16 | ADV-S16 | 10 | 9 | -1 | 1 |
| 17 | ADV-S17 | 10 | 10 | +0 | 1 |
| 18 | ADV-S18 | 9 | 9 | +0 | 2 |
| 19 | ADV-S19 | 9 | 9 | +0 | 2 |
| 20 | ADV-S20 | 10 | 10 | +0 | 2 |
| 21 | ADV-S21 | 9 | 10 | +1 | 1 |
| 22 | ADV-S22 | 9 | 9 | +0 | 2 |
| 23 | ADV-S23 | 9 | 9 | +0 | 2 |
| 24 | ADV-S24 | 10 | 10 | +0 | 1 |
| 25 | ADV-S25 | 9 | 8 | -1 | 3 |

## Interpretation

The replication strengthens confidence that the 25/25 independent result was not a single-run accident: a fresh Gemini execution and a separate Claude Opus judge again cleared every frozen scenario without a hard failure.

It also sharpens the limitation. The judge still found many omitted secondary criteria in passing answers. Therefore the correct claim remains independently behaviorally validated for this frozen scenario set, not universally expert or complete on unseen Product Engineering problems.

The next meaningful maturity jump is not a third rerun of the same 25 cases. It is an unseen holdout / mutation eval set, ideally with specialist human review on R3–R4 stages.
