import json
with open('dividend_insights.json', encoding='utf-8') as f:
    d = json.load(f)
stocks = d['stocks']
picks = ['ARR','VZ','T','KO','V','MSFT','AAPL','SCHD','O','ACN','MCD','QCOM','IBM','MMM','ABBV','JNJ','PG','KO','CVX','XOM']
print(f"{'Ticker':6} | {'Yield':>6} | {'Payout':>7} | {'FCF':>6} | {'Streak':>6} | {'Grade':8} | {'Price':>8} | Name")
print("-"*100)
for s in stocks:
    if s['ticker'] in picks:
        print(
            f"{s['ticker']:6} | {s['dividend_yield']:5.2f}% | {s['payout_ratio']:6.1f}% | "
            f"{s['fcf_coverage']:5.2f}x | {s['dividend_growth_years']:4d}yr | "
            f"{s['grade']:8} | ${s['current_price']:7.2f} | {s['name'][:30]}"
        )
