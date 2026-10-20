from pathlib import Path

path = Path("scripts/app.py")
text = path.read_text(encoding="utf-8")

# 1. 加载 AI 算力链
old_chains = 'CHAIN_FILES = [Path("chains/semiconductor.json"), Path("chains/newenergy.json")]'
new_chains = 'CHAIN_FILES = [Path("chains/semiconductor.json"), Path("chains/newenergy.json"), Path("chains/ai_compute.json")]'
if old_chains not in text:
    raise SystemExit("没找到 CHAIN_FILES 行")
text = text.replace(old_chains, new_chains, 1)

# 2. 把 AGENT 引用改成 call_agent，让 Web 页面也能走 LLM
text = text.replace("from run_golden import AGENT", "from run_golden import call_agent", 1)
text = text.replace("result = AGENT.query(query)", "result = call_agent(query)", 1)

path.write_text(text, encoding="utf-8")
print("已修 app.py：加载 AI 链，/ask 走 call_agent")