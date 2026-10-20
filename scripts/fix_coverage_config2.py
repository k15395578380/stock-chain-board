from pathlib import Path

path = Path("scripts/check_coverage.py")
text = path.read_text(encoding="utf-8")

if "from chains_config import CHAIN_FILES" in text:
    print("已走统一配置，跳过")
    raise SystemExit(0)

# 找到 CHAIN_FILES = [ 到对应的 ]
start = text.find("CHAIN_FILES = [")
if start == -1:
    raise SystemExit("没找到 CHAIN_FILES = [")
end = text.find("]", start)
if end == -1:
    raise SystemExit("没找到 CHAIN_FILES 闭合括号")
end += 1

replacement = "import sys\nsys.path.insert(0, str(Path(__file__).parent))\nfrom chains_config import CHAIN_FILES"
text = text[:start] + replacement + text[end:]

path.write_text(text, encoding="utf-8")
print("check_coverage.py 已改用 chains_config")