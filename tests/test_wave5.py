from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
REQ=[
 '06-modules/product-intelligence/PRODUCT-ANALYTICS.md','06-modules/product-intelligence/EXPERIMENTATION.md','06-modules/product-intelligence/FEEDBACK-LOOP.md',
 '07-templates/METRIC-TREE.md','07-templates/TRACKING-PLAN.md','07-templates/EXPERIMENT-PLAN.md','07-templates/OUTCOME-REVIEW.md'
]
def test_wave5_files(): assert not [x for x in REQ if not (ROOT/x).exists()]
def test_wave5_sources():
 ids={x['id'] for x in json.loads((ROOT/'01-governance/source-registry.json').read_text())['sources']}
 for x in ['GOOGLE-HEART','OCE-GUIDE','MS-SRM','GOVUK-MEASURE','AMPLITUDE-NORTHSTAR']: assert x in ids
def test_wave5_evidence(): assert len(json.loads((ROOT/'02-evidence/evidence-ledger.json').read_text())['items'])>=55
def test_wave5_evals():
 d=json.loads((ROOT/'05-evals/golden-evals.json').read_text()); assert len(d['cases'])>=56
 tags={t for c in d['cases'] for t in c.get('tags',[])}
 for x in ['metric-tree','event-taxonomy','ab-testing','sample-ratio-mismatch','feedback-loop']: assert x in tags
def test_wave5_version():
 m=json.loads((ROOT/'manifest.json').read_text()); assert tuple(map(int,m['version'].split('.'))) >= (0,5,0); assert m['status'] in {'foundation-through-wave-5','integrated'}
