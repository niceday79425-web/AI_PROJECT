import yfinance as yf
import feedparser
import google.generativeai as genai
import requests
import json
import os
import datetime
from dotenv import load_dotenv
import time

# 환경 변수 로드
load_dotenv()

# Gemini API 설정
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# 설정
TICKERS = ["SCHD", "O", "AAPL", "JEPI"]
RSS_URLS = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=SCHD,O,AAPL,JEPI&region=US&lang=en-US",
    "https://www.investing.com/rss/news_25.rss"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_stock_info(ticker_symbol):
    """티커 정보를 가져옴"""
    print(f"[*] {ticker_symbol} 데이터 수집 중...")
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        history = ticker.history(period="1d")
        
        current_price = history['Close'].iloc[-1] if not history.empty else info.get('currentPrice', 0)
        dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
        
        return {
            "symbol": ticker_symbol,
            "name": info.get('longName', ticker_symbol),
            "price": current_price,
            "dividend_yield": dividend_yield,
            "sector": info.get('sector', 'N/A')
        }
    except Exception as e:
        print(f"[!] {ticker_symbol} 정보 수집 실패: {e}")
        return None

def get_latest_news():
    """뉴스 RSS를 통해 최신 뉴스 제목들을 가져옴"""
    print("[*] 최신 투자 뉴스 수집 중...")
    news_items = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                news_items.append(f"- {entry.title} ({entry.link})")
            time.sleep(1) # 차단 방지 딜레이
        except Exception as e:
            print(f"[!] 뉴스 수집 실패 ({url}): {e}")
    return "\n".join(news_items)

def generate_content(stock_data, news_text):
    """Gemini를 사용해 블로그 본문 생성"""
    if not GEMINI_API_KEY:
        print("[!] GEMINI_API_KEY가 없습니다. 기본 템플릿을 사용합니다.")
        return f"<h1>{stock_data['symbol']} 분석 리포트</h1><p>현재가: ${stock_data['price']:.2f}, 배당수익률: {stock_data['dividend_yield']:.2f}%</p>", "기본 분석 리포트"

    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    당신은 20년 경력의 전문 미국 주식 투자 전략가입니다.
    아래 데이터를 바탕으로 한국 독자들을 위한 '수익형 블로그 포스팅'을 작성하세요.

    [주식 데이터]
    - 종목명: {stock_data['name']} ({stock_data['symbol']})
    - 현재가: ${stock_data['price']:.2f}
    - 배당수익률: {stock_data['dividend_yield']:.2f}%
    - 섹터: {stock_data['sector']}

    [최신 뉴스 뉴스 요약]
    {news_text}

    [요구사항]
    1. 제목: 독자의 클릭을 유도하는 매력적인 제목 (SEO 최적화)
    2. 본문: 
       - 전문 투자자의 관점에서 본 3줄 핵심 요약.
       - 해당 종목의 배당 매력 및 투자 인사이트.
       - HTML 태그(h2, p, ul, li)를 사용하여 깔끔하게 구성.
    3. 톤앤매너: 신뢰감 있으면서도 친절한 말투.
    4. 출력 형식: 반드시 JSON 형식으로 반환하세요.
    {{
        "title": "여기에 제목 작성",
        "content": "여기에 HTML 본문 작성",
        "summary": "블로그 목록에 표시할 100자 내외 요약"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # JSON 문자열만 추출 (마크다운 포맷 제외)
        json_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(json_text)
    except Exception as e:
        print(f"[!] Gemini 콘텐츠 생성 실패: {e}")
        return None

def save_and_index(content, ticker):
    """HTML 파일 저장 및 posts.json 업데이트"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{ticker}.html"
    filepath = os.path.join("blog", filename)
    
    # 1. HTML 파일 생성
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{content['title']} | StockWise</title>
        <link rel="stylesheet" href="../css/style.css">
        <style>
            .blog-post {{ max-width: 800px; margin: 4rem auto; padding: 0 2rem; }}
            .post-header {{ margin-bottom: 3rem; text-align: center; }}
            .post-content h2 {{ margin: 2rem 0 1rem; color: #a855f7; }}
            .post-content p {{ margin-bottom: 1.2rem; color: #cbd5e1; line-height: 1.8; }}
            .back-btn {{ display: inline-block; margin-top: 2rem; color: #6366f1; text-decoration: none; font-weight: 600; }}
        </style>
    </head>
    <body class="dark-mode">
        <div class="container blog-post">
            <header class="post-header">
                <span class="blog-date">{today}</span>
                <h1 style="font-size: 2.5rem; margin-top: 1rem;">{content['title']}</h1>
            </header>
            <article class="post-content">
                {content['content']}
            </article>
            <a href="../index.html" class="back-btn">← 메인으로 돌아가기</a>
        </div>
    </body>
    </html>
    """
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    # 2. posts.json 업데이트
    posts_path = "posts.json"
    posts = []
    if os.path.exists(posts_path):
        with open(posts_path, "r", encoding="utf-8") as f:
            posts = json.load(f)
    
    new_post = {
        "title": content['title'],
        "date": today,
        "link": f"blog/{filename}",
        "summary": content['summary']
    }
    
    # 중복 체크 후 추가 (최신글이 위로)
    posts = [new_post] + [p for p in posts if p['link'] != new_post['link']]
    
    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(posts[:10], f, ensure_ascii=False, indent=4) # 최근 10개만 유지

    print(f"[*] 포스팅 완료: {filename}")

def main():
    print("=== StockWise Auto Poster Running ===")
    news_text = get_latest_news()
    
    for ticker in TICKERS:
        stock_data = get_stock_info(ticker)
        if stock_data:
            content = generate_content(stock_data, news_text)
            if content:
                save_and_index(content, ticker)
            time.sleep(2) # API 할당량 관리 및 차단 방지

if __name__ == "__main__":
    main()
