from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]

def test_adversarial_behavioral_run():
    p=subprocess.run([sys.executable,str(ROOT/'scripts/audit_adversarial_run.py')],capture_output=True,text=True)
    assert p.returncode==0, p.stdout+p.stderr
