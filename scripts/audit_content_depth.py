#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]

# Intentionally concise files are contracts, templates, crosswalks or entry-point routing docs.
def intentionally_concise(p: Path) -> bool:
    rel=p.relative_to(ROOT).as_posix()
    if rel.startswith('07-templates/'): return True
    if rel.startswith('05-evals/') and p.name.endswith('-PROMPT.md'): return True
    if rel.endswith('/MODULE.md'): return True
    if rel.startswith('08-adapters/'): return True
    if rel.startswith('skills/product-engineering-os/') and '/references/stages/' not in rel: return True
    if rel in {
        '03-decisions/DECISION-RECORD-TEMPLATE.md',
        '10-source-notes/README.md',
        '11-maturity/MATURITY.md',
        'tests/baseline-pressure-scenarios.md',
        'examples/idempotent-enrollment/EVALUATION.md',
        'examples/idempotent-enrollment/README.md',
        '06-modules/STAGE-INDEX.md',
    }: return True
    return False

errors=[]
checked=0
for p in ROOT.rglob('*.md'):
    if any(x in p.parts for x in {'.git','__pycache__','.pytest_cache','.venv'}):
        continue
    rel=p.relative_to(ROOT).as_posix()
    # Skill stage copies are validated byte-for-byte elsewhere.
    if rel.startswith('skills/product-engineering-os/references/stages/'):
        continue
    words=len(re.findall(r'\b[\w-]+\b',p.read_text(),flags=re.UNICODE))
    if intentionally_concise(p):
        continue
    if p.name.startswith('STAGE-'):
        checked += 1
        if words < 350: errors.append(f'{rel}: stage playbook too short ({words} words)')
        continue
    checked += 1
    if words < 250:
        errors.append(f'{rel}: unexplained shallow markdown ({words} words)')

if errors:
    print('FAIL content depth')
    for e in errors: print('-',e)
    sys.exit(1)
print(f'OK: content-depth policy passed for {checked} substantive markdown files; concise contracts/templates are explicitly exempted.')
