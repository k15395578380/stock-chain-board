import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))
from run_golden import call_agent
from chains_config import CHAIN_FILES

SEGMENT_COMPANIES = {}
SEGMENT_INFO = {}
DATA_DATES = []

for path in CHAIN_FILES:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    DATA_DATES.append(data.get("data_date", ""))
    for seg in data["segments"]:
        SEGMENT_INFO[seg["id"]] = seg
        SEGMENT_COMPANIES.setdefault(seg["id"], [])
    for comp in data["companies"]:
        for sid in comp.get("segment_ids", []):
            if sid in SEGMENT_COMPANIES:
                SEGMENT_COMPANIES[sid].append({
                    "id": comp["id"],
                    "name": comp["name"],
                    "relevance": comp.get("relevance", {}).get(sid, 0),
                    "basis": comp.get("relevance_basis", ""),
                })

LATEST_DATE = max(DATA_DATES) if DATA_DATES else "未知"

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>产业链问答</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 760px; margin: 40px auto; padding: 0 16px; color: #222; }
  h1 { font-size: 20px; margin-bottom: 4px; }
  .subtitle { color: #666; font-size: 13px; margin-bottom: 20px; }
  .row { display: flex; gap: 8px; margin: 16px 0; }
  input { flex: 1; padding: 10px; font-size: 15px; border: 1px solid #ccc; border-radius: 6px; }
  button { padding: 10px 18px; font-size: 15px; border: none; border-radius: 6px; background: #2563eb; color: #fff; cursor: pointer; }
  button:disabled { background: #93b4f5; }
  .card { border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin-top: 16px; background: #fafafa; }
  .label { font-size: 12px; color: #666; margin-top: 12px; }
  .value { font-size: 14px; margin-top: 4px; white-space: pre-wrap; }
  .warn { color: #b45309; }
  .seg-btn { display: inline-block; margin: 4px 6px 4px 0; padding: 4px 10px; font-size: 13px; border: 1px solid #c7d2fe; border-radius: 999px; background: #eef2ff; color: #3730a3; cursor: pointer; }
  .seg-btn:hover, .seg-btn.active { background: #e0e7ff; border-color: #818cf8; }
  .company-list { margin-top: 8px; border-left: 3px solid #c7d2fe; padding-left: 12px; }
  .company-item { font-size: 13px; margin: 4px 0; }
  .rel { color: #6b7280; font-size: 12px; }
  .source-item { font-size: 12px; color: #4b5563; margin: 2px 0; }
  .history { margin-top: 12px; font-size: 13px; color: #666; }
  .history span { display: inline-block; margin: 2px 8px 2px 0; padding: 2px 8px; border-radius: 4px; background: #f3f4f6; cursor: pointer; }
  .history span:hover { background: #e5e7eb; }
  .footer { margin-top: 32px; font-size: 12px; color: #9ca3af; text-align: center; }
</style>
</head>
<body>
<h1>股票产业链问答</h1>
<div class="subtitle">研究参考，不构成投资建议。数据截止：__LATEST_DATE__</div>
<div class="row">
  <input id="q" placeholder="例如：中芯国际在半导体产业链什么位置？" />
  <button id="btn">查询</button>
</div>
<div id="history" class="history"></div>
<div id="out"></div>
<div class="footer">数据以链文件为准，LLM 仅做推理补充。</div>
<script>
const btn = document.getElementById('btn');
const q = document.getElementById('q');
const out = document.getElementById('out');
const historyEl = document.getElementById('history');

function loadHistory() {
  const h = JSON.parse(localStorage.getItem('q_history') || '[]');
  if (!h.length) { historyEl.innerHTML = ''; return; }
  historyEl.innerHTML = '最近查询：' + h.map(x => `<span onclick="quickAsk('${x.replace(/'/g, "\\'")}')">${x}</span>`).join('');
}

function saveHistory(query) {
  let h = JSON.parse(localStorage.getItem('q_history') || '[]');
  h = [query, ...h.filter(x => x !== query)].slice(0, 5);
  localStorage.setItem('q_history', JSON.stringify(h));
  loadHistory();
}

function quickAsk(query) {
  q.value = query;
  ask();
}

async function ask() {
  const query = q.value.trim();
  if (!query) return;
  btn.disabled = true;
  out.innerHTML = '<div class="card">查询中...</div>';
  saveHistory(query);
  try {
    const res = await fetch('/ask', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({query})
    });
    const data = await res.json();
    render(data);
  } catch (e) {
    out.innerHTML = '<div class="card warn">请求失败：' + e.message + '</div>';
  } finally {
    btn.disabled = false;
  }
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function render(data) {
  const segs = data.segments || [];
  const segHtml = segs.length
    ? segs.map(id => `<span class="seg-btn" data-id="${esc(id)}">${esc(id)}</span>`).join('')
    : '<span class="rel">无</span>';
  const srcCount = (data.sources || []).length;
  const srcHtml = srcCount
    ? `<details><summary style="cursor:pointer;font-size:13px;color:#2563eb;">查看 ${srcCount} 条来源</summary>` +
      (data.sources || []).map(s => `<div class="source-item">${esc(s.source_title || '')} · ${esc(s.data_date || '')} · ${esc(s.source_url_or_id || '')}</div>`).join('') +
      '</details>'
    : '<span class="rel">无</span>';
  const note = data.boundary_note
    ? `<div class="label">边界说明</div><div class="value">${esc(data.boundary_note)}</div>`
    : '';
  out.innerHTML = `
    <div class="card">
      <div class="value">${esc(data.text || '')}</div>
      <div class="label">涉及环节（点击展开公司）</div>
      <div class="value">${segHtml}</div>
      <div id="seg-detail"></div>
      <div class="label">来源</div><div class="value">${srcHtml}</div>
      ${note}
    </div>`;
  document.querySelectorAll('.seg-btn').forEach(el => {
    el.onclick = () => {
      document.querySelectorAll('.seg-btn').forEach(b => b.classList.remove('active'));
      el.classList.add('active');
      loadSegment(el.dataset.id);
    };
  });
}

async function loadSegment(id) {
  const detail = document.getElementById('seg-detail');
  if (!detail) return;
  detail.innerHTML = '<div class="label">加载中...</div>';
  try {
    const res = await fetch('/segment/' + encodeURIComponent(id));
    const data = await res.json();
    const comps = data.companies || [];
    const srcs = data.sources || [];
    const compHtml = comps.length
      ? comps.map(c => `<div class="company-item">${esc(c.name)} <span class="rel">（${esc(c.id)}，相关度 ${c.relevance}）</span><br><span class="rel">${esc(c.basis)}</span></div>`).join('')
      : '<div class="company-item rel">该环节暂无收录公司</div>';
    const srcHtml = srcs.length
      ? srcs.map(s => `<div class="source-item">${esc(s.source_title)} · ${esc(s.data_date)} · ${esc(s.source_url_or_id)}</div>`).join('')
      : '<div class="source-item">无来源</div>';
    detail.innerHTML = `
      <div class="label">${esc(data.name || id)} 的公司</div>
      <div class="company-list">${compHtml}</div>
      <div class="label">环节来源</div>
      ${srcHtml}`;
  } catch (e) {
    detail.innerHTML = '<div class="label warn">加载失败：' + esc(e.message) + '</div>';
  }
}

btn.onclick = ask;
q.addEventListener('keydown', e => { if (e.key === 'Enter') ask(); });
loadHistory();
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False), "application/json; charset=utf-8")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            html = HTML.replace("__LATEST_DATE__", LATEST_DATE)
            self._send(200, html, "text/html; charset=utf-8")
            return

        if path.startswith("/segment/"):
            seg_id = path[len("/segment/"):]
            if seg_id not in SEGMENT_INFO:
                self._json(404, {"error": "segment not found"})
                return
            seg = SEGMENT_INFO[seg_id]
            self._json(200, {
                "id": seg_id,
                "name": seg.get("name", seg_id),
                "tier": seg.get("tier", ""),
                "companies": SEGMENT_COMPANIES.get(seg_id, []),
                "sources": seg.get("sources", []),
            })
            return

        self._send(404, "not found", "text/plain; charset=utf-8")

    def do_POST(self):
        if self.path != "/ask":
            self._send(404, "not found", "text/plain; charset=utf-8")
            return
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self._json(400, {"text": "请求格式错误"})
            return
        query = payload.get("query", "")
        result = call_agent(query)
        self._json(200, result)


def main():
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print(f"服务已启动: http://127.0.0.1:8000  |  数据截止 {LATEST_DATE}")
    print("按 Ctrl+C 停止")
    server.serve_forever()


if __name__ == "__main__":
    main()