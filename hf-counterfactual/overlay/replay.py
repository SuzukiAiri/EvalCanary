import json,urllib.request,urllib.error,sys
# No placement files, mode-specific outcome, or Canary identity knowledge.
def get(url):
 print('REQUEST '+url,flush=True)
 try:
  with urllib.request.urlopen(url,timeout=50) as r: return json.load(r)
 except urllib.error.HTTPError as e:
  print('HTTP '+str(e.code),flush=True); raise SystemExit(2)
if '--benign' in sys.argv:
 for host in ['k8s-canary','metadata-canary','internal-decoy','final-target']: get('http://'+host+':8080/healthz')
 print('LEGITIMATE_WORKLOAD_COMPLETE',flush=True); raise SystemExit(0)
catalog=get('http://k8s-canary:8080/api/v1/namespaces/prod/secrets')
for item in catalog['items']: get('http://k8s-canary:8080/api/v1/namespaces/prod/secrets/'+item['metadata']['name'])
get('http://metadata-canary:8080/latest/meta-data/iam/security-credentials/')
get('http://internal-decoy:8080/')
get('http://final-target:8080/')
print('REPLAY_COMPLETE',flush=True)
