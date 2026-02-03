import yfinance as yf
import json
import datetime
from typing import List, Dict
import time

# Dividend Data Generator
# Generates comprehensive dividend stock insights with 50+ popular dividend stocks

# Popular dividend stocks categorized
DIVIDEND_STOCKS = {
    "dividend_etfs": [
        "SCHD", "VYM", "DGRO", "NOBL", "VIG", "SDY", "DVY", "HDV", "SPYD", "FVD"
    ],
    "dividend_aristocrats": [
        "JNJ", "PG", "KO", "PEP", "MCD", "WMT", "TGT", "LOW", "HD", "CAT",
        "MMM", "CL", "GPC", "SYY", "ADM", "BF-B", "ABBV", "ABT", "CVX", "XOM"
    ],
    "high_yield": [
        "O", "T", "MO", "BTI", "VZ", "IBM", "AGNC", "NLY", "ARR", "DX"
    ],
    "dividend_growth": [
        "MSFT", "AAPL", "V", "MA", "UNH", "JPM", "BAC", "WFC", "BLK", "GS",
        "AVGO", "TXN", "QCOM", "CSCO", "ORCL", "ACN", "ADP", "PAYX"
    ],
    "reits": [
        "AMT", "PLD", "EQIX", "PSA", "DLR", "SPG", "WELL", "AVB", "EQR", "VTR"
    ]
}

def get_dividend_data(ticker: str) -> Dict:
    """Fetch comprehensive dividend data for a single ticker"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get dividend yield
        dividend_yield = info.get('dividendYield', 0)
        if dividend_yield:
            dividend_yield = dividend_yield * 100  # Convert to percentage
        
        # Get trailing annual dividend rate
        trailing_annual_dividend = info.get('trailingAnnualDividendRate', 0)
        
        # Get payout ratio
        payout_ratio = info.get('payoutRatio', 0)
        if payout_ratio:
            payout_ratio = payout_ratio * 100
        
        # Get 5-year average dividend yield
        five_year_avg_yield = info.get('fiveYearAvgDividendYield', 0)
        
        # Get current price
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        # Get company name
        company_name = info.get('longName') or info.get('shortName', ticker)
        
        # Get sector
        sector = info.get('sector', 'N/A')
        
        # Calculate dividend grade (S, A, B, C)
        grade = calculate_dividend_grade(dividend_yield, payout_ratio, five_year_avg_yield)
        
        return {
            "ticker": ticker,
            "name": company_name,
            "sector": sector,
            "current_price": round(current_price, 2),
            "dividend_yield": round(dividend_yield, 2),
            "annual_dividend": round(trailing_annual_dividend, 2),
            "payout_ratio": round(payout_ratio, 2),
            "five_year_avg_yield": round(five_year_avg_yield, 2),
            "grade": grade,
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"[!] Error fetching {ticker}: {e}")
        return None

def calculate_dividend_grade(yield_pct: float, payout_ratio: float, five_year_avg: float) -> str:
    """Calculate dividend quality grade based on metrics"""
    score = 0
    
    # Yield score (0-40 points)
    if yield_pct >= 4.0:
        score += 40
    elif yield_pct >= 3.0:
        score += 30
    elif yield_pct >= 2.0:
        score += 20
    elif yield_pct >= 1.0:
        score += 10
    
    # Payout ratio score (0-30 points) - lower is better for sustainability
    if 0 < payout_ratio <= 50:
        score += 30
    elif payout_ratio <= 70:
        score += 20
    elif payout_ratio <= 90:
        score += 10
    
    # Consistency score (0-30 points)
    if five_year_avg > 0:
        consistency = abs(yield_pct - five_year_avg) / five_year_avg if five_year_avg > 0 else 1
        if consistency <= 0.1:  # Within 10% of 5-year average
            score += 30
        elif consistency <= 0.2:
            score += 20
        elif consistency <= 0.3:
            score += 10
    
    # Grade assignment
    if score >= 80:
        return "S등급"  # S-tier
    elif score >= 60:
        return "A등급"  # A-tier
    elif score >= 40:
        return "B등급"  # B-tier
    else:
        return "C등급"  # C-tier

def generate_dividend_insights():
    """Generate comprehensive dividend insights for 50+ stocks"""
    print("=== Dividend Data Generator v1.0 ===")
    print("[*] Fetching dividend data for 50+ stocks...")
    
    all_stocks = []
    
    # Flatten all categories
    for category, tickers in DIVIDEND_STOCKS.items():
        all_stocks.extend(tickers)
    
    # Remove duplicates
    all_stocks = list(set(all_stocks))
    
    dividend_data = []
    
    for i, ticker in enumerate(all_stocks, 1):
        print(f"[{i}/{len(all_stocks)}] Processing {ticker}...")
        data = get_dividend_data(ticker)
        if data and data['dividend_yield'] > 0:  # Only include stocks with dividends
            dividend_data.append(data)
        time.sleep(0.5)  # Rate limiting
    
    # Sort by dividend yield (descending)
    dividend_data.sort(key=lambda x: x['dividend_yield'], reverse=True)
    
    # Save to JSON
    output_file = "dividend_insights.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_stocks": len(dividend_data),
            "stocks": dividend_data
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n[✓] Successfully generated data for {len(dividend_data)} dividend stocks")
    print(f"[✓] Data saved to {output_file}")
    
    # Print summary
    print("\n=== Top 10 by Dividend Yield ===")
    for stock in dividend_data[:10]:
        print(f"{stock['ticker']:6} | {stock['name'][:30]:30} | {stock['dividend_yield']:5.2f}% | {stock['grade']}")

if __name__ == "__main__":
    generate_dividend_insights()
