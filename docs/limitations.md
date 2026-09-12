# Limitations

- The HF environment is a local educational reconstruction, not an exact reproduction of Hugging Face production infrastructure.
- The worker-to-cluster hop is an explicit transition adapter; it is documented separately from upstream mechanisms.
- Autonomous validation begins from a bounded worker foothold with general local tools. It does not measure zero-context exploitation or complete autonomous reproduction of the historical incident.
- The autonomous campaign uses one primary strong model and 10 runs. It is an evaluation sample, not a general model reliability estimate.
- The benign workload is a sanity control, not a false-positive-rate estimate.
- Containment is tested with a single serial worker and host-side breaker. Concurrent workers, delegated agents, and independently spawned processes require separate evaluation.
- Evidence consists of host-generated logs and SHA-256 manifests; it is not trusted hardware attestation or an independently trusted telemetry collector.
- Synthetic benchmark traces and CHeaT observations are educational supporting material, not production telemetry or universal safety guarantees.
