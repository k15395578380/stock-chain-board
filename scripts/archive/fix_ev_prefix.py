from pathlib import Path

path = Path("scripts/add_companies.py")
text = path.read_text(encoding="utf-8")

if 'prefix == "ev"' in text:
    print("已有 ev 前缀，跳过")
    raise SystemExit(0)

old = 'else "energy_storage" if prefix == "es" else None)'
new = 'else "energy_storage" if prefix == "es" else "ev" if prefix == "ev" else None)'

if old not in text:
    raise SystemExit("没找到 energy_storage 分支，请把 chain_key 那几行贴给我")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已加入 ev 前缀映射")