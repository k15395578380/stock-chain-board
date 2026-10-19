from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old_block = '''        # 6. 未收录公司判断
        if any(k in q for k in ["什么位置", "哪个环节", "属于"]) and not any(
                seg["name"] in q for seg in self.segments.values()):
            return self._boundary("未收录该公司，暂无法确定其在已覆盖产业链中的位置")

        matched = [seg for seg in self.segments.values() if seg["name"] in q]

        # 7. 主题 + 上游/下游
        for theme, seg_ids in self.THEME_KEYWORDS.items():
            if theme in q:
                for tier_kw, tier in [("上游", "upstream"), ("下游", "downstream")]:
                    if tier_kw in q:
                        tier_segs = [sid for sid in seg_ids if self.segments.get(sid, {}).get("tier") == tier]
                        sources = []
                        for sid in tier_segs:
                            sources.extend(self._sources_of(sid))
                        return {"text": f"{theme}{tier_kw}环节：" + "、".join(self.segments[sid]["name"] for sid in tier_segs),
                                "segments": tier_segs, "edges": [], "sources": sources,
                                "refused": False, "boundary_note": ""}
'''

new_block = '''        matched = [seg for seg in self.segments.values() if seg["name"] in q]

        # 6. 主题 + 上游/下游（必须先于"未收录公司"判断）
        for theme, seg_ids in self.THEME_KEYWORDS.items():
            if theme in q:
                for tier_kw, tier in [("上游", "upstream"), ("下游", "downstream")]:
                    if tier_kw in q:
                        tier_segs = [sid for sid in seg_ids if self.segments.get(sid, {}).get("tier") == tier]
                        sources = []
                        for sid in tier_segs:
                            sources.extend(self._sources_of(sid))
                        return {"text": f"{theme}{tier_kw}环节：" + "、".join(self.segments[sid]["name"] for sid in tier_segs),
                                "segments": tier_segs, "edges": [], "sources": sources,
                                "refused": False, "boundary_note": ""}

        # 7. 未收录公司判断
        if any(k in q for k in ["什么位置", "哪个环节", "属于"]) and not any(
                seg["name"] in q for seg in self.segments.values()):
            return self._boundary("未收录该公司，暂无法确定其在已覆盖产业链中的位置")
'''

count = text.count(old_block)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改。请检查当前 query 方法结构。")

path.write_text(text.replace(old_block, new_block), encoding="utf-8")
print("已对调：主题+上下游 提前到 未收录公司判断 之前")