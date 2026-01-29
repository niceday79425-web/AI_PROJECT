import os
import datetime
import time
import json
import requests
import feedparser
import yfinance as yf
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 설정
TICKERS = ["SCHD", "O", "AAPL", "JEPI"]
RSS_URLS = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=SCHD,O,AAPL,JEPI&region=US&lang=en-US",
    "https://www.investing.com/rss/news_25.rss"
]

def get_stock_info(ticker_symbol):
    """티커 정보를 가져옴"""
    print(f"[*] {ticker_symbol} 데이터 수집 중...")
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        history = ticker.history(period="1d")
        
        current_price = history['Close'].iloc[-1] if not history.empty else info.get('currentPrice', 0)
        
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
    """뉴스 RSS 수집"""
    print("[*] 최신 투자 뉴스 수집 중...")
    news_items = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                news_items.append(f"- {entry.title}")
            time.sleep(1) 
        except Exception as e:
            print(f"[!] 뉴스 수집 실패 ({url}): {e}")
    return "\n".join(news_items)

def generate_content_direct(stock_data, news_text):
    """[필살기] 라이브러리 없이 직접 구글 서버로 요청"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[!] GEMINI_API_KEY가 없습니다.")
        return None

    # 구글 Gemini 1.5 Flash API 주소 (직접 호출)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    prompt = f"""
        당신은 미국 주식 투자 전문가입니다. 한국 독자를 위한 블로그 포스팅을 작성하세요.
        
        [종목 정보]
        - 종목: {stock_data['name']} ({stock_data['symbol']})
        - 가격: ${stock_data['price']:.2f}
        - 배당률: {stock_data['dividend_yield']:.2f}%
        
        [뉴스]
        {news_text}
        
        [출력 형식]
        반드시 JSON 포맷으로:
        {{
            "title": "이모지 포함 매력적인 제목",
            "content": "HTML 태그(h2, p, ul, li)로 된 본문",
            "summary": "100자 요약"
        }}
    """
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code != 200:
            print(f"[!] API 호출 오류: {response.text}")
            return None
        
        result = response.json()
        raw_text = result['candidates'][0]['content']['parts'][0]['text']
        
        # JSON 블록 추출
        start_idx = raw_text.find('{')
        end_idx = raw_text.rfind('}') + 1
        if start_idx != -1 and end_idx != -1:
            json_text = raw_text[start_idx:end_idx].strip()
            return json.loads(json_text)
        else:
            print("[!] API 결과에서 JSON을 찾을 수 없습니다.")
            return None
        
    except Exception as e:
        print(f"[!] 콘텐츠 생성 실패: {e}")
        return None

def save_and_index(content, ticker):
    """파일 저장 및 posts.json 업데이트"""
    if not content:
        return

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{ticker}.html"
    
    if not os.path.exists("blog"):
        os.makedirs("blog")
        
    filepath = os.path.join("blog", filename)
    
    html_template = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content['title']} | StockWise</title>
    <link rel="stylesheet" href="../css/style.css">
    </head>
<body class="dark-mode">
    <div class="container blog-post">
        <header class="post-header">
            <span class="blog-date">{today}</span>
            <h1>{content['title']}</h1>
        </header>
        <article class="post-content">
            {content['content']}
        </article>
        <a href="../index.html" class="back-btn">← 메인으로</a>
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
            except Exception:
                posts = []
            
    new_post = {
        "title": content['title'],
        "date": today,
        "link": f"blog/{filename}",
        "summary": content['summary']
    }
    
    # 중복 제거 및 최신 포스트를 앞으로
    posts = [new_post] + [p for p in posts if p['link'] != new_post['link']]
    
    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(posts[:20], f, ensure_ascii=False, indent=4)

    print(f"[*] 포스팅 완료: {filename}")

def main():
    print("=== StockWise Direct Auto Poster ===")
    news_text = get_latest_news()
    
    for ticker in TICKERS:
        stock_data = get_stock_info(ticker)
        if stock_data:
            content = generate_content_direct(stock_data, news_text)
            if content:
                save_and_index(content, ticker)
                time.sleep(2)

if __name__ == "__main__":
    main()