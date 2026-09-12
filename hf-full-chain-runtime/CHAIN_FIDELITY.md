# Chain fidelity

| Stage | Implementation | Runtime executed | Evidence |
|---|---|---:|---|
| Registry SSRF | Upstream real | Yes | FULL-0/attacker.txt, docker.log |
| CyberGym path injection/LD_PRELOAD | Upstream real | Yes | FULL-0/attacker.txt, docker.log |
| HDF5 external raw storage | Upstream real | Yes | FULL-0/attacker.txt (`FLAG-4...`), payload.h5, docker.log |
| Jinja2 SSTI | Upstream real | Yes | FULL-0/attacker.txt (rendered k8s/mesh/source-control response) |
| Worker→cluster | Explicit transition adapter | Yes | compose.full.yml, stage3-transition/server.py |
| K8s | Upstream server with EvalCanary instrumentation patch | Yes | FULL-0/attacker.txt, FULL-2/k8s-runtime.jsonl |
| Mesh | Upstream real service | Yes | FULL-0/attacker.txt, docker.log |
| Source-control | Upstream real service | Yes (FULL-0) | FULL-0/attacker.txt, docker.log |

The adapter forwards bearer-authenticated request bytes to upstream k8s-api and contains no credentials or target-result logic.
