from pathlib import Path

path = Path("scripts/llm_agent.py")
text = path.read_text(encoding="utf-8")

if "传导强度" in text:
    print("已有传导方向规则，跳过")
    raise SystemExit(0)

old = "7. 输出必须是 JSON，不要输出任何 JSON 之外的内容。"
new = """7. 当被问到"影响、带动、传导方向"时，可以基于产业链结构给出方向性判断，但必须同时说明"数据未提供传导强度的量化依据"，不要给出具体幅度或时间。
8. 任何回答的 text 末尾都必须包含一句边界说明（"数据未提供…"或"未查到可靠来源"或"无法确认…"），即使只是方向性判断。
9. 输出必须是 JSON，不要输出任何 JSON 之外的内容。"""

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已加入传导方向规则和强制边界说明")