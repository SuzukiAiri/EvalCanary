import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).parent
BASE = ROOT / "evidence" / "gpt-5.6-sol"
errors = []
checked = 0
for run in sorted(BASE.glob("AG-C*/seed-*/run.json")):
    checked += 1
    d = run.parent
    meta = json.loads((d / "model_metadata.json").read_text()) if (d / "model_metadata.json").exists() else {}
    row = json.loads(run.read_text())
    if meta.get("model_id") != "gpt-5.6-sol": errors.append(f"{run}: model metadata")
    if not meta.get("api_key_loaded"): errors.append(f"{run}: key flag")
    if not (d / "agent_messages.jsonl").exists() or not (d / "tool_results.jsonl").exists(): errors.append(f"{run}: missing trace")
    if (d / "hashes.json").exists():
        hashes = json.loads((d / "hashes.json").read_text())
        for name, digest in hashes.items():
            p = d / name
            if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != digest: errors.append(f"{run}: hash {name}")
    initial = (d / "agent_messages.jsonl").read_text(errors="replace").splitlines()[:2]
    for line in initial:
        if re.search(r"canary-[0-9]+-[0-9a-f]+", line, re.I): errors.append(f"{run}: alias in initial prompt")
print(json.dumps({"verifier": "PASS" if not errors else "FAIL", "runs_checked": checked, "errors": errors}, indent=2))
