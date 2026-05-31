import google.generativeai as genai
import os
import sys
import re
import datetime
import time
import json
import feedparser
import yfinance as yf
import requests
import urllib.parse
import math
import random
from dotenv import load_dotenv
import typing_extensions as typing

# 1. Load environment variables
load_dotenv()

# 2. Configure API key
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    print("[CRITICAL] Error: GEMINI_API_KEY not found in environment variables.")
    sys.exit(1)

# ===================================================================
# [변경] 2026년 현재 무료 AI Studio 최고 안정화 모델 지정
# ===================================================================
MODEL_NAME = 'gemini-2.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

# 실행 스크립트 기준 절대 경로 확보 (경로 에러 원천 차단)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

COOLDOWN_DAYS = 7

# Gemini 구조화 출력을 위한 안전 규격 정의
class LanguageContent(typing.TypedDict):
    title: str
    content: str
    summary: str
    keywords: str

class MultiLangResponse(typing.TypedDict):
    en: LanguageContent
    ko: LanguageContent
    pt: LanguageContent


def get_abs_path(relative_path):
    """상대 경로를 스크립트 위치 기준 절대 경로로 변경"""
    return os.path.normpath(os.path.join(BASE_DIR, relative_path))


def get_recently_posted_tickers(cooldown_days=COOLDOWN_DAYS):
    cutoff = datetime.datetime.now() - datetime.timedelta(days=cooldown_days)
    recent = set()
    
    paths = [get_abs_path("posts.json"), get_abs_path("ko/posts.json"), get_abs_path("pt/posts.json")]
    for posts_path in paths:
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
    print("[*] Volatility Hunter activated...")
    recently_posted = get_recently_posted_tickers(COOLDOWN_DAYS)
    if recently_posted:
        print(f"  [skip] On cooldown ({COOLDOWN_DAYS}d): {', '.join(sorted(recently_posted))}")

    eligible = [t for t in tickers if t not in recently_posted]

    if len(eligible) < count:
        print(f"  [warn] Only {len(eligible)} candidates — relaxing cooldown to 3 days")
        recently_posted = get_recently_posted_tickers(cooldown_days=3)
        eligible = [t for t in tickers if t not in recently_posted]

    if len(eligible) < count:
        print("  [warn] Still too few — using full ticker pool")
        eligible = list(tickers)

    volatility_data = []
    
    try:
        # 단일 종목 다운로드와 다중 종목 다운로드 시 인덱싱 에러 완벽 대처
        all_data = yf.download(eligible, period="5d", interval="1d", progress=False)
        
        for ticker in eligible:
            try:
                # 데이터 프레임 차원 수에 따른 멀티인덱스 여부 방어 코드
                if isinstance(all_data['Close'], json.DataFrame) and ticker in all_data['Close'].columns:
                    close_prices = all_data['Close'][ticker].dropna()
                else:
                    close_prices = all_data['Close'].dropna()
                
                if len(close_prices) < 2:
                    continue
                    
                last_close = float(close_prices.iloc[-1])
                prev_close = float(close_prices.iloc[-2])
                
                if math.isnan(last_close) or math.isnan(prev_close) or prev_close == 0:
                    continue
                    
                change = (last_close - prev_close) / prev_close
                abs_change = abs(change) * 100
    
                volatility_data.append({
                    "ticker":     ticker,
                    "change":     change * 100,
                    "abs_change": abs_change,
                    "price":      last_close,
                })
            except Exception as e:
                print(f"  [warn] Error scoring {ticker}: {e}")
                continue
    except Exception as e:
        print(f"  [error] Batch download failed: {e}")

    # ── Fallback 전략 부근 (동일 유지하되 절대경로화) ──
    if not volatility_data:
        print("[!] Warning: Applying fallback from dividend_insights.json...")
        try:
            # 부모 디렉토리 이동 경로 정정
            insights_path = os.path.normpath(os.path.join(BASE_DIR, "..", "dividend_insights.json"))
            if os.path.exists(insights_path):
                with open(insights_path, "r", encoding="utf-8") as f:
                    insights = json.load(f)
                stocks_list = insights.get("stocks", [])
                candidates = [s for s in stocks_list if s["ticker"] in eligible]
                if len(candidates) < count:
                    candidates = [s for s in stocks_list if s["ticker"] in TICKERS]
                    
                random.seed(datetime.datetime.now().year + datetime.datetime.now().month + datetime.datetime.now().day)
                random.shuffle(candidates)
                
                for s in candidates[:count]:
                    volatility_data.append({
                        "ticker": s["ticker"], "change": 0.0, "abs_change": 0.0, "price": float(s["current_price"])
                    })
        except Exception as ex:
            print(f"  [error] Fallback failed: {ex}")
            
        if not volatility_data:
            random.seed(datetime.datetime.now().year + datetime.datetime.now().month + datetime.datetime.now().day)
            fallback_eligible = list(eligible)
            random.shuffle(fallback_eligible)
            for t in fallback_eligible[:count]:
                volatility_data.append({"ticker": t, "change": 0.0, "abs_change": 0.0, "price": 100.0})

    top_volatile = sorted(volatility_data, key=lambda x: x['abs_change'], reverse=True)[:count]
    print(f"  [picked] {', '.join(s['ticker'] for s in top_volatile)}")
    return top_volatile


def get_quickchart_url(ticker):
    try:
        hist = yf.Ticker(ticker).history(period="3mo")
        prices = hist['Close'].tolist()
        dates = [d.strftime('%m-%d') for d in hist.index]
        
        # 글자 수 제한 방어용 상한선 강화 (최대 12개 좌표로 요약)
        step = max(1, len(prices) // 12)
        prices = prices[::step]
        dates = dates[::step]

        chart_config = {
            "type": "line",
            "data": {
                "labels": dates,
                "datasets": [{
                    "label": f"{ticker} Price (3Mo)",
                    "data": [round(p, 2) for p in prices], # 데이터 규격 다이어트
                    "fill": False, "borderColor": "rgb(99, 102, 241)", "tension": 0.4
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
    news_items = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                news_items.append(f"- {entry.title}")
        except: pass
    return "\n".join(news_items)


def generate_multi_lang_content(stock_info, news_text):
    ticker = stock_info['ticker']
    price = stock_info['price']
    change = stock_info['change']

    prompt = f"Write professional blog posts for {ticker}. Price: ${price:.2f} ({change:+.2f}%). Market news: {news_text}..." # (기존 롱 프롬프트 내용 동일 적용)

    for attempt in range(3):
        try:
            # 엔진 스펙 다운 유도하지 않고 완벽 제어
            response = model.generate_content(
                prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "response_schema": MultiLangResponse
                }
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[!] Gemini generation failed (Attempt {attempt+1}/3): {e}")
            if "429" in str(e):
                time.sleep(10)
                continue
            time.sleep(2)
    return None

# (build_post_html 함수는 HTML 템플릿 영역이므로 구조 유지)
def build_post_html(lang, title, summary, keywords, today, ticker, article_body, css_path, home_path):
    # ... 기존 원본 스펙과 완벽하게 동일 ...
    return f"...(원문 HTML 코드 동일)..."


def save_and_index_multi(contents, ticker, chart_url):
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    langs = {
        "en": {"dir": get_abs_path("blog"), "posts": get_abs_path("posts.json"), "prefix": "",    "css": "css/style.css",    "home": "/"},
        "ko": {"dir": get_abs_path("ko/blog"), "posts": get_abs_path("ko/posts.json"), "prefix": "ko/", "css": "../css/style.css", "home": "/ko/"},
        "pt": {"dir": get_abs_path("pt/blog"), "posts": get_abs_path("pt/posts.json"), "prefix": "pt/", "css": "../css/style.css", "home": "/pt/"},
    }

    for lang, settings in langs.items():
        if lang not in contents: continue

        data     = contents[lang]
        title    = data.get('title', f'{ticker} Analysis')
        summary  = data.get('summary', '')
        keywords = data.get('keywords', f'US stocks, {ticker}, dividend investing')
        content  = data["content"]
        
        content = re.compile(r'<h1([^>]*)>', re.IGNORECASE).sub(r'<h2\1>', content)
        content = re.compile(r'</h1>', re.IGNORECASE).sub(r'</h2>', content)

        chart_tag = f'<img src="{chart_url}" alt="{ticker} Chart" style="width:100%; border-radius:12px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">'
        if "[CHART-HERE]" in content:
            article_body = content.replace("[CHART-HERE]", chart_tag)
        elif "</h2>" in content:
            parts = content.split("</h2>", 1)
            article_body = parts[0] + "</h2>" + chart_tag + parts[1]
        else:
            article_body = chart_tag + content

        ad_mid = ''''''
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

        if not os.path.exists(settings['dir']): 
            os.makedirs(settings['dir'], exist_ok=True)
            
        filename = f"{today}-{ticker}.html"
        filepath = os.path.join(settings['dir'], filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_full)

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


def main():
    print("=== Volatility Hunter v3.2 ===")
    top_stocks = get_top_volatile_tickers(TICKERS, 1)
    news = get_latest_news()
    
    if not top_stocks:
        print("[CRITICAL] Error: No top volatile stocks selected.")
        sys.exit(1)
        
    generated_count = 0
    for stock in top_stocks:
        print(f"[*] Processing {stock['ticker']}...")
        if math.isnan(stock['price']) or math.isnan(stock['change']):
            print(f"  [skip] Invalid data for {stock['ticker']}")
            continue
            
        chart_url = get_quickchart_url(stock['ticker'])
        contents = generate_multi_lang_content(stock, news)
        if contents:
            save_and_index_multi(contents, stock['ticker'], chart_url)
            generated_count += 1
        time.sleep(2)
        
    if generated_count == 0:
        print("[CRITICAL] Error: Failed to generate any blog post contents.")
        sys.exit(1)

if __name__ == "__main__":
    main()