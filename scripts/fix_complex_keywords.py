from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old = '        complex_keywords = ["比较", "哪个更", "技术壁垒", "瓶颈", "哪个环节最"]'
new = '        complex_keywords = ["比较", "哪个更", "哪个技术", "技术壁垒", "技术门槛", "门槛更高", "瓶颈", "哪个环节最", "更高"]'

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已扩展 complex_keywords")