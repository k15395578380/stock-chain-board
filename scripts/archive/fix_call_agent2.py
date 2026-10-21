from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

old_start = "def call_agent(query: str) -> dict:"
start = text.find(old_start)
if start == -1:
    raise SystemExit("没找到 call_agent")

# 找到下一个顶层 def 或文件末尾
next_def = text.find("\ndef ", start + len(old_start))
if next_def == -1:
    next_def = len(text)

new_func = '''def call_agent(query: str) -> dict:
    rule_result = AGENT.query(query)

    # 1. 对抗拒绝：规则 Agent 的拒绝是底线，直接返回
    if rule_result.get("refused"):
        rule_result["via"] = "rule"
        return rule_result

    # 2. 有具体环节且有来源：规则 Agent 的真答案，直接返回
    if rule_result.get("segments") and rule_result.get("sources"):
        rule_result["via"] = "rule"
        return rule_result

    # 3. 明确的边界回答：直接返回
    explicit_boundaries = ["未覆盖", "仅覆盖A股", "不做盈利比较", "不提供实时比率", "暂未覆盖"]
    note = rule_result.get("boundary_note", "")
    if any(b in note for b in explicit_boundaries):
        rule_result["via"] = "rule"
        return rule_result

    # 4. 其他情况（模糊边界、无来源、空结果）：交给 LLM
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
        return rule_result
'''

text = text[:start] + new_func + text[next_def:]
path.write_text(text, encoding="utf-8")
print("已收紧 call_agent 判定")