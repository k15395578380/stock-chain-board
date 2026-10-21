from pathlib import Path

path = Path("scripts/llm_agent.py")
text = path.read_text(encoding="utf-8")

old = "6. 输出必须是 JSON，不要输出任何 JSON 之外的内容。"
new = """6. 当被问到“影响、带动、传导方向”时，可以基于产业链结构给出方向性判断，但必须同时说明“数据未提供传导强度的量化依据”，不要给出具体幅度或时间。
7. 输出必须是 JSON，不要输出任何 JSON 之外的内容。"""

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已在 prompt 中加入传导方向边界规则")