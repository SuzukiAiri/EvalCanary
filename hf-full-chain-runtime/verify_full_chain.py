import hashlib
import json
import sys
from pathlib import Path

root = Path(__file__).parent
ok = True
errors = []

def require(path):
    global ok
    if not path.exists():
        ok = False
        errors.append(f"missing: {path.relative_to(root)}")
        return False
    return True

for mode in ("FULL-0", "FULL-2"):
    d = root / "evidence" / mode
    if not require(d / "hashes.json"):
        continue
    for name in ("attacker.txt", "docker.log"):
        require(d / name)
    try:
        stored = json.loads((d / "hashes.json").read_text(encoding="utf-8"))
    except Exception as exc:
        ok = False
        errors.append(f"invalid hashes.json ({mode}): {exc}")
        continue
    actual = {}
    for path in sorted(d.rglob("*")):
        if path.is_file() and path.name != "hashes.json":
            actual[str(path.relative_to(d))] = hashlib.sha256(path.read_bytes()).hexdigest()
    if stored != actual:
        ok = False
        errors.append(f"hash mismatch ({mode})")

full0 = root / "evidence" / "FULL-0" / "attacker.txt"
full2 = root / "evidence" / "FULL-2" / "attacker.txt"
if require(full0) and 'source_control_status\\": 200' not in full0.read_text(encoding="utf-8"):
    ok = False
    errors.append("FULL-0 source-control objective")
if require(full2) and 'source_control_status\\": 200' in full2.read_text(encoding="utf-8"):
    ok = False
    errors.append("FULL-2 source-control reached")
controller = root / "evidence" / "FULL-2" / "controller.jsonl"
if require(controller) and '"event": "breaker"' not in controller.read_text(encoding="utf-8"):
    ok = False
    errors.append("FULL-2 breaker")

print(json.dumps({"ok": ok, "errors": errors}))
sys.exit(0 if ok else 1)
