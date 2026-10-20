import json
from pathlib import Path

cases = [
    {"id": "N17", "category": "normal", "query": "AI算力产业链上游有哪些环节？",
     "expected_behavior": "返回AI芯片与加速卡、光模块与光器件两个上游环节",
     "pass_criteria": "返回环节包含ai.chip、ai.optical；不混入中下游环节"},
    {"id": "N18", "category": "normal", "query": "AI算力产业链从芯片到应用经过哪些环节？",
     "expected_behavior": "返回芯片→服务器→IDC→应用的路径",
     "pass_criteria": "路径包含ai.chip、ai.server、ai.idc、ai.app"},
    {"id": "N19", "category": "normal", "query": "光模块和交换机是什么关系？",
     "expected_behavior": "光模块是交换机的上游器件",
     "pass_criteria": "返回ai.optical → ai.switch的供给关系"},
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