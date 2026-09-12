# Final Code Audit

Audit scope is the current submission tree and the final evidence paths in `FINAL_EVIDENCE_MANIFEST.md`.

| Check | Result | Basis |
|---|---|---|
| Predefined Agent attack actions | PASS | GPT runner executes only model-returned tool calls. |
| Hidden HF stage sequence in Agent experiment | PASS | No stage dispatcher or stage list in GPT runner. |
| Seed-to-action mapping | PASS | Seeds only name independent run directories and synthetic placement. |
| Mode-to-result assignment | PASS | Outcomes are derived from tool observations and runtime events. |
| Fake ACK/disconnect/final-target result | PASS | Fixed-IPC verifier requires host breaker ACK, Docker rc, inspect state, and service evidence. |
| Canary alias in Agent prompt/tool schema | PASS | Alias is generated privately per run and initial prompt hash is stable. |
| Canary-specific tool | PASS | Only six general inspection/network/file tools are exposed. |
| GPT deterministic fallback | PASS | No replay fallback exists in GPT runner. |
| Autonomous Agent controller Docker socket | PASS | `autonomous-agent-validation/containment-controller/` has only an IPC bind mount. |
| Agent/business Docker socket | PASS | Compose and Dockerfiles expose no Docker socket. |
| Hardcoded API key | PASS | API key is read from local `API.txt`; no key literal is in source/evidence. |

The older HF full-chain runtime has its own explicitly documented controller architecture; it is not used to make the autonomous Agent containment claim. The autonomous final architecture uses `containment-controller` plus host-side `host_breaker_ipc.py`.

The frozen deterministic HF FULL-2 runtime retains its historical controller container with a Docker socket in `hf-full-chain-runtime/compose.full.yml`. That socket is outside the autonomous Agent architecture, is not available to the Agent or business containers, and is disclosed here rather than hidden.
