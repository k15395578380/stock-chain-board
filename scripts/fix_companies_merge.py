from pathlib import Path

path = Path("scripts/run_golden.py")
lines = path.read_text(encoding="utf-8").splitlines()

target = None
for i, line in enumerate(lines):
    if 'for comp in data["companies"]:' in line and i + 1 < len(lines) and 'self.companies' in lines[i + 1]:
        target = i
        break

if target is None:
    raise SystemExit('没找到 for comp in data["companies"]: 循环')

indent = len(lines[target]) - len(lines[target].lstrip())
base = " " * indent
body = " " * (indent + 4)

new_lines = [
    base + 'for comp in data["companies"]:',
    body + 'name = comp["name"]',
    body + 'if name in self.companies:',
    body + '    existing = self.companies[name]',
    body + '    for sid in comp.get("segment_ids", []):',
    body + '        if sid not in existing.setdefault("segment_ids", []):',
    body + '            existing["segment_ids"].append(sid)',
    body + '    for sid, rel in comp.get("relevance", {}).items():',
    body + '        if sid not in existing.setdefault("relevance", {}):',
    body + '            existing["relevance"][sid] = rel',
    body + '    existing_src = existing.setdefault("sources", [])',
    body + '    seen = set(s.get("source_url_or_id") for s in existing_src)',
    body + '    for s in comp.get("sources", []):',
    body + '        if s.get("source_url_or_id") not in seen:',
    body + '            existing_src.append(s)',
    body + 'else:',
    body + '    self.companies[name] = comp',
]

lines = lines[:target] + new_lines + lines[target + 2:]
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("RuleAgent 已支持按 name 合并跨链公司")