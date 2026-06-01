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
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

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
                import pandas as pd
                if isinstance(all_data['Close'], pd.DataFrame) and ticker in all_data['Close'].columns:
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
            insights_path = os.path.normpath(os.path.join(BASE_DIR, "dividend_insights.json"))
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

    Output MUST be valid JSON matching this exact schema:
    {{
        "en": {{ "title": "...", "content": "HTML body", "summary": "...", "keywords": "US stocks, {ticker}, dividend investing, stock analysis" }},
        "ko": {{ "title": "...", "content": "HTML body", "summary": "...", "keywords": "미국 주식, {ticker}, 배당 투자, 주식 분석" }},
        "pt": {{ "title": "...", "content": "HTML body", "summary": "...", "keywords": "ações dos EUA, {ticker}, dividendos, análise de ações" }}
    }}

    Requirements:
    - Minimum 600 words per language (quality over quantity, keep it concise to prevent JSON truncation)
    - Use semantic HTML (h2, p, ul, li, strong, em)
    - Include [CHART-HERE] placeholder where the stock chart should appear
    - REQUIRED SECTIONS (use <h2> for each):
      1. Executive Summary (3-sentence overview with current price data)
      2. Recent Performance & Key Events (with specific numbers/percentages)
      3. Technical Analysis (support/resistance levels, RSI, momentum)
      4. Dividend Investor Perspective (dividend history, payout ratio, sustainability)
      5. Risk Factors (minimum 3 specific risks with explanation)
      6. Conclusion & Investor Action Points
      7. FAQ (3 Q&A pairs relevant to this stock)
    - Make English content professional and data-driven with specific numbers
    - Ensure translations are natural, not just word-for-word
    - Focus on actionable insights that help investors make informed decisions
    - Add internal links: mention US Dividend Stock Search at /list and US Stock Compound Interest at /calculator
    """

    models_to_try = [
        MODEL_NAME, 
        'gemini-3.5-flash', 
        'gemini-flash-latest', 
        'gemini-2.5-flash-lite', 
        'gemini-3.1-flash-lite', 
        'gemini-flash-lite-latest'
    ]
    for model_name in models_to_try:
        print(f"[*] Attempting content generation with {model_name}...")
        try:
            current_model = genai.GenerativeModel(model_name)
        except Exception as init_err:
            print(f"[!] Failed to initialize model {model_name}: {init_err}")
            continue

        for attempt in range(3):
            try:
                response = current_model.generate_content(
                    prompt,
                    generation_config={
                        "response_mime_type": "application/json",
                        "max_output_tokens": 8192
                    }
                )
                return json.loads(response.text)
            except Exception as e:
                err_str = str(e)
                print(f"[!] Gemini generation failed with {model_name} (Attempt {attempt+1}/3): {err_str}")
                if "429" in err_str:
                    if "PerDay" in err_str or "limit: 0" in err_str:
                        print("  [Daily Quota Exceeded] Daily quota exhausted or model disabled. Switching to fallback model immediately...")
                        break
                    # 무료 티어 분당 호출량 한도 리셋을 위해 35초 대기
                    print("  [429 Quota] Rate limit hit. Sleeping 35 seconds to reset...")
                    time.sleep(35)
                else:
                    time.sleep(2)
        print(f"[!] All attempts with {model_name} failed. Trying fallback model...")
    return None

def build_post_html(lang, title, summary, keywords, today, ticker, article_body, css_path, home_path):
    """Build premium HTML for a daily blog post."""
    change_color = "#10b981" if "+" in ticker else "#ef4444"

    ad_header = ''''''
    ad_mid = ''''''
    ad_footer = ''''''

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
    blog_path = f"/{'' if lang == 'en' else lang + '/'}blog"

    nav_ko_active   = 'active' if lang == 'ko' else ''
    nav_en_active   = 'active' if lang == 'en' else ''
    nav_pt_active   = 'active' if lang == 'pt' else ''

    # 1. Optimize Title for SEO (target: 50-60 chars)
    brand = " | WiseAIWiseU"
    clean_t = title.strip()
    suffixes_to_clean = [
        " | U.S. Stock Analysis · WiseAIWiseU",
        " | U.S. Stock Analysis - WiseAIWiseU",
        " | U.S. Stock Analysis | WiseAIWiseU",
        " | U.S. Stock Analysis",
        " · WiseAIWiseU",
        " - WiseAIWiseU",
        " | WiseAIWiseU",
        " | WiseAI",
        " | WiseU",
        " | 미국 주식 분석 · WiseAIWiseU",
        " | 미국 주식 분석 - WiseAIWiseU",
        " | 미국 주식 분석",
        " | Analise de Ações dos EUA · WiseAIWiseU",
        " | Analise de Ações dos EUA",
        " | Análise de Ações dos EUA · WiseAIWiseU"
    ]
    for suffix in suffixes_to_clean:
        if clean_t.endswith(suffix):
            clean_t = clean_t[:-len(suffix)].strip()
            
    max_clean_len = 60 - len(brand)
    if len(clean_t) > max_clean_len:
        clean_t = clean_t[:max_clean_len - 3] + "..."
    optimized_title = clean_t + brand
    
    # 2. Optimize Description for SEO (target: 130-150 chars)
    clean_desc = summary.strip()
    if len(clean_desc) < 120:
        if lang == "en":
            padding = " Read the full in-depth U.S. stock market and dividend analysis on WiseAIWiseU."
        elif lang == "pt":
            padding = " Leia a análise detalhada completa do mercado de ações e dividendos no WiseAIWiseU."
        else:
            padding = " WiseAIWiseU에서 제공하는 미국 주식 및 배당주 시장의 실시간 분석과 전망을 확인해 보세요."
        clean_desc = clean_desc + padding
        
    if len(clean_desc) > 150:
        clean_desc = clean_desc[:147] + "..."
    optimized_desc = clean_desc

    # Generate SEO canonical & alternate tags
    post_slug = f"{today}-{ticker}"
    canonical_url = f"https://wiseaiwiseu.com/{'' if lang == 'en' else lang + '/'}blog/{post_slug}"
    alt_en = f"https://wiseaiwiseu.com/blog/{post_slug}"
    alt_ko = f"https://wiseaiwiseu.com/ko/blog/{post_slug}"
    alt_pt = f"https://wiseaiwiseu.com/pt/blog/{post_slug}"

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{optimized_title}</title>
  <meta name="description" content="{optimized_desc}">
  <meta name="keywords" content="{keywords}">
  <meta property="og:title" content="{optimized_title}">
  <meta property="og:description" content="{optimized_desc}">
  <meta property="og:type" content="article">
  <link rel="canonical" href="{canonical_url}" />
  <link rel="alternate" hreflang="en" href="{alt_en}" />
  <link rel="alternate" hreflang="ko" href="{alt_ko}" />
  <link rel="alternate" hreflang="pt" href="{alt_pt}" />
  <link rel="alternate" hreflang="x-default" href="{alt_en}" />
  <link rel="stylesheet" href="{css_path}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    /* ── Reading Progress Bar ── */
    #progress-bar {{
      position: fixed; top: 0; left: 0; height: 3px; width: 0%;
      background: linear-gradient(90deg, #6366f1, #2dd4bf);
      z-index: 9999; transition: width 0.1s linear;
    }}
    /* ── Post Styles ── */
    body {{ font-family: 'Inter', sans-serif; background: var(--bg-color); color: var(--text-primary); margin: 0; }}
    
    .post-hero {{
      padding: 6rem 1.5rem 5rem; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05);
      background: radial-gradient(circle at top, rgba(99,102,241,0.05) 0%, transparent 70%);
    }}
    .post-hero .ticker-badge {{
      display: inline-block; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
      color: #60a5fa; font-size: 0.8rem; font-weight: 700; letter-spacing: 1.5px;
      text-transform: uppercase; padding: 0.5rem 1.4rem; border-radius: 999px;
      margin-bottom: 2rem; backdrop-filter: blur(10px);
    }}
    .post-hero h1 {{
      font-size: clamp(2.2rem, 6vw, 3.5rem); font-weight: 800; letter-spacing: -1.5px;
      line-height: 1.1; max-width: 900px; margin: 0 auto 2rem; color: var(--text-primary);
    }}
    .post-hero .meta {{
      font-size: 0.95rem; color: var(--text-secondary); display: flex;
      gap: 2rem; justify-content: center; flex-wrap: wrap; margin-top: 1rem;
      opacity: 0.8;
    }}
    
    /* ── Article Layout ── */
    .post-content {{
      max-width: 760px; margin: 0 auto; padding: 4rem 1.5rem;
    }}
    .post-content h2 {{
      font-size: 1.85rem; font-weight: 700; color: var(--text-primary);
      margin: 4rem 0 1.5rem; letter-spacing: -0.5px;
      display: flex; align-items: center; gap: 0.75rem;
    }}
    .post-content h2::before {{
      content: ''; display: inline-block; width: 4px; height: 1.5rem;
      background: var(--primary-gradient); border-radius: 2px;
    }}
    .post-content h3 {{ 
      font-size: 1.4rem; font-weight: 600; color: var(--text-primary); 
      margin: 3rem 0 1.25rem; letter-spacing: -0.3px;
    }}
    .post-content p {{ 
      line-height: 1.9; color: var(--text-secondary); 
      margin-bottom: 1.75rem; font-size: 1.125rem; font-weight: 400; 
    }}
    .post-content ul, .post-content ol {{
      padding-left: 1.5rem; margin-bottom: 1.75rem;
    }}
    .post-content li {{ 
      line-height: 1.9; color: var(--text-secondary); 
      margin-bottom: 0.75rem; font-size: 1.125rem; 
    }}
    .post-content strong {{ color: var(--text-primary); font-weight: 600; }}
    .post-content img {{
      width: 100%; border-radius: 16px; margin: 2.5rem 0;
      border: 1px solid rgba(255,255,255,0.05);
      box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }}
    
    /* ── Key Point ── */
    .key-point {{ 
      background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
      border-left: 4px solid #6366f1; 
      border-radius: 12px; padding: 2rem; margin: 3rem 0; 
      color: var(--text-primary); font-size: 1.1rem; 
      backdrop-filter: blur(5px);
    }}
    .key-point strong {{ color: #60a5fa; }}
    
    /* ── Key Metrics Card ── */
    .metrics-bar {{
      display: flex; gap: 1.5rem; flex-wrap: wrap;
      background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);
      border-radius: 16px; padding: 2rem; margin: 3rem 0;
      backdrop-filter: blur(10px);
    }}
    .metric-item {{ flex: 1; min-width: 140px; text-align: center; }}
    .metric-item .label {{ font-size: 0.85rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.75rem; display: block; opacity: 0.8; }}
    .metric-item .value {{ font-size: 1.75rem; font-weight: 800; color: var(--text-primary); }}
    
    /* ── Disclaimer ── */
    .disclaimer {{
      margin-top: 5rem; padding: 2rem;
      background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.05);
      border-radius: 16px; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.8;
    }}
    .disclaimer .disc-title {{ font-weight: 700; color: var(--text-primary); margin-bottom: 0.75rem; display: block; }}
    
    /* ── Back Button ── */
    .back-btn {{
      display: inline-flex; align-items: center; gap: 0.75rem;
      color: var(--text-secondary); font-weight: 600; text-decoration: none;
      font-size: 1rem; margin-bottom: 3rem; transition: all 0.3s;
      padding: 0.5rem 1rem; border-radius: 8px; background: rgba(255,255,255,0.03);
    }}
    .back-btn:hover {{ color: var(--text-primary); background: rgba(255,255,255,0.08); transform: translateX(-5px); }}
  </style>
</head>
<body>
  <div id="progress-bar"></div>
  <div class="container">
    <header>
      <a href="{home_path}" class="logo">WiseAIWiseU</a>
      <nav class="lang-selector">
        <a href="/ko/blog" class="lang-link {nav_ko_active}">KO</a>
        <a href="/blog"    class="lang-link {nav_en_active}">EN</a>
        <a href="/pt/blog" class="lang-link {nav_pt_active}">PT</a>
      </nav>
    </header>

    {ad_header}

    <section class="post-hero">
      <span class="ticker-badge">📈 {ticker} · US Stock Analysis</span>
      <h1>{"미국 주식 인사이트" if lang == "ko" else ("Insights de Ações dos EUA" if lang == "pt" else "US Stock Insights")}: {title.split(" | ")[0] if " | " in title else title}</h1>
      <div class="meta">
        <span>📅 {today}</span>
        <span>🌐 WiseAIWiseU</span>
      </div>
    </section>

    <main class="post-content">
      <a href="{blog_path}" class="back-btn">{back_label}</a>

      <div style="display:flex;align-items:center;gap:1rem;background:#f8f9fb;border:1px solid #e5e7eb;border-radius:12px;padding:1rem 1.2rem;margin-bottom:2rem;">
        <div style="width:48px;height:48px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
          <span style="color:#fff;font-weight:700;font-size:1.1rem;">W</span>
        </div>
        <div>
          <strong style="display:block;color:#1e1b4b;font-size:0.95rem;">WiseAIWiseU Research Team</strong>
          <span style="font-size:0.8rem;color:#6b7280;">Data-driven dividend &amp; market analysis | Published: {today} | Educational purposes only</span>
        </div>
      </div>

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
        content  = data.get("content", "")
        
        if not content:
            print(f"  [warn] Missing 'content' for lang={lang}. Keys present: {list(data.keys())}")
            if 'LanguageContent' in data:
                 print(f"  [warn] Found 'LanguageContent' wrapper! Extracting...")
                 data = data['LanguageContent']
                 content = data.get("content", "")
                 if not content:
                     continue
            else:
                 continue
            
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