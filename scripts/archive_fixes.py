from pathlib import Path

archive_dir = Path("scripts/archive")
archive_dir.mkdir(exist_ok=True)

fix_scripts = [
    "add_ev_cases.py", "add_ev_regression.py",
    "fix_boundary_words.py", "fix_call_agent2.py", "fix_call_agent_debug.py",
    "fix_complex_query.py", "fix_es_aliases3.py", "fix_es_prefix2.py",
    "fix_es_prefix3.py", "fix_ev_prefix.py", "fix_l03_query.py",
    "fix_llm_chains.py", "fix_llm_prompt.py", "fix_match_merge.py",
    "write_llm_cases.py"
]

moved = 0
for name in fix_scripts:
    src = Path("scripts") / name
    if src.exists():
        src.rename(archive_dir / name)
        moved += 1

print(f"已将 {moved} 个一次性脚本移动到 scripts/archive/")