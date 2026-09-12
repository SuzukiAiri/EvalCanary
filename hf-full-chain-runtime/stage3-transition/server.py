import os, httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
app=FastAPI(title='Explicit Stage3 Transition Adapter')
K8S=os.environ.get('K8S_URL','http://k8s-api:8080')
@app.get('/healthz')
def healthz(): return {'status':'ok','classification':'EXPLICIT TRANSITION ADAPTER'}
@app.api_route('/k8s/{path:path}',methods=['GET','POST','PUT','PATCH','DELETE'])
async def forward(path:str,request:Request):
    auth=request.headers.get('authorization','')
    if not auth.startswith('Bearer '): raise HTTPException(401,'adapter requires forwarded bearer credential')
    body=await request.body()
    async with httpx.AsyncClient(timeout=20) as c:
        r=await c.request(request.method,f'{K8S}/{path}',content=body or None,headers={'Authorization':auth})
    return Response(r.content,status_code=r.status_code,headers={'Content-Type':r.headers.get('content-type','application/json')})
