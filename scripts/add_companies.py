import json
import sys
from pathlib import Path

CHAIN_FILES = {
    "semiconductor": Path("chains/semiconductor.json"),
    "newenergy": Path("chains/newenergy.json"),
    "ai_compute": Path("chains/ai_compute.json"),
}
INPUT = Path("data/companies_to_add.json")


def load_chain(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(company, chain_data):
    errors = []
    cid = company.get("id", "")
    if not cid or len(cid) != 6 or not cid.isdigit():
        errors.append(f"{cid}: 代码必须是 6 位数字")
    seg_ids = company.get("segment_ids", [])
    if not seg_ids:
        errors.append(f"{cid}: segment_ids 不能为空")
    valid_segs = {s["id"] for s in chain_data["segments"]}
    for sid in seg_ids:
        if sid not in valid_segs:
            errors.append(f"{cid}: segment_id {sid} 不在链中")
    if not company.get("sources"):
        errors.append(f"{cid}: sources 不能为空")
    for s in company.get("sources", []):
        for k in ["source_type", "source_title", "source_url_or_id", "data_date"]:
            if not s.get(k):
                errors.append(f"{cid}: source 缺少 {k}")
    return errors


def main():
    if not INPUT.exists():
        print(f"找不到 {INPUT}")
        sys.exit(1)
    companies = json.loads(INPUT.read_text(encoding="utf-8"))
    if not isinstance(companies, list):
        print("companies_to_add.json 必须是数组")
        sys.exit(1)

    by_chain = {"semiconductor": [], "newenergy": [], "ai_compute": []}
    all_errors = []
    for c in companies:
        segs = c.get("segment_ids", [])
        if not segs:
            all_errors.append(f"{c.get('id')}: 没有 segment_ids")
            continue
        prefix = segs[0].split(".")[0]
        chain_key = ("semiconductor" if prefix == "semi"
                     else "newenergy" if prefix in ("pv", "wind")
                     else "ai_compute" if prefix == "ai" else None)
        if not chain_key:
            all_errors.append(f"{c.get('id')}: 无法判断归属链（segment 前缀 {prefix}）")
            continue
        chain_data = load_chain(CHAIN_FILES[chain_key])
        errs = validate(c, chain_data)
        if errs:
            all_errors.extend(errs)
        else:
            by_chain[chain_key].append(c)

    if all_errors:
        print("校验失败,未写入：")
        for e in all_errors:
            print("  -", e)
        sys.exit(1)

    for chain_key, items in by_chain.items():
        if not items:
            continue
        path = CHAIN_FILES[chain_key]
        data = load_chain(path)
        existing_ids = {c["id"] for c in data["companies"]}
        added = 0
        for c in items:
            if c["id"] in existing_ids:
                print(f"  跳过已存在: {c['id']} {c['name']}")
                continue
            data["companies"].append(c)
            added += 1
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{path}: 追加 {added} 家")


if __name__ == "__main__":
    main()