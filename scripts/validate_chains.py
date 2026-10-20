import json
import sys
from pathlib import Path

REQUIRED_SOURCE_FIELDS = ["source_type", "source_title", "source_url_or_id", "data_date"]
from chains_config import CHAIN_FILES

def validate_file(path: Path):
    errors = []
    if not path.exists():
        return [f"文件不存在: {path}"]
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"{path} JSON 解析失败: {e}"]

    for edge in data.get("edges", []):
        edge_id = edge.get("id", "<unknown>")
        sources = edge.get("sources", [])
        if not sources:
            errors.append(f"{path} edge {edge_id} 缺少 sources")
            continue
        for idx, s in enumerate(sources):
            missing = [k for k in REQUIRED_SOURCE_FIELDS if not s.get(k)]
            if missing:
                errors.append(f"{path} edge {edge_id} source[{idx}] 缺少字段: {missing}")

    for seg in data.get("segments", []):
        if not seg.get("sources"):
            errors.append(f"{path} segment {seg.get('id')} 缺少 sources")

    for comp in data.get("companies", []):
        if not comp.get("sources"):
            errors.append(f"{path} company {comp.get('id')} 缺少 sources")

    return errors

def main():
    all_errors = []
    for p in CHAIN_FILES:
        all_errors.extend(validate_file(p))
    if all_errors:
        print("校验失败：")
        for e in all_errors:
            print("  -", e)
        sys.exit(1)
    print("链文件校验通过")

if __name__ == "__main__":
    main()