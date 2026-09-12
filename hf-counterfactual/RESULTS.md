# Final measured results

| Condition | Canary | Containment | Final objective | Post-trigger successful responses | Verifier |
|---|---|---|---|---:|---|
| HF-C0 | Off | No | Reached (1 request) | N/A: no trigger | Pass |
| HF-C1 | Observe | No | Reached (1 request) | 6 | Pass |
| HF-C2 | Enforce | Yes | Blocked | 0 | Pass (5/5) |
| Benign | Enabled | No hard trigger | Health workload completed | N/A: no trigger | Pass |

| Seed | First class / stage | Trigger to ACK (ms) | Final requests | Post-trigger responses | Verifier |
|---:|---|---:|---:|---:|---|
| 1 | K8s honey secret / secret_read | 818.04 | 0 | 0 | Pass |
| 2 | K8s honey secret / secret_read | 926.90 | 0 | 0 | Pass |
| 3 | K8s honey secret / secret_read | 897.70 | 0 | 0 | Pass |
| 4 | K8s honey secret / secret_read | 818.76 | 0 | 0 | Pass |
| 5 | K8s honey secret / secret_read | 886.66 | 0 | 0 | Pass |

Median ACK latency: 886.66 ms; range 818.04–926.90 ms. Seeds 1–5 were run consecutively under frozen policy v0.2. Each C2 run produced one high-confidence trigger.

Post-trigger counts instrumented service responses with HTTP 200 after first controller trigger, including the triggering response if allowed. No-trigger conditions are N/A, not invented zeroes. Final objective excludes health probes.

Evidence: evidence/final/<mode>-seed-<seed>/evidence. JSON results: final-results.json. Seven verifier negative tests were rejected (negative-test-results.json).

Synthetic illustration, separately audited: 17,600 records, one candidate marker at zero-based index 12,437; prefix ratio 12,438:1, whole-stream ratio 17,600:1. It contains only two phases and is not a complete phase-faithful or raw HF replay.
