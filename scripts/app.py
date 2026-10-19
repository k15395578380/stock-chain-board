import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from run_golden import AGENT

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>产业链问答</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 760px; margin: 40px auto; padding: 0 16px; color: #222; }
  h1 { font-size: 20px; }
  .row { display: flex; gap: 8px; margin: 16px 0; }
  input { flex: 1; padding: 10px; font-size: 15px; border: 1px solid #ccc; border-radius: 6px; }
  button { padding: 10px 18px; font-size: 15px; border: none; border-radius: 6px; background: #2563eb; color: #fff; cursor: pointer; }
  button:disabled { background: #93b4f5; }
  .card { border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin-top: 16px; background: #fafafa; }
  .label { font-size: 12px; color: #666; margin-top: 12px; }
  .value { font-size: 14px; margin-top: 4px; white-space: pre-wrap; }
  .warn { color: #b45309; }
</style>
</head>
<body>
<h1>股票产业链问答</h1>
<p style="color:#666;font-size:14px;">研究参考，不构成投资建议。数据以链文件为准。</p>
<div class="row">
  <input id="q" placeholder="例如：中芯国际在半导体产业链什么位置？" />
  <button id="btn">查询</button>
</div>
<div id="out"></div>
<script>
const btn = document.getElementById('btn');
const q = document.getElementById('q');
const out = document.getElementById('out');

async function ask() {
  const query = q.value.trim();
  if (!query) return;
  btn.disabled = true;
  out.innerHTML = '<div class="card">查询中...</div>';
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

function render(data) {
  const segs = (data.segments || []).join(', ') || '无';
  const srcCount = (data.sources || []).length;
  const note = data.boundary_note ? `<div class="label">边界说明</div><div class="value">${data.boundary_note}</div>` : '';
  out.innerHTML = `
    <div class="card">
      <div class="value">${data.text || ''}</div>
      <div class="label">涉及环节</div><div class="value">${segs}</div>
      <div class="label">来源数</div><div class="value">${srcCount}</div>
      ${note}
    </div>`;
}

btn.onclick = ask;
q.addEventListener('keydown', e => { if (e.key === 'Enter') ask(); });
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

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, HTML, "text/html; charset=utf-8")
        else:
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
            self._send(400, json.dumps({"text": "请求格式错误"}), "application/json; charset=utf-8")
            return
        query = payload.get("query", "")
        result = AGENT.query(query)
        self._send(200, json.dumps(result, ensure_ascii=False), "application/json; charset=utf-8")


def main():
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("服务已启动: http://127.0.0.1:8000")
    print("按 Ctrl+C 停止")
    server.serve_forever()


if __name__ == "__main__":
    main()