#!/usr/bin/env python3
from pathlib import Path
import json, sys

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
    source_ids=set(ids)
else: source_ids=set()
if evidence:
    eids=[]
    for e in evidence.get('items',[]):
        eids.append(e['id'])
        missing=set(e.get('source_ids',[]))-source_ids
        if missing: errors.append(f"{e['id']} unknown sources: {sorted(missing)}")
    if len(eids)!=len(set(eids)): errors.append('duplicate evidence ids')
if evals and len(evals.get('cases',[]))<20: errors.append('need >=20 golden evals')


# Wave 2 deep-contract checks
for rel in ['06-modules/system-architecture/DECISION-PROTOCOL.md','06-modules/system-architecture/FITNESS-FUNCTIONS.md','06-modules/software-engineering/FRONTEND-ARCHITECTURE.md','06-modules/software-engineering/BACKEND-API.md','06-modules/software-engineering/DATA-PERSISTENCE.md']:
    if not (ROOT/rel).exists(): errors.append(f'missing wave2 contract: {rel}')

if errors:
    print('FAIL')
    for x in errors: print('-',x)
    sys.exit(1)
print('OK: Product Engineering OS contract, references and cross-links validated')
