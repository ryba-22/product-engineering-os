from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    'README.md','BRAIN.md','manifest.json',
    '00-core/lifecycle.md','00-core/operating-profile.md','00-core/risk-model.md','00-core/routing.md',
    '00-core/engineering-control-loop.md','07-templates/ENGINEERING-CONTROL-LOOP.md',
    '01-governance/source-registry.json','01-governance/knowledge-lifecycle.md',
    '02-evidence/evidence.schema.json','02-evidence/evidence-ledger.json',
    '03-decisions/decision-record.schema.json','03-decisions/DECISION-RECORD-TEMPLATE.md',
    '04-gates/quality-gates.json','05-evals/golden-evals.json',
    'skills/product-engineering-os/SKILL.md','scripts/validate.py',
]

MODULES = [
    'product-strategy','product-discovery','domain','requirements','system-architecture',
    'experience','software-engineering','quality-engineering','security-reliability',
    'delivery-production','product-intelligence','knowledge-governance'
]


def test_required_files_exist():
    missing = [p for p in REQUIRED if not (ROOT/p).exists()]
    assert not missing, f'Missing required files: {missing}'


def test_all_modules_have_contract():
    missing = [m for m in MODULES if not (ROOT/'06-modules'/m/'MODULE.md').exists()]
    assert not missing, f'Missing module contracts: {missing}'


def test_manifest_has_all_25_stages_and_12_modules():
    data = json.loads((ROOT/'manifest.json').read_text())
    assert len(data['lifecycle_stages']) == 25
    assert len(data['modules']) == 12
    assert set(m['id'] for m in data['modules']) == set(MODULES)


def test_clifton_complement_profile_is_explicit():
    text = (ROOT/'00-core'/'operating-profile.md').read_text().lower()
    for theme in ['activator','focus','discipline','responsibility','arranger']:
        assert theme in text
    assert 'stop-analysis' in text
    assert 'evidence before claims' in text


def test_quality_gates_cover_full_lifecycle():
    gates = json.loads((ROOT/'04-gates'/'quality-gates.json').read_text())
    ids = [g['id'] for g in gates['gates']]
    assert ids == [f'G{i}' for i in range(12)]
    assert all(g.get('exit_evidence') for g in gates['gates'])


def test_evals_cover_analysis_paralysis_architecture_inflation_and_unverified_claims():
    data = json.loads((ROOT/'05-evals'/'golden-evals.json').read_text())
    tags = {tag for case in data['cases'] for tag in case.get('tags', [])}
    for required in ['analysis-paralysis','architecture-inflation','verification','product-discovery','production-evidence']:
        assert required in tags
    assert len(data['cases']) >= 20


def test_evidence_and_decision_schemas_are_json_schema():
    for p in ['02-evidence/evidence.schema.json','03-decisions/decision-record.schema.json']:
        data = json.loads((ROOT/p).read_text())
        assert data['$schema'].startswith('https://json-schema.org/')
        assert data['type'] == 'object'


def test_source_registry_has_multi_domain_authority():
    data = json.loads((ROOT/'01-governance'/'source-registry.json').read_text())
    domains = {d for s in data['sources'] for d in s['domains']}
    for required in ['product','research','architecture','security','reliability','delivery','api','ux']:
        assert required in domains
    assert len(data['sources']) >= 20


def test_engineering_control_loop_covers_cross_cutting_risk_contract():
    text = (ROOT/'00-core'/'engineering-control-loop.md').read_text().lower()
    for phrase in [
        'falsification / unknown-unknown',
        'invariant + consistency + enforcement',
        'concurrency and failure model',
        'verification budget',
        'architecture economics',
        'consumer-oriented contract',
        'production learning closure',
    ]:
        assert phrase in text
    brain = (ROOT/'BRAIN.md').read_text().lower()
    assert 'engineering-control-loop.md' in brain
    assert 'human ownership rule' in brain
