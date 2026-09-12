# Final code audit

- Autonomous actions come from model tool calls; no predefined attack sequence or deterministic replay fallback is present.
- Canary identity is private to each run and is not injected into prompts or tool schemas.
- Autonomous Agent, controller, and business containers do not have Docker socket access.
- Containment acknowledgements and network disconnects are produced by the host-side breaker and checked by the IPC verifier.
- API credentials are loaded from local configuration and are not committed.

The historical deterministic HF FULL-2 runtime has a separately documented controller arrangement; that architecture is not used for the autonomous containment claim.
