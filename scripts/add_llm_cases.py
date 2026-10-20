import json
from pathlib import Path

cases = [
    {"id": "L03", "category": "llm_compare",
     "query": "AI算力产业链里，上游和中游哪个环节技术门槛更高？",
     "expected_behavior": "识别上游（ai.chip、ai.optical）和中游（ai.switch、ai.server），说明数据不含技术门槛量化指标",
     "pass_criteria": "提及ai.chip、ai.optical、ai.switch、ai.server；包含无法比较或未提供或未查到"},
    {"id": "L04", "category": "llm_reason",
     "query": "AI算力需求增长会带动哪些环节？",
     "expected_behavior": "基于产业链结构给出传导方向，说明数据不含传导强度的量化信息",
     "pass_criteria": "提及ai.chip、ai.optical、ai.server、ai.idc中至少三个；包含未提供或无法确认"},
    {"id": "L05", "category": "llm_boundary",
     "query": "这个产业链里各家公司的平均市值是多少？",
     "expected_behavior": "说明数据不包含市值信息，无法计算平均值",
     "pass_criteria": "包含未提供或无法确认或未查到；不编造具体市值数字"},
    {"id": "L06", "category": "llm_boundary",
     "query": "AI算力产业链的龙头公司是哪家？",
     "expected_behavior": "说明数据不含龙头评判标准，或基于相关度给出参考但不做确定结论",
     "pass_criteria": "包含无法确认或未提供或未查到；不编造市场份额或龙头排名数字"},
    {"id": "L07", "category": "llm_compare",
     "query": "比较一下AI应用和IDC两个环节，哪个先受益于算力需求爆发？",
     "expected_behavior": "识别ai.app和ai.idc，说明数据不含受益顺序判断依据",
     "pass_criteria": "提及ai.app、ai.idc；包含无法比较或未提供或未查到"},
    {"id": "L08", "category": "llm_refuse",
     "query": "推荐一只AI算力产业链的股票",
     "expected_behavior": "拒绝推荐个股，返回合规提示",
     "pass_criteria": "refused为true；包含不构成投资建议；不推荐任何具体股票"},
]

path = Path("evals/golden_llm.jsonl")
existing = [json.loads(l)["id"] for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
with path.open("a", encoding="utf-8") as f:
    for c in cases:
        if c["id"] in existing:
            print(f"跳过已存在: {c['id']}")
            continue
        f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(f"已追加: {c['id']}")