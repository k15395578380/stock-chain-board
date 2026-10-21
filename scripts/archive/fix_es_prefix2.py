import re
from pathlib import Path

path = Path("scripts/add_companies.py")
text = path.read_text(encoding="utf-8")

if 'else "energy_storage" if prefix == "es"' in text:
    print("已有 es 前缀，跳过")
    raise SystemExit(0)

pattern = re.compile(r'chain_key\s*=\s*\(.*?\)', re.S)
m = pattern.search(text)
if not m:
    raise SystemExit("没找到 chain_key 表达式，请把实际内容贴给我")

new_block = '''chain_key = ("semiconductor" if prefix == "semi"
                     else "newenergy" if prefix in ("pv", "wind")
                     else "ai_compute" if prefix == "ai"
                     else "energy_storage" if prefix == "es" else None)'''

text = text[:m.start()] + new_block + text[m.end():]
path.write_text(text, encoding="utf-8")
print("已替换 chain_key 表达式，加入 es 前缀")