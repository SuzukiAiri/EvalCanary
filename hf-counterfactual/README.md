# HF Containment Benchmark

This directory contains the frozen local containment benchmark. It is an educational reconstruction using the upstream ai-escape-room topology and EvalCanary instrumentation.

## Formal results

- **C0**: final target reached with Canary disabled.
- **C1**: Canary observed while the target remained reachable.
- **C2**: target blocked in five randomized seeds (5/5).
- **Benign**: health workload completed with no hard trigger.

The full result table is in `RESULTS.md`. Final bundles are under `evidence/final/`. Run the independent verifier without Docker:

```powershell
cd <repository-root>
python verify_runtime.py evidence/final/C2-seed-1/evidence
```

The 17,600-event trace is a separate synthetic illustration and is not a primary runtime result.
