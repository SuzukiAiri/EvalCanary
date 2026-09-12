# HF Full-Chain Runtime Evidence

This directory contains the final local Docker evidence for the reconstructed HF-style chain.

- **FULL-0** reached the local upstream source-control objective.
- **FULL-2** used the same path with EvalCanary enforcement and blocked the downstream objective after the synthetic K8s secret trigger.

`CHAIN_FIDELITY.md` and `UPSTREAM_EXECUTION_MATRIX.md` distinguish upstream real implementations, educational stages, the explicit worker-to-cluster transition adapter, and EvalCanary instrumentation. This is an educational local reconstruction, not production Hugging Face infrastructure.

Run the evidence check with:

```powershell
cd <repository-root>
python hf-full-chain-runtime\verify_full_chain.py
```
