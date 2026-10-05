#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import sys
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "05-evals" / "independent-run-v2"
errors = []

def load(name):
    try:
        return json.loads((BASE / name).read_text())
    except Exception as exc:
        errors.append(f"{name}: {exc}")
        return {}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

manifest = load("run-manifest.json")
executor_input = load("executor-input.json")
rubric = load("judge-rubric.json")
executor = load("executor-results.json")
judge = load("judge-results.json")
round1_executor = load("executor-results-round1.json")
round1_judge = load("judge-results-round1.json")
round2_executor = load("executor-results-round2.json")
round2_judge = load("judge-results-round2.json")
source_files = load("source-files.json")
coverage = json.loads((ROOT / "11-maturity" / "stage-coverage.json").read_text())

if manifest.get("status") != "completed":
    errors.append("run manifest not completed")
if manifest.get("runtime_version") != "1.2.0":
    errors.append(f"unexpected runtime version: {manifest.get('runtime_version')}")

suite = manifest.get("suite", {})
if suite.get("total") != 28 or suite.get("regression_cases") != 25 or suite.get("loop_closure_cases") != 3:
    errors.append(f"unexpected suite shape: {suite}")
if suite.get("executor_input_sha256") != sha(BASE / "executor-input.json"):
    errors.append("executor input hash mismatch")
if suite.get("judge_rubric_sha256") != sha(BASE / "judge-rubric.json"):
    errors.append("judge rubric hash mismatch")
if manifest.get("actual_executor", {}).get("result_sha256") != sha(BASE / "executor-results.json"):
    errors.append("executor result hash mismatch")
if manifest.get("actual_judge", {}).get("result_sha256") != sha(BASE / "judge-results.json"):
    errors.append("judge result hash mismatch")

# The evaluated runtime is historical evidence. Verify hashes against the
# recorded runtime commit, not against the current working tree. This lets PEOS
# evolve without rewriting or invalidating the frozen v2 evidence.
runtime_commit = source_files.get("runtime_commit")
if runtime_commit != manifest.get("runtime_commit_final"):
    errors.append("source-files runtime commit differs from final runtime commit")
for item in source_files.get("files", []):
    rel = item.get("path", "")
    try:
        payload = subprocess.check_output(
            ["git", "show", f"{runtime_commit}:{rel}"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        errors.append(f"missing frozen runtime file at {runtime_commit}: {rel}")
        continue
    actual = hashlib.sha256(payload).hexdigest()
    if actual != item.get("sha256"):
        errors.append(f"frozen runtime hash mismatch at {runtime_commit}: {rel}")

# Blinding: executor input must not contain judge-only fields.
for case in executor_input.get("cases", []):
    leaked = {
        "must_do", "must_not_do", "expected", "forbidden", "scores",
        "scoring", "pass_threshold", "hard_fail_conditions"
    } & set(case)
    if leaked:
        errors.append(f"{case.get('id')} executor input leaks {sorted(leaked)}")

expected_ids = [f"ADV-S{i:02d}" for i in range(1, 26)] + [
    "V2-LC-ATDD", "V2-LC-AIGOV", "V2-LC-PROD"
]
for label, obj in [
    ("executor input", executor_input),
    ("rubric", rubric),
    ("executor", executor),
    ("judge", judge),
]:
    got = [case.get("id") for case in obj.get("cases", [])]
    if got != expected_ids:
        errors.append(f"{label} ids/order mismatch: {got}")

ex = executor.get("executor", {})
jg = judge.get("judge", {})
if ex.get("provider") != "Anthropic" or "claude-opus-5-5" not in ex.get("model_requested", "").lower():
    errors.append(f"bad executor provenance: {ex}")
if "OpenAI" not in jg.get("provider", "") or "gpt-6-luna" not in jg.get("model_resolved", "").lower():
    errors.append(f"bad judge provenance: {jg}")
if ex.get("provider") == jg.get("provider"):
    errors.append("executor and judge providers are not distinct")
if jg.get("independent_from_executor") is not True or ex.get("independent_from_judge") is not True:
    errors.append("independence flags are not true")

summary = judge.get("summary", {})
if (
    summary.get("total") != 28
    or summary.get("passed") != 28
    or summary.get("failed") != 0
    or summary.get("hard_failures") != []
):
    errors.append(f"final summary not 28/28 clean: {summary}")

computed_scores = []
for case in judge.get("cases", []):
    total = sum(case.get("scores", {}).values())
    if total != case.get("total"):
        errors.append(f"{case.get('id')} score sum mismatch")
    should_pass = total >= rubric.get("pass_threshold", 8) and not case.get("hard_fail")
    if case.get("pass") != should_pass:
        errors.append(f"{case.get('id')} pass logic mismatch")
    if case.get("hard_fail"):
        errors.append(f"{case.get('id')} hard fail remains")
    computed_scores.append(total)
if computed_scores and round(sum(computed_scores) / len(computed_scores), 2) != summary.get("average_score"):
    errors.append("average score mismatch")

# Preserve the failure-and-remediation chain. Round 1 must still contain the
# original failures; round 2 may replace only those exact cases.
r1_summary = round1_judge.get("summary", {})
if (
    r1_summary.get("total") != 28
    or r1_summary.get("passed") != 26
    or r1_summary.get("failed") != 2
    or sorted(r1_summary.get("hard_failures", [])) != ["ADV-S04", "ADV-S18"]
):
    errors.append(f"round-1 failure history changed: {r1_summary}")

failed_ids = ["ADV-S04", "ADV-S18"]
for label, obj in [("round2 executor", round2_executor), ("round2 judge", round2_judge)]:
    ids = [case.get("id") for case in obj.get("cases", [])]
    if ids != failed_ids:
        errors.append(f"{label} scope is not exact failed-case rerun: {ids}")

r2_cases = round2_judge.get("cases", [])
if (
    len(r2_cases) != 2
    or any(not case.get("pass") for case in r2_cases)
    or any(case.get("hard_fail") for case in r2_cases)
    or {case.get("id"): case.get("total") for case in r2_cases} != {"ADV-S04": 9, "ADV-S18": 9}
):
    errors.append(f"round-2 result not clean: {r2_cases}")

def case_map(obj):
    return {case["id"]: case for case in obj.get("cases", [])}

final_exec = case_map(executor)
final_judge = case_map(judge)
r1_exec = case_map(round1_executor)
r1_judge = case_map(round1_judge)
r2_exec = case_map(round2_executor)
r2_judge = case_map(round2_judge)
for case_id in expected_ids:
    if case_id in failed_ids:
        if final_exec.get(case_id) != r2_exec.get(case_id):
            errors.append(f"{case_id} final executor result is not round-2 result")
        if final_judge.get(case_id) != r2_judge.get(case_id):
            errors.append(f"{case_id} final judge result is not round-2 result")
    else:
        if final_exec.get(case_id) != r1_exec.get(case_id):
            errors.append(f"{case_id} final executor result differs from round 1")
        if final_judge.get(case_id) != r1_judge.get(case_id):
            errors.append(f"{case_id} final judge result differs from round 1")

# Current stage maturity must point at the v2 evidence for all 25 lifecycle stages.
by_stage = {
    case["stage_id"]: case
    for case in judge.get("cases", [])
    if case.get("id", "").startswith("ADV-S")
}
for stage in coverage.get("stages", []):
    if stage.get("behavioral_validation") != "independently-behaviorally-validated-v2":
        errors.append(f"stage {stage['id']} not independently validated v2")
    if stage.get("behavioral_run_id") != manifest.get("run_id"):
        errors.append(f"stage {stage['id']} run id mismatch")
    if stage.get("behavioral_evidence") != "05-evals/independent-run-v2/judge-results.json":
        errors.append(f"stage {stage['id']} evidence path mismatch")
    if stage.get("behavioral_independent") is not True:
        errors.append(f"stage {stage['id']} independence flag false")
    judged = by_stage.get(stage["id"])
    if not judged or stage.get("behavioral_score") != judged.get("total"):
        errors.append(f"stage {stage['id']} score mismatch")
    if stage.get("behavioral_hard_fail") is not False:
        errors.append(f"stage {stage['id']} hard fail flag")

focus = {
    "V2-LC-ATDD": 9,
    "V2-LC-AIGOV": 10,
    "V2-LC-PROD": 10,
}
for case_id, score in focus.items():
    case = final_judge.get(case_id)
    if not case or case.get("total") != score or not case.get("pass") or case.get("hard_fail"):
        errors.append(f"loop-closure focus case not clean: {case_id}")

if errors:
    print("FAIL independent eval v2")
    for error in errors:
        print("-", error)
    sys.exit(1)

print(
    "OK: independent eval v2 28/28, "
    f"avg={summary.get('average_score')}, "
    f"executor={ex.get('model_requested')}, "
    f"judge={jg.get('model_resolved')}"
)
