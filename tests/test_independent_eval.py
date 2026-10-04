from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def run(script):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script)],
        capture_output=True,
        text=True,
    )

def test_independent_eval_v1_audit_preserves_historical_evidence():
    result = run("audit_independent_eval.py")
    assert result.returncode == 0, result.stdout + result.stderr

def test_independent_eval_v2_audit_validates_current_maturity_claim():
    result = run("audit_independent_eval_v2.py")
    assert result.returncode == 0, result.stdout + result.stderr
