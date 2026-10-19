import json
from pathlib import Path

path = Path("artifacts/eval-report/report.json")
if not path.exists():
    print("  报告不存在，跳过失败明细")
    raise SystemExit(0)

r = json.loads(path.read_text(encoding="utf-8"))
fails = [c for c in r.get("cases", []) if c.get("status") != "pass"]
if not fails:
    print("  无失败 case")
else:
    for c in fails:
        print(f"  {c['id']} {c['category']} | {c.get('detail', '')}")