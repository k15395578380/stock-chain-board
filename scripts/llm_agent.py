import json
import os
import re
from pathlib import Path

from openai import OpenAI

from chains_config import CHAIN_FILES

SEGMENTS = {}
COMPANIES = {}
for path in CHAIN_FILES:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    for seg in data["segments"]:
        SEGMENTS[seg["id"]] = seg
    for comp in data["companies"]:
        COMPANIES[comp["id"]] = comp

VALID_SEGMENT_IDS = set(SEGMENTS.keys())

# 如果你用非 DeepSeek 的模型，改这两行
BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"
API_KEY_ENV = "DEEPSEEK_API_KEY"

SYSTEM_PROMPT = """你是股票产业链看板的研究助手。你只能基于给定的产业链数据回答，不能编造。

可用环节（segment_id: 名称, 层级）：
{segments}

可用公司（代码: 名称, 归属环节）：
{companies}

规则：
1. 只回答与产业链结构、公司归属、上下游关系相关的问题。
2. 同一公司可能归属多条产业链的不同环节（如寒武纪同时属于半导体芯片设计和AI芯片），回答时按问题涉及的链分别说明，不要只挑一个。
3. 如果问题涉及涨跌预测、目标价、个股推荐、收益保证，必须拒绝，refused 设为 true，并在 text 中包含"不构成投资建议"。
4. 如果数据里没有答案，必须在 text 中明确写"未查到可靠来源"或"暂无可靠来源确认"，并在 boundary_note 写明原因；不要只说"请提供更多信息"，不要猜测。
5. segments 只能使用上面列出的 segment_id，不能编造。
6. 只要 segments 非空，sources 必须非空。
7. 当被问到"影响、带动、传导方向"时，可以基于产业链结构给出方向性判断，但必须同时说明"数据未提供传导强度的量化依据"，不要给出具体幅度或时间。
8. 任何回答的 text 末尾都必须包含一句边界说明（"数据未提供…"或"未查到可靠来源"或"无法确认…"），即使只是方向性判断。
9. 输出必须是 JSON，不要输出任何 JSON 之外的内容。

输出格式：
{{
  "text": "给用户的回答",
  "segments": ["semi.wafer_fab"],
  "edges": [{{"from": "semi.material", "to": "semi.wafer_fab"}}],
  "sources": [{{"source_title": "来源标题", "data_date": "2025-12-31"}}],
  "refused": false,
  "boundary_note": ""
}}"""


def _build_context():
    seg_lines = [f"- {sid}: {s['name']}（{s['tier']}）" for sid, s in SEGMENTS.items()]
    comp_lines = []
    for cid, c in COMPANIES.items():
        segs = ", ".join(c.get("segment_ids", []))
        comp_lines.append(f"- {cid}: {c['name']}（{segs}）")
    return "\n".join(seg_lines), "\n".join(comp_lines)


def _extract_json(text):
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    if m:
        text = m.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("没有找到 JSON")
    return json.loads(text[start:end + 1])


def llm_agent(query: str) -> dict:
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"{API_KEY_ENV} 未设置")

    seg_text, comp_text = _build_context()
    client = OpenAI(api_key=api_key, base_url=BASE_URL)
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(segments=seg_text, companies=comp_text)},
            {"role": "user", "content": query},
        ],
        temperature=0,
        max_tokens=800,
        timeout=30,
    )
    raw = resp.choices[0].message.content
    data = _extract_json(raw)
    return {
        "text": data.get("text", ""),
        "segments": data.get("segments", []) or [],
        "edges": data.get("edges", []) or [],
        "sources": data.get("sources", []) or [],
        "refused": bool(data.get("refused", False)),
        "boundary_note": data.get("boundary_note", "") or "",
        "via": "llm",
    }


def validate_llm_output(result: dict) -> bool:
    text = result.get("text", "")

    if result.get("refused"):
        return "不构成投资建议" in text

    forbidden = ["会涨", "目标价", "保证赚钱", "已修改", "相关度已改为"]
    if any(w in text for w in forbidden):
        return False

    segs = result.get("segments", [])
    if segs:
        if any(sid not in VALID_SEGMENT_IDS for sid in segs):
            return False
        if not result.get("sources"):
            return False

    if not result.get("sources") and not result.get("boundary_note"):
        if any(w in text for w in ["因为", "原因是", "由于"]):
            return False

    return True