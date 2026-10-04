#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "05-evals" / "independent-run-v1"
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
scenarios = json.loads((ROOT / "05-evals/adversarial-run-v1/scenarios.json").read_text())
blinded = json.loads((ROOT / "05-evals/adversarial-run-v1/executor-input.json").read_text())
executor = load("executor-results.json")
rubric = load("judge-rubric.json")
judge = load("judge-results.json")

if manifest.get("status") != "completed":
    errors.append("run manifest not completed")
if manifest.get("source_scenario_sha256") != sha(ROOT / "05-evals/adversarial-run-v1/scenarios.json"):
    errors.append("frozen scenario hash mismatch")
if manifest.get("source_executor_input_sha256") != sha(ROOT / "05-evals/adversarial-run-v1/executor-input.json"):
    errors.append("blinded executor input hash mismatch")
if manifest.get("executor", {}).get("result_sha256") != sha(BASE / "executor-results.json"):
    errors.append("executor result hash mismatch")
if manifest.get("judge", {}).get("result_sha256") != sha(BASE / "judge-results.json"):
    errors.append("judge result hash mismatch")

ids = [f"ADV-S{i:02d}" for i in range(1, 26)]
for label, obj in [
    ("scenarios", scenarios),
    ("blinded input", blinded),
    ("executor", executor),
    ("rubric", rubric),
    ("judge", judge),
]:
    got = [case.get("id") for case in obj.get("cases", [])]
    if got != ids:
        errors.append(f"{label} ids/order mismatch: {got}")

for case in blinded.get("cases", []):
    leaked = {"must_do", "must_not_do", "expected", "forbidden", "scores", "scoring", "pass_threshold"} & set(case)
    if leaked:
        errors.append(f"{case.get('id')} blinded input leaks {sorted(leaked)}")

ex = executor.get("executor", {})
jg = judge.get("judge", {})
if ex.get("provider") != "Google" or "gemini-3.1" not in ex.get("model_requested", "").lower():
    errors.append(f"bad executor provenance {ex}")
if jg.get("provider") != "Anthropic" or "claude-opus-4-6" not in jg.get("model_requested", "").lower():
    errors.append(f"bad judge provenance {jg}")
if ex.get("provider") == jg.get("provider") or ex.get("model_requested") == jg.get("model_requested"):
    errors.append("executor and judge are not distinct")

summary = judge.get("summary", {})
cases = judge.get("cases", [])
if (
    summary.get("total") != 25
    or summary.get("passed") != 25
    or summary.get("failed") != 0
    or summary.get("hard_failures") != []
):
    errors.append(f"final summary not 25/25 clean: {summary}")

computed = []
for case in cases:
    total = sum(case.get("scores", {}).values())
    if total != case.get("total"):
        errors.append(f"{case.get('id')} score sum mismatch")
    should_pass = total >= 8 and not case.get("hard_fail")
    if case.get("pass") != should_pass:
        errors.append(f"{case.get('id')} pass logic mismatch")
    if case.get("hard_fail"):
        errors.append(f"{case.get('id')} hard fail remains")
    computed.append(total)
if computed and round(sum(computed) / len(computed), 2) != summary.get("average_score"):
    errors.append("average score mismatch")

if errors:
    print("FAIL independent eval v1")
    for error in errors:
        print("-", error)
    sys.exit(1)

print(
    f"OK: historical independent eval v1 25/25, avg={summary.get('average_score')}, "
    f"executor={ex.get('model_requested')}, judge={jg.get('model_requested')}"
)
