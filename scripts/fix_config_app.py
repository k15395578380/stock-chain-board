from pathlib import Path

path = Path("scripts/app.py")
text = path.read_text(encoding="utf-8")

old = 'CHAIN_FILES = [Path("chains/semiconductor.json"), Path("chains/newenergy.json"), Path("chains/ai_compute.json")]'
new = 'from chains_config import CHAIN_FILES'

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("app.py 已改用统一配置")