from pathlib import Path

path = Path("scripts/add_companies.py")
text = path.read_text(encoding="utf-8")

old_files = '''CHAIN_FILES = {
    "semiconductor": Path("chains/semiconductor.json"),
    "newenergy": Path("chains/newenergy.json"),
    "ai_compute": Path("chains/ai_compute.json"),
}'''
new_files = 'from chains_config import CHAIN_FILES_MAP as CHAIN_FILES'
if old_files not in text:
    raise SystemExit("没找到 CHAIN_FILES 字典，请检查实际内容")
text = text.replace(old_files, new_files, 1)

old_by_chain = '    by_chain = {"semiconductor": [], "newenergy": [], "ai_compute": []}'
new_by_chain = '    by_chain = {k: [] for k in CHAIN_FILES}'
if old_by_chain not in text:
    raise SystemExit("没找到 by_chain 行，请检查实际内容")
text = text.replace(old_by_chain, new_by_chain, 1)

path.write_text(text, encoding="utf-8")
print("add_companies.py 已改用统一配置，by_chain 动态生成")