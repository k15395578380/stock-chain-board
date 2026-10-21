from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old = '''def call_agent(query: str) -> dict:
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
        return rule_result'''

new = '''def call_agent(query: str) -> dict:
    rule_result = AGENT.query(query)
    if rule_result.get("segments") or rule_result.get("boundary_note") or rule_result.get("refused"):
        rule_result["via"] = "rule"
        return rule_result

    try:
        from llm_agent import llm_agent, validate_llm_output
        llm_result = llm_agent(query)
        if validate_llm_output(llm_result):
            llm_result["via"] = "llm"
            return llm_result
        rule_result["via"] = "rule(llm_rejected)"
        return rule_result
    except Exception as e:
        print(f"[LLM fallback] {type(e).__name__}: {e}")
        rule_result["via"] = "rule(llm_error)"
        return rule_result'''

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已给 call_agent 加调试输出")