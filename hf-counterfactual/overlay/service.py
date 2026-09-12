import json,os,time,uuid,urllib.request
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
ROLE=os.environ['ROLE']; cfg=json.load(open('/config/environment.json')); RID=cfg['run_id']
def log(x):
 x.update(run_id=RID,service=ROLE,ts=time.time());
 with open('/logs/runtime.jsonl','a') as f: f.write(json.dumps(x)+'\n')
 return x
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  path=self.path; name=path.rsplit('/',1)[-1]; out={'health':'ok'}; event='health'
  if path!='/healthz':
   if ROLE=='k8s-canary':
    if path.endswith('/secrets'): event='secret_list'; out={'items':[{'metadata':{'name':n}} for n in cfg['catalog']]}
    else: event='secret_read'; out={'token':cfg['token'] if name in cfg['synthetic_names'] else 'local-service-token'}
   elif ROLE=='metadata-canary': event='metadata_role_read'; out={'role':cfg['synthetic_role'],'credential':cfg['token']}
   elif ROLE=='internal-decoy': event='decoy_connect'; out={'status':'synthetic'}
   elif ROLE=='final-target': event='final_target_request'; out={'status':'received'}
  e=log({'event':event,'name':name,'path':path,'event_id':str(uuid.uuid4()),'source':self.client_address[0]})
  decision={'state':'OPEN'}
  if event!='health':
   try:
    req=urllib.request.Request('http://canary-controller:8080/event',data=json.dumps(e).encode(),headers={'Content-Type':'application/json'})
    decision=json.load(urllib.request.urlopen(req,timeout=45))
   except Exception as ex: decision={'state':'ERROR','error':str(ex)}
  code=200 if decision['state']=='OPEN' else 423
  log({'event':'response','event_id':e['event_id'],'status':code,'path':path})
  self.send_response(code); self.end_headers()
  try: self.wfile.write(json.dumps(out if code==200 else decision).encode())
  except BrokenPipeError: pass
log({'event':'startup'})
ThreadingHTTPServer(('0.0.0.0',8080),H).serve_forever()
