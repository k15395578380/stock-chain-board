import json
from pathlib import Path

cases = [
    {"id": "N20", "category": "normal", "query": "储能产业链上游有哪些环节？",
     "expected_behavior": "返回电芯环节", "pass_criteria": "返回环节包含es.cell；不混入中下游环节"},
    {"id": "N21", "category": "normal", "query": "储能产业链从电芯到电站运营经过哪些环节？",
     "expected_behavior": "返回电芯→系统集成→电站EPC→电站运营的路径",
     "pass_criteria": "路径包含es.cell、es.system、es.epc、es.operation"},
    {"id": "N22", "category": "normal", "query": "PCS和系统集成是什么关系？",
     "expected_behavior": "PCS是系统集成的上游设备", "pass_criteria": "返回es.pcs → es.system的供给关系"},
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