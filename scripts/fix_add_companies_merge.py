from pathlib import Path

path = Path("scripts/add_companies.py")
lines = path.read_text(encoding="utf-8").splitlines()

target = None
for i, line in enumerate(lines):
    if 'existing_ids = {c["id"] for c in data["companies"]}' in line:
        target = i
        break

if target is None:
    raise SystemExit("没找到 existing_ids 行，请把 for chain_key, items 那段贴给我")

indent = len(lines[target]) - len(lines[target].lstrip())
base = " " * indent
body = " " * (indent + 4)

new_lines = [
    base + 'id_to_company = {c["id"]: c for c in data["companies"]}',
    base + 'added = 0',
    base + 'merged = 0',
    base + 'for c in items:',
    body + 'if c["id"] in id_to_company:',
    body + '    existing = id_to_company[c["id"]]',
    body + '    touched = False',
    body + '    for sid in c.get("segment_ids", []):',
    body + '        if sid not in existing.setdefault("segment_ids", []):',
    body + '            existing["segment_ids"].append(sid)',
    body + '            touched = True',
    body + '    for sid, rel in c.get("relevance", {}).items():',
    body + '        if sid not in existing.setdefault("relevance", {}):',
    body + '            existing["relevance"][sid] = rel',
    body + '            touched = True',
    body + '    if touched:',
    body + '        print("  合并环节: " + c["id"] + " " + c["name"])',
    body + '        merged += 1',
    body + '    else:',
    body + '        print("  已完整，跳过: " + c["id"] + " " + c["name"])',
    body + '    continue',
    body + 'data["companies"].append(c)',
    body + 'id_to_company[c["id"]] = c',
    body + 'added += 1',
]

end = None
for j in range(target, len(lines)):
    if 'path.write_text' in lines[j]:
        end = j
        break
if end is None:
    raise SystemExit("没找到 path.write_text 行")

lines = lines[:target] + new_lines + lines[end:]
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("add_companies 已支持已存在公司合并环节")