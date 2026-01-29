import os
import datetime
import time
import json
import requests
import feedparser
import yfinance as yf
from google import genai  # [중요] 최신 라이브러리 사용
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

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
        # fast_info 사용이 더 빠르고 안정적일 수 있음
        info = ticker.info
        history = ticker.history(period="1d")
        
        current_price = history['Close'].iloc[-1] if not history.empty else info.get('currentPrice', 0)
        
        # 배당률 처리 안전장치 추가
        div_yield = info.get('dividendYield')
        dividend_yield = div_yield * 100 if div_yield else 0
        
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
            for entry in feed.entries[:3]: # 종목별로 너무 많지 않게 조절
                news_items.append(f"- {entry.title}")
            time.sleep(1) 
        except Exception as e:
            print(f"[!] 뉴스 수집 실패 ({url}): {e}")
    return "\n".join(news_items)

def generate_content(stock_data, news_text):
    """Gemini를 사용해 블로그 본문 생성 (최신 google-genai 라이브러리 사용)"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[!] GEMINI_API_KEY가 없습니다.")
        return None

    # [핵심 변경] 최신 Client 방식 초기화
    client = genai.Client(api_key=api_key)

    prompt = f"""
        당신은 20년 경력의 전문 미국 주식 투자 전략가입니다.
        아래 데이터를 바탕으로 한국 독자들을 위한 '수익형 블로그 포스팅'을 작성하세요.

        [주식 데이터]
        - 종목명: {stock_data['name']} ({stock_data['symbol']})
        - 현재가: ${stock_data['price']:.2f}
        - 배당수익률: {stock_data['dividend_yield']:.2f}%
        - 섹터: {stock_data['sector']}

        [관련 뉴스 헤드라인]
        {news_text}

        [요구사항]
        1. 제목: 클릭을 유도하는 매력적인 제목 (이모지 포함)
        2. 본문 내용: 
            - 3줄 핵심 요약
            - 이 종목의 배당 매력 분석
            - 투자자를 위한 한마디
            - HTML 태그(<h2>, <p>, <ul>, <li>)만 사용해서 작성.
            - 마크다운(```html 등)은 절대 포함하지 마세요.
        3. 출력 형식: 반드시 JSON 포맷으로 반환하세요.
        {{
            "title": "제목 내용",
            "content": "HTML 본문 내용",
            "summary": "100자 요약"
        }}
    """
    
    try:
        # [핵심 변경] generate_content 호출 방식 변경
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        
        # JSON 파싱 (마크다운 제거 후 파싱)
        raw_text = response.text
        json_text = raw_text.replace('```json', '').replace('```', '').strip()
        
        return json.loads(json_text)
    except Exception as e:
        print(f"[!] Gemini 콘텐츠 생성 실패: {e}")
        return None

def save_and_index(content, ticker):
    """HTML 파일 저장 및 posts.json 업데이트"""
    if not content:
        return

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{ticker}.html"
    
    # blog 폴더가 없으면 생성
    if not os.path.exists("blog"):
        os.makedirs("blog")
        
    filepath = os.path.join("blog", filename)
    
    # HTML 템플릿
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
        
    # posts.json 업데이트
    posts_path = "posts.json"
    posts = []
    if os.path.exists(posts_path):
        with open(posts_path, "r", encoding="utf-8") as f:
            try:
                posts = json.load(f)
            except:
                posts = []
                
    new_post = {
        "title": content['title'],
        "date": today,
        "link": f"blog/{filename}",
        "summary": content['summary']
    }
    
    # 중복 체크 (같은 링크가 있으면 삭제 후 맨 앞에 추가)
    posts = [p for p in posts if p['link'] != new_post['link']]
    posts.insert(0, new_post)
    
    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(posts[:20], f, ensure_ascii=False, indent=4)

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
                time.sleep(2) # 429 에러 방지 딜레이

if __name__ == "__main__":
    main()