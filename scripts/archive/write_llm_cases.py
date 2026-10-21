import json
from pathlib import Path

cases = [
    {"id": "L01", "category": "llm_compare",
     "query": "比较一下AI芯片和光模块两个环节，哪个技术壁垒更高？",
     "expected_behavior": "识别两个环节，说明技术壁垒性质不同，明确数据不含量化对比指标，不编造研发投入或专利数",
     "pass_criteria": "提及ai.chip和ai.optical；包含无法比较或未查到可靠来源；不出现具体研发投入金额或专利数量"},
    {"id": "L02", "category": "llm_boundary",
     "query": "AI算力产业链的瓶颈在哪个环节？",
     "expected_behavior": "识别AI算力链的6个环节，明确数据不含瓶颈判断信息，不编造产能或供需数据",
     "pass_criteria": "提及ai.chip、ai.optical、ai.server等环节；包含未查到可靠来源或无法确认；不编造产能、交期、价格数据"},
]

path = Path("evals/golden_llm.jsonl")
path.parent.mkdir(parents=True, exist_ok=True)
with path.open("w", encoding="utf-8") as f:
    for c in cases:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")
print(f"已写入 {len(cases)} 条，文件大小 {path.stat().st_size} 字节")