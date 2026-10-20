from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old = '''        "boundary_threshold_met": bt > 0 and bp / bt >= 6 / 8,'''
new = '''        "boundary_threshold_met": bt > 0 and bp == bt,'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已把 boundary 阈值改为全过")