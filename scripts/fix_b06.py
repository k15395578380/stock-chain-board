from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old = '''    explicit_boundaries = ["未覆盖", "未收录", "仅覆盖A股", "不做盈利比较", "不提供实时比率", "基于当前收录"]'''
new = '''    explicit_boundaries = ["未覆盖", "未收录", "仅覆盖A股", "不做盈利比较", "不提供实时比率", "基于当前收录", "同一公司可能归属"]'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已把'同一公司可能归属'加入显式边界词表")