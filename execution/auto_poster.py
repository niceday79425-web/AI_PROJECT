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
        content = data.get('conte nt', '')
        chart_tag = f'<img src="{chart_url}" alt="{ticker} Chart" style="width:100%; border-radius:12px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">'
        
        if "[CHART-HERE]" in content:
            html_body = content.replace("[CHART-HERE]", chart_tag)
        else:
            # If placeholder is missing, insert chart after the first heading or at the top
            if "</h2>" in content:
                parts = content.split("</h2>", 1)
                html_body = parts[0] + "</h2>" + chart_tag + parts[1]
            else:
                html_body = chart_tag + content
        
        # AdSense Insertion (Middle of the article)
        ad_tag = '<div class="ad-in-article" style="min-height: 250px; background: #f9fafb; border: 1px dashed #ddd; margin: 25px 0; display: flex; align-items: center; justify-content: center; color: #999; font-size: 14px;">[ AdSense - In Article ]</div>'
        if "</p>" in html_body:
            p_tags = html_body.split("</p>")
            mid_point = len(p_tags) // 2
            if mid_point > 0:
                html_body = "</p>".join(p_tags[:mid_point]) + "</p>" + ad_tag + "</p>".join(p_tags[mid_point:])
            else:
                html_body += ad_tag
        else:
            html_body += ad_tag
        
        # Create directory if it doesn't exist
        if not os.path.exists(settings['dir']): os.makedirs(settings['dir'])
        
        filename = f"{today}-{ticker}.html"
        filepath = os.path.join(settings['dir'], filename)
        
        # Save HTML file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_body)
            
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
            json.dump(posts[:20], f, ensure_ascii=False, indent=4)
            
    print(f"[✓] {ticker} - English content generated with Korean & Portuguese translations")

def main():
    print("=== Volatility Hunter v2.0 ===")
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
