from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
REQ=[
 '06-modules/quality-engineering/RISK-BASED-TESTING.md',
 '06-modules/quality-engineering/PERFORMANCE-ENGINEERING.md',
 '06-modules/security-reliability/THREAT-MODELING.md',
 '06-modules/security-reliability/SECURE-SDLC.md',
 '07-templates/TEST-STRATEGY.md','07-templates/PERFORMANCE-BUDGET.md','07-templates/THREAT-MODEL.md'
]
def test_wave3_files(): assert not [x for x in REQ if not (ROOT/x).exists()]
def test_wave3_sources():
    ids={x['id'] for x in json.loads((ROOT/'01-governance/source-registry.json').read_text())['sources']}
    for x in ['OWASP-THREAT','SLSA','K6','WEBDEV-BUDGET','OPENSSF-SCORECARD']: assert x in ids
def test_wave3_evidence():
    data=json.loads((ROOT/'02-evidence/evidence-ledger.json').read_text())
    assert len(data['items'])>=35
def test_wave3_evals():
    d=json.loads((ROOT/'05-evals/golden-evals.json').read_text())
    assert len(d['cases'])>=40
    tags={t for c in d['cases'] for t in c.get('tags',[])}
    for x in ['risk-based-testing','threat-model','performance-budget','supply-chain','load-testing']: assert x in tags
def test_wave3_version():
    m=json.loads((ROOT/'manifest.json').read_text()); assert tuple(map(int,m['version'].split('.'))) >= (0,3,0); assert m['status'] in {'foundation-through-wave-3','foundation-through-wave-4','foundation-through-wave-5','integrated','deep-stage-playbooks'}
