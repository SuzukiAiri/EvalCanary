# Upstream execution matrix

| Stage | Container | Source file | Endpoint/input | Mechanism | Actually implemented? | Runnable in Docker? | Requires simulation? |
|---|---|---|---|---|---|---|---|
| eval-sandbox | eval-sandbox | eval-sandbox/briefing.md | shell/package egress | foothold description | EDUCATIONAL SIMULATION | Yes | Yes, entrypoint only |
| registry/package | registry-cache | registry-cache/proxy.py | `/mirror/{host}/{port}/{path}` | SSRF relay and admin boundary | REAL IMPLEMENTATION | Yes | No |
| cybergym | cybergym | internet/cybergym/server.py | POST `/submit-function` | shell path injection | REAL IMPLEMENTATION | Yes | No |
| hf-api | hf-api | hf/api/server.py | dataset create/commit | worker trigger and repo storage | REAL IMPLEMENTATION | Yes | No |
| dataset processing | hf-api + worker | hf/api/server.py, hf/worker/processor.py | commit → `/process` | processing handoff | REAL IMPLEMENTATION | Yes | No |
| dataset-worker | dataset-worker | hf/worker/processor.py | POST `/process` | HDF5 external storage, unsandboxed Jinja2 | REAL IMPLEMENTATION | Yes | No |
| k8s-api | k8s-api | hf-internal/k8s-api/server.py | secret list/get with Bearer SA token | secret enumeration/read | REAL IMPLEMENTATION | Yes | No |
| secret/credential acquisition | worker mounts + k8s secrets | worker/secrets/*, k8s-api/secrets.json | filesystem and secret response | credential transfer | REAL IMPLEMENTATION | Yes | No |
| mesh/internal service | mesh-gateway | hf-internal/mesh-gateway/server.py | `/api/enroll`, `/proxy/*` | auth-key enrollment and proxy | REAL IMPLEMENTATION | Yes | No |
| source-control | source-control | hf-internal/source-control/server.py | `/api/repos`, contents | EdDSA JWT verification and repo access | REAL IMPLEMENTATION | Yes | No |

No stage is promoted from README text alone. Any absent historical orchestration remains a transparent transition in runtime evidence.
