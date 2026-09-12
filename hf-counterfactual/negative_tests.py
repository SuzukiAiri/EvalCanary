import json,hashlib,shutil,tempfile
from pathlib import Path
from verify_runtime import verify
src=Path('evidence/final/C2-seed-1/evidence'); assert verify(src)['ok']
results=[]
for case in ['missing_ack','wrong_run','old_ack','target_after_trigger','disconnect_failure','ack_before_trigger','hash_tamper']:
 with tempfile.TemporaryDirectory(prefix='hf-verifier-negative-') as td:
  p=Path(td)/'bundle'; shutil.copytree(src,p)
  def edit(n,fn):
   x=json.loads((p/n).read_text()); fn(x); (p/n).write_text(json.dumps(x))
  if case=='missing_ack': (p/'containment_ack.json').unlink()
  if case in ['wrong_run','old_ack']: edit('containment_ack.json',lambda x:x.update(run_id='stale-run',trigger_id='old-trigger'))
  if case=='disconnect_failure': edit('breaker.json',lambda x:x['actions'][0].update(rc=1))
  if case=='ack_before_trigger': edit('containment_ack.json',lambda x:x.update(ack_ts=0))
  if case=='target_after_trigger':
   req=json.loads((p/'containment_request.json').read_text())
   with (p/'final-target.jsonl').open('a') as f: f.write(json.dumps({'event':'final_target_request','run_id':req['run_id'],'ts':req['request_ts']+1,'service':'final-target'})+'\n')
  if case=='hash_tamper':
   with (p/'replay.log').open('a') as f: f.write('tampered')
  else:
   (p/'hashes.json').write_text(json.dumps({q.name:hashlib.sha256(q.read_bytes()).hexdigest() for q in p.iterdir() if q.name!='hashes.json'}))
  result=verify(p); assert not result['ok'],case
  results.append({'case':case,'rejected':True,'reason':result['error']})
Path('negative-test-results.json').write_text(json.dumps(results,indent=2)); print(json.dumps(results,indent=2))
