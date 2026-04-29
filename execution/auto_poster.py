import google.generativeai as genai
import os
import re
import datetime
import time
import json
import feedparser
import yfinance as yf
import requests
import urllib.parse
from dotenv import load_dotenv

# Auto Poster - English-First Content Generation
# Generates professional US stock market analysis in English (primary)
# with Korean and Portuguese translations saved to /ko/ and /pt/

# 1. Load environment variables
load_dotenv()

# 2. Configure API key
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    print("[!] Warning: API key not found.")

model = genai.GenerativeModel('gemini-2.5-flash') # Using stable flash model

# Extended ticker list (50+ stocks)
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "BRK-B", "JPM", "V", 
    "JNJ", "WMT", "PG", "MA", "UNH", "HD", "DIS", "PYPL", "BAC", "VZ", 
    "ADBE", "CMCSA", "NFLX", "KO", "PEP", "XOM", "CVX", "ABT", "T", "ABBV",
    "COST", "PFE", "MRK", "NKE", "LLY", "AVGO", "ORCL", "ACN", "DHR", "TMO",
    "MCD", "CSCO", "ABNB", "CRM", "AMD", "QCOM", "INTC", "TXN", "HON", "UPS",
    "BTC-USD", "ETH-USD", "SCHD", "JEPI", "VIST", "GEV"
]

RSS_URLS = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=" + ",".join(TICKERS[:10]) + "&region=US&lang=en-US",
    "https://www.investing.com/rss/news_25.rss"
]

COOLDOWN_DAYS = 7  # A ticker won't be re-posted within this many days

def get_recently_posted_tickers(cooldown_days=COOLDOWN_DAYS):
    """Read posts.json files and return set of tickers posted within cooldown_days."""
    cutoff = datetime.datetime.now() - datetime.timedelta(days=cooldown_days)
    recent = set()
    for posts_path in ["posts.json", "ko/posts.json", "pt/posts.json"]:
        if not os.path.exists(posts_path):
            continue
        try:
            with open(posts_path, "r", encoding="utf-8") as f:
                posts = json.load(f)
            for p in posts:
                try:
                    post_date = datetime.datetime.strptime(p.get("date", ""), "%Y-%m-%d")
                except ValueError:
                    continue
                if post_date >= cutoff:
                    fname = os.path.basename(p.get("link", ""))
                    if re.match(r'\d{4}-\d{2}-\d{2}-', fname):
                        ticker = os.path.splitext(fname)[0].split("-", 3)[-1]
                        recent.add(ticker)
        except Exception:
            continue
    return recent

def get_top_volatile_tickers(tickers, count=3):
    """Select highest-volatility tickers, skipping those posted recently (cooldown)."""
    print("[*] Volatility Hunter activated...")

    # --- Cooldown filter ---
    recently_posted = get_recently_posted_tickers(COOLDOWN_DAYS)
    if recently_posted:
        print(f"  [skip] On cooldown ({COOLDOWN_DAYS}d): {', '.join(sorted(recently_posted))}")

    eligible = [t for t in tickers if t not in recently_posted]

    # Relax to 3 days if too few candidates
    if len(eligible) < count:
        print(f"  [warn] Only {len(eligible)} candidates — relaxing cooldown to 3 days")
        recently_posted = get_recently_posted_tickers(cooldown_days=3)
        eligible = [t for t in tickers if t not in recently_posted]

    # Last resort: ignore cooldown entirely
    if len(eligible) < count:
        print("  [warn] Still too few — using full ticker pool")
        eligible = list(tickers)

    # --- Fetch & score volatility ---
    data = yf.download(eligible, period="5d", interval="1d", group_by='ticker', progress=False)

    volatility_data = []
    for ticker in eligible:
        try:
            ticker_data = data[ticker] if len(eligible) > 1 else data
            if len(ticker_data) < 2:
                continue
            last_close = float(ticker_data['Close'].iloc[-1])
            prev_close = float(ticker_data['Close'].iloc[-2])
            if prev_close == 0:
                continue
            change = (last_close - prev_close) / prev_close
            volatility_data.append({
                "ticker":     ticker,
                "change":     change * 100,
                "abs_change": abs(change) * 100,
                "price":      last_close,
            })
        except Exception:
            continue

    top_volatile = sorted(volatility_data, key=lambda x: x['abs_change'], reverse=True)[:count]
    print(f"  [picked] {', '.join(s['ticker'] for s in top_volatile)}")
    return top_volatile

def get_quickchart_url(ticker):
    """Generate 3-month stock price chart using QuickChart API"""
    # Fetch actual 3-month data from yfinance
    try:
        hist = yf.Ticker(ticker).history(period="3mo")
        prices = hist['Close'].tolist()
        dates = [d.strftime('%m-%d') for d in hist.index]
        
        # Reduce data points if too many
        step = max(1, len(prices) // 15)
        prices = prices[::step]
        dates = dates[::step]

        chart_config = {
            "type": "line",
            "data": {
                "labels": dates,
                "datasets": [{
                    "label": f"{ticker} Price (3Mo)",
                    "data": prices,
                    "fill": False,
                    "borderColor": "rgb(99, 102, 241)",
                    "tension": 0.4
                }]
            },
            "options": {
                "plugins": {
                    "legend": {"display": False},
                    "title": {"display": True, "text": f"{ticker} 3-Month Trend", "font": {"size": 20}}
                }
            }
        }
        
        encoded_config = urllib.parse.quote(json.dumps(chart_config))
        return f"https://quickchart.io/chart?c={encoded_config}&width=600&height=300"
    except:
        return ""

def get_latest_news():
    """Collect latest market news"""
    news_items = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                news_items.append(f"- {entry.title}")
        except: pass
    return "\n".join(news_items)

def generate_multi_lang_content(stock_info, news_text):
    """Generate English content first (primary), then Korean and Portuguese translations"""
    ticker = stock_info['ticker']
    price = stock_info['price']
    change = stock_info['change']

    # SEO title format rules per language
    # en: [Topic | US Stock Analysis · WiseAIWiseU]
    # ko: [주제 | 미국 주식 분석 · WiseAIWiseU]
    # pt: [Tópico | Análise de Ações dos EUA · WiseAIWiseU]

    prompt = f"""
    You are a professional US stock market analyst writing for a global audience.
    Write a highly engaging, SEO-optimized blog post about {ticker}.

    Current Price: ${price:.2f} ({change:+.2f}%)
    Related Market News: {news_text}

    IMPORTANT SEO TITLE RULES:
    - English title format: "[Compelling Topic about {ticker}] | US Stock Analysis · WiseAIWiseU"
      Example: "Apple (AAPL) Earnings Preview: What US Stock Investors Must Know | US Stock Analysis · WiseAIWiseU"
    - Korean title format: "[한국어 주제 ({ticker})] | 미국 주식 분석 · WiseAIWiseU"
      Example: "애플(AAPL) 실적 프리뷰: 미국 주식 투자자가 알아야 할 것 | 미국 주식 분석 · WiseAIWiseU"
    - Portuguese title format: "[Tópico em Português ({ticker})] | Análise de Ações dos EUA · WiseAIWiseU"
      Example: "Prévia de Resultados da Apple (AAPL): O Que Investidores em Ações dos EUA Devem Saber | Análise de Ações dos EUA · WiseAIWiseU"

    IMPORTANT DESCRIPTION RULES:
    - English summary: Must contain "US stock" or "US stocks". 1-2 sentences, click-worthy.
    - Korean summary: Must contain "미국 주식". 1-2 sentences in Korean.
    - Portuguese summary: Must contain "ações dos EUA". 1-2 sentences in Portuguese.

    Generate content in 3 languages:
    1. English (en) - Primary, professional, insightful
    2. Korean (ko) - Full Korean translation
    3. Portuguese (pt) - Full Portuguese translation

    Output MUST be valid JSON:
    {{
        "en": {{ "title": "...", "content": "HTML body", "summary": "...", "keywords": "US stocks, {ticker}, dividend investing, stock analysis" }},
        "ko": {{ "title": "...", "content": "HTML body", "summary": "...", "keywords": "미국 주식, {ticker}, 배당 투자, 주식 분석" }},
        "pt": {{ "title": "...", "content": "HTML body", "summary": "...", "keywords": "ações dos EUA, {ticker}, dividendos, análise de ações" }}
    }}

    Requirements:
    - Use semantic HTML (h2, p, ul, li, strong, em)
    - Include [CHART-HERE] placeholder where the stock chart should appear
    - Make English content professional and data-driven
    - Ensure translations maintain the same tone and information
    - Focus on investment insights, market trends, and actionable analysis
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        print(f"[!] Gemini generation failed: {e}")
        return None

def build_post_html(lang, title, summary, keywords, today, ticker, article_body, css_path, home_path):
    """Build premium HTML for a daily blog post."""
    change_color = "#10b981" if "+" in ticker else "#ef4444"

    ad_header = '''<div class="ad-slot" style="margin:1.5rem auto;max-width:860px;">
      <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
        data-ad-slot="XXXXXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins>
      <script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>
    </div>'''

    ad_mid = '''<div class="ad-in-article" style="margin:2rem 0;text-align:center;">
      <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
        data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
      <script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>
    </div>'''

    ad_footer = '''<div class="ad-slot" style="margin:2rem auto;max-width:860px;">
      <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
        data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
      <script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>
    </div>'''

    disclaimer_texts = {
        "en": ("<strong>All information is for educational purposes only and does not constitute investment advice.</strong><br>"
               "Dividends and yields may fluctuate and are not guaranteed. Past performance does not guarantee future results."),
        "ko": ("<strong>본 사이트의 모든 정보는 정보 제공 및 교육 목적이며, 투자 자문이 아닙니다.</strong><br>"
               "배당금 및 배당률은 변동될 수 있으며 보장되지 않습니다. 과거 성과가 미래 수익을 보장하지 않습니다."),
        "pt": ("<strong>Todas as informações são apenas para fins educacionais e não constituem aconselhamento de investimento.</strong><br>"
               "Dividendos e rendimentos podem flutuar e não são garantidos. Resultados passados não garantem resultados futuros."),
    }
    disclaimer_text = disclaimer_texts.get(lang, disclaimer_texts["en"])

    back_labels = {"en": "← Back to Blog", "ko": "← 블로그로 돌아가기", "pt": "← Voltar ao Blog"}
    back_label = back_labels.get(lang, "← Back to Blog")
    blog_path = f"/{'' if lang == 'en' else lang + '/'}blog.html"

    nav_ko_active   = 'active' if lang == 'ko' else ''
    nav_en_active   = 'active' if lang == 'en' else ''
    nav_pt_active   = 'active' if lang == 'pt' else ''

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{summary[:160]}">
  <meta name="keywords" content="{keywords}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{summary[:160]}">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="{css_path}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
  <style>
    /* ── Reading Progress Bar ── */
    #progress-bar {{
      position: fixed; top: 0; left: 0; height: 3px; width: 0%;
      background: linear-gradient(90deg, #6366f1, #8b5cf6);
      z-index: 9999; transition: width 0.1s linear;
    }}
    /* ── Post Styles ── */
    body {{ font-family: 'Inter', sans-serif; background: #f8f9fb; color: #1a1a2e; margin: 0; }}
    .post-hero {{
      background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
      color: #fff; padding: 4rem 1.5rem 3rem; text-align: center;
    }}
    .post-hero .ticker-badge {{
      display: inline-block; background: rgba(99,102,241,0.8);
      color: #fff; font-size: 0.8rem; font-weight: 700; letter-spacing: 2px;
      text-transform: uppercase; padding: 0.35rem 1rem; border-radius: 999px;
      margin-bottom: 1.2rem;
    }}
    .post-hero h1 {{
      font-size: clamp(1.6rem, 4vw, 2.6rem); font-weight: 800;
      line-height: 1.3; max-width: 820px; margin: 0 auto 1rem;
    }}
    .post-hero .meta {{
      font-size: 0.9rem; opacity: 0.7; display: flex;
      gap: 1.2rem; justify-content: center; flex-wrap: wrap;
    }}
    /* ── Article Layout ── */
    .post-content {{
      max-width: 860px; margin: 0 auto; padding: 2.5rem 1.5rem;
    }}
    .post-content h2 {{
      font-size: 1.45rem; font-weight: 700; color: #1e1b4b;
      margin: 2.5rem 0 1rem; border-left: 4px solid #6366f1;
      padding-left: 0.75rem;
    }}
    .post-content p {{ line-height: 1.85; color: #374151; margin-bottom: 1.2rem; }}
    .post-content ul, .post-content ol {{
      padding-left: 1.5rem; margin-bottom: 1.2rem;
    }}
    .post-content li {{ line-height: 1.8; color: #374151; margin-bottom: 0.4rem; }}
    .post-content strong {{ color: #1e1b4b; }}
    .post-content img {{
      width: 100%; border-radius: 14px; margin: 1.8rem 0;
      box-shadow: 0 8px 32px rgba(99,102,241,0.15);
    }}
    /* ── Key Metrics Card ── */
    .metrics-bar {{
      display: flex; gap: 1rem; flex-wrap: wrap;
      background: #fff; border: 1px solid #e5e7eb;
      border-radius: 14px; padding: 1.2rem 1.5rem;
      margin: 2rem 0; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }}
    .metric-item {{ flex: 1; min-width: 120px; text-align: center; }}
    .metric-item .label {{ font-size: 0.75rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px; }}
    .metric-item .value {{ font-size: 1.3rem; font-weight: 700; color: #1e1b4b; margin-top: 0.2rem; }}
    /* ── Disclaimer ── */
    .disclaimer {{
      margin-top: 3rem; padding: 1.25rem 1.5rem;
      background: #fff7f7; border-left: 4px solid #ef4444;
      border-radius: 10px; font-size: 0.83rem; color: #666; line-height: 1.7;
    }}
    .disclaimer .disc-title {{ font-weight: 700; color: #ef4444; margin-bottom: 0.5rem; }}
    /* ── Back Button ── */
    .back-btn {{
      display: inline-flex; align-items: center; gap: 0.4rem;
      color: #6366f1; font-weight: 600; text-decoration: none;
      font-size: 0.9rem; margin-bottom: 1.5rem;
      transition: opacity 0.2s;
    }}
    .back-btn:hover {{ opacity: 0.7; }}
  </style>
</head>
<body>
  <div id="progress-bar"></div>
  <div class="container">
    <header>
      <a href="{home_path}" class="logo">WiseAIWiseU</a>
      <nav class="lang-selector">
        <a href="/ko/blog.html" class="lang-link {nav_ko_active}">KO</a>
        <a href="/blog.html"    class="lang-link {nav_en_active}">EN</a>
        <a href="/pt/blog.html" class="lang-link {nav_pt_active}">PT</a>
      </nav>
    </header>

    {ad_header}

    <!-- Hero -->
    <section class="post-hero">
      <span class="ticker-badge">📈 {ticker} · US Stock Analysis</span>
      <h1>{title.split(" | ")[0] if " | " in title else title}</h1>
      <div class="meta">
        <span>📅 {today}</span>
        <span>🌐 WiseAIWiseU</span>
      </div>
    </section>

    <!-- Article -->
    <main class="post-content">
      <a href="{blog_path}" class="back-btn">{back_label}</a>

      {article_body}

      <div class="disclaimer">
        <div class="disc-title">⚠️ Legal Disclaimer / 법적 고지</div>
        <p>{disclaimer_text}</p>
      </div>
    </main>

    {ad_footer}

    <footer>
      <div class="footer-content">
        <p>&copy; 2026 WiseAIWiseU - Smart Dividend Investing</p>
        <p style="font-size:0.85rem;"><a href="{home_path}" style="color:#666;">{back_label}</a></p>
      </div>
    </footer>
  </div>

  <script>
    // Reading progress bar
    window.addEventListener('scroll', () => {{
      const el = document.getElementById('progress-bar');
      const total = document.body.scrollHeight - window.innerHeight;
      el.style.width = (window.scrollY / total * 100) + '%';
    }});
  </script>
</body>
</html>'''

def save_and_index_multi(contents, ticker, chart_url):
    """Generate English content first, then save translations to /ko/ and /pt/"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    langs = {
        "en": {"dir": "blog", "posts": "posts.json", "prefix": "",    "css": "css/style.css",    "home": "/"},
        "ko": {"dir": "ko/blog", "posts": "ko/posts.json", "prefix": "ko/", "css": "../css/style.css", "home": "/ko/"},
        "pt": {"dir": "pt/blog", "posts": "pt/posts.json", "prefix": "pt/", "css": "../css/style.css", "home": "/pt/"},
    }

    for lang, settings in langs.items():
        if lang not in contents: continue

        data     = contents[lang]
        title    = data.get('title', f'{ticker} Analysis')
        summary  = data.get('summary', '')
        keywords = data.get('keywords', f'US stocks, {ticker}, dividend investing')

        content   = data.get('content', '')
        chart_tag = (f'<img src="{chart_url}" alt="{ticker} 3-Month Price Chart" '
                     f'style="width:100%;border-radius:14px;margin:1.8rem 0;'
                     f'box-shadow:0 8px 32px rgba(99,102,241,0.15);">')

        if "[CHART-HERE]" in content:
            article_body = content.replace("[CHART-HERE]", chart_tag)
        elif "</h2>" in content:
            parts = content.split("</h2>", 1)
            article_body = parts[0] + "</h2>" + chart_tag + parts[1]
        else:
            article_body = chart_tag + content

        # Mid-article ad insertion
        ad_mid = '''<div class="ad-in-article" style="margin:2rem 0;text-align:center;">
          <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
            data-ad-slot="XXXXXXXXXX" data-ad-format="auto" data-full-width-responsive="true"></ins>
          <script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>
        </div>'''
        if "</p>" in article_body:
            p_tags   = article_body.split("</p>")
            mid      = len(p_tags) // 2
            article_body = "</p>".join(p_tags[:mid]) + "</p>" + ad_mid + "</p>".join(p_tags[mid:]) if mid > 0 else article_body + ad_mid
        else:
            article_body += ad_mid

        html_full = build_post_html(
            lang=lang, title=title, summary=summary, keywords=keywords,
            today=today, ticker=ticker, article_body=article_body,
            css_path=settings["css"], home_path=settings["home"]
        )

        if not os.path.exists(settings['dir']): os.makedirs(settings['dir'])
        filename = f"{today}-{ticker}.html"
        filepath = os.path.join(settings['dir'], filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_full)

        # Update posts.json
        posts_path = settings['posts']
        posts = []
        if os.path.exists(posts_path):
            with open(posts_path, "r", encoding="utf-8") as f:
                try: posts = json.load(f)
                except: posts = []

        link     = f"blog/{filename}"
        new_post = {"title": title, "date": today, "link": link, "summary": summary}
        posts    = [new_post] + [p for p in posts if p['link'] != new_post['link']]
        with open(posts_path, "w", encoding="utf-8") as f:
            json.dump(posts[:60], f, ensure_ascii=False, indent=4)

    print(f"[OK] {ticker} - posts saved (EN + KO + PT)")
        



def cleanup_old_posts(keep_days=30):
    """Delete dated blog HTML files older than keep_days and sync posts.json.
    Files without YYYY-MM-DD prefix (e.g. edu blog posts) are preserved.
    """
    print(f"[*] Cleaning up posts older than {keep_days} days...")
    cutoff = datetime.datetime.now() - datetime.timedelta(days=keep_days)

    blog_configs = [
        {"dir": "blog",    "posts": "posts.json",    "link_prefix": "blog/"},
        {"dir": "ko/blog", "posts": "ko/posts.json", "link_prefix": "blog/"},
        {"dir": "pt/blog", "posts": "pt/posts.json", "link_prefix": "blog/"},
    ]

    for cfg in blog_configs:
        blog_dir  = cfg["dir"]
        posts_path = cfg["posts"]
        link_prefix = cfg["link_prefix"]

        if not os.path.exists(blog_dir):
            continue

        deleted_links = set()

        # Scan HTML files — only delete those with YYYY-MM-DD prefix
        for fname in os.listdir(blog_dir):
            if not fname.endswith(".html"):
                continue

            # Extract date prefix (first 10 chars: YYYY-MM-DD)
            date_str = fname[:10]
            try:
                file_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                # No date prefix → edu blog post, skip
                continue

            if file_date < cutoff:
                filepath = os.path.join(blog_dir, fname)
                os.remove(filepath)
                deleted_links.add(link_prefix + fname)
                print(f"  [del] {filepath}")

        # Sync posts.json — remove entries pointing to deleted files
        if not os.path.exists(posts_path):
            continue

        with open(posts_path, "r", encoding="utf-8") as f:
            try:
                posts = json.load(f)
            except Exception:
                posts = []

        # Filter out deleted entries
        posts = [p for p in posts if p.get("link") not in deleted_links]

        # Re-sort by date desc, keep latest 60
        posts.sort(key=lambda x: x.get("date", ""), reverse=True)
        posts = posts[:60]

        with open(posts_path, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)

        print(f"  [sync] {posts_path}: {len(posts)} entries remaining")

    print("[OK] Cleanup complete.")




def main():
    print("=== Volatility Hunter v2.0 ===")
    cleanup_old_posts()  # Remove posts older than 30 days first
    top_stocks = get_top_volatile_tickers(TICKERS, 3)
    news = get_latest_news()
    
    for stock in top_stocks:
        print(f"[*] Processing {stock['ticker']}...")
        chart_url = get_quickchart_url(stock['ticker'])
        contents = generate_multi_lang_content(stock, news)
        if contents:
            save_and_index_multi(contents, stock['ticker'], chart_url)
        time.sleep(2)

if __name__ == "__main__":
    main()
