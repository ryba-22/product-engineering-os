#!/usr/bin/env python3
from pathlib import Path
import argparse,json,datetime,sys
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument('--as-of',default=datetime.date.today().isoformat()); p.add_argument('--max-age-days',type=int,default=365); args=p.parse_args()
asof=datetime.date.fromisoformat(args.as_of)
reg=json.loads((ROOT/'01-governance/source-registry.json').read_text())
stale=[]
skipped=[]
for s in reg['sources']:
    if s.get('availability') == 'optional-not-bundled':
        skipped.append(s['id']); continue
    v=s.get('verified_at')
    if not v: stale.append((s['id'],'missing verified_at')); continue
    age=(asof-datetime.date.fromisoformat(v)).days
    if age < 0: stale.append((s['id'],'verification date is in the future')); continue
    if age>args.max_age_days: stale.append((s['id'],f'{age} days'))
if stale:
    print('STALE/MISSING')
    for x in stale: print('-',*x)
    sys.exit(1)
print(f"OK: {len(reg['sources'])-len(skipped)} source records within {args.max_age_days} days as of {asof}")

if skipped: print("OPTIONAL/NOT CONNECTED:", ", ".join(skipped))
