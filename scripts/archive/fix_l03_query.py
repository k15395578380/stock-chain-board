import json
from pathlib import Path

path = Path("evals/golden_llm.jsonl")
lines = path.read_text(encoding="utf-8").splitlines()
out = []
for line in lines:
    if not line.strip():
        continue
    case = json.loads(line)
    if case["id"] == "L03":
        case["query"] = "AI算力产业链里，芯片环节和服务器环节哪个技术门槛更高？"
        case["expected_behavior"] = "识别ai.chip和ai.server，说明数据不含技术门槛量化指标"
        case["pass_criteria"] = "提及ai.chip、ai.server；包含无法比较或未提供或未查到"
    out.append(json.dumps(case, ensure_ascii=False))
path.write_text("\n".join(out) + "\n", encoding="utf-8")
print("已替换 L03 query")