import json, os, subprocess, time
from pathlib import Path
ROOT=Path(__file__).parent/'runtime'/'ipc'; TARGET='agent-foothold'; NETS=['agentlab_hf-prod-net','agentlab_hf-cluster-net']; seen=set()
def docker(*a):
 r=subprocess.run(['docker',*a],capture_output=True,text=True,encoding='utf8',errors='replace'); return r
def atomic(p,o):
 p.parent.mkdir(parents=True,exist_ok=True); t=p.with_suffix('.tmp'); t.write_text(json.dumps(o,indent=2)); os.replace(t,p)
def process(d,req):
 rid=req.get('run_id'); tid=req.get('trigger_id')
 if rid not in str(d) or req.get('target_container')!=TARGET or set(req.get('expected_networks',[]))!=set(NETS): return
 before=[]
 ins=docker('inspect',TARGET)
 if ins.returncode==0:
  try: before=list(json.loads(ins.stdout)[0]['NetworkSettings']['Networks'])
  except Exception: before=[]
 actions=[]
 for n in NETS:
  r=docker('network','disconnect',n,TARGET); actions.append({'network':n,'rc':r.returncode,'stderr':r.stderr})
 after=[]; ins=docker('inspect',TARGET)
 if ins.returncode==0:
  try: after=list(json.loads(ins.stdout)[0]['NetworkSettings']['Networks'])
  except Exception: after=[]
 stop=docker('stop','--time','0',TARGET)
 ack={'run_id':rid,'trigger_id':tid,'disconnect_rc':max([a['rc'] for a in actions] or [0]),'networks_before':before,'networks_after':after,'container_stopped':stop.returncode==0,'stop_rc':stop.returncode,'timestamp':time.time()}
 atomic(d/'ack'/'containment_ack.json',ack); seen.add(str(d))
while True:
 for reqp in ROOT.glob('*/request/containment_request.json'):
  if str(reqp.parent.parent) in seen: continue
  try: process(reqp.parent.parent,json.loads(reqp.read_text()))
  except Exception: pass
 time.sleep(.1)
