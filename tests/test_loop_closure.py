from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "06-modules/requirements/ATDD-EXAMPLE-MAPPING.md",
    "06-modules/product-intelligence/PRODUCTION-LEARNING-LOOP.md",
    "06-modules/security-reliability/AI-GOVERNANCE.md",
    "07-templates/EXAMPLE-MAP.md",
    "07-templates/PRODUCTION-LEARNING-RECORD.md",
    "07-templates/AI-CAPABILITY-MATRIX.md",
]

def test_loop_closure_artifacts_exist():
    assert not [p for p in REQUIRED if not (ROOT / p).exists()]

def test_quality_gates_enforce_loop_closure():
    gates = {g["id"]: g for g in json.loads((ROOT / "04-gates/quality-gates.json").read_text())["gates"]}
    g3 = " ".join(gates["G3"]["exit_evidence"]).lower()
    g8 = " ".join(gates["G8"]["exit_evidence"]).lower()
    g10 = " ".join(gates["G10"]["exit_evidence"]).lower()
    g11 = " ".join(gates["G11"]["exit_evidence"]).lower()
    assert "executable" in g3 and "example" in g3
    assert "ai governance" in g8
    assert "expected vs observed" in g10
    assert "model/test/eval/knowledge" in g11 and "definition of value" in g11

def test_loop_closure_evals_exist():
    cases = json.loads((ROOT / "05-evals/golden-evals.json").read_text())["cases"]
    tags = {tag for case in cases for tag in case.get("tags", [])}
    for required in ["example-mapping", "production-learning", "ai-governance"]:
        assert required in tags

def test_runtime_requires_closed_learning_loop():
    runtime = (ROOT / "BRAIN.md").read_text().lower()
    for term in ["example mapping", "expected vs observed", "capability matrix", "definition of value"]:
        assert term in runtime


def test_example_mapping_does_not_invent_missing_policy():
    atdd = (ROOT / "06-modules/requirements/ATDD-EXAMPLE-MAPPING.md").read_text().lower()
    stage4 = (ROOT / "06-modules/requirements/STAGE-04-REQUIREMENTS.md").read_text().lower()
    for term in ["normalization", "retry", "open/hypothesis", "must not manufacture"]:
        assert term in atdd
    assert "does not authorize invention" in stage4
    assert "do not turn a plausible technical default" in stage4


def test_delivery_does_not_infer_health_from_deployment():
    stage18 = (ROOT / "06-modules/delivery-production/STAGE-18-CI-CD.md").read_text().lower()
    assert "deployed to staging ≠ staging healthy" in stage18
    assert "deployed/unverified health" in stage18
    assert "runtime health" in stage18
