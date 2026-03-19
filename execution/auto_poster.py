import google.generativeai as genai
import os
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

def get_top_volatile_tickers(tickers, count=3):
    """Select stocks with highest volatility (absolute returns) over the last 5 days"""
    print("[*] Volatility Hunter activated...")
    volatility_data = []
    
    # Fetch all data at once (performance optimization)
    data = yf.download(tickers, period="5d", interval="1d", group_by='ticker', progress=False)
    
    for ticker in tickers:
        try:
            ticker_data = data[ticker] if len(tickers) > 1 else data
            if len(ticker_data) < 2: continue
            
            # Compare last close with previous close
            last_close = ticker_data['Close'].iloc[-1]
            prev_close = ticker_data['Close'].iloc[-2]
            
            change = (last_close - prev_close) / prev_close
            abs_change = abs(change)
            
            volatility_data.append({
                "ticker": ticker,
                "change": change * 100,
                "abs_change": abs_change * 100,
                "price": last_close
            })
        except:
            continue
    
    # Sort by volatility
    top_volatile = sorted(volatility_data, key=lambda x: x['abs_change'], reverse=True)[:count]
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
    
    prompt = f"""
    You are a professional US stock market analyst writing for a global audience.
    Write a highly engaging, SEO-optimized blog post about {ticker}.
    
    Current Price: ${price:.2f} ({change:+.2f}%)
    Related Market News: {news_text}
    
    IMPORTANT: English is the PRIMARY language. This is a US stock market blog targeting English-speaking investors.
    Korean (ko) and Portuguese (pt) are TRANSLATIONS for international readers.
    
    Generate content in 3 languages with this priority:
    1. English (en) - Primary, professional, insightful, SEO-optimized
    2. Korean (ko) - Translation of English content
    3. Portuguese (pt) - Translation of English content
    
    Output MUST be valid JSON with this exact structure:
    {{
        "en": {{ "title": "Engaging English Title", "content": "HTML body", "summary": "Brief summary" }},
        "ko": {{ "title": "한국어 제목", "content": "HTML body", "summary": "요약" }},
        "pt": {{ "title": "Título em Português", "content": "HTML body", "summary": "Resumo" }}
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

def save_and_index_multi(contents, ticker, chart_url):
    """Generate English content first, then save translations to /ko/ and /pt/"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # English is the primary language (root directory)
    # Korean and Portuguese are translations (in subdirectories)
    langs = {
        "en": {"dir": "blog", "posts": "posts.json", "prefix": ""},
        "ko": {"dir": "ko/blog", "posts": "ko/posts.json", "prefix": "ko/"},
        "pt": {"dir": "pt/blog", "posts": "pt/posts.json", "prefix": "pt/"}
    }
     
     
    for lang, settings in langs.items():
        if lang not in contents: continue
        
        data = contents[lang]
        title = data.get('title', f'{ticker} Analysis')
        summary = data.get('summary', '')

        # HTML content refinement
        content = data.get('content', '')
        chart_tag = f'<img src="{chart_url}" alt="{ticker} Chart" style="width:100%; border-radius:12px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">'
        
        if "[CHART-HERE]" in content:
            article_body = content.replace("[CHART-HERE]", chart_tag)
        else:
            # If placeholder is missing, insert chart after the first heading or at the top
            if "</h2>" in content:
                parts = content.split("</h2>", 1)
                article_body = parts[0] + "</h2>" + chart_tag + parts[1]
            else:
                article_body = chart_tag + content
        
        # AdSense Insertion (Middle of the article)
        ad_tag = '''
        <div class="ad-in-article" style="margin: 30px 0; text-align: center;">
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
                 data-ad-slot="XXXXXXXXXX"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>
                 (adsbygoogle = window.adsbygoogle || []).push({});
            </script>
        </div>
        '''
        
        if "</p>" in article_body:
            p_tags = article_body.split("</p>")
            mid_point = len(p_tags) // 2
            if mid_point > 0:
                article_body = "</p>".join(p_tags[:mid_point]) + "</p>" + ad_tag + "</p>".join(p_tags[mid_point:])
            else:
                article_body += ad_tag
        else:
            article_body += ad_tag
        
        # Legal Disclaimer (Korean + English)
        legal_disclaimer = '''
        <div class="legal-disclaimer" style="margin-top: 3rem; padding: 1.5rem; background: #f9fafb; border-left: 4px solid #ef4444; border-radius: 8px;">
            <h4 style="margin-bottom: 0.5rem; font-size: 0.9rem; color: #ef4444;">⚠️ Legal Disclaimer / 법적 고지</h4>
            <p style="font-size: 0.85rem; line-height: 1.6; color: #666;">
                <strong>본 사이트의 모든 정보는 정보 제공 및 교육 목적이며, 투자 자문 또는 투자 권유가 아닙니다.</strong><br>
                배당금 및 배당률은 변동될 수 있으며 보장되지 않습니다.<br>
                과거의 성과가 미래의 수익을 보장하지 않습니다.<br>
                본 사이트의 정보를 이용한 투자 결과에 대해 책임을 지지 않습니다.<br><br>
                <em>All information on this site is for informational and educational purposes only and does not constitute investment advice or recommendations. Dividends and dividend yields may fluctuate and are not guaranteed. Past performance does not guarantee future returns. We are not responsible for investment decisions made based on information from this site.</em>
            </p>
        </div>
        '''
        
        # Complete HTML structure
        html_full = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | WiseAIWiseU</title>
    <meta name="description" content="{summary[:150]}">
    <link rel="stylesheet" href="{'../css/style.css' if lang != 'en' else 'css/style.css'}">
    
    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
     crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        <header>
            <a href="{'/' if lang == 'en' else '/' + lang + '/'}" class="logo">WiseAIWiseU</a>
            <nav class="lang-selector">
                <a href="/ko/blog.html" class="lang-link {'active' if lang == 'ko' else ''}">KO</a>
                <a href="/blog.html" class="lang-link {'active' if lang == 'en' else ''}">EN</a>
                <a href="/pt/blog.html" class="lang-link {'active' if lang == 'pt' else ''}">PT</a>
            </nav>
        </header>

        <!-- Google AdSense - Header Banner -->
        <div class="ad-slot" style="margin: 2rem auto; max-width: 800px;">
             <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
                data-ad-slot="XXXXXXXXXX" data-ad-format="horizontal" data-full-width-responsive="true"></ins>
            <script>
                (adsbygoogle = window.adsbygoogle || []).push({{}});
            </script>
        </div>

        
        <article style="max-width: 800px; margin: 2rem auto; padding: 0 1rem;">
            <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">{title}</h1>
            <p style="color: #666; margin-bottom: 2rem;">📅 {today}</p>
            
            {article_body}
            
            {legal_disclaimer}
        </article>
        
        <!-- Google AdSense - Footer -->
        <div class="ad-slot" style="margin: 2rem auto; max-width: 800px;">
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
                 data-ad-slot="XXXXXXXXXX"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>
                 (adsbygoogle = window.adsbygoogle || []).push({{}});
            </script>
        </div>
        
        <footer>
            <div class="footer-content">
                <p>&copy; 2026 WiseAIWiseU - Smart Dividend Investing</p>
                <p style="font-size: 0.85rem;"><a href="/" style="color: #666;">← Back to Home</a></p>
            </div>
        </footer>
    </div>
</body>
</html>
'''
        
        # Create directory if it doesn't exist
        if not os.path.exists(settings['dir']): os.makedirs(settings['dir'])
        
        filename = f"{today}-{ticker}.html"
        filepath = os.path.join(settings['dir'], filename)
        
        # Save HTML file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_full)
            
        # Update posts.json
        posts_path = settings['posts']
        posts = []
        if os.path.exists(posts_path):
            with open(posts_path, "r", encoding="utf-8") as f:
                try: posts = json.load(f)
                except: posts = []
        
        # Set link path (relative to root)
        link = f"blog/{filename}" # 각 언어 폴더 내부의 posts.json 입장에서는 blog/filename 임
        
        new_post = {"title": title, "date": today, "link": link, "summary": summary}
        posts = [new_post] + [p for p in posts if p['link'] != new_post['link']]
        
        with open(posts_path, "w", encoding="utf-8") as f:
            json.dump(posts[:60], f, ensure_ascii=False, indent=4)
            
    print(f"[✓] {ticker} - English content generated with Korean & Portuguese translations")

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
