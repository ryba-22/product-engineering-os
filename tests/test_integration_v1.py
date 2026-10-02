from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]

def test_manifest_and_stage_count():
    m=json.loads((ROOT/'manifest.json').read_text())
    assert tuple(map(int,m['version'].split('.'))) >= (1,1,0)
    assert len(m['lifecycle_stages']) == 25
    assert all(s.get('playbook') for s in m['lifecycle_stages'])

def test_all_stages_have_deep_playbooks():
    d=json.loads((ROOT/'11-maturity/stage-coverage.json').read_text())
    assert len(d['stages'])==25
    for s in d['stages']:
        assert s['status']=='deep-structural', s
        assert len(s['evidence_ids'])>=2, s
        assert len(s['eval_ids'])>=1, s
        assert s.get('stage_playbook'), s
        assert s.get('behavioral_validation') in {'pending-independent-eval','executed','executed-self-assessed'}, s
        assert all(s['criteria'].values()), s

def test_global_depth_inputs_exist():
    assert len(json.loads((ROOT/'02-evidence/evidence-ledger.json').read_text())['items'])>=65
    assert len(json.loads((ROOT/'05-evals/golden-evals.json').read_text())['cases'])>=80

def test_skill_is_self_contained_and_has_stage_depth():
    s=(ROOT/'skills/product-engineering-os/SKILL.md').read_text()
    assert '../../../' not in s
    assert 'references/runtime.md' in s
    stages=list((ROOT/'skills/product-engineering-os/references/stages').glob('STAGE-*.md'))
    assert len(stages)==25
