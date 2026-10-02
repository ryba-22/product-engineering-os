from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

REQUIRED=[
 '06-modules/system-architecture/DECISION-PROTOCOL.md',
 '06-modules/system-architecture/FITNESS-FUNCTIONS.md',
 '06-modules/software-engineering/FRONTEND-ARCHITECTURE.md',
 '06-modules/software-engineering/BACKEND-API.md',
 '06-modules/software-engineering/DATA-PERSISTENCE.md',
 '07-templates/ARCHITECTURE-DRIVERS.md',
 '07-templates/API-CONTRACT.md',
 '07-templates/DATA-CHANGE-PLAN.md',
]

def test_wave2_files_exist():
    assert not [p for p in REQUIRED if not (ROOT/p).exists()]

def test_wave2_source_families_are_registered():
    reg=json.loads((ROOT/'01-governance/source-registry.json').read_text())
    ids={s['id'] for s in reg['sources']}
    for x in ['ISO-25010','RFC9110','AWS-OUTBOX','REACT-STATE','REACT-EFFECTS']:
        assert x in ids

def test_wave2_evidence_depth():
    data=json.loads((ROOT/'02-evidence/evidence-ledger.json').read_text())
    assert len(data['items']) >= 25
    domains={d for e in data['items'] for d in e['domains']}
    for x in ['architecture','frontend','backend','api','data']:
        assert x in domains

def test_wave2_evals_cover_core_engineering_failures():
    data=json.loads((ROOT/'05-evals/golden-evals.json').read_text())
    assert len(data['cases']) >= 32
    tags={t for c in data['cases'] for t in c.get('tags',[])}
    for x in ['dual-write','idempotency','state-ownership','concurrency','api-contract','data-migration']:
        assert x in tags

def test_wave2_manifest_version():
    m=json.loads((ROOT/'manifest.json').read_text())
    assert tuple(map(int,m['version'].split('.'))) >= (0,2,0)
    assert m['status'] in {'foundation-through-wave-2','foundation-through-wave-3','foundation-through-wave-4','foundation-through-wave-5','integrated','deep-stage-playbooks'}
