from pathlib import Path

path = Path("scripts/run_golden.py")
text = path.read_text(encoding="utf-8")

if "regression_cases_pass" in text:
    print("已有回归门禁，跳过")
    raise SystemExit(0)

old = '    gates["overall"] = "PASS" if all(gates.values()) else "FAIL"'
if old not in text:
    raise SystemExit("没找到 gates['overall'] 行，请手动检查 run_golden.py")

new = '''    # 回归 case 硬门禁：任何一条 fail，overall 直接 FAIL
    REGRESSION_IDS = {"N12", "N13", "N14", "N15", "N16"}
    regression_failures = [c["id"] for c in results if c["id"] in REGRESSION_IDS and c["status"] != "pass"]
    gates["regression_cases_pass"] = len(regression_failures) == 0
    gates["overall"] = "PASS" if all(gates.values()) else "FAIL"
    if regression_failures:
        print(f"回归 case 失败: {regression_failures}")'''

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("已加入回归 case 硬门禁：N12-N16")