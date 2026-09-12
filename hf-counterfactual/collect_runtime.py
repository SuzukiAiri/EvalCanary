import hashlib,json,shutil,sys
from pathlib import Path
from verify_runtime import verify
root=Path(sys.argv[1] if len(sys.argv)>1 else 'runtime'); out=root/'evidence'; out.mkdir(exist_ok=False)
for n in ['run_manifest.json','canary_policy.yaml','placement_public.json','replay.log']:
 shutil.copy2(root/n,out/n)
for svc in ['k8s-canary','metadata-canary','internal-decoy','final-target']:
 shutil.copy2(root/'logs'/svc/'runtime.jsonl',out/(svc+'.jsonl'))
d=root/'logs/canary-controller'
for q in d.glob('*.json*'): shutil.copy2(q,out/q.name)
if not (out/'controller.jsonl').exists(): (out/'controller.jsonl').write_text('')
(out/'hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir()},indent=2))
r=verify(out); (root/'verification.json').write_text(json.dumps(r,indent=2)); print(json.dumps(r)); sys.exit(0 if r['ok'] else 1)
