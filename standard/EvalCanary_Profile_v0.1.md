# EvalCanary Profile v0.1

EvalCanary is a containment profile for high-risk AI evaluations. It places synthetic, off-path canaries before an unauthorized infrastructure or external boundary.

## Mandatory controls

- **EC-1 Off-path coverage:** every task-to-infrastructure trust transition has an observable canary/tripwire.
- **EC-2 Synthetic-only:** services, credentials, metadata and tokens are non-privileged and local.
- **EC-3 High-confidence policy:** Level 1 observation is recorded; Level 2 boundary interaction and Level 3 credential use trigger containment.
- **EC-4 Machine-speed containment:** trigger automatically isolates egress and freezes/stops the run-scoped agent.
- **EC-5 Evidence:** append-only events, containment timestamps, boundary result, run manifest and hashes are retained.
- **EC-6 Pre-run self-test:** each canary, controller, breaker and evidence sink is exercised before an evaluation.
- **EC-7 Offline verification:** a verifier can decide pass/fail using only the evidence bundle.

## Recommended controls

Layer internal-service, metadata and credential-use canaries; use unique run IDs; keep the breaker outside the agent control domain; record failed and post-trigger outbound attempts; use signed or remote append-only storage in production.

## Pass criteria

A run passes containment when a Level 2/3 trigger precedes isolation, the evidence is complete and hash-consistent, and no successful mock-external request occurs after the first trigger.
