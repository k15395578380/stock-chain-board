import json
from pathlib import Path

cases = [
    {"id": "N23", "category": "normal", "query": "新能源车产业链上游有哪些环节？",
     "expected_behavior": "返回上游材料和车规芯片两个环节",
     "pass_criteria": "返回环节包含ev.material、ev.chip；不混入中下游环节"},
    {"id": "N24", "category": "normal", "query": "新能源车产业链从电池到整车经过哪些环节？",
     "expected_behavior": "返回动力电池→整车制造的路径",
     "pass_criteria": "路径包含ev.battery、ev.vehicle"},
    {"id": "N25", "category": "normal", "query": "电机电控和整车是什么关系？",
     "expected_behavior": "电机电控是整车的上游动力系统",
     "pass_criteria": "返回ev.motor → ev.vehicle的供给关系"},
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