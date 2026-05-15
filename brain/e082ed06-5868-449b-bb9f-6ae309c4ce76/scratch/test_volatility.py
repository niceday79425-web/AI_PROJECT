import yfinance as yf
import datetime
import math
import json
import os
import re

TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "BRK-B", "JPM", "V", 
    "JNJ", "WMT", "PG", "MA", "UNH", "HD", "DIS", "PYPL", "BAC", "VZ", 
    "ADBE", "CMCSA", "NFLX", "KO", "PEP", "XOM", "CVX", "ABT", "T", "ABBV",
    "COST", "PFE", "MRK", "NKE", "LLY", "AVGO", "ORCL", "ACN", "DHR", "TMO",
    "MCD", "CSCO", "ABNB", "CRM", "AMD", "QCOM", "INTC", "TXN", "HON", "UPS",
    "BTC-USD", "ETH-USD", "SCHD", "JEPI", "VIST", "GEV"
]

def get_recently_posted_tickers(cooldown_days=7):
    cutoff = datetime.datetime.now() - datetime.timedelta(days=cooldown_days)
    recent = set()
    for posts_path in ["posts.json", "ko/posts.json", "pt/posts.json"]:
        p_abs = os.path.join("d:\\AI_PROJECT", posts_path)
        if not os.path.exists(p_abs): continue
        try:
            with open(p_abs, "r", encoding="utf-8") as f:
                posts = json.load(f)
            for p in posts:
                try:
                    post_date = datetime.datetime.strptime(p.get("date", ""), "%Y-%m-%d")
                except ValueError: continue
                if post_date >= cutoff:
                    fname = os.path.basename(p.get("link", ""))
                    if re.match(r'\d{4}-\d{2}-\d{2}-', fname):
                        ticker = os.path.splitext(fname)[0].split("-", 3)[-1]
                        recent.add(ticker)
        except Exception: continue
    return recent

recently_posted = get_recently_posted_tickers(7)
eligible = [t for t in TICKERS if t not in recently_posted]
print(f"Eligible: {eligible}")

data = yf.download(eligible, period="5d", interval="1d", group_by='ticker', progress=False)
print("V data head:\n", data['V'].head())
print("Data head columns:", data.columns[:10])

volatility_data = []
for ticker in eligible:
    try:
        ticker_data = data[ticker]
        if len(ticker_data) < 2:
            print(f"{ticker}: not enough data")
            continue
        
        last_close = float(ticker_data['Close'].iloc[-1])
        prev_close = float(ticker_data['Close'].iloc[-2])
        
        if math.isnan(last_close) or math.isnan(prev_close) or prev_close == 0:
            print(f"{ticker}: NaN or zero")
            continue
            
        change = (last_close - prev_close) / prev_close
        abs_change = abs(change) * 100
        
        volatility_data.append({
            "ticker": ticker,
            "change": change * 100,
            "abs_change": abs_change,
            "price": last_close,
        })
    except Exception as e:
        print(f"{ticker}: Error {e}")

print(f"\nVolatility Data count: {len(volatility_data)}")
top_volatile = sorted(volatility_data, key=lambda x: x['abs_change'], reverse=True)[:3]
for item in top_volatile:
    print(f"Top: {item['ticker']} ({item['abs_change']:.2f}%)")
