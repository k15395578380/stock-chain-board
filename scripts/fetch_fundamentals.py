import argparse
import json
import sys
from pathlib import Path

import akshare as ak
import baostock as bs

sys.path.insert(0, str(Path(__file__).parent))
from chains_config import CHAIN_FILES


def load_all_companies():
    companies = {}
    for path in CHAIN_FILES:
        data = json.loads(path.read_text(encoding="utf-8"))
        for comp in data["companies"]:
            companies[comp["id"]] = comp
    return companies


def to_bs_code(code):
    """将 6 位代码转为 BaoStock 格式（sh.600000 / sz.000001）。"""
    if code.startswith("6"):
        return f"sh.{code}"
    elif code.startswith(("0", "3")):
        return f"sz.{code}"
    elif code.startswith(("4", "8")):
        return f"bj.{code}"
    return code


def get_industry_baostock(code):
    """用 BaoStock 查行业分类。"""
    bs_code = to_bs_code(code)
    rs = bs.query_stock_industry(code=bs_code)
    if rs.error_code != "0":
        return f"查询失败 ({rs.error_msg})"
    data = []
    while rs.next():
        data.append(rs.get_row_data())
    if not data:
        return "未获取"
    # 返回格式: [updateDate, code, code_name, industry, industryClassification]
    return data[0][3] if len(data[0]) > 3 else "未获取"


def get_main_business_akshare(code):
    """用 AkShare 同花顺接口查主营介绍。"""
    try:
        df = ak.stock_zyjs_ths(symbol=code)
        if df is None or df.empty:
            return []
        return df.head(5).to_dict("records")
    except Exception as e:
        return [{"error": str(e)}]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", help="单只股票代码，如 688981")
    parser.add_argument("--all", action="store_true", help="校验所有已收录公司")
    args = parser.parse_args()

    companies = load_all_companies()

    if args.code:
        codes = [args.code]
    elif args.all:
        codes = list(companies.keys())
    else:
        print("用法: python scripts/fetch_fundamentals.py --code 688981 或 --all")
        sys.exit(1)

    # 登录 BaoStock（无账号密码，直接登录）
    lg = bs.login()
    if lg.error_code != "0":
        print(f"BaoStock 登录失败: {lg.error_msg}")
        sys.exit(1)

    try:
        for code in codes:
            comp = companies.get(code, {"name": "未知"})
            print(f"\n=== {code} {comp['name']} ===")

            # 1. 行业分类（BaoStock）
            industry = get_industry_baostock(code)
            print(f"  行业: {industry}")

            # 2. 主营介绍（AkShare 同花顺）
            biz = get_main_business_akshare(code)
            if biz and "error" in biz[0]:
                print(f"  主营: 获取失败 ({biz[0]['error']})")
            elif biz:
                for b in biz[:3]:
                    # 同花顺接口返回字段可能包含 主营业务、产品类型、产品名称
                    main_biz = b.get("主营业务", "") or b.get("产品名称", "") or str(b)[:60]
                    print(f"  主营: {main_biz[:80]}")
            else:
                print("  主营: 暂无数据")
    finally:
        bs.logout()


if __name__ == "__main__":
    main()