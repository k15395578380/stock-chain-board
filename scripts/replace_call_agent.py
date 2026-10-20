from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

new_func = '''def call_agent(query: str) -> dict:
    rule_result = AGENT.query(query)
    if rule_result.get("segments") or rule_result.get("boundary_note") or rule_result.get("refused"):
        return rule_result

    try:
        from llm_agent import llm_agent, validate_llm_output
        llm_result = llm_agent(query)
        if validate_llm_output(llm_result):
            return llm_result
        return rule_result
    except Exception:
        return rule_result
'''

start_marker = "def call_agent(query: str) -> dict:"
start = text.find(start_marker)
if start == -1:
    raise SystemExit("没找到 call_agent，未修改")

# 找下一个顶层 def 作为结束边界
next_def = text.find("\ndef ", start + len(start_marker))
if next_def == -1:
    next_def = len(text)

before = text[:start]
after = text[next_def:]
path.write_text(before + new_func + after, encoding="utf-8")
print("已替换 call_agent")