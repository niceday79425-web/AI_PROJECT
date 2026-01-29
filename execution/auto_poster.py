import google.generativeai as genai
import os
import datetime
import time
import json
import feedparser
import yfinance as yf
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()

# 2. API 키 설정
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("[!] 경고: API 키가 없습니다.")

# 3. 모델 설정
# 현재 가장 안정적인 '1.5-flash'를 사용합니다.
model = genai.GenerativeModel('gemini-2.5-flash')

# 설정값
TICKERS = ["VIST", "GEV", "AAPL", "JEPI"]
RSS_URLS = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=VIST,GEV,AAPL,JEPI&region=US&lang=en-US",
    "https://www.investing.com/rss/news_25.rss"
]

def get_stock_info(ticker_symbol):
    """주가 정보 수집"""
    print(f"[*] {ticker_symbol} 데이터 수집 중...")
    try:
        ticker = yf.Ticker(ticker_symbol)
        history = ticker.history(period="1d")
        info = ticker.info
        
        current_price = history['Close'].iloc[-1] if not history.empty else info.get('currentPrice', 0)
        div = info.get('dividendYield', 0)
        if div is None:
            div = 0
            
        return {
            "name": info.get('longName', ticker_symbol),
            "symbol": ticker_symbol,
            "price": current_price,
            "dividend_yield": div * 100
        }
    except Exception as e:
        print(f"[!] {ticker_symbol} 정보 실패: {e}")
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
            time.sleep(1)
        except:
            pass
    return "\n".join(news_items)

def generate_content(stock_data, news_text):
    """Gemini를 사용해 글 작성"""
    prompt = f"""
        당신은 미국 주식 투자 전문가입니다. 한국 독자를 위한 블로그 포스팅을 작성하세요.
        
        [데이터]
        종목: {stock_data['name']} ({stock_data['symbol']})
        가격: ${stock_data['price']:.2f}
        배당률: {stock_data['dividend_yield']:.2f}%
        최신 뉴스:
        {news_text}
            
        [출력 형식]
        반드시 JSON 포맷으로만 응답하세요:
        {{
            "title": "이모지 포함 매력적인 제목",
            "content": "HTML 태그(h2, p, ul, li)로 된 상세한 본문",
            "summary": "100자 요약"
        }}
    """
    
    try:
        response = model.generate_content(prompt)
        # JSON 블록 추출 및 정리
        text = response.text.replace('```json', '').replace('```', '').strip()
        # 가끔 앞뒤에 붙는 텍스트 방어
        start_idx = text.find('{')
        end_idx = text.rfind('}') + 1
        if start_idx != -1 and end_idx != -1:
            return json.loads(text[start_idx:end_idx])
        return json.loads(text)
    except Exception as e:
        print(f"[!] Gemini 생성 실패: {e}")
        return None

def save_and_index(content, ticker):
    """파일 저장 및 목록 갱신"""
    if not content:
        return
        
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{ticker}.html"
    
    if not os.path.exists("blog"):
        os.makedirs("blog")
    filepath = os.path.join("blog", filename)
    
    # 프리미엄 HTML 템플릿 적용
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
    
    # 중복 제거 및 최신 글 위로
    posts = [new_post] + [p for p in posts if p['link'] != new_post['link']]
    
    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(posts[:20], f, ensure_ascii=False, indent=4)
    print(f"[*] 저장 완료: {filename}")

def main():
    print("=== StockWise Standard Auto Poster ===")
    news = get_latest_news()
    for ticker in TICKERS:
        data = get_stock_info(ticker)
        if data:
            content = generate_content(data, news)
            if content:
                save_and_index(content, ticker)
            else:
                print(f"[!] {ticker} 콘텐츠 생성 실패")
            time.sleep(5) # API 할당량 초과 방지

if __name__ == "__main__":
    main()
