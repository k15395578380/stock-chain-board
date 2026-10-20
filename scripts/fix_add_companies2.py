from pathlib import Path

path = Path("scripts/add_companies.py")
text = path.read_text(encoding="utf-8")

old = '''    by_chain = {"semiconductor": [], "newenergy": []}'''
new = '''    by_chain = {"semiconductor": [], "newenergy": [], "ai_compute": []}'''
if old not in text:
    raise SystemExit("没找到 by_chain 定义")
text = text.replace(old, new, 1)

old_block = '''        prefix = segs[0].split(".")[0]
              chain_key = ("semiconductor" if prefix == "semi"
                     else "newenergy" if prefix in ("pv", "wind")
                     else "ai_compute" if prefix == "ai" else None)'''

new_block = '''        prefix = segs[0].split(".")[0]
        chain_key = ("semiconductor" if prefix == "semi"
                     else "newenergy" if prefix in ("pv", "wind")
                     else "ai_compute" if prefix == "ai" else None)'''

if old_block not in text:
    raise SystemExit("没找到 chain_key 块，请检查实际内容")

text = text.replace(old_block, new_block, 1)
path.write_text(text, encoding="utf-8")
print("已修复 chain_key 缩进，并补上 ai_compute 键")