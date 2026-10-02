from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=[
    '## Purpose','## Required inputs','## Questions the Brain must answer','## Workflow',
    '## Decision rules','## Evidence standard','## Canonical outputs','## Failure modes',
    '## Exit conditions','## Handoff'
]

def test_stage_playbooks_are_substantive_and_linked():
    cov=json.loads((ROOT/'11-maturity/stage-coverage.json').read_text())
    for s in cov['stages']:
        p=ROOT/s['stage_playbook']
        assert p.exists(), p
        text=p.read_text()
        assert len(re.findall(r'\b[\w-]+\b', text, flags=re.UNICODE)) >= 350, p
        for section in REQUIRED:
            assert section in text, (p,section)
        for eid in s['evidence_ids']:
            assert eid in text, (p,eid)

def test_skill_stage_copies_match_canonical():
    cov=json.loads((ROOT/'11-maturity/stage-coverage.json').read_text())
    for s in cov['stages']:
        canonical=ROOT/s['stage_playbook']
        copied=ROOT/'skills/product-engineering-os/references/stages'/canonical.name
        assert copied.exists(), copied
        assert copied.read_text()==canonical.read_text(), copied

def test_manifest_points_to_same_playbooks_as_coverage():
    m=json.loads((ROOT/'manifest.json').read_text())
    c={s['id']:s for s in json.loads((ROOT/'11-maturity/stage-coverage.json').read_text())['stages']}
    for s in m['lifecycle_stages']:
        assert s['playbook']==c[s['id']]['stage_playbook']

def test_stage15_completion_state_guard():
    text=(ROOT/'06-modules/quality-engineering/STAGE-15-TESTING.md').read_text()
    assert 'Designing a test strategy' in text
    assert 'not **VERIFIED**' in text
    assert 'Use VERIFIED only after' in text
