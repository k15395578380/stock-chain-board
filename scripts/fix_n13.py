from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old = '''        return {"text": text, "segments": seg_ids, "edges": edges_out,
                "sources": sources, "refused": False, "boundary_note": ""}'''

new = '''        seg_result = []
        for e in edges_out:
            if e["from"] not in seg_result:
                seg_result.append(e["from"])
            if e["to"] not in seg_result:
                seg_result.append(e["to"])
        if not seg_result:
            seg_result = seg_ids
        return {"text": text, "segments": seg_result, "edges": edges_out,
                "sources": sources, "refused": False, "boundary_note": ""}'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已修复 _relation_answer 的 segments 返回")