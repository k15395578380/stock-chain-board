import re
from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

pattern = re.compile(r'REGRESSION_IDS\s*=\s*\{[^}]*\}')
m = pattern.search(text)
if not m:
    raise SystemExit("没找到 REGRESSION_IDS")

new_ids = 'REGRESSION_IDS = {"N12", "N13", "N14", "N15", "N16", "N20", "N21", "N22", "N23", "N24", "N25"}'
if m.group(0) == new_ids:
    print("回归 ID 已是最新，跳过")
    raise SystemExit(0)

text = text[:m.start()] + new_ids + text[m.end():]
path.write_text(text, encoding="utf-8")
print("已把 N23-N25 加入回归硬门禁")