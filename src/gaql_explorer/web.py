"""Optional Flask web UI for GAQL Explorer."""

try:
    from flask import Flask, jsonify, render_template_string, request
except ImportError:
    raise RuntimeError("Flask not installed. Install with: pip install 'gaql-explorer[web]'")

from .demo_data import resolve_query
from .templates import TEMPLATES, get_by_name, get_categories, get_by_category

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GAQL Explorer</title>
<style>
  :root { --bg: #0B1120; --surface: #131B2E; --border: #1E293B; --text: #E2E8F0; --dim: #94A3B8; --accent: #6366F1; --green: #22C55E; --amber: #F59E0B; --red: #EF4444; --mono: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
  .container { max-width: 1200px; margin: 0 auto; padding: 2rem 1.5rem; }
  h1 { font-size: 1.5rem; margin-bottom: 0.5rem; }
  h1 span { color: var(--accent); }
  .subtitle { color: var(--dim); margin-bottom: 2rem; }
  .editor { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem; }
  textarea { width: 100%; min-height: 100px; background: var(--bg); color: var(--text); border: 1px solid var(--border); border-radius: 6px; padding: 0.75rem; font-family: var(--mono); font-size: 0.875rem; resize: vertical; }
  textarea:focus { outline: 2px solid var(--accent); border-color: transparent; }
  .actions { display: flex; gap: 0.75rem; margin-top: 0.75rem; align-items: center; }
  button { background: var(--accent); color: white; border: none; padding: 0.5rem 1.25rem; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.875rem; }
  button:hover { filter: brightness(1.1); }
  .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--dim); }
  .btn-outline:hover { border-color: var(--accent); color: var(--text); }
  .templates { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.75rem; margin-bottom: 2rem; }
  .tmpl-card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem 1rem; cursor: pointer; transition: border-color 0.15s; }
  .tmpl-card:hover { border-color: var(--accent); }
  .tmpl-name { font-family: var(--mono); font-size: 0.8rem; color: var(--accent); }
  .tmpl-desc { font-size: 0.8rem; color: var(--dim); margin-top: 0.25rem; }
  .cat-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--dim); margin: 1rem 0 0.5rem; }
  table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
  th { text-align: left; padding: 0.5rem 0.75rem; border-bottom: 2px solid var(--border); color: var(--dim); font-weight: 600; text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.05em; }
  td { padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--border); font-family: var(--mono); font-size: 0.8rem; }
  tr:hover td { background: rgba(99, 102, 241, 0.05); }
  .results { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; overflow-x: auto; }
  .empty { text-align: center; padding: 2rem; color: var(--dim); }
  .badge { display: inline-block; padding: 0.125rem 0.5rem; border-radius: 9999px; font-size: 0.7rem; font-weight: 600; }
  .badge-green { background: rgba(34,197,94,0.15); color: var(--green); }
  .badge-amber { background: rgba(245,158,11,0.15); color: var(--amber); }
</style>
</head>
<body>
<div class="container">
  <h1><span>GAQL</span> Explorer</h1>
  <p class="subtitle">Google Ads Query Language toolkit — demo mode</p>

  <div class="editor">
    <textarea id="query" placeholder="SELECT campaign.name, metrics.cost_micros FROM campaign ORDER BY metrics.cost_micros DESC">SELECT campaign.name, campaign.status, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.ctr FROM campaign ORDER BY metrics.cost_micros DESC</textarea>
    <div class="actions">
      <button onclick="runQuery()">Run Query</button>
      <span style="color:var(--dim);font-size:0.8rem" id="status"></span>
    </div>
  </div>

  <h2 style="font-size:1.1rem;margin-bottom:0.5rem">Templates</h2>
  <div id="templates"></div>

  <h2 style="font-size:1.1rem;margin:1.5rem 0 0.5rem">Results</h2>
  <div class="results" id="results"><div class="empty">Run a query to see results</div></div>
</div>
<script>
const templatesEl = document.getElementById('templates');
const resultsEl = document.getElementById('results');
const queryEl = document.getElementById('query');
const statusEl = document.getElementById('status');

fetch('/api/templates').then(r=>r.json()).then(data => {
  let html = '';
  for (const [cat, tmpls] of Object.entries(data)) {
    html += `<div class="cat-title">${cat}</div><div class="templates">`;
    for (const t of tmpls) {
      html += `<div class="tmpl-card" onclick="loadTemplate('${t.name}')">
        <div class="tmpl-name">${t.name}</div>
        <div class="tmpl-desc">${t.description}</div>
      </div>`;
    }
    html += '</div>';
  }
  templatesEl.innerHTML = html;
});

function loadTemplate(name) {
  fetch('/api/templates/' + name).then(r=>r.json()).then(t => {
    queryEl.value = t.query;
    runQuery();
  });
}

function runQuery() {
  const q = queryEl.value.trim();
  if (!q) return;
  statusEl.textContent = 'Running...';
  fetch('/api/query', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({query: q})})
    .then(r=>r.json()).then(data => {
      if (!data.rows || !data.rows.length) {
        resultsEl.innerHTML = '<div class="empty">No results</div>';
        statusEl.textContent = '';
        return;
      }
      let html = '<table><thead><tr>';
      for (const h of data.headers) html += `<th>${h.split('.').pop()}</th>`;
      html += '</tr></thead><tbody>';
      for (const row of data.rows) {
        html += '<tr>';
        for (const h of data.headers) {
          let v = row[h];
          if (h.includes('micros') && typeof v === 'number') v = '$' + (v/1e6).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2});
          else if ((h.includes('ctr') || h.includes('share')) && typeof v === 'number') v = (v*100).toFixed(1) + '%';
          else if (typeof v === 'number') v = v.toLocaleString();
          html += `<td>${v ?? '—'}</td>`;
        }
        html += '</tr>';
      }
      html += '</tbody></table>';
      resultsEl.innerHTML = html;
      statusEl.textContent = `${data.rows.length} rows`;
    });
}
</script>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(PAGE)


@app.route("/api/templates")
def api_templates():
    result = {}
    for cat in get_categories():
        result[cat] = [{"name": t.name, "description": t.description} for t in get_by_category(cat)]
    return jsonify(result)


@app.route("/api/templates/<name>")
def api_template_detail(name):
    t = get_by_name(name)
    if not t:
        return jsonify({"error": "not found"}), 404
    return jsonify({
        "name": t.name,
        "category": t.category,
        "description": t.description,
        "query": t.query,
        "when_to_use": t.when_to_use,
    })


@app.route("/api/query", methods=["POST"])
def api_query():
    data = request.get_json()
    query = data.get("query", "")
    headers, rows = resolve_query(query)
    return jsonify({"headers": headers, "rows": rows})


def run_server(host: str = "127.0.0.1", port: int = 5000, debug: bool = False):
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_server(debug=True)
