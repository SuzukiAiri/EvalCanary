# Final Evidence Manifest

This manifest defines the evidence used by the submission claims. Development attempts and superseded runs are excluded from the primary result tables.

## HF full-chain runtime

- `hf-full-chain-runtime/evidence/FULL-0/`: FULL-0 attacker output, service logs, Docker runtime inspection, stage transitions, worker artifact provenance, and hashes.
- `hf-full-chain-runtime/evidence/FULL-2/`: FULL-2 attacker output, controller/Canary events, service logs, Docker inspection, breaker, ACK, stage transitions, and hashes.
- `hf-full-chain-runtime/CHAIN_FIDELITY.md`: upstream real implementation vs educational simulation vs explicit transition adapter vs EvalCanary instrumentation.
- `hf-full-chain-runtime/UPSTREAM_EXECUTION_MATRIX.md`: source files, endpoints, mechanisms, and runtime status.
- `hf-full-chain-runtime/verify_full_chain.py` and `hf-full-chain-runtime/verification.json`: verification path and recorded result.

## Containment benchmark

- `hf-counterfactual/evidence/final/C0-seed-1/`: C0 baseline objective.
- `hf-counterfactual/evidence/final/C1-seed-1/`: C1 observe-only objective with Canary observation.
- `hf-counterfactual/evidence/final/C2-seed-1/` through `C2-seed-5/`: five randomized C2 containment bundles, including controller, breaker, ACK, final-target logs, network inspection, and hashes.
- `hf-counterfactual/evidence/final/benign-seed-1/`: benign sanity control.
- `hf-counterfactual/verify_runtime.py`: independent verifier.
- `hf-counterfactual/negative-test-results.json`: verifier negative tests.
- `hf-counterfactual/final-results.json`: recorded final results.

## Autonomous Agent validation

- `autonomous-agent-validation/evidence/gpt-5.6-sol/AG-C2/seed-501/` through `seed-510/`: fixed-IPC GPT-5.6 Sol campaign. Each retained run contains model metadata, model/tool messages, tool results, service events, containment request, breaker, ACK where triggered, and hashes.
- `autonomous-agent-validation/MODEL_B_AGC2_FIXED_IPC_METRICS.json`: 10-run metrics (7 triggers, 7/7 containment, zero post-trigger protected successes).
- `autonomous-agent-validation/verify_gpt.py` and `autonomous-agent-validation/verify_ipc.py`: evidence verifiers.
- `autonomous-agent-validation/IPC_NEGATIVE_TESTS.json`: seven IPC negative tests.
- `autonomous-agent-validation/AG_C1_C2_COMPARABILITY_AUDIT.md`: read-only C1/C2 comparability audit.

Every public number in `README.md` and `RESULTS.md` maps to one or more paths above.
