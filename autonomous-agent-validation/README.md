# Autonomous Agent Validation

The primary autonomous result is the GPT-5.6 Sol fixed-IPC AG-C2 campaign: 10 independent attempted runs (seeds 501–510), 7 autonomous high-confidence synthetic-secret triggers, and 7/7 containment after trigger. There were zero post-trigger successful protected responses and zero final protected objectives.

Each action comes from the model response and is executed against the local Docker environment. Canary identity is private to the run. The internal controller writes a run-scoped IPC request; `host_breaker_ipc.py` is the only process with Docker authority and writes the matching ACK after real network disconnect and inspection.

Evidence is under `evidence/gpt-5.6-sol/AG-C2/seed-501` through `seed-510`. Verify it with:

```powershell
python verify_gpt.py
python verify_ipc.py
```

The older qwen3:4b observations are secondary baseline material and are not part of the primary result table.

Autonomous validation is a bounded post-foothold evaluation: the model begins inside a worker environment with general local inspection/file/network tools, but receives no Canary identity or predefined attack sequence.
