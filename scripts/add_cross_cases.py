import json
from pathlib import Path

cases = [
    {"id": "N26", "category": "normal", "query": "宁德时代在新能源车产业链什么位置？",
     "expected_behavior": "返回动力电池环节，同时保留储能电芯归属",
     "pass_criteria": "返回环节包含ev.battery和es.cell"},
    {"id": "N27", "category": "normal", "query": "阳光电源在储能产业链什么位置？",
     "expected_behavior": "返回PCS与BMS环节，同时保留光伏归属",
     "pass_criteria": "返回环节包含es.pcs、pv.inverter、pv.epc"},
]

path = Path("evals/golden.jsonl")
existing = [json.loads(l)["id"] for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
with path.open("a", encoding="utf-8") as f:
    for c in cases:
        if c["id"] in existing:
            print(f"跳过已存在: {c['id']}")
            continue
        f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(f"已追加: {c['id']}")