import os
import datetime
import time
import json
import requests
import feedparser
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

# 설정
TICKERS = ["VIST", "GEV", "AAPL", "JEPI"]
RSS_URLS = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=VIST,GEV,AAPL,JEPI&region=US&lang=en-US",
    "https://www.investing.com/rss/news_25.rss"
]

# [핵심] 시도할 모델 목록 (순서대로 다 해봄)
MODELS_TO_TRY = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-1.0-pro",
    "gemini-pro"
]

def get_stock_info(ticker_symbol):
    """티커 정보 수집 (에러 방지 강화)"""
    print(f"[*] {ticker_symbol} 데이터 수집 중...")
    try:
        ticker = yf.Ticker(ticker_symbol)
        history = ticker.history(period="1d")
        info = ticker.info
        
        current_price = 0
        if not history.empty:
            current_price = history['Close'].iloc[-1]
        elif 'currentPrice' in info:
            current_price = info['currentPrice']
        
        div_yield = info.get('dividendYield', 0)
        if div_yield is None:
            div_yield = 0
            
        return {
            "symbol": ticker_symbol,
            "name": info.get('longName', ticker_symbol),
            "price": current_price,
            "dividend_yield": div_yield * 100,
            "sector": info.get('sector', 'N/A')
        }
    except Exception as e:
        print(f"[!] {ticker_symbol} 실패: {e}")
        return None

def get_latest_news():
    """뉴스 수집"""
    print("[*] 최신 투자 뉴스 수집 중...")
    news_items = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:
                news_items.append(f"- {entry.title}")
        except:
            continue
    return "\n".join(news_items)

def generate_content_universal(stock_data, news_text):
    """[만능키] 여러 모델을 순서대로 시도하여 성공하는 것을 찾음"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[!] GEMINI_API_KEY가 설정되지 않았습니다.")
        return None

    prompt = f"""
        당신은 전문 주식 투자자입니다. 한국 독자를 위한 블로그 포스팅을 작성하세요.
        - 종목: {stock_data['name']} ({stock_data['symbol']})
        - 가격: ${stock_data['price']:.2f}
        - 배당률: {stock_data['dividend_yield']:.2f}%
        - 관련 뉴스:
        {news_text}
            
        [출력 형식] 반드시 JSON 포맷으로만 응답하세요:
        {{
            "title": "이모지 포함 매력적인 제목",
            "content": "HTML 태그(h2, p, ul, li)로 된 상세한 본문",
            "summary": "100자 내외의 요약"
        }}
    """
    
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    # 여기서 모델을 하나씩 돌려가며 시도
    for model_name in MODELS_TO_TRY:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            print(f"[*] 모델 시도 중: {model_name} ...")
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"[SUCCESS] {model_name} 모델로 성공했습니다! 🎉")
                result = response.json()
                raw_text = result['candidates'][0]['content']['parts'][0]['text']
                
                # JSON 블록 추출 (마크다운 제거 등)
                start_idx = raw_text.find('{')
                end_idx = raw_text.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_text = raw_text[start_idx:end_idx].strip()
                    return json.loads(json_text)
            else:
                print(f"[FAIL] {model_name} 실패 (코드: {response.status_code})")
                time.sleep(1) # 잠시 대기
        except Exception as e:
            print(f"[ERROR] {model_name} 연결 오류: {e}")
            
    print("[!] 모든 모델 시도 실패. API 키나 할당량을 확인하세요.")
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
    
    # 프리미엄 HTML 템플릿 복구
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
            except:
                posts = []
                
    new_post = {
        "title": content['title'],
        "date": today,
        "link": f"blog/{filename}",
        "summary": content['summary']
    }
    
    # 중복 제거 및 최신 포스팅을 맨 위로
    posts = [new_post] + [p for p in posts if p['link'] != new_post['link']]
    
    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(posts[:20], f, ensure_ascii=False, indent=4)

    print(f"[*] 포스팅 완료: {filename}")

def main():
    print("=== StockWise Universal Auto Poster ===")
    news_text = get_latest_news()
    for ticker in TICKERS:
        stock_data = get_stock_info(ticker)
        if stock_data:
            content = generate_content_universal(stock_data, news_text)
            if content:
                save_and_index(content, ticker)
                # 429 에러 방지 및 모델 부하 분산
                time.sleep(5)
            else:
                print(f"[!] {ticker} 콘텐츠 생성 실패")

if __name__ == "__main__":
    main()