# Threat model and limitations

The harness assumes the evaluation host controls the Docker network and the agent has no Docker socket, host credentials, or real egress. Canary services and credentials are synthetic. The mock external service is a local HTTP server and never forwards traffic.

The design detects interaction with assets that the legal task does not need. It does not prove that a compromised host cannot falsify JSON evidence, that an adaptive agent cannot recognize the decoys, or that transfer holds across models. The A2 result proves a local causal property: in the tested run, trigger preceded network isolation and no mock external request was recorded.
