#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'05-evals'/'independent-run-v3'
errors=[]

def load(name):
    try: return json.loads((D/name).read_text())
    except Exception as e: errors.append(f'{name}: {e}'); return {}

def sha(name): return hashlib.sha256((D/name).read_bytes()).hexdigest()

manifest=load('run-manifest.json')
inputs=load('executor-input.json')
executor=load('executor-results.json')
rubric=load('judge-rubric.json')
judge=load('judge-results.json')
ids=[c.get('id') for c in inputs.get('cases',[])]
if len(ids)!=12 or len(set(ids))!=12: errors.append('expected 12 unique holdout ids')
for c in inputs.get('cases',[]):
    if set(c)-{'id','scenario','decision_to_make','mutation_axes'}: errors.append(f"{c.get('id')}: executor input contains unexpected/leaky fields")
    if len(c.get('mutation_axes',[]))<4: errors.append(f"{c.get('id')}: insufficient mutation axes")
if {c.get('id') for c in executor.get('cases',[])} != set(ids): errors.append('executor id set mismatch')
if {c.get('id') for c in judge.get('cases',[])} != set(ids): errors.append('judge id set mismatch')
for c in executor.get('cases',[]):
    for key in ['decision','actions','required_evidence','risks_or_unknowns','stop_condition']:
        if not c.get(key): errors.append(f"{c.get('id')}: missing executor {key}")
for c in judge.get('cases',[]):
    if c.get('score',0)<8 or c.get('hard_fail') is not False or c.get('verdict')!='PASS': errors.append(f"{c.get('id')}: not PASS")
for name in ['executor-input.json','judge-rubric.json','executor-results.json','judge-results.json']:
    expected=manifest.get('sha256',{}).get(name)
    if expected!=sha(name): errors.append(f'{name}: hash mismatch')
if manifest.get('result')!={'passed':12,'failed':0,'hard_failures':0,'average_score':9.0}: errors.append('manifest result mismatch')
if rubric.get('pass_rule',{}).get('min_score')!=8: errors.append('rubric pass threshold mismatch')
if errors:
    print('FAIL independent eval v3')
    for e in errors: print('-',e)
    sys.exit(1)
print('PASS independent eval v3: 12/12 unseen holdouts, 0 hard failures, avg 9.0/10')
