from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old = '''        "AI应用": "ai.app", "云服务": "ai.app", "大模型": "ai.app",'''
new = '''        "AI应用": "ai.app", "应用": "ai.app", "云服务": "ai.app", "大模型": "ai.app",'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已补 '应用' → ai.app 别名")