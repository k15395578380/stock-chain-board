import re
from pathlib import Path

path = Path("scripts/add_companies.py")
text = path.read_text(encoding="utf-8")

pattern = re.compile(r'[ \t]*chain_key\s*=\s*\(.*?\)', re.S)
m = pattern.search(text)
if not m:
    raise SystemExit("没找到 chain_key 表达式")

new_block = '''        chain_key = ("semiconductor" if prefix == "semi"
                     else "newenergy" if prefix in ("pv", "wind")
                     else "ai_compute" if prefix == "ai"
                     else "energy_storage" if prefix == "es" else None)'''

text = text[:m.start()] + new_block + text[m.end():]
path.write_text(text, encoding="utf-8")
print("已修复 chain_key 缩进")