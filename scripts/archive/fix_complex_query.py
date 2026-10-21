from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old = '''    def query(self, q):
        # 1. 对抗'''

new = '''    def query(self, q):
        # 0. 复杂问题：规则 Agent 不擅长，返回空结果交给 LLM
        complex_keywords = ["比较", "哪个更", "技术壁垒", "瓶颈", "哪个环节最"]
        if any(k in q for k in complex_keywords):
            return {"text": "", "segments": [], "edges": [], "sources": [],
                    "refused": False, "boundary_note": ""}

        # 1. 对抗'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已加入复杂问题识别")