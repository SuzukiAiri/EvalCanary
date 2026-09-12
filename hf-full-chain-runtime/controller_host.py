import json,subprocess,time,uuid,os
from http.server import BaseHTTPRequestHandler,HTTPServer
ROOT=os.path.abspath(os.path.dirname(__file__)); LOG=os.path.join(ROOT,'full2_controller.jsonl'); TARGET='dataset-worker'; NETS=['ai-escape-room_hf-prod-net','ai-escape-room_hf-cluster-net']
def emit(x):
 with open(LOG,'a') as f:f.write(json.dumps({'ts':time.time(),**x})+'\n')
def run(*args):
 r=subprocess.run(['docker',*args],capture_output=True,text=True); return {'args':args,'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
class H(BaseHTTPRequestHandler):
 def do_POST(self):
  e=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0')))); tid=str(uuid.uuid4()); emit({'event':'controller_trigger','trigger_id':tid,'input':e})
  acts=[run('network','disconnect',n,TARGET) for n in NETS]; stop=run('stop','--time','0',TARGET)
  emit({'event':'breaker','trigger_id':tid,'container':TARGET,'networks':NETS,'actions':acts,'stop':stop,'disconnect_rc':max([a['rc'] for a in acts]+[0])})
  out={'state':'CONTAINED','trigger_id':tid,'container':TARGET,'networks':NETS,'disconnect_rc':max([a['rc'] for a in acts]+[0])}
  b=json.dumps(out).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
 def log_message(self,*a): pass
emit({'event':'controller_start','target':TARGET,'networks':NETS})
HTTPServer(('0.0.0.0',18090),H).serve_forever()
