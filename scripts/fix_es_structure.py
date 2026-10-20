import re
from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")
changed = []

# 1. 插入储能别名：找到 SEGMENT_ALIASES = { 的闭合 }
if '"PCS": "es.pcs"' not in text:
    marker = "SEGMENT_ALIASES = {"
    start = text.find(marker)
    if start == -1:
        raise SystemExit("没找到 SEGMENT_ALIASES")
    close = text.find("}", start)
    if close == -1:
        raise SystemExit("没找到别名表闭合括号")
    insert_lines = '''
          "PCS": "es.pcs", "BMS": "es.pcs", "变流器": "es.pcs",
          "系统集成": "es.system", "储能系统": "es.system",
          "电芯": "es.cell", "储能电芯": "es.cell",
          "电站EPC": "es.epc", "储能EPC": "es.epc",
          "电站运营": "es.operation", "储能运营": "es.operation",
          "回收": "es.recycle", "梯次利用": "es.recycle",
'''
    text = text[:close] + insert_lines + text[close:]
    changed.append("别名")
else:
    print("别名已存在，跳过")

# 2. 更新 REGRESSION_IDS：正则匹配整行
pattern = re.compile(r'REGRESSION_IDS\s*=\s*\{[^}]*\}')
m = pattern.search(text)
if not m:
    raise SystemExit("没找到 REGRESSION_IDS")
new_ids = 'REGRESSION_IDS = {"N12", "N13", "N14", "N15", "N16", "N20", "N21", "N22"}'
if m.group(0) != new_ids:
    text = text[:m.start()] + new_ids + text[m.end():]
    changed.append("回归ID")
else:
    print("回归ID已是最新，跳过")

path.write_text(text, encoding="utf-8")
print(f"已修改: {', '.join(changed) if changed else '无'}")