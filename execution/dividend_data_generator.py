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
        
        # Check if it's already in percentage (some APIs return 16.5 instead of 0.165)
        # If it's small (e.g. 0.05), multiply by 100. If it's big (e.g. 5.0), leave it.
        # But be careful with 0. 
        if dividend_yield:
            # Most dividend yields are below 20%. If it's > 0.5 (50%), it's likely already a percentage or an error.
            # But let's assume raw data is usually decimal (0.05).
            # If we see > 1, treating it as percentage. 
            if dividend_yield < 1: 
                dividend_yield = dividend_yield * 100
            
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
        grade = calculate_dividend_grade(dividend_yield, payout_ratio, five_year_avg_yield, sector)
        
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

def calculate_dividend_grade(yield_pct: float, payout_ratio: float, five_year_avg: float, sector: str = "N/A") -> str:
    """Calculate dividend quality grade based on metrics with sector adjustments"""
    score = 0
    
    # 1. Yield Score (Max 40 points)
    # Focus: Is the current return attractive?
    if yield_pct >= 5.0:
        score += 40
    elif yield_pct >= 4.0:
        score += 35
    elif yield_pct >= 3.0:
        score += 25
    elif yield_pct >= 2.0:
        score += 15
    elif yield_pct >= 1.0:
        score += 5
    
    # 2. Payout Ratio Score (Max 30 points)
    # Focus: Sustainability. Lower is better, but depends on sector.
    
    is_reit = sector == "Real Estate" or "REIT" in sector.upper()
    
    if is_reit:
        # REITs are required to pay >90% of taxable income to shareholders.
        # So a high payout ratio (around 90-100%) is normal and healthy.
        if 0 < payout_ratio <= 95:
            score += 30  # Excellent for REIT
        elif payout_ratio <= 105:
            score += 20  # Acceptable
        elif payout_ratio <= 120:
            score += 10  # Riskier
    else:
        # Standard corporations
        if 0 < payout_ratio <= 50:
            score += 30  # Very Safe
        elif payout_ratio <= 70:
            score += 20  # Safe
        elif payout_ratio <= 90:
            score += 10  # Caution
            
    # 3. Consistency/Stability Score (Max 30 points)
    # Focus: Is the current yield consistent with history? (Proxyl for price/div stability)
    if five_year_avg > 0:
        # Calculate deviation from 5-year average
        deviation = abs(yield_pct - five_year_avg) / five_year_avg
        
        if deviation <= 0.1:  # Within 10% deviation
            score += 30
        elif deviation <= 0.2: # Within 20%
            score += 20
        elif deviation <= 3.0: # Within 30%
            score += 10
            
    # Bonus: Dividend Growth (Simplified logic if data not available)
    # If yield is moderate (2-5%) and payout is healthy, it's likely a grower.
    if 2.0 <= yield_pct <= 5.0 and score >= 50:
        score += 5

    # Grade Assignment
    if score >= 80:
        return "S등급"
    elif score >= 65:
        return "A등급"
    elif score >= 50:
        return "B등급"
    else:
        return "C등급"

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
    
    print(f"\n[OK] Successfully generated data for {len(dividend_data)} dividend stocks")
    print(f"[OK] Data saved to {output_file}")
    
    # Print summary
    print("\n=== Top 10 by Dividend Yield ===")
    for stock in dividend_data[:10]:
        print(f"{stock['ticker']:6} | {stock['name'][:30]:30} | {stock['dividend_yield']:5.2f}% | {stock['grade']}")

    # Improvements: SSG Implementation
    update_html_files(dividend_data)

def update_html_files(data):
    """Inject dividend table rows directly into HTML files for SEO (SSG)"""
    print("\n[*] Updating HTML files with static data...")
    
    files = {
        "en": "d:\\AI_PROJECT\\list.html",
        "ko": "d:\\AI_PROJECT\\ko\\list.html",
        "pt": "d:\\AI_PROJECT\\pt\\list.html"
    }
    
    # Text mappings for Grades
    grade_map = {
        "en": {"S등급": "S-Tier", "A등급": "A-Tier", "B등급": "B-Tier", "C등급": "C-Tier"},
        "ko": {"S등급": "S등급", "A등급": "A등급", "B등급": "B등급", "C등급": "C등급"},
        "pt": {"S등급": "Classe S", "A등급": "Classe A", "B등급": "Classe B", "C등급": "Classe C"}
    }
    
    grade_colors = {
        "S등급": "background: linear-gradient(135deg, #FFD700 0%, #FDB931 100%); color: black; box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);",
        "A등급": "background: #10B981; color: white;",
        "B등급": "background: #3B82F6; color: white;",
        "C등급": "background: #6B7280; color: white;"
    }

    for lang, filepath in files.items():
        try:
            # Generate HTML rows
            html_rows = ""
            for stock in data:
                grade_text = grade_map[lang].get(stock['grade'], stock['grade'])
                grade_style = grade_colors.get(stock['grade'], "background: #666; color: white;")
                
                html_rows += f"""
                    <tr style="border-bottom: 1px solid #333;">
                        <td style="padding: 1rem; font-weight: bold; color: #fff;">{stock['ticker']}</td>
                        <td style="padding: 1rem; color: #ccc;">{stock['name']}</td>
                        <td style="padding: 1rem; text-align: right; color: #4ADE80; font-weight: bold;">{stock['dividend_yield']}%</td>
                        <td style="padding: 1rem; text-align: center;">
                            <span style="padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85rem; {grade_style}">{grade_text}</span>
                        </td>
                    </tr>"""
            
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find tbody content to replace
            # Pattern: <tbody id="dividendTableBody"> ... </tbody>
            # careful with newlines and existing content
            import re
            pattern = re.compile(r'(<tbody id="dividendTableBody">)(.*?)(</tbody>)', re.DOTALL)
            
            if pattern.search(content):
                new_content = pattern.sub(f'\\1{html_rows}\\3', content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"[UPDATED] {filepath}")
            else:
                print(f"[WARNING] Could not find tbody in {filepath}")
                
        except Exception as e:
            print(f"[ERROR] Updating {lang}: {e}")

if __name__ == "__main__":
    generate_dividend_insights()
