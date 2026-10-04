#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
idx=json.loads((ROOT/'PACKAGE-INDEX.json').read_text())
exclude={'.git','__pycache__','.pytest_cache','.venv'}
actual=[]
for p in ROOT.rglob('*'):
    if not p.is_file(): continue
    if any(x in p.parts for x in exclude): continue
    if p.suffix in {'.pyc','.pyo'}: continue
    actual.append(p.relative_to(ROOT).as_posix())
actual=sorted(actual)
listed=sorted(idx.get('files',[]))
missing=sorted(set(actual)-set(listed))
stale=sorted(set(listed)-set(actual))
errors=[]
if idx.get('version')!='1.2.0': errors.append(f"index version {idx.get('version')} != 1.2.0")
if missing: errors.append('missing from index: '+', '.join(missing))
if stale: errors.append('stale index entries: '+', '.join(stale))
if len(listed)!=len(set(listed)): errors.append('duplicate index entries')
if errors:
    print('FAIL package index')
    for e in errors: print('-',e)
    sys.exit(1)
print(f'OK: package index matches {len(actual)} files')
