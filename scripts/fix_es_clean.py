from pathlib import Path

path = Path("scripts/add_companies.py")
lines = path.read_text(encoding="utf-8").splitlines()

# 找到 chain_key 起始行
start = None
for i, line in enumerate(lines):
    if line.strip().startswith("chain_key = ("):
        start = i
        break

if start is None:
    raise SystemExit("没找到 chain_key = (")

# 正确块是 4 行，后面的 else 行全部删掉，直到遇到 if not chain_key
correct = lines[start:start + 4]
if not any('energy_storage' in l for l in correct):
    raise SystemExit("前 4 行里没有 energy_storage，请把实际内容贴给我")

end = start + 4
while end < len(lines) and lines[end].strip().startswith("else "):
    end += 1

removed = end - (start + 4)
if removed == 0:
    print("没有多余行，无需删除")
    raise SystemExit(0)

lines = lines[:start + 4] + lines[end:]
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"已删除 {removed} 行多余的 else 续行")