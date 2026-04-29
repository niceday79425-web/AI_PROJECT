"""
Retroactively apply the new premium design to all existing daily blog posts.
Preserves: article body content, title, date, ticker.
Replaces: full HTML shell (head, header, hero, footer, styles).
"""
import os
import re

ROOT = r"d:\AI_PROJECT"

BLOG_DIRS = [
    {"dir": "blog",    "lang": "en", "css": "css/style.css",    "home": "/"},
    {"dir": "ko/blog", "lang": "ko", "css": "../css/style.css", "home": "/ko/"},
    {"dir": "pt/blog", "lang": "pt", "css": "../css/style.css", "home": "/pt/"},
]

BACK_LABELS  = {"en": "← Back to Blog", "ko": "← 블로그로 돌아가기", "pt": "← Voltar ao Blog"}
BLOG_PATHS   = {"en": "/blog.html",      "ko": "/ko/blog.html",         "pt": "/pt/blog.html"}
DISCLAIMERS  = {
    "en": ("<strong>All information is for educational purposes only and does not constitute investment advice.</strong><br>"
           "Dividends and yields may fluctuate and are not guaranteed. Past performance does not guarantee future results."),
    "ko": ("<strong>본 사이트의 모든 정보는 정보 제공 및 교육 목적이며, 투자 자문이 아닙니다.</strong><br>"
           "배당금 및 배당률은 변동될 수 있으며 보장되지 않습니다. 과거 성과가 미래 수익을 보장하지 않습니다."),
    "pt": ("<strong>Todas as informações são apenas para fins educacionais e não constituem aconselhamento de investimento.</strong><br>"
           "Dividendos e rendimentos podem flutuar e não são garantidos. Resultados passados não garantem resultados futuros."),
}

def extract_meta(content, attr, name):
    """Extract meta tag content value."""
    pat = rf'<meta\s+{attr}="{re.escape(name)}"\s+content="(.*?)"'
    m = re.search(pat, content, re.I | re.S)
    if not m:
        pat2 = rf'<meta\s+content="(.*?)"\s+{attr}="{re.escape(name)}"'
        m = re.search(pat2, content, re.I | re.S)
    return m.group(1).strip() if m else ""

def extract_title_tag(content):
    m = re.search(r'<title>(.*?)</title>', content, re.I | re.S)
    return m.group(1).strip() if m else ""

def extract_date(content, filename):
    """Try to get date from meta or filename prefix."""
    m = re.search(r'📅\s*(\d{4}-\d{2}-\d{2})', content)
    if m: return m.group(1)
    if re.match(r'\d{4}-\d{2}-\d{2}', filename):
        return filename[:10]
    return "2026-01-01"

def extract_ticker(filename):
    """Extract ticker from filename like 2026-04-29-AAPL.html"""
    base = os.path.splitext(filename)[0]
    parts = base.split("-")
    if len(parts) >= 4:
        return parts[-1]
    return "STOCK"

def extract_article_body(content):
    """Extract body content between <article ...> and </article> or <main ...> and </main>."""
    # Try <article>
    m = re.search(r'<article[^>]*>(.*?)</article>', content, re.I | re.S)
    if m:
        body = m.group(1)
        # Strip h1 + date paragraph at top (we'll re-render them in hero)
        body = re.sub(r'<h1[^>]*>.*?</h1>', '', body, count=1, flags=re.I | re.S)
        body = re.sub(r'<p[^>]*>📅.*?</p>', '', body, count=1, flags=re.I | re.S)
        # Strip legal disclaimer at bottom (we re-add it)
        body = re.sub(r'<div[^>]*class="legal-disclaimer"[^>]*>.*?</div>', '', body, flags=re.I | re.S)
        body = re.sub(r'<div[^>]*class="disclaimer"[^>]*>.*?</div>', '', body, flags=re.I | re.S)
        # Strip mid-article ad blocks
        body = re.sub(r'<div[^>]*class="ad-in-article"[^>]*>.*?</div>', '', body, flags=re.I | re.S)
        return body.strip()
    # Fallback: everything between <body> and </body> minus header/footer
    m = re.search(r'<body[^>]*>(.*?)</body>', content, re.I | re.S)
    if m:
        return m.group(1).strip()
    return ""

def rebuild_html(lang, title, description, keywords, date, ticker, body, css, home):
    nav_ko = 'active' if lang == 'ko' else ''
    nav_en = 'active' if lang == 'en' else ''
    nav_pt = 'active' if lang == 'pt' else ''
    back   = BACK_LABELS[lang]
    blog   = BLOG_PATHS[lang]
    disc   = DISCLAIMERS[lang]
    hero_title = title.split(" | ")[0] if " | " in title else title

    # Mid-article ad
    ad_mid = '''<div class="ad-in-article" style="margin:2rem 0;text-align:center;">
      <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
        data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
      <script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>
    </div>'''
    if "</p>" in body:
        parts = body.split("</p>")
        mid   = max(len(parts) // 2, 1)
        body  = "</p>".join(parts[:mid]) + "</p>" + ad_mid + "</p>".join(parts[mid:])

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description[:160]}">
  <meta name="keywords" content="{keywords}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description[:160]}">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="{css}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
  <style>
    #progress-bar {{
      position:fixed;top:0;left:0;height:3px;width:0%;
      background:linear-gradient(90deg,#6366f1,#8b5cf6);z-index:9999;transition:width .1s linear;
    }}
    body{{font-family:'Inter',sans-serif;background:#f8f9fb;color:#1a1a2e;margin:0;}}
    .post-hero{{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:#fff;padding:4rem 1.5rem 3rem;text-align:center;}}
    .post-hero .ticker-badge{{display:inline-block;background:rgba(99,102,241,.8);color:#fff;font-size:.8rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:.35rem 1rem;border-radius:999px;margin-bottom:1.2rem;}}
    .post-hero h1{{font-size:clamp(1.6rem,4vw,2.6rem);font-weight:800;line-height:1.3;max-width:820px;margin:0 auto 1rem;}}
    .post-hero .meta{{font-size:.9rem;opacity:.7;display:flex;gap:1.2rem;justify-content:center;flex-wrap:wrap;}}
    .post-content{{max-width:860px;margin:0 auto;padding:2.5rem 1.5rem;}}
    .post-content h2{{font-size:1.45rem;font-weight:700;color:#1e1b4b;margin:2.5rem 0 1rem;border-left:4px solid #6366f1;padding-left:.75rem;}}
    .post-content p{{line-height:1.85;color:#374151;margin-bottom:1.2rem;}}
    .post-content ul,.post-content ol{{padding-left:1.5rem;margin-bottom:1.2rem;}}
    .post-content li{{line-height:1.8;color:#374151;margin-bottom:.4rem;}}
    .post-content strong{{color:#1e1b4b;}}
    .post-content img{{width:100%;border-radius:14px;margin:1.8rem 0;box-shadow:0 8px 32px rgba(99,102,241,.15);}}
    .disclaimer{{margin-top:3rem;padding:1.25rem 1.5rem;background:#fff7f7;border-left:4px solid #ef4444;border-radius:10px;font-size:.83rem;color:#666;line-height:1.7;}}
    .disclaimer .disc-title{{font-weight:700;color:#ef4444;margin-bottom:.5rem;}}
    .back-btn{{display:inline-flex;align-items:center;gap:.4rem;color:#6366f1;font-weight:600;text-decoration:none;font-size:.9rem;margin-bottom:1.5rem;transition:opacity .2s;}}
    .back-btn:hover{{opacity:.7;}}
  </style>
</head>
<body>
  <div id="progress-bar"></div>
  <div class="container">
    <header>
      <a href="{home}" class="logo">WiseAIWiseU</a>
      <nav class="lang-selector">
        <a href="/ko/blog.html" class="lang-link {nav_ko}">KO</a>
        <a href="/blog.html"    class="lang-link {nav_en}">EN</a>
        <a href="/pt/blog.html" class="lang-link {nav_pt}">PT</a>
      </nav>
    </header>
    <div class="ad-slot" style="margin:1.5rem auto;max-width:860px;">
      <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
        data-ad-slot="XXXXXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins>
      <script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script>
    </div>
    <section class="post-hero">
      <span class="ticker-badge">📈 {ticker} · US Stock Analysis</span>
      <h1>{hero_title}</h1>
      <div class="meta"><span>📅 {date}</span><span>🌐 WiseAIWiseU</span></div>
    </section>
    <main class="post-content">
      <a href="{blog}" class="back-btn">{back}</a>
      {body}
      <div class="disclaimer">
        <div class="disc-title">⚠️ Legal Disclaimer / 법적 고지</div>
        <p>{disc}</p>
      </div>
    </main>
    <div class="ad-slot" style="margin:2rem auto;max-width:860px;">
      <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
        data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
      <script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script>
    </div>
    <footer>
      <div class="footer-content">
        <p>&copy; 2026 WiseAIWiseU - Smart Dividend Investing</p>
        <p style="font-size:.85rem;"><a href="{home}" style="color:#666;">{back}</a></p>
      </div>
    </footer>
  </div>
  <script>
    window.addEventListener('scroll',()=>{{
      const el=document.getElementById('progress-bar');
      const total=document.body.scrollHeight-window.innerHeight;
      el.style.width=(window.scrollY/total*100)+'%';
    }});
  </script>
</body>
</html>'''

updated = 0
for cfg in BLOG_DIRS:
    blog_dir = os.path.join(ROOT, cfg["dir"])
    lang     = cfg["lang"]
    if not os.path.exists(blog_dir):
        continue
    for fname in os.listdir(blog_dir):
        if not fname.endswith(".html"):
            continue
        if not re.match(r'\d{4}-\d{2}-\d{2}-', fname):
            continue  # skip edu posts

        fpath = os.path.join(blog_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        title       = extract_title_tag(content)
        description = extract_meta(content, "name", "description")
        keywords    = extract_meta(content, "name", "keywords")
        date        = extract_date(content, fname)
        ticker      = extract_ticker(fname)
        body        = extract_article_body(content)

        if not title:
            title = f"{ticker} Analysis | US Stock Analysis · WiseAIWiseU"
        if not description:
            description = f"In-depth US stock analysis of {ticker}. Expert insights for dividend investors."
        if not keywords:
            keywords = f"US stocks, {ticker}, dividend investing, stock analysis"

        new_html = rebuild_html(lang, title, description, keywords, date, ticker, body,
                                cfg["css"], cfg["home"])
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_html)
        updated += 1
        print(f"[OK] {cfg['dir']}/{fname}")

print(f"\nDone: {updated} posts redesigned.")
