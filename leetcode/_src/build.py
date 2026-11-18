#!/usr/bin/env python3
"""Generate AliZafar120/leetcode/<slug>/index.html and leetcode/index.html from problems/*.py."""
import os, sys, json, glob, html, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT", os.path.normpath(os.path.join(HERE, "..")))
CAT_ORDER = ["Array","Binary","Dynamic Programming","Graph","Interval","Linked List","Matrix","String","Tree","Heap"]
PROBLEM_CSS = open(os.path.join(HERE, "problem.css")).read()
INDEX_CSS = open(os.path.join(HERE, "index.css")).read()

def load_all():
    out = []
    for p in sorted(glob.glob(os.path.join(HERE, "problems", "*.py"))):
        spec = importlib.util.spec_from_file_location("p", p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        out.append(m.PROBLEM)
    return out

PAGE_SCRIPT = r"""
var lang = DATA.order[0], idx = 0;
var codecol=document.getElementById("codecol"), panel=document.getElementById("panel"), introEl=document.getElementById("intro");
function renderCode(){
  var L=DATA.langs[lang]; introEl.innerHTML = L.intro || "";
  var html="";
  L.blocks.forEach(function(b,i){
    var clickable = b.explain!==null;
    html += '<button class="blk'+(clickable?'':' static')+(clickable&&i===idx?' on':'')+'" data-i="'+i+'"'+(clickable?'':' tabindex="-1"')+'>'+b.code+'</button>';
  });
  codecol.innerHTML=html;
  codecol.querySelectorAll(".blk").forEach(function(el){
    if(el.classList.contains("static")) return;
    el.onclick=function(){ idx=+el.dataset.i; renderCode(); renderPanel(); };
  });
}
function renderPanel(){
  var L=DATA.langs[lang], b=L.blocks[idx];
  if(!b || b.explain===null){ panel.innerHTML='<div class="hint">Select a line of code to see what it does.</div>'; return; }
  var n=L.blocks.filter(function(x){return x.explain!==null;}).length;
  var c=0; for(var i=0;i<=idx;i++){ if(L.blocks[i].explain!==null) c++; }
  var html='<div class="step">Step '+c+' of '+n+'</div><div class="exp">'+b.explain+'</div>';
  if(b.diagram) html+='<pre class="ascii">'+b.diagram.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")+'</pre>';
  panel.innerHTML=html;
}
document.addEventListener("keydown",function(e){
  if(e.key!=="ArrowDown"&&e.key!=="ArrowUp") return;
  var L=DATA.langs[lang], n=L.blocks.length, d=e.key==="ArrowDown"?1:-1, j=idx;
  for(var k=0;k<n;k++){ j=(j+d+n)%n; if(L.blocks[j].explain!==null){ idx=j; break; } }
  renderCode(); renderPanel(); e.preventDefault();
});
var KEY="leetcode-progress", slug=DATA.slug;
function loadP(){try{return JSON.parse(localStorage.getItem(KEY)||"{}");}catch(e){return {};}}
var st=document.getElementById("status");
function paintStatus(){ var s=loadP()[slug]||"todo"; st.querySelectorAll("button").forEach(function(b){ b.classList.toggle("on", b.dataset.s===s); }); }
st.querySelectorAll("button").forEach(function(b){ b.onclick=function(){ var p=loadP(); p[slug]=b.dataset.s; try{localStorage.setItem(KEY, JSON.stringify(p));}catch(e){} paintStatus(); }; });
paintStatus();
renderCode(); renderPanel();
"""

def problem_page(P, prev_next):
    blocks = [{"code": html.escape(b["code"]), "explain": b["explain"], "diagram": b["diagram"]} for b in P["blocks"]]
    data = {"authored": True, "slug": P["slug"], "order": ["py"], "langs": {"py": {"label": "Python", "intro": P["intro_html"], "blocks": blocks}}}
    full_code = "\n".join(b["code"] for b in P["blocks"])
    prem = ' <span class="tag" title="LeetCode Premium problem">premium</span>' if P["premium"] else ""
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(P["title"])} · LeetCode</title><meta name="robots" content="noindex,nofollow">
<style>{PROBLEM_CSS}
.status{{display:flex;gap:6px;align-items:center;font-size:13px;color:var(--muted)}}.status button{{border:1px solid var(--border);background:var(--panel);color:var(--fg);padding:4px 10px;border-radius:999px;cursor:pointer;font-size:12px}}
.status button.on[data-s="solving"]{{background:var(--medium);color:#fff;border-color:var(--medium)}}.status button.on[data-s="solved"]{{background:var(--solved);color:#fff;border-color:var(--solved)}}.status button.on[data-s="todo"]{{background:var(--todo);color:#fff;border-color:var(--todo)}}
.meta{{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;margin:8px 0 2px;font-size:14px;color:var(--muted)}}
.full{{margin-top:18px}}.full summary{{cursor:pointer;color:var(--muted);font-size:14px}}.full pre{{background:var(--code);color:#d7e3ef;padding:14px;border-radius:10px;overflow:auto;font-size:13px;line-height:1.5}}
.pn{{display:flex;justify-content:space-between;gap:12px;margin-top:22px;font-size:14px}}
</style></head>
<body><div class="wrap">
<div class="top">
  <a href="../" class="back">← All problems</a>
  <div class="ttl"><span class="num">#{P["number"]}</span> {html.escape(P["title"])} <span class="badge {P["difficulty"]}">{P["difficulty"]}</span>{prem}</div>
  <div class="langs"><button class="on">Python</button></div>
</div>
<div class="meta"><span>{html.escape(P["category"])}</span><span>{html.escape(P["complexity"])}</span><a href="{html.escape(P["url"])}" target="_blank" rel="noopener">Open on leetcode.com ↗</a>
  <span class="status" id="status">Status: <button data-s="todo">to do</button><button data-s="solving">solving</button><button data-s="solved">solved</button></span></div>
<div class="statement">{P["statement_html"]}</div>
<div class="intro md" id="intro"></div>
<div class="grid">
  <div class="codecol" id="codecol"></div>
  <aside class="panel" id="panel"><div class="hint">Select a line of code to see what it does.</div></aside>
</div>
<details class="full"><summary>Full solution (copy)</summary><pre>{html.escape(full_code)}</pre></details>
<div class="pn">{prev_next}</div>
<div class="foot">Problem statements are paraphrased; the originals are on <a href="https://leetcode.com">leetcode.com</a>. List from the <a href="https://www.teamblind.com/post/New-Year-Gift---Curated-List-of-Top-75-LeetCode-Questions-to-Save-Your-Time-OaM1orEU">Blind 75</a>.</div>
</div>
<script>
var DATA = {json.dumps(data, ensure_ascii=False)};
{PAGE_SCRIPT}</script></body></html>"""

def index_page(probs):
    bycat = {c: [p for p in probs if p["category"] == c] for c in CAT_ORDER}
    tiers = ""
    for c in CAT_ORDER:
        ps = bycat[c]
        if not ps: continue
        rows = "".join(f'''<div class="row" data-slug="{p["slug"]}" data-title="{html.escape(p["title"].lower())}" data-diff="{p["difficulty"]}">
        <span class="dot" data-dot="{p["slug"]}" title="click to cycle: to do / solving / solved"></span>
        <span class="num">#{p["number"]}</span>
        <a class="t" href="./{p["slug"]}/">{html.escape(p["title"])}</a><span class="badge {p["difficulty"]}" style="font-size:10px">{p["difficulty"]}</span>{'<span class="tag">premium</span>' if p["premium"] else ''}</div>''' for p in ps)
        tiers += f'<div class="tier" data-tier="{html.escape(c)}"><h2>{html.escape(c)} <span style="color:var(--muted);font-weight:400;font-size:15px">({len(ps)})</span></h2><div class="rows">{rows}</div></div>'
    slugs = json.dumps([p["slug"] for p in probs])
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LeetCode — Blind 75 Walkthroughs</title><meta name="robots" content="noindex,nofollow">
<style>{INDEX_CSS}
.row .badge{{padding:1px 7px}}</style></head>
<body><div class="wrap">
<div class="hdr"><h1>LeetCode · Blind 75</h1>
<p>{len(probs)} problems, every one solved in Python with a line-by-line walkthrough and ASCII traces. Grouped by the categories of the <a href="https://www.teamblind.com/post/New-Year-Gift---Curated-List-of-Top-75-LeetCode-Questions-to-Save-Your-Time-OaM1orEU">Blind 75</a> list.</p></div>
<div class="bar"><span id="fill"></span></div><div id="count" style="color:var(--muted);font-size:14px"></div>
<div class="controls">
  <input id="q" placeholder="Search problems…">
  <button class="fbtn on" data-f="all">All</button>
  <button class="fbtn" data-f="Easy">Easy</button>
  <button class="fbtn" data-f="Medium">Medium</button>
  <button class="fbtn" data-f="Hard">Hard</button>
  <button class="fbtn" data-f="todo">Not solved</button>
</div>
<div id="list">{tiers}</div>
<div class="foot">Statements paraphrased; originals on <a href="https://leetcode.com">leetcode.com</a>. Click a dot to mark a problem to do / solving / solved; progress is stored in this browser.</div>
<script>
var KEY="leetcode-progress";
function load(){{try{{return JSON.parse(localStorage.getItem(KEY)||"{{}}");}}catch(e){{return {{}};}}}}
var state=load(), slugs={slugs}, ORDER=["todo","solving","solved"];
function paint(){{
  slugs.forEach(function(s){{var d=document.querySelector('[data-dot="'+s+'"]'); if(d) d.className="dot "+(state[s]||"todo");}});
  var solved=slugs.filter(function(s){{return state[s]==="solved";}}).length;
  document.getElementById("count").textContent=solved+" / "+slugs.length+" solved";
  document.getElementById("fill").style.width=(100*solved/slugs.length)+"%";
}}
paint();
document.querySelectorAll(".dot").forEach(function(d){{ d.style.cursor="pointer"; d.onclick=function(){{ var s=d.dataset.dot, cur=state[s]||"todo"; state[s]=ORDER[(ORDER.indexOf(cur)+1)%3]; try{{localStorage.setItem(KEY, JSON.stringify(state));}}catch(e){{}} paint(); apply(); }}; }});
var q=document.getElementById("q"), filter="all";
function apply(){{
  var term=q.value.trim().toLowerCase();
  document.querySelectorAll(".row").forEach(function(r){{
    var okT = filter==="all" || (filter==="todo" ? (state[r.dataset.slug]||"todo")!=="solved" : r.dataset.diff===filter);
    var okQ = !term || r.dataset.title.indexOf(term)>=0;
    r.style.display = (okT&&okQ)?"":"none";
  }});
  document.querySelectorAll(".tier").forEach(function(t){{
    var any=[].slice.call(t.querySelectorAll(".row")).some(function(r){{return r.style.display!=="none";}});
    t.style.display=any?"":"none";
  }});
}}
q.oninput=apply;
document.querySelectorAll(".fbtn").forEach(function(b){{b.onclick=function(){{
  document.querySelectorAll(".fbtn").forEach(function(x){{x.classList.remove("on");}});
  b.classList.add("on"); filter=b.dataset.f; apply();
}};}});
</script>
</div></body></html>"""

if __name__ == "__main__":
    probs = load_all()
    order = {c: i for i, c in enumerate(CAT_ORDER)}
    probs.sort(key=lambda p: (order.get(p["category"], 99), p["number"]))
    os.makedirs(OUT, exist_ok=True)
    for i, P in enumerate(probs):
        prev = f'<a href="../{probs[i-1]["slug"]}/">← {html.escape(probs[i-1]["title"])}</a>' if i > 0 else "<span></span>"
        nxt = f'<a href="../{probs[i+1]["slug"]}/">{html.escape(probs[i+1]["title"])} →</a>' if i + 1 < len(probs) else "<span></span>"
        d = os.path.join(OUT, P["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(problem_page(P, prev + nxt))
    open(os.path.join(OUT, "index.html"), "w").write(index_page(probs))
    print(f"built {len(probs)} problem pages + index into {OUT}")
