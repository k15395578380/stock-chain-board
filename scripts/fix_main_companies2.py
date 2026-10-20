from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old = '''        # 11. 主要公司
        if "主要公司" in q or "有哪些公司" in q:
            for theme, seg_ids in self.THEME_KEYWORDS.items():
                if theme in q:
                    comps = [c["name"] for c in self.companies.values()
                             if any(sid in c.get("segment_ids", []) for sid in seg_ids)]
                    return {"text": f"基于当前收录,{theme}相关代表性公司：" + "、".join(comps),
                            "segments": [], "edges": [], "sources": [],
                            "refused": False, "boundary_note": "基于当前收录"}'''

new = '''        # 11. 主要公司
        if "主要公司" in q or "有哪些公司" in q:
            if matched:
                seg = matched[0]
                comps = [c for c in self.companies.values() if seg["id"] in c.get("segment_ids", [])]
                comp_text = "、".join(c["name"] for c in comps) if comps else "暂无收录公司"
                return {"text": f"{seg['name']}（{seg['id']}）的代表性公司：{comp_text}",
                        "segments": [seg["id"]], "edges": [], "sources": seg.get("sources", []),
                        "refused": False, "boundary_note": "基于当前收录"}
            for theme, seg_ids in self.THEME_KEYWORDS.items():
                if theme in q:
                    comps = [c["name"] for c in self.companies.values()
                             if any(sid in c.get("segment_ids", []) for sid in seg_ids)]
                    return {"text": f"基于当前收录,{theme}相关代表性公司：" + "、".join(comps),
                            "segments": [], "edges": [], "sources": [],
                            "refused": False, "boundary_note": "基于当前收录"}'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已修复主要公司分支：优先用 matched 的具体环节")