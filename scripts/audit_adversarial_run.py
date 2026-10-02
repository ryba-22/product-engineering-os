#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'05-evals/adversarial-run-v1'
errors=[]

def load(name):
    try:
        return json.loads((BASE/name).read_text())
    except Exception as e:
        errors.append(f'{name}: {e}')
        return {}

sc=load('scenarios.json')
inp=load('executor-input.json')
j1=load('judge-results-round1.json')
j2=load('judge-results-round2-s15.json')
final=load('final-results.json')

cases=sc.get('cases',[])
ids=[x.get('id') for x in cases]
stages=[x.get('stage_id') for x in cases]
if len(cases)!=25: errors.append(f'scenarios: expected 25, got {len(cases)}')
if len(set(ids))!=25: errors.append('scenario ids must be unique')
if sorted(stages)!=list(range(1,26)): errors.append('scenarios must cover stages 1..25 exactly')

icases=inp.get('cases',[])
if [x.get('id') for x in icases] != ids: errors.append('executor input ids/order differ from frozen scenarios')
for x in icases:
    if 'must_do' in x or 'must_not_do' in x:
        errors.append(f"{x.get('id')}: executor input leaked judge criteria")

s1=j1.get('summary',{})
if s1.get('passed')!=24 or s1.get('failed')!=1 or s1.get('hard_failures')!=['ADV-S15']:
    errors.append(f'round1 expected 24/25 with ADV-S15 hard fail, got {s1}')

s2=j2.get('summary',{})
if s2.get('passed')!=1 or s2.get('failed')!=0:
    errors.append(f'round2 expected targeted pass, got {s2}')

fs=final.get('final_summary',{})
if fs.get('passed')!=25 or fs.get('failed')!=0 or fs.get('hard_failures')!=[]:
    errors.append(f'final expected 25/25 no hard failures, got {fs}')

fcases=final.get('cases',[])
if len(fcases)!=25: errors.append(f'final cases expected 25, got {len(fcases)}')

weights={'decision_correctness':4,'evidence_scope':2,'risk_and_constraints':1,'execution_closure':1,'verification':1,'traceability':1}
for x in fcases:
    scores=x.get('scores',{})
    if set(scores)!=set(weights): errors.append(f"{x.get('id')}: score dimensions differ")
    for k,maxv in weights.items():
        v=scores.get(k,-1)
        if not isinstance(v,int) or not (0<=v<=maxv): errors.append(f"{x.get('id')}: invalid {k}={v}")
    if x.get('total') != sum(scores.values()): errors.append(f"{x.get('id')}: total mismatch")
    if not x.get('pass'): errors.append(f"{x.get('id')}: final case not passing")
    if x.get('hard_fail'): errors.append(f"{x.get('id')}: final hard fail remains")

round2ids=[x.get('id') for x in fcases if x.get('source_round')==2]
if round2ids!=['ADV-S15']: errors.append(f'only ADV-S15 should come from round2, got {round2ids}')

gold=json.loads((ROOT/'05-evals/golden-evals.json').read_text())
if not any(x.get('id')=='EV-S15-STATE' for x in gold.get('cases',[])):
    errors.append('missing EV-S15-STATE regression eval')
stage15=(ROOT/'06-modules/quality-engineering/STAGE-15-TESTING.md').read_text()
if 'Completion-state guard' not in stage15 or 'not **VERIFIED**' not in stage15:
    errors.append('Stage 15 completion-state regression guard missing')

if errors:
    print('FAIL adversarial run')
    for e in errors: print('-',e)
    sys.exit(1)
print('OK: adversarial run is complete, frozen/blinded inputs are intact, round1 defect is preserved, and final 25/25 evidence is internally consistent')
