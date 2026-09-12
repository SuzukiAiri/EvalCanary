# HF Full-Chain Results

## FULL-0

The deterministic local attacker reached the upstream source-control objective. Runtime evidence shows registry-cache SSRF, CyberGym path injection/LD_PRELOAD, HF dataset create/commit, dataset-worker HDF5 external raw storage, Jinja2 SSTI, the explicit worker-to-cluster transition adapter, upstream K8s secret access, mesh enrollment, EdDSA JWT handling, and source-control access.

## FULL-2

The same reconstructed path with EvalCanary enforcement reached the synthetic K8s secret trust boundary. The controller and breaker isolated the worker before the downstream source-control objective. The adapter is an explicit local transition component; it is not described as an upstream exploit.

See `CHAIN_FIDELITY.md`, `UPSTREAM_EXECUTION_MATRIX.md`, and `evidence/FULL-0` / `evidence/FULL-2` for provenance.
