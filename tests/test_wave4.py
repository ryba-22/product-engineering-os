from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
REQ=[
 '06-modules/delivery-production/CI-CD.md','06-modules/delivery-production/RELEASE-ENGINEERING.md',
 '06-modules/security-reliability/OBSERVABILITY.md','06-modules/security-reliability/RESILIENCE-INCIDENTS.md',
 '07-templates/RELEASE-EVIDENCE.md','07-templates/SLO.md','07-templates/INCIDENT-RUNBOOK.md','07-templates/RESTORE-DRILL.md'
]
def test_wave4_files(): assert not [x for x in REQ if not (ROOT/x).exists()]
def test_wave4_sources():
 ids={x['id'] for x in json.loads((ROOT/'01-governance/source-registry.json').read_text())['sources']}
 for x in ['SRE-CANARY','SRE-POSTMORTEM','OTEL-SIGNALS']: assert x in ids
def test_wave4_evidence():
 assert len(json.loads((ROOT/'02-evidence/evidence-ledger.json').read_text())['items'])>=45
def test_wave4_evals():
 d=json.loads((ROOT/'05-evals/golden-evals.json').read_text()); assert len(d['cases'])>=48
 tags={t for c in d['cases'] for t in c.get('tags',[])}
 for x in ['rollout','observability','restore-drill','incident-response','release-provenance']: assert x in tags
def test_wave4_version():
 m=json.loads((ROOT/'manifest.json').read_text()); assert tuple(map(int,m['version'].split('.'))) >= (0,4,0); assert m['status'] in {'foundation-through-wave-4','foundation-through-wave-5','integrated'}
