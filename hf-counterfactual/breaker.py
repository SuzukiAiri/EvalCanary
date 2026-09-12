import argparse,json,subprocess,time
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--runtime',default='runtime'); a=p.parse_args(); root=Path(a.runtime).resolve(); rid=json.loads((root/'run_manifest.json').read_text())['run_id']; d=root/'logs/canary-controller'
def docker(*args):
 t=time.time(); r=subprocess.run(['docker',*args],capture_output=True,text=True); return {'started':t,'finished':time.time(),'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def atomic(n,x):
 q=d/(n+'.tmp'); q.write_text(json.dumps(x)); q.replace(d/n)
end=time.monotonic()+90
while not (d/'containment_request.json').exists():
 if time.monotonic()>end: raise SystemExit('request timeout')
 time.sleep(.02)
r=json.loads((d/'containment_request.json').read_text()); target='hfbench-replay'; nets=['hfbench_hf-cluster-net','hfbench_control']
assert r['run_id']==rid and r['trigger_id'] and r['container']==target and r['networks']==nets
info=json.loads(docker('inspect',target)['stdout'])[0]
assert info['Config']['Labels']['hfbench.run_id']==rid
assert sorted(info['NetworkSettings']['Networks'])==sorted(nets)
identity={k:r[k] for k in ['run_id','trigger_id','container','networks']}; actions=[]
for net in nets: actions.append(dict(docker('network','disconnect',net,target),network=net))
inspection=docker('inspect',target); remaining=json.loads(inspection['stdout'])[0]['NetworkSettings']['Networks']
b=dict(identity,actions=actions,inspection=inspection,remaining_networks=list(remaining)); atomic('breaker.json',b)
assert all(x['rc']==0 for x in actions) and not remaining
ack=dict(identity,network_isolated=True,disconnect_rc=0,ack_ts=time.time()); atomic('containment_ack.json',ack)
stop=docker('stop','--time','0',target); atomic('stop.json',dict(identity,**stop)); print(json.dumps(ack),flush=True)
