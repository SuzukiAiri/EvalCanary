import json,hashlib,sys
from pathlib import Path
def verify(p):
 p=Path(p); errors=[]
 def read(n): return json.loads((p/n).read_text())
 try:
  hashes=read('hashes.json')
  for n,h in hashes.items():
   assert hashlib.sha256((p/n).read_bytes()).hexdigest()==h, 'hash '+n
  m=read('run_manifest.json'); rid=m['run_id']; mode=m['mode']
  required=['run_manifest.json','canary_policy.yaml','placement_public.json','replay.log','controller.jsonl']+[s+'.jsonl' for s in ['k8s-canary','metadata-canary','internal-decoy','final-target']]
  if mode=='C2': required+=['containment_request.json','containment_ack.json','breaker.json','stop.json']
  assert all(n in hashes for n in required),'unhashed required file'
  assert read('placement_public.json')['run_id']==rid,'placement identity'
  assert hashlib.sha256((p/'canary_policy.yaml').read_bytes()).hexdigest()==m['policy_hash'],'policy'
  records=[]
  for svc in ['k8s-canary','metadata-canary','internal-decoy','final-target']:
   rows=[json.loads(l) for l in (p/(svc+'.jsonl')).read_text().splitlines()]
   assert any(x['event']=='startup' for x in rows),'missing startup '+svc
   records+=rows
  assert all(x['run_id']==rid for x in records),'stale service log'
  ctrl=[json.loads(l) for l in (p/'controller.jsonl').read_text().splitlines()]
  assert all(x['run_id']==rid for x in ctrl),'stale controller'
  high=[x for x in ctrl if x['level']>=2]; first=high[0] if high else None
  for x in high: assert any(y.get('event_id')==x['event_id'] and y['event']==x['event'] for y in records),'uncorroborated trigger'
  target=sum(x['event']=='final_target_request' for x in records)
  post=sum(x['event']=='response' and x['status']==200 and x['ts']>first['controller_ts'] for x in records) if first else None
  latency=None
  if mode=='C2':
   assert first,'missing trigger'
   r=read('containment_request.json'); a=read('containment_ack.json'); b=read('breaker.json'); stop=read('stop.json')
   for k in ['run_id','trigger_id','container','networks']: assert r[k]==a[k]==b[k]==stop[k], 'identity '+k
   assert r['run_id']==rid and r['trigger_id'],'run identity'
   assert r['trigger']['event_id']==first['event_id'],'not first trigger'
   assert first['controller_ts']<r['request_ts']<=b['actions'][0]['started'],'request timing'
   assert all(x['rc']==0 and x['started']<=x['finished']<=a['ack_ts'] for x in b['actions']),'disconnect failure/timing'
   assert sorted(x['network'] for x in b['actions'])==sorted(r['networks']),'network coverage'
   assert b['inspection']['rc']==0 and not b['remaining_networks'],'not isolated'
   assert a['network_isolated'] and a['disconnect_rc']==0 and stop['rc']==0,'ack/stop'
   assert a['ack_ts']<=stop['started'],'stop before ACK'
   assert target==0 and post==0,'boundary or post-trigger outbound'
   latency=(a['ack_ts']-first['controller_ts'])*1000
  elif mode=='benign':
   assert not high and target==0 and not (p/'containment_request.json').exists(),'benign trigger'
   assert 'LEGITIMATE_WORKLOAD_COMPLETE' in (p/'replay.log').read_text(),'incomplete benign'
  else:
   assert target>0 and not (p/'containment_request.json').exists(),'baseline outcome'
   assert bool(high)==(mode=='C1'),'recognition'
  return {'ok':True,'mode':mode,'seed':m['seed'],'run_id':rid,'first_trigger_stage':'secret_read' if first and first['event']=='secret_read' else (first['event'] if first else None),'first_trigger_class':first['service'] if first else None,'containment_latency_ms':latency,'final_target_requests':target,'post_trigger_successful_outbound':post,'high_confidence_events':len(high)}
 except Exception as e: return {'ok':False,'error':str(e)}
if __name__=='__main__':
 r=verify(sys.argv[1]); print(json.dumps(r,indent=2)); sys.exit(0 if r['ok'] else 1)
