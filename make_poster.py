"""Render a 1080x1080 HiveNexis poster: python3 make_poster.py spec.json posts/NAME.png"""
import base64, html, re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "img/logo.png").read_bytes()).decode()
CHECK = '<span class="ck"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>'
UP = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#17a34a" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20V5M5 12l7-7 7 7"/></svg>'

SHOP_VIS = """
<div class="pp">
 <div class="pp-bar"><i></i><i></i><i></i><span>yourstore.com/products</span></div>
 <div class="pp-body">
  <div class="pp-img"><svg viewBox="0 0 200 220" width="170" height="187">
   <ellipse cx="100" cy="205" rx="62" ry="9" fill="#1c0f6b" opacity=".14"/>
   <rect x="80" y="14" width="40" height="30" rx="5" fill="#1c0f6b"/>
   <rect x="70" y="40" width="60" height="16" rx="4" fill="#2a1a8a"/>
   <rect x="52" y="54" width="96" height="150" rx="20" fill="#5b2be0"/>
   <rect x="52" y="54" width="34" height="150" rx="17" fill="#7a52f0" opacity=".7"/>
   <rect x="66" y="104" width="68" height="62" rx="8" fill="#fff"/>
   <rect x="76" y="118" width="48" height="7" rx="3.5" fill="#1c0f6b"/><rect x="76" y="133" width="34" height="6" rx="3" fill="#b9a4f5"/><rect x="76" y="146" width="40" height="6" rx="3" fill="#b9a4f5"/>
  </svg><b class="badge">Best Seller</b></div>
  <div class="pp-info">
   <div class="pp-t">Your Product</div>
   <div class="stars">★★★★★ <span>4.9</span></div>
   <div class="price">$49.00</div>
   <div class="atc">Add to Cart</div>
   <div class="ship">Free shipping · Easy returns</div>
  </div>
 </div>
</div>
<div class="chip c1">%UP%<div><small>Orders</small><b>+38%</b></div></div>
<div class="sales"><div class="s-t">Store Sales <em>this month</em></div>
<svg viewBox="0 0 308 96" width="270" height="84"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5b2be0" stop-opacity=".38"/><stop offset="1" stop-color="#5b2be0" stop-opacity="0"/></linearGradient></defs>
<path d="M4 80 L50 68 L92 72 L138 50 L180 56 L226 30 L296 10 L296 92 L4 92 Z" fill="url(#g)"/><path d="M4 80 L50 68 L92 72 L138 50 L180 56 L226 30 L296 10" fill="none" stroke="#5b2be0" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="296" cy="10" r="7" fill="#5b2be0"/></svg></div>
""".replace("%UP%", UP)

SEO_VIS = """
<div class="search"><span>best shopify agency near me</span><i><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M16 16l5 5"/></svg></i></div>
<div class="rank">
 <div class="r-t">Google Rankings</div>
 <div class="r-row"><b>#1</b>%UP%<span>buy leather bags online</span></div>
 <div class="r-row"><b>#2</b>%UP%<span>handmade gifts store</span></div>
 <div class="r-row"><b>#3</b>%UP%<span>organic skincare shop</span></div>
</div>
<div class="ai"><div class="ai-h"><svg viewBox="0 0 24 24" width="26" height="26" fill="#5b2be0"><path d="M12 2l2.2 6.3L20.5 10l-6.3 2.2L12 18.5l-2.2-6.3L3.5 10l6.3-1.7z"/><path d="M19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.100-.9z"/></svg>AI Answer</div>
 <div class="ai-l"></div><div class="ai-l s"></div>
 <div class="cite">Source: <b>yourbrand.com</b></div></div>
<div class="score"><svg viewBox="0 0 120 120" width="124" height="124"><circle cx="60" cy="60" r="50" fill="#fff" stroke="#e6dcff" stroke-width="11"/><circle cx="60" cy="60" r="50" fill="none" stroke="#5b2be0" stroke-width="11" stroke-linecap="round" stroke-dasharray="280 314" transform="rotate(-90 60 60)"/><text x="60" y="58" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="32" fill="#100c2a">89</text><text x="60" y="78" text-anchor="middle" font-family="Poppins" font-weight="500" font-size="12" fill="#17a34a">SEO Score</text></svg></div>
""".replace("%UP%", UP)

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1080px;overflow:hidden;font-family:Poppins,sans-serif;color:#100c2a;position:relative;
 background:radial-gradient(circle at 100% 30%,#d6c8ff 0,rgba(214,200,255,0) 52%),radial-gradient(circle at 0% 100%,#e3d9ff 0,rgba(227,217,255,0) 40%),#fbfaff}
.dots{position:absolute;width:240px;height:240px;background-image:radial-gradient(#b9a4f5 3px,transparent 3.5px);background-size:22px 22px;opacity:.5}
.d1{left:0;top:0;-webkit-mask-image:linear-gradient(135deg,#000,transparent 70%)}.d2{right:0;bottom:140px;-webkit-mask-image:linear-gradient(315deg,#000,transparent 70%)}
.wrap{position:absolute;inset:0;padding:52px 64px 44px;display:flex;flex-direction:column}
.top{flex:none;display:flex;justify-content:space-between;align-items:center}
.top img{height:84px;display:block}
.tag{background:#5b2be0;color:#fff;font-weight:700;font-size:34px;letter-spacing:1px;padding:8px 26px;transform:rotate(-3deg);white-space:nowrap}
h1{flex:none;margin-top:30px;font-weight:700;line-height:1.02;letter-spacing:-3.5px;white-space:nowrap;-webkit-text-stroke:2.5px currentColor}
.hl{color:#5b2be0}
.rule{flex:none;width:430px;height:8px;background:#5b2be0;margin:18px 0 0;transform:rotate(-.8deg);border-radius:4px}
.cols{flex:1;min-height:0;display:flex;gap:34px;margin-top:22px}
.left{width:500px;flex:none;display:flex;flex-direction:column;justify-content:space-between}
.sub{font-size:31px;line-height:1.28;font-weight:500}
.sub b{color:#5b2be0;font-weight:700}
.card{background:#1c0f6b;border-radius:28px;padding:22px 28px;display:flex;flex-direction:column;gap:13px;color:#fff}
.li{display:flex;align-items:center;gap:16px;font-size:27px;font-weight:500;line-height:1.2}
.li+.li{border-top:2px dashed rgba(255,255,255,.28);padding-top:13px}
.ck{flex:none;width:42px;height:42px;border-radius:50%;background:#5b2be0;display:flex;align-items:center;justify-content:center}
.right{flex:1;position:relative}
.bar{flex:none;margin-top:24px;height:104px;border-radius:28px;background:linear-gradient(90deg,#4a1fd1,#6a3cf0);display:flex;align-items:center;padding:0 30px;gap:22px;color:#fff}
.cta{font-weight:700;font-size:25px;line-height:1.1;letter-spacing:.5px}
.cta small{display:block;font-weight:500;font-size:19px;opacity:.9;letter-spacing:0}
.sep{width:2px;height:60px;background:rgba(255,255,255,.35)}
.url{background:#1c0f6b;border-radius:40px;padding:8px 28px;font-weight:700;font-size:36px}
.say{margin-left:auto;font-style:italic;font-weight:500;font-size:23px;line-height:1.2;text-align:right;transform:rotate(-4deg)}
.sh{box-shadow:0 14px 36px rgba(60,30,160,.2)}
/* shopify visual */
.pp{position:absolute;right:0;top:0;width:410px;background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 14px 36px rgba(60,30,160,.2)}
.pp-bar{height:38px;background:#f1ecff;display:flex;align-items:center;gap:7px;padding:0 14px}
.pp-bar i{width:11px;height:11px;border-radius:50%;background:#c9bbf7}.pp-bar span{margin-left:10px;font-size:15px;color:#6b6590;font-weight:500}
.pp-body{display:flex;gap:16px;padding:16px}
.pp-img{position:relative;width:176px;height:214px;border-radius:16px;background:linear-gradient(160deg,#efe9ff,#d9ccff);display:flex;align-items:flex-end;justify-content:center;flex:none}
.badge{position:absolute;left:10px;top:10px;background:#1c0f6b;color:#fff;font-size:13px;font-weight:600;border-radius:20px;padding:3px 10px}
.pp-info{display:flex;flex-direction:column;gap:7px;min-width:0;padding-top:4px}
.pp-t{font-weight:700;font-size:25px;line-height:1.1}
.stars{color:#f5a623;font-size:19px;letter-spacing:1px}.stars span{color:#6b6590;font-weight:600;font-size:16px;letter-spacing:0}
.price{font-weight:700;font-size:30px;color:#5b2be0}
.atc{background:#5b2be0;color:#fff;font-weight:700;font-size:19px;text-align:center;border-radius:12px;padding:10px 0;margin-top:2px}
.ship{font-size:13px;color:#6b6590;font-weight:500}
.chip{position:absolute;background:#fff;border-radius:18px;padding:10px 16px;display:flex;align-items:center;gap:10px;box-shadow:0 12px 30px rgba(60,30,160,.22)}
.chip small{display:block;font-size:14px;color:#6b6590;font-weight:500;line-height:1}.chip b{font-size:26px;line-height:1.15;color:#17a34a}
.c1{left:-26px;top:236px}
.sales{position:absolute;right:0;bottom:0;width:306px;background:#fff;border-radius:22px;padding:14px 18px 10px;box-shadow:0 14px 36px rgba(60,30,160,.2)}
.s-t{font-weight:700;font-size:20px}.s-t em{font-style:normal;font-weight:500;color:#6b6590;font-size:15px}
/* seo visual */
.search{position:absolute;right:0;top:0;width:410px;height:60px;border:2.5px solid #5b2be0;border-radius:40px;background:#fff;display:flex;align-items:center;justify-content:space-between;overflow:hidden}
.search span{padding-left:22px;font-size:19px;color:#3d3766;font-weight:500;white-space:nowrap}
.search i{background:#5b2be0;height:100%;width:70px;display:flex;align-items:center;justify-content:center;flex:none}
.rank{position:absolute;left:-10px;top:84px;width:286px;background:#fff;border-radius:22px;padding:16px 20px;box-shadow:0 14px 36px rgba(60,30,160,.2);display:flex;flex-direction:column;gap:8px}
.r-t{font-weight:700;font-size:22px}
.r-row{display:flex;align-items:center;gap:8px;font-size:15.5px;font-weight:500;color:#3d3766;white-space:nowrap}
.r-row b{font-size:25px;color:#100c2a;width:42px}
.score{position:absolute;right:-6px;top:96px}
.ai{position:absolute;right:0;bottom:0;width:330px;background:#fff;border-radius:22px;padding:16px 20px;box-shadow:0 14px 36px rgba(60,30,160,.2);display:flex;flex-direction:column;gap:9px}
.ai-h{display:flex;align-items:center;gap:8px;font-weight:700;font-size:22px}
.ai-l{height:10px;border-radius:5px;background:#e6dcff}.ai-l.s{width:70%}
.cite{font-size:18px;font-weight:500;color:#3d3766;background:#f1ecff;border-radius:12px;padding:6px 12px;align-self:flex-start}.cite b{color:#5b2be0}
"""


FONT_CSS = "".join(
    f"@font-face{{font-family:Poppins;font-weight:{w};font-style:{st};src:url('file://{ROOT}/fonts/Poppins-{n}.ttf')}}"
    for n, w, st in (("Regular", 400, "normal"), ("Medium", 500, "normal"), ("MediumItalic", 500, "italic"), ("Bold", 700, "normal")))

DEFAULTS = {
    "shopify": dict(tag="SHOPIFY EXPERTS", say="your sales", product="Your Product", price="$49.00", badge="Best Seller",
                    chip_label="Orders", chip_value="+38%"),
    "seo": dict(tag="SEO · AEO · GEO", say="your rankings", query="best shopify agency near me",
                keywords=["buy leather bags online", "handmade gifts store", "organic skincare shop"], score="89"),
}


def visual(s):
    e = html.escape
    if s["category"] == "shopify":
        v = SHOP_VIS
        for a, b in (("Your Product", s["product"]), ("$49.00", s["price"]), ("Best Seller", s["badge"]),
                     ("<small>Orders</small>", f"<small>{e(s['chip_label'])}</small>"), ("+38%", s["chip_value"])):
            v = v.replace(a, b if a.startswith("<") else e(b))
        return v
    v = SEO_VIS.replace("best shopify agency near me", e(s["query"])).replace(">89<", f">{e(str(s['score']))}<")
    for old, new in zip(DEFAULTS["seo"]["keywords"], s["keywords"]):
        v = v.replace(old, e(new))
    return v


def page(s):
    e = html.escape
    head = "".join("<div>" + re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', e(ln)) + "</div>" for ln in s["headline"].split("|"))
    sub = re.sub(r"\*(.+?)\*", r"<b>\1</b>", e(s["sub"]))
    lis = "".join(f'<div class="li">{CHECK}<span>{e(b)}</span></div>' for b in s["bullets"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}{CSS}</style></head><body>
<div class="dots d1"></div><div class="dots d2"></div><div class="wrap">
<div class="top"><img src="{LOGO}"><div class="tag">{e(s['tag'])}</div></div>
<h1 id="h">{head}</h1><div class="rule"></div>
<div class="cols"><div class="left"><div class="sub">{sub}</div><div class="card">{lis}</div></div><div class="right">{visual(s)}</div></div>
<div class="bar"><div class="cta">MESSAGE US<small>for a quote today</small></div><div class="sep"></div><div class="url">hivenexis.com</div><div class="say">Let's grow<br>{e(s['say'])} together!</div></div>
</div></body></html>"""


FIT = """()=>{const h=document.getElementById('h'),left=document.querySelector('.left'),cols=document.querySelector('.cols');let s=136;
const w=()=>Math.max(...[...h.children].map(d=>{const r=document.createRange();r.selectNodeContents(d);return r.getBoundingClientRect().width}));
const need=()=>[...left.children].reduce((a,c)=>a+c.getBoundingClientRect().height,0)+18;
const ok=()=>{h.style.fontSize=s+'px';return w()<=945&&need()<=cols.clientHeight};
while(!ok()&&s>64)s-=4;return {size:s,fits:ok(),width:Math.round(w()),need:Math.round(need()),room:cols.clientHeight}}"""


def render(spec, out):
    s = {**DEFAULTS[spec["category"]], **spec}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1080})
        pg.set_content(page(s))
        pg.evaluate("document.fonts.ready.then(()=>1)")
        info = pg.evaluate(FIT)
        pg.screenshot(path=str(out))
        b.close()
    return info


if __name__ == "__main__":
    import json, sys
    spec = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    info = render(spec, out)
    print(json.dumps({"out": str(out), **info}))
    if not info["fits"]:
        sys.exit("TEXT DOES NOT FIT: shorten the headline, sub or bullets and render again")
