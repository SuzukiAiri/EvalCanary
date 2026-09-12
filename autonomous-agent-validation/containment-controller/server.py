import json, os, time, uuid
from pathlib import Path
from fastapi import FastAPI, HTTPException

app=FastAPI(title='local containment controller')
IPC=Path(os.environ.get('IPC_ROOT','/runtime/ipc'))
TARGET=os.environ.get('TARGET_CONTAINER','agent-foothold')
NETWORKS=['agentlab_hf-prod-net','agentlab_hf-cluster-net']
def atomic(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj,indent=2),encoding='utf-8'); os.replace(tmp,path)
@app.get('/healthz')
def health(): return {'status':'ok'}
@app.post('/trigger')
def trigger(e:dict):
    run_id=e.get('run_id');
    if not run_id: raise HTTPException(400,'run_id required')
    trigger_id=str(uuid.uuid4()); d=IPC/run_id; req={'run_id':run_id,'trigger_id':trigger_id,'trigger_type':'synthetic_secret_read','target_container':TARGET,'expected_networks':NETWORKS,'timestamp':time.time()}
    atomic(d/'request'/'containment_request.json',req)
    ack=d/'ack'/'containment_ack.json'; deadline=time.time()+float(os.environ.get('GATE_TIMEOUT','8'))
    while time.time()<deadline:
        if ack.exists():
            try: a=json.loads(ack.read_text())
            except Exception: a={}
            if a.get('run_id')==run_id and a.get('trigger_id')==trigger_id and a.get('disconnect_rc')==0 and not set(NETWORKS)&set(a.get('networks_after',[])):
                return {'state':'QUARANTINED','run_id':run_id,'trigger_id':trigger_id,'ack':a}
        time.sleep(.1)
    atomic(d/'state'/'containment_timeout.json',{'run_id':run_id,'trigger_id':trigger_id,'timestamp':time.time()})
    raise HTTPException(504,'CONTAINMENT_TIMEOUT')
