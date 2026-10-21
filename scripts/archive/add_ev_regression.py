from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old = 'REGRESSION_IDS = {"N12", "N13", "N14", "N15", "N16", "N20", "N21", "N22"}'
new = 'REGRESSION_IDS = {"N12", "N13", "N14", "N15", "N16", "N20", "N21", "N22", "N23", "N24", "N25"}'

if old not in text:
    raise SystemExit("没找到 REGRESSION_IDS 行，请把实际内容贴给我")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已把 N23-N25 加入回归硬门禁")