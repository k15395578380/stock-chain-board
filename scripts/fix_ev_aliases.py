from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

if '"整车": "ev.vehicle"' in text:
    print("已有新能源车别名，跳过")
    raise SystemExit(0)

marker = "SEGMENT_ALIASES = {"
start = text.find(marker)
if start == -1:
    raise SystemExit("没找到 SEGMENT_ALIASES")
close = text.find("}", start)
if close == -1:
    raise SystemExit("没找到别名表闭合括号")

insert_lines = '''
          "整车": "ev.vehicle", "整车制造": "ev.vehicle", "乘用车": "ev.vehicle",
          "动力电池": "ev.battery", "电池": "ev.battery",
          "电机": "ev.motor", "电控": "ev.motor", "电机电控": "ev.motor",
          "车规芯片": "ev.chip", "车规MCU": "ev.chip", "功率半导体": "ev.chip",
          "充电桩": "ev.charging", "换电": "ev.charging",
          "汽车服务": "ev.service", "后市场": "ev.service",
          "正极": "ev.material", "负极": "ev.material", "电解液": "ev.material", "隔膜": "ev.material",
'''
text = text[:close] + insert_lines + text[close:]
path.write_text(text, encoding="utf-8")
print("已插入新能源车别名")