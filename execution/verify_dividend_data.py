import json, yfinance as yf

with open('dividend_insights.json', encoding='utf-8') as f:
    data = json.load(f)

stocks = data['stocks']
print(f"Generated: {data['generated_at']}")
print(f"Total stocks: {data['total_stocks']}")
print()
print(f"{'Ticker':<8} {'Yield':>7} {'Payout':>9} {'5YrAvg':>8} {'Price':>9} {'Grade':<8} Name")
print('-'*85)
for s in stocks[:25]:
    print(f"{s['ticker']:<8} {s['dividend_yield']:>6.2f}%  {s['payout_ratio']:>7.1f}%  {s['five_year_avg_yield']:>6.1f}%  ${s['current_price']:>7.2f}  {s['grade']:<8} {s['name'][:30]}")

# Now verify top 5 against live yfinance
print('\n--- Live Verification (top 5 by yield) ---')
for s in stocks[:5]:
    try:
        info = yf.Ticker(s['ticker']).info
        live_yield = round((info.get('dividendYield') or 0) * 100, 2)
        live_price = round(info.get('currentPrice') or info.get('regularMarketPrice') or 0, 2)
        live_payout = round((info.get('payoutRatio') or 0) * 100, 1)
        match_y = abs(live_yield - s['dividend_yield']) < 0.5
        match_p = live_price > 0
        print(f"{s['ticker']:<8}  Stored: {s['dividend_yield']}% / Live: {live_yield}%  {'OK' if match_y else 'MISMATCH'}  |  Price Stored: ${s['current_price']} / Live: ${live_price}  {'OK' if match_p else '?'}")
    except Exception as e:
        print(f"{s['ticker']}: ERROR - {e}")
