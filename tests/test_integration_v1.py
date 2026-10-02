from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
REQ=[
 'machine/crosswalk.json','11-maturity/stage-coverage.json','11-maturity/MATURITY.md',
 'scripts/audit_coverage.py','scripts/audit_freshness.py',
 '08-adapters/ui-brain-crosswalk.md','08-adapters/ddd-brain-crosswalk.md',
 'skills/product-engineering-os/references/runtime.md','skills/product-engineering-os/references/module-map.md'
]
def test_v1_files_exist(): assert not [x for x in REQ if not (ROOT/x).exists()]
def test_v1_manifest():
 m=json.loads((ROOT/'manifest.json').read_text()); assert m['version']=='1.0.0'; assert m['status']=='integrated'
def test_all_stages_very_strong():
 d=json.loads((ROOT/'11-maturity/stage-coverage.json').read_text())
 assert len(d['stages'])==25
 for s in d['stages']:
  assert s['status']=='very-strong', s
  assert len(s['evidence_ids'])>=2, s
  assert len(s['eval_ids'])>=1, s
  assert all(s['criteria'].values()), s
def test_global_depth():
 assert len(json.loads((ROOT/'02-evidence/evidence-ledger.json').read_text())['items'])>=65
 assert len(json.loads((ROOT/'05-evals/golden-evals.json').read_text())['cases'])>=80
def test_skill_is_self_contained():
 s=(ROOT/'skills/product-engineering-os/SKILL.md').read_text()
 assert '../../../' not in s
 assert 'references/runtime.md' in s
