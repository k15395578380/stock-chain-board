from pathlib import Path

path = Path("scripts/llm_agent.py")
text = path.read_text(encoding="utf-8")

old = 'CHAIN_FILES = [Path("chains/semiconductor.json"), Path("chains/newenergy.json")]'
new = 'CHAIN_FILES = [Path("chains/semiconductor.json"), Path("chains/newenergy.json"), Path("chains/ai_compute.json")]'

count = text.count(old)
if count != 1:
    raise SystemExit(f"匹配到 {count} 处，预期 1 处，未修改。请先看第 1~20 行实际内容")

path.write_text(text.replace(old, new), encoding="utf-8")
print("已把 ai_compute.json 加入 LLM 上下文")