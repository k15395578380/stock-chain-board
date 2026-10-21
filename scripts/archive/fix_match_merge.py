from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old = '''    def _match_segments(self, q):
        matched = [seg for seg in self.segments.values() if seg["name"] in q]
        if matched:
            return matched
        hit_ids = []
        for alias, sid in self.SEGMENT_ALIASES.items():
            if alias in q and sid in self.segments and sid not in hit_ids:
                hit_ids.append(sid)
        return [self.segments[sid] for sid in hit_ids]'''

new = '''    def _match_segments(self, q):
        hit_ids = []
        for seg in self.segments.values():
            if seg["name"] in q and seg["id"] not in hit_ids:
                hit_ids.append(seg["id"])
        for alias, sid in self.SEGMENT_ALIASES.items():
            if alias in q and sid in self.segments and sid not in hit_ids:
                hit_ids.append(sid)
        return [self.segments[sid] for sid in hit_ids]'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已改为完整名称和别名合并匹配")