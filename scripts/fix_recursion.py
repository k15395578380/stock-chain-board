from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old = '''    def _match_segments(self, q):
        matched = self._match_segments(q)'''

new = '''    def _match_segments(self, q):
        matched = [seg for seg in self.segments.values() if seg["name"] in q]'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已修复 _match_segments 的递归调用")