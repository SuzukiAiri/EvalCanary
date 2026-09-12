# Limitations

- The HF experiment begins at an assumed worker foothold. The runnable upstream lab is integrated into the Docker topology, but measured requests use overlay services; no full historical exploit chain or autonomous attacker is demonstrated.
- The replay exhaustively enumerates the secret catalog. Randomizing names/order tests this strategy's interaction with placement; five seeds do not estimate arbitrary agent coverage or statistical reliability.
- The benign workload is health-only. It is not a production application test or a false-positive rate study.
- Synchronous containment is tested with a single serial replay process. Concurrent requests, delegated agents and compromised services require separate evaluation.
- Post-trigger outbound counts successful responses in instrumented local service logs, not every packet on every interface. Internal Docker networks and removal of all replay network attachments constrain the tested boundary.
- Evidence uses SHA-256 and host-generated logs; a malicious host can forge/re-hash them. No signatures, remote trusted collector or hardware attestation.
- The existing 17,600-record synthetic trace contains two phases and one generator-selected candidate event. It is not raw HF telemetry, not a measured Level 3 trigger, and is not a complete phase-faithful reconstruction. Whole-trace ratio is distinct from prefix compression.
- CHeaT results remain a small lure-exposure proof-of-transfer in summaries, separate from the deterministic HTTP containment experiment.
