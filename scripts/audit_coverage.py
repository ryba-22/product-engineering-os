#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
cov=json.loads((ROOT/'11-maturity/stage-coverage.json').read_text())
ledger={x['id'] for x in json.loads((ROOT/'02-evidence/evidence-ledger.json').read_text())['items']}
evals={x['id'] for x in json.loads((ROOT/'05-evals/golden-evals.json').read_text())['cases']}
required_sections=[
    '## Purpose','## Required inputs','## Questions the Brain must answer','## Workflow',
    '## Decision rules','## Evidence standard','## Canonical outputs','## Failure modes',
    '## Exit conditions','## Handoff'
]
errors=[]
for s in cov['stages']:
    if s.get('status')!='deep-structural': errors.append(f"stage {s['id']} status {s.get('status')}")
    if len(s.get('evidence_ids',[]))<2: errors.append(f"stage {s['id']} has <2 evidence anchors")
    missing=set(s.get('evidence_ids',[]))-ledger
    if missing: errors.append(f"stage {s['id']} missing evidence {sorted(missing)}")
    missing_eval=set(s.get('eval_ids',[]))-evals
    if missing_eval: errors.append(f"stage {s['id']} missing evals {sorted(missing_eval)}")
    if not all(s.get('criteria',{}).values()): errors.append(f"stage {s['id']} incomplete structural criteria")
    p=ROOT/s.get('stage_playbook','')
    if not p.exists():
        errors.append(f"stage {s['id']} missing stage playbook {p}")
        continue
    text=p.read_text()
    words=len(re.findall(r"\b[\w-]+\b", text, flags=re.UNICODE))
    if words < 350: errors.append(f"stage {s['id']} playbook too shallow: {words} words")
    for section in required_sections:
        if section not in text: errors.append(f"stage {s['id']} missing section {section}")
    for eid in s.get('evidence_ids',[]):
        if eid not in text: errors.append(f"stage {s['id']} playbook does not declare {eid}")
    if s.get('behavioral_validation') not in {'pending-independent-eval','executed','executed-self-assessed','independently-behaviorally-validated-v1','independently-behaviorally-validated-v2','revalidation-required'}:
        errors.append(f"stage {s['id']} invalid behavioral_validation")
    if s.get('behavioral_validation') == 'executed-self-assessed':
        ev=ROOT/s.get('behavioral_evidence','')
        if not ev.exists(): errors.append(f"stage {s['id']} missing behavioral evidence file {ev}")
        if s.get('behavioral_independent') is not False: errors.append(f"stage {s['id']} self-assessed run must set behavioral_independent=false")
    if s.get('behavioral_validation') == 'revalidation-required':
        if s.get('behavioral_run_id') is not None or s.get('behavioral_evidence') is not None:
            errors.append(f"stage {s['id']} revalidation-required must not expose current run/evidence")
        if not s.get('last_behavioral_run_id') or not s.get('last_behavioral_evidence'):
            errors.append(f"stage {s['id']} revalidation-required missing historical evidence pointer")
    if s.get('behavioral_validation','').startswith('independently-behaviorally-validated-v'):
        ev=ROOT/s.get('behavioral_evidence','')
        if not ev.exists(): errors.append(f"stage {s['id']} missing independent behavioral evidence file {ev}")
        if s.get('behavioral_independent') is not True: errors.append(f"stage {s['id']} independent run must set behavioral_independent=true")
        if s.get('behavioral_score',0) < 8: errors.append(f"stage {s['id']} independent score below threshold")
        if s.get('behavioral_hard_fail') is not False: errors.append(f"stage {s['id']} independent hard fail remains")
if errors:
    print('FAIL coverage/depth')
    for e in errors: print('-',e)
    sys.exit(1)
print('OK: 25 stage playbooks have evidence linkage, substantive decision workflows and structural integration. Behavioral effectiveness is reported separately.')
