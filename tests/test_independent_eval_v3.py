import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_independent_eval_v3_evidence_chain():
    p=subprocess.run(['python3',str(ROOT/'scripts'/'audit_independent_eval_v3.py')],capture_output=True,text=True)
    assert p.returncode==0, p.stdout+p.stderr
    assert '12/12 unseen holdouts' in p.stdout
