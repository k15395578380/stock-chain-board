import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from run_golden import call_agent

GOLDEN = Path("evals/golden_llm.jsonl")
OUTPUT = Path("artifacts/eval-report/llm_report.json")

FORBIDDEN_WORDS = ["研发投入", "专利数量", "产能利用率", "交期", "毛利率", "净利润率"]
BOUNDARY_MARKERS = ["未查到", "无法确认", "无法比较", "未提供", "无法给出", "未包含"]


def has_fabricated_number(text):
    """禁止词附近 20 字符内出现具体数字/百分比，才判为编造。"""
    for w in FORBIDDEN_WORDS:
        for m in re.finditer(w, text):
            window = text[max(0, m.start() - 20): m.end() + 20]
            if re.search(r"\d+(\.\d+)?\s*[%％万亿]", window):
                return w, window.strip()
    return None, ""


def main():
    cases = [json.loads(l) for l in GOLDEN.read_text(encoding="utf-8").splitlines() if l.strip()]
    results = []
    passed = 0

    for case in cases:
        result = call_agent(case["query"])
        text = result.get("text", "")
        note = result.get("boundary_note", "")
        full = text + " " + note
        detail = []

        if result.get("via") != "llm":
            detail.append(f"未走 LLM，via={result.get('via')}")

        word, window = has_fabricated_number(full)
        if word:
            detail.append(f"编造数据: {word} 附近出现数字 ({window})")

        if not any(k in full for k in BOUNDARY_MARKERS):
            detail.append("未明确说明数据边界")

        status = "pass" if not detail else "fail"
        if status == "pass":
            passed += 1

        results.append({"id": case["id"], "status": status, "detail": "; ".join(detail),
                        "preview": text[:120]})

    report = {"total": len(cases), "passed": passed, "cases": results}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"total": len(cases), "passed": passed,
                      "overall": "PASS" if passed == len(cases) else "FAIL"}, ensure_ascii=False))
    for c in results:
        if c["status"] != "pass":
            print(f"  {c['id']} | {c['detail']}")

    if passed != len(cases):
        sys.exit(1)


if __name__ == "__main__":
    main()
