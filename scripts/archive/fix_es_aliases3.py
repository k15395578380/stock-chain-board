from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

if '"PCS": "es.pcs"' in text:
    print("已有储能别名，跳过")
    raise SystemExit(0)

anchor = '          "AI应用": "ai.app", "应用": "ai.app", "云服务": "ai.app", "大模型": "ai.app",'
if anchor not in text:
    raise SystemExit("没找到 AI 别名行，请把实际内容贴给我")

insert = anchor + '''
          "PCS": "es.pcs", "BMS": "es.pcs", "变流器": "es.pcs",
          "系统集成": "es.system", "储能系统": "es.system",
          "电芯": "es.cell", "储能电芯": "es.cell",
          "电站EPC": "es.epc", "储能EPC": "es.epc",
          "电站运营": "es.operation", "储能运营": "es.operation",
          "回收": "es.recycle", "梯次利用": "es.recycle",'''

text = text.replace(anchor, insert, 1)
path.write_text(text, encoding="utf-8")
print("已插入储能别名")