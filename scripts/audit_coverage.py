#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
cov=json.loads((ROOT/'11-maturity/stage-coverage.json').read_text())
ledger={x['id'] for x in json.loads((ROOT/'02-evidence/evidence-ledger.json').read_text())['items']}
evals={x['id'] for x in json.loads((ROOT/'05-evals/golden-evals.json').read_text())['cases']}
errors=[]
for s in cov['stages']:
    if s['status']!='very-strong': errors.append(f"stage {s['id']} status {s['status']}")
    if len(s['evidence_ids'])<2: errors.append(f"stage {s['id']} has <2 evidence anchors")
    missing=set(s['evidence_ids'])-ledger
    if missing: errors.append(f"stage {s['id']} missing evidence {sorted(missing)}")
    missing_eval=set(s['eval_ids'])-evals
    if missing_eval: errors.append(f"stage {s['id']} missing evals {sorted(missing_eval)}")
    if not all(s['criteria'].values()): errors.append(f"stage {s['id']} incomplete criteria")
    for ref in s['artifact_refs']+[s['decision_system']]:
        if not (ROOT/ref).exists(): errors.append(f"stage {s['id']} missing artifact {ref}")
if errors:
    print('FAIL coverage')
    for e in errors: print('-',e)
    sys.exit(1)
print('OK: 25/25 stages satisfy very-strong structural baseline')
