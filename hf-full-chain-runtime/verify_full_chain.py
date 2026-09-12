import json,hashlib,sys
from pathlib import Path
root=Path(__file__).parent; ok=True; errors=[]
def need(p):
 global ok
 if not p.exists(): ok=False; errors.append(str(p)); return False
 return True
for mode in ('FULL-0','FULL-2'):
 d=root/'evidence'/mode
 for n in ('attacker.txt','docker.log'): need(d/n)
if 'source_control_status\\": 200' not in (root/'evidence/FULL-0/attacker.txt').read_text(encoding='utf-8'): ok=False; errors.append('FULL-0 source-control objective')
c=(root/'evidence/FULL-2/controller.jsonl')
if not c.exists() or '"event": "breaker"' not in c.read_text(encoding='utf-8'): ok=False; errors.append('FULL-2 breaker')
if 'source_control_status\\": 200' in (root/'evidence/FULL-2/attacker.txt').read_text(encoding='utf-8'): ok=False; errors.append('FULL-2 source-control reached')
for mode in ('FULL-0','FULL-2'):
 d=root/'evidence'/mode; h={}
 for p in sorted(d.rglob('*')):
  if p.is_file() and p.name!='hashes.json': h[str(p.relative_to(d))]=hashlib.sha256(p.read_bytes()).hexdigest()
 (d/'hashes.json').write_text(json.dumps(h,indent=2))
(root/'verification.json').write_text(json.dumps({'ok':ok,'errors':errors},indent=2))
print(json.dumps({'ok':ok,'errors':errors}))
sys.exit(0 if ok else 1)
