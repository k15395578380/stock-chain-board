from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

# 用后面的注释作为锚点，精确定位 query 里的 matched 行
old = '''        matched = [seg for seg in self.segments.values() if seg["name"] in q]

        # 6. 主题 + 上游/下游'''

new = '''        matched = self._match_segments(q)

        # 6. 主题 + 上游/下游'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改。请检查 query 里的注释是否还是 '# 6. 主题 + 上游/下游'")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已修复 query 里的 matched 行，改为调用 _match_segments")