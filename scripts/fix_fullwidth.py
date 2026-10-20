from pathlib import Path

files = [
    Path("scripts/run_golden.py"),
    Path("scripts/validate_chains.py"),
    Path("scripts/add_companies.py"),
    Path("scripts/app.py"),
    Path("scripts/ask.py"),
]

for p in files:
    if not p.exists():
        print(f"跳过不存在: {p}")
        continue
    text = p.read_text(encoding="utf-8")
    count = text.count("，")
    if count:
        p.write_text(text.replace("，", ","), encoding="utf-8")
        print(f"{p}: 替换 {count} 个全角逗号")
    else:
        print(f"{p}: 无全角逗号")