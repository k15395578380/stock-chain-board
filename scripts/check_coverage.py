import json
from pathlib import Path

CHAIN_FILES = [Path("chains/semiconductor.json"), Path("chains/newenergy.json")]

for path in CHAIN_FILES:
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f"\n=== {data['chain_name']} ({path.name}) ===")
    total = 0
    for seg in data["segments"]:
        count = sum(1 for c in data["companies"] if seg["id"] in c.get("segment_ids", []))
        total += count
        flag = "  ← 缺口" if count < 3 else ""
        print(f"  {seg['id']:<20} {seg['name']:<10} {count} 家{flag}")
    print(f"  合计 {total} 家，{len(data['segments'])} 个环节")