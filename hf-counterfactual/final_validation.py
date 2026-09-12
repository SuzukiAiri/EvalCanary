import json,subprocess,sys,shutil,time
from pathlib import Path
R=Path(__file__).resolve().parent

def cmd(args,log,check=True):
 p=subprocess.run(args,cwd=R,capture_output=True,text=True,encoding="utf-8",errors="replace")
 with log.open('a',encoding='utf-8') as f: f.write('\nCOMMAND '+str(args)+'\n'+p.stdout+p.stderr)
 if check and p.returncode: raise RuntimeError(str(args)+' rc='+str(p.returncode))
 return p

def archive():
 rt=R/'runtime'
 if not rt.exists(): return
 dest=R/'evidence/archive'/('prior-'+str(time.time_ns())); dest.parent.mkdir(parents=True,exist_ok=True)
 if (rt/'compose.json').exists(): cmd(['docker','compose','-f',str(rt/'compose.json'),'down'],R/'final-validation.log')
 shutil.move(str(rt),str(dest))

def run(mode,seed):
 archive(); log=R/'final-validation.log'
 cmd([sys.executable,'prepare_run.py','--seed',str(seed),'--mode',mode],log)
 rt=R/'runtime'; compose=['docker','compose','-f',str(rt/'compose.json')]
 cmd(compose+['up','-d','--no-build'],log)
 # Real health probes; /healthz is not a Canary interaction or final objective.
 probe="import urllib.request; [urllib.request.urlopen('http://'+s+':8080/healthz',timeout=2).read() for s in ['k8s-canary','metadata-canary','internal-decoy','final-target']]"
 for attempt in range(30):
  p=cmd(['docker','exec','hfbench-replay','python','-c',probe],log,False)
  if p.returncode==0: break
  time.sleep(1)
 else: raise RuntimeError('health timeout')
 networks=json.loads(subprocess.check_output(['docker','network','inspect','hfbench_hf-cluster-net','hfbench_control'],text=True)); assert all(n['Internal'] for n in networks)
 (rt/'network-inspect.json').write_text(json.dumps(networks,indent=2))
 bp=None; bf=None
 if mode=='C2':
  bf=(rt/'breaker-process.log').open('w'); bp=subprocess.Popen([sys.executable,'breaker.py','--runtime',str(rt)],cwd=R,stdout=bf,stderr=bf)
 p=cmd(['docker','exec','hfbench-replay','python','/app/replay.py']+(['--benign'] if mode=='benign' else []),log,False)
 (rt/'replay.log').write_text(p.stdout+p.stderr)
 if bp:
  bp.wait(timeout=60); bf.close()
  assert bp.returncode==0,'breaker failed'
 cmd(compose+['logs','--no-color'],rt/'docker.log',False)
 # Stop without restarting replay; logs are quiescent before collection.
 cmd(compose+['stop'],log)
 p=cmd([sys.executable,'collect_runtime.py',str(rt)],log,False)
 dest=R/'evidence/final'/f'{mode}-seed-{seed}'; dest.parent.mkdir(parents=True,exist_ok=True)
 assert not dest.exists(); shutil.copytree(rt,dest)
 result=json.loads((rt/'verification.json').read_text()); print(json.dumps(result),flush=True)
 if not result['ok']: raise RuntimeError('verification failed; preserved '+str(dest))
 return result
if __name__=='__main__':
 results=[]
 for mode,seed in [('benign',1),('C2',1),('C2',2),('C2',3),('C2',4),('C2',5),('C0',1),('C1',1)]:
  results.append(run(mode,seed)); (R/'final-results.json').write_text(json.dumps(results,indent=2))
