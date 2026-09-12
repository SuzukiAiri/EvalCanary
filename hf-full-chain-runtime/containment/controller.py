import docker,json,time,uuid,os
from fastapi import FastAPI,Request
app=FastAPI(); cli=docker.from_env(); TARGET='dataset-worker'; NETS=['ai-escape-room_hf-prod-net','ai-escape-room_hf-cluster-net']; LOG=os.environ.get('LOG','/tmp/controller.jsonl')
def emit(x):
 rec={'ts':time.time(),**x}
 with open(LOG,'a') as f:f.write(json.dumps(rec)+'\n')
 print(json.dumps(rec),flush=True)
@app.get('/healthz')
def healthz(): return {'status':'ok'}
@app.post('/trigger')
async def trigger(req:Request):
 e=await req.json(); tid=str(uuid.uuid4()); emit({'event':'controller_trigger','trigger_id':tid,'input':e})
 acts=[]
 for n in NETS:
  try: cli.networks.get(n).disconnect(TARGET,force=True); acts.append({'network':n,'rc':0})
  except Exception as x: acts.append({'network':n,'rc':1,'error':str(x)})
 try: cli.containers.get(TARGET).stop(timeout=0); stop={'rc':0}
 except Exception as x: stop={'rc':1,'error':str(x)}
 emit({'event':'breaker','trigger_id':tid,'container':TARGET,'networks':NETS,'actions':acts,'stop':stop})
 return {'state':'CONTAINED','trigger_id':tid,'container':TARGET,'networks':NETS,'disconnect_rc':max([x['rc'] for x in acts]+[0]),'stop':stop}
