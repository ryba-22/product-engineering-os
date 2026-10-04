import importlib.util
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_optional_integrations_are_reported_without_failing_default_audit():
    result = subprocess.run([sys.executable, str(ROOT / "scripts/audit_freshness.py"), "--as-of", "2026-10-04"], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OPTIONAL/NOT CONNECTED:" in result.stdout

def test_future_verification_dates_fail():
    result = subprocess.run([sys.executable, str(ROOT / "scripts/audit_freshness.py"), "--as-of", "2020-01-01"], capture_output=True, text=True)
    assert result.returncode == 1
    assert "future" in result.stdout

def test_stale_required_sources_fail():
    result = subprocess.run([sys.executable, str(ROOT / "scripts/audit_freshness.py"), "--as-of", "2030-01-01"], capture_output=True, text=True)
    assert result.returncode == 1
    assert "STALE/MISSING" in result.stdout
