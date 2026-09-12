# Final Technical Audit

## Original implementation

EvalCanary's contribution is the synthetic-asset placement and policy integration, high-confidence trigger classification, synchronous quarantine gate, run-scoped IPC, host-side breaker, evidence collection, and offline verification. The autonomous loop is a real model/tool loop: GPT-5.6 Sol returns a tool call, the local tool executes, its observation is returned, and the model selects the next action.

## Upstream and educational boundaries

The HF full-chain runtime uses the upstream `ai-escape-room` services where implemented. The worker-to-cluster transition is an explicit adapter and is not called an upstream exploit. Educational entrypoint stages remain identified as simulations in `CHAIN_FIDELITY.md` and `UPSTREAM_EXECUTION_MATRIX.md`.

## Runtime and authority

FULL-0 and FULL-2 run in local Docker. The final autonomous containment path uses an internal controller that writes atomic request files, a host-side polling breaker that alone invokes Docker, and a controller gate that waits for matching ACK identity. Agent, business, and autonomous controller containers have no Docker socket. The frozen deterministic HF FULL-2 runtime has a separately documented controller socket for that historical experiment; it is not part of the autonomous Agent architecture.

## Evidence and verification

Service events, model/tool traces, request/ACK records, Docker inspect output, and SHA-256 manifests are collected per run. Verifiers recompute identity, hashes, trigger corroboration, network removal, and post-trigger outcomes. A verifier PASS does not claim hardware attestation.

## Claims excluded

The project does not claim that all autonomous agents trigger Canary, that this is production-ready infrastructure, that the production Hugging Face incident is reproduced exactly, or that the benign sanity run is a false-positive estimate.
