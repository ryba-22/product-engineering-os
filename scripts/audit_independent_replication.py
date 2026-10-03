#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys, subprocess

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'05-evals/independent-replication-v1'
errors=[]

def load(name):
    try:
        return json.loads((BASE/name).read_text())
    except Exception as e:
        errors.append(f'{name}: {e}')
        return {}

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

manifest=load('run-manifest.json')
executor=load('executor-results.json')
exprov=load('executor-provenance.json')
judge=load('judge-results.json')
model_judge=load('judge-model-output.json')
normalization=load('judge-normalization.json')
jgprov=load('judge-provenance.json')
rubric=load('judge-rubric.json')
exws=load('executor-workspace-files.json')
jgws=load('judge-workspace-files.json')
comparison=load('comparison.json')

if manifest.get('status')!='completed':
    errors.append('replication manifest not completed')
if manifest.get('source_scenario_sha256')!=sha(ROOT/'05-evals/adversarial-run-v1/scenarios.json'):
    errors.append('source scenario hash mismatch')
if manifest.get('source_executor_input_sha256')!=sha(ROOT/'05-evals/adversarial-run-v1/executor-input.json'):
    errors.append('source executor-input hash mismatch')
if manifest.get('rubric_sha256')!=sha(BASE/'judge-rubric.json'):
    errors.append('rubric hash mismatch')
if manifest.get('executor',{}).get('result_sha256')!=sha(BASE/'executor-results.json'):
    errors.append('executor result hash mismatch')
if manifest.get('judge',{}).get('result_sha256')!=sha(BASE/'judge-results.json'):
    errors.append('judge result hash mismatch')

if exprov.get('raw_output_sha256')!=sha(BASE/'executor-raw-envelope.json'):
    errors.append('executor raw envelope hash mismatch')
if exprov.get('structured_output_sha256')!=sha(BASE/'executor-results.json'):
    errors.append('executor structured output hash mismatch')
if jgprov.get('raw_output_sha256')!=sha(BASE/'judge-raw-envelope.json'):
    errors.append('judge raw envelope hash mismatch')
if jgprov.get('model_structured_output_sha256')!=sha(BASE/'judge-model-output.json'):
    errors.append('judge model structured output hash mismatch')
if jgprov.get('normalized_result_sha256')!=sha(BASE/'judge-results.json'):
    errors.append('judge normalized result hash mismatch')
if normalization.get('model_output_sha256')!=sha(BASE/'judge-model-output.json'):
    errors.append('normalization model-output hash mismatch')
if normalization.get('normalized_summary')!=judge.get('summary'):
    errors.append('normalization summary mismatch')
if model_judge.get('cases')!=judge.get('cases') or model_judge.get('judge')!=judge.get('judge') or model_judge.get('run_id')!=judge.get('run_id'):
    errors.append('normalization changed case judgments or judge identity')
if model_judge.get('summary',{}).get('average_score')!=9.12 or judge.get('summary',{}).get('average_score')!=9.16:
    errors.append('expected 9.12 raw -> 9.16 deterministic summary normalization not preserved')

ids=[f'ADV-S{i:02d}' for i in range(1,26)]
for label,obj in [('executor',executor),('judge',judge),('rubric',rubric)]:
    got=[c.get('id') for c in obj.get('cases',[])]
    if got!=ids:
        errors.append(f'{label} ids/order mismatch: {got}')

ex=executor.get('executor',{})
jg=judge.get('judge',{})
if ex.get('provider')!='Google Antigravity' or ex.get('model')!='gemini-3.1-pro-high':
    errors.append(f'bad executor identity {ex}')
if jg.get('provider')!='Anthropic Claude Code' or jg.get('model')!='claude-opus-4-6':
    errors.append(f'bad judge identity {jg}')
if ex.get('provider')==jg.get('provider') or ex.get('model')==jg.get('model'):
    errors.append('executor and judge not distinct')
if exprov.get('criteria_blinded') is not True:
    errors.append('executor provenance does not assert criteria_blinded=true')
if jgprov.get('prior_results_blinded') is not True:
    errors.append('judge provenance does not assert prior_results_blinded=true')

expected_ex_eval=[
    '05-evals/adversarial-run-v1/executor-input.json',
    '05-evals/independent-run-v1/executor-output-schema.json'
]
if exws.get('evaluation_files')!=expected_ex_eval:
    errors.append(f'executor isolated eval files differ: {exws.get("evaluation_files")}')
if exws.get('forbidden_prior_result_files_present') not in ([],None):
    errors.append(f'executor workspace leaked prior result files: {exws.get("forbidden_prior_result_files_present")}')
expected_judge_eval=[
    '05-evals/independent-run-v1/executor-results.json',
    '05-evals/independent-run-v1/judge-output-schema.json',
    '05-evals/independent-run-v1/judge-rubric.json'
]
if jgws.get('evaluation_files')!=expected_judge_eval:
    errors.append(f'judge isolated eval files differ: {jgws.get("evaluation_files")}')
if jgws.get('forbidden_prior_result_files_present') not in ([],None):
    errors.append(f'judge workspace leaked prior result files: {jgws.get("forbidden_prior_result_files_present")}')

summary=judge.get('summary',{})
cases=judge.get('cases',[])
if summary.get('total')!=25 or summary.get('passed')!=25 or summary.get('failed')!=0 or summary.get('hard_failures')!=[]:
    errors.append(f'replication summary not 25/25 clean: {summary}')
computed=[]
for c in cases:
    total=sum(c.get('scores',{}).values())
    if total!=c.get('total'):
        errors.append(f'{c.get("id")} score sum mismatch')
    should=total>=8 and not c.get('hard_fail')
    if c.get('pass')!=should:
        errors.append(f'{c.get("id")} pass logic mismatch')
    if c.get('hard_fail'):
        errors.append(f'{c.get("id")} hard fail remains')
    computed.append(total)
if computed and round(sum(computed)/len(computed),2)!=summary.get('average_score'):
    errors.append('replication average score mismatch')

if comparison.get('all_25_pass_both_runs') is not True:
    errors.append('not all 25 passed both independent runs')
if comparison.get('hard_fail_in_either_run') is not False:
    errors.append('hard fail exists in one independent run')
v1=json.loads((ROOT/'05-evals/independent-run-v1/judge-results.json').read_text())
if v1.get('summary',{}).get('passed')!=25 or v1.get('summary',{}).get('hard_failures')!=[]:
    errors.append('independent v1 no longer clean')

coverage=json.loads((ROOT/'11-maturity/stage-coverage.json').read_text())
by_stage={c['stage_id']:c for c in cases}
for s in coverage.get('stages',[]):
    if s.get('behavioral_replication_run_id')!=manifest.get('run_id'):
        errors.append(f'stage {s["id"]} replication run id mismatch')
    jc=by_stage.get(s['id'])
    if not jc or s.get('behavioral_replication_score')!=jc.get('total'):
        errors.append(f'stage {s["id"]} replication score mismatch')
    if s.get('behavioral_replication_hard_fail') is not False:
        errors.append(f'stage {s["id"]} replication hard fail flag')

if errors:
    print('FAIL independent replication')
    for e in errors:
        print('-',e)
    sys.exit(1)
print(f'OK: independent replication 25/25, avg={summary.get("average_score")}, executor={ex.get("model")}, judge={jg.get("model")}, same frozen scenario set')
