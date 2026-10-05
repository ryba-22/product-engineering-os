#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[1]
errors=[]

def load(rel):
    try: return json.loads((ROOT/rel).read_text())
    except Exception as e: errors.append(f'{rel}: {e}'); return None

manifest=load('manifest.json')
gates=load('04-gates/quality-gates.json')
sources=load('01-governance/source-registry.json')
evidence=load('02-evidence/evidence-ledger.json')
evals=load('05-evals/golden-evals.json')
delta_policy=load('machine/source-delta-policy.json')
delta_schema=load('01-governance/source-delta.schema.json')
memory_policy=load('machine/memory-knowledge-policy.json')
memory_schema=load('01-governance/memory-knowledge.schema.json')

if manifest:
    if len(manifest.get('lifecycle_stages',[]))!=25: errors.append('manifest must contain 25 lifecycle stages')
    if len(manifest.get('modules',[]))!=12: errors.append('manifest must contain 12 modules')
    for m in manifest.get('modules',[]):
        p=ROOT/'06-modules'/m['id']/'MODULE.md'
        if not p.exists(): errors.append(f'missing module contract: {p}')
if gates and [g['id'] for g in gates.get('gates',[])] != [f'G{i}' for i in range(12)]: errors.append('gates must be G0..G11')
if sources:
    ids=[s['id'] for s in sources.get('sources',[])]
    if len(ids)!=len(set(ids)): errors.append('duplicate source ids')
    for source_id in ids:
        if not re.fullmatch(r'[A-Z0-9-]+', source_id): errors.append(f'invalid source id: {source_id}')
        if source_id in {'EVIDENCE-LEDGER','SOURCE-REGISTRY'}: errors.append(f'{source_id} is reserved for synthetic source-delta events')
    source_ids=set(ids)
else: source_ids=set()
if evidence:
    eids=[]
    for e in evidence.get('items',[]):
        eids.append(e['id'])
        cited=e.get('source_ids',[])
        if not cited: errors.append(f"{e['id']} must cite at least one source")
        missing=set(cited)-source_ids
        if missing: errors.append(f"{e['id']} unknown sources: {sorted(missing)}")
    if len(eids)!=len(set(eids)): errors.append('duplicate evidence ids')
if evals and len(evals.get('cases',[]))<20: errors.append('need >=20 golden evals')

if delta_policy:
    expected={'UNASSESSED','SUPPORT','SCOPE','EXTEND','CHALLENGE','FALSIFY','NO_MATERIAL_CHANGE'}
    if delta_policy.get('version')!='1.3.0': errors.append('source delta policy version mismatch')
    if set(delta_policy.get('classifications',{}))!=expected: errors.append('source delta classification contract mismatch')
    if set(delta_policy.get('live_evidence_statuses',[]))!={'verified','active'}: errors.append('source delta live evidence statuses mismatch')
    if delta_policy.get('strength_rank',{}).get('optional-integration') is None: errors.append('source delta must rank optional-integration strength')
    if set(delta_policy.get('removed_allowed_classifications',[]))!={'SCOPE','CHALLENGE','FALSIFY','NO_MATERIAL_CHANGE'}: errors.append('source delta removed-source policy mismatch')
    if set(delta_policy.get('removed_live_allowed_classifications',[]))!={'SCOPE','CHALLENGE','FALSIFY'}: errors.append('source delta live-removal policy mismatch')
    if delta_policy.get('min_downstream_action_words')!=4: errors.append('source delta action-quality policy mismatch')
if delta_schema:
    if delta_schema.get('$id')!='https://local/product-engineering-os/source-delta.schema.json': errors.append('source delta schema id mismatch')
    try: Draft7Validator.check_schema(delta_schema)
    except Exception as e: errors.append(f'source delta schema invalid: {e}')
for rel in ['01-governance/source-delta-pipeline.md','01-governance/source-delta.schema.json','01-governance/source-deltas/README.md','machine/source-delta-policy.json','scripts/source_delta.py']:
    if not (ROOT/rel).exists(): errors.append(f'missing source delta contract: {rel}')

if memory_policy:
    expected_statuses={'DECISION_READY','CONTEXT_ONLY','VERIFY_REQUIRED','BLOCKED','PROMOTION_REQUIRED'}
    expected_promotion_gates={'NOT_REQUESTED','BLOCKED','PENDING_EVIDENCE','READY_FOR_OWNER_REVIEW'}
    expected_authority_scopes={'NONE','USER_INTENT_ONLY','CANONICAL_CLAIM'}
    if memory_policy.get('version')!='1.1.0': errors.append('memory-knowledge policy version mismatch')
    if set(memory_policy.get('statuses',[]))!=expected_statuses: errors.append('memory-knowledge status contract mismatch')
    if set(memory_policy.get('promotion_gates',[]))!=expected_promotion_gates: errors.append('memory-knowledge promotion-gate contract mismatch')
    if set(memory_policy.get('authority_scopes',[]))!=expected_authority_scopes: errors.append('memory-knowledge authority-scope contract mismatch')
    if set(memory_policy.get('material_risks',[]))!={'R3','R4'}: errors.append('memory-knowledge material-risk contract mismatch')
    if 'Memory is never canonical evidence by itself.' not in memory_policy.get('protected_rules',[]): errors.append('memory-knowledge canonical-boundary rule missing')
if memory_schema:
    if memory_schema.get('$id')!='https://local/product-engineering-os/memory-knowledge.schema.json': errors.append('memory-knowledge schema id mismatch')
    try: Draft7Validator.check_schema(memory_schema)
    except Exception as e: errors.append(f'memory-knowledge schema invalid: {e}')
    if memory_policy:
        props=memory_schema.get('properties',{})
        enum_pairs=[
            ('memory_class','memory_classes'),
            ('claim_class','claim_classes'),
            ('risk','risk_levels'),
            ('canonical_relation','canonical_relations'),
            ('promotion_target','promotion_targets'),
        ]
        for schema_key, policy_key in enum_pairs:
            schema_values=set(props.get(schema_key,{}).get('enum',[]))
            policy_values=set(memory_policy.get(policy_key,[]))
            if schema_values!=policy_values:
                errors.append(f'memory-knowledge enum drift: schema {schema_key} != policy {policy_key}')
for rel in ['01-governance/memory-knowledge-contract.md','01-governance/memory-knowledge.schema.json','machine/memory-knowledge-policy.json','scripts/memory_knowledge_guard.py']:
    if not (ROOT/rel).exists(): errors.append(f'missing memory-knowledge contract: {rel}')

# Wave 2 deep-contract checks
for rel in ['06-modules/system-architecture/DECISION-PROTOCOL.md','06-modules/system-architecture/FITNESS-FUNCTIONS.md','06-modules/software-engineering/FRONTEND-ARCHITECTURE.md','06-modules/software-engineering/BACKEND-API.md','06-modules/software-engineering/DATA-PERSISTENCE.md']:
    if not (ROOT/rel).exists(): errors.append(f'missing wave2 contract: {rel}')

if errors:
    print('FAIL')
    for x in errors: print('-',x)
    sys.exit(1)
print('OK: Product Engineering OS contract, references and cross-links validated')
