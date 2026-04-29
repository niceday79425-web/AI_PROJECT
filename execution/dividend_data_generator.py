import yfinance as yf
import json
import datetime
import time
from typing import Dict

DIVIDEND_STOCKS = {
    "dividend_etfs": [
        "SCHD", "VYM", "DGRO", "NOBL", "VIG", "SDY", "DVY", "HDV", "SPYD", "FVD"
    ],
    "dividend_aristocrats": [
        "JNJ", "PG", "KO", "PEP", "MCD", "WMT", "TGT", "LOW", "HD", "CAT",
        "MMM", "CL", "GPC", "SYY", "ADM", "ABBV", "ABT", "CVX", "XOM", "GD"
    ],
    "high_yield": [
        "O", "T", "MO", "BTI", "VZ", "IBM", "AGNC", "NLY", "ARR", "DX"
    ],
    "dividend_growth": [
        "MSFT", "AAPL", "V", "MA", "UNH", "JPM", "BAC", "BLK",
        "AVGO", "TXN", "QCOM", "CSCO", "ORCL", "ACN", "ADP", "PAYX"
    ],
    "reits": [
        "AMT", "PLD", "EQIX", "PSA", "DLR", "SPG", "WELL", "AVB", "EQR", "VTR"
    ]
}

def get_dividend_growth_years(ticker: str) -> int:
    """Count consecutive years of dividend increases from history."""
    try:
        stock = yf.Ticker(ticker)
        divs = stock.dividends
        if divs.empty or len(divs) < 4:
            return 0
        # Normalize timezone-aware index
        try:
            divs.index = divs.index.tz_convert(None)
        except Exception:
            try:
                divs.index = divs.index.tz_localize(None)
            except Exception:
                pass
        # Annual sum
        annual = divs.groupby(divs.index.year).sum()
        if len(annual) < 2:
            return 0
        
        years = sorted(annual.index, reverse=True)
        streak = 0
        
        # If the most recent year is the current incomplete year and its sum is smaller than last year,
        # we start counting from the previous year.
        current_year = datetime.datetime.now().year
        start_idx = 0
        if years[0] == current_year and annual[years[0]] <= annual[years[1]] * 1.02:
            start_idx = 1
            
        for i in range(start_idx, len(years) - 1):
            if annual[years[i]] >= annual[years[i + 1]] * 0.98:  # Allow 2% rounding tolerance
                streak += 1
            else:
                break
        return streak
    except Exception:
        return 0

def get_dividend_data(ticker: str) -> Dict:
    """Fetch comprehensive dividend data for a single ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # --- Price (works for stocks and ETFs) ---
        current_price = float(
            info.get('currentPrice') or
            info.get('regularMarketPrice') or
            info.get('navPrice') or
            info.get('previousClose') or 0
        )

        # --- Annual dividend ---
        annual_dividend = float(info.get('trailingAnnualDividendRate') or 0)

        # --- Dividend Yield: prefer fundamental calc, fall back to API field ---
        if current_price > 0 and annual_dividend > 0:
            # Most reliable: calculate from first principles
            dividend_yield = round((annual_dividend / current_price) * 100, 2)
        else:
            # yfinance returns dividendYield in two different formats depending on security type:
            # - Stocks (older format): raw fraction  e.g. 0.0087 = 0.87%  → need * 100
            # - ETFs (newer format):   already as %  e.g. 3.44   = 3.44%  → do NOT * 100
            raw = float(info.get('dividendYield') or info.get('trailingAnnualDividendYield') or 0)
            if raw > 0.5:
                # Already a percentage value (e.g. 3.44 means 3.44%)
                dividend_yield = round(raw, 2)
            else:
                # Raw fraction (e.g. 0.0087 means 0.87%)
                dividend_yield = round(raw * 100, 2)

        # Skip if no dividend
        if dividend_yield <= 0:
            return None

        # --- Payout Ratio (comes as fraction from yfinance, e.g. 0.22 = 22%) ---
        raw_payout = float(info.get('payoutRatio') or 0)
        payout_ratio = round(raw_payout * 100, 2)

        # --- 5-year average yield ---
        five_year_avg_yield = float(info.get('fiveYearAvgDividendYield') or 0)

        # --- FCF Coverage: FreeCashFlow / total dividends paid ---
        fcf = float(info.get('freeCashflow') or 0)
        shares = float(info.get('sharesOutstanding') or 0)
        total_divs = shares * annual_dividend
        if total_divs > 0:
            fcf_coverage = round(fcf / total_divs, 2)
        else:
            fcf_coverage = 0.0

        # --- Dividend Growth Streak ---
        growth_years = get_dividend_growth_years(ticker)

        # --- Company info ---
        company_name = info.get('longName') or info.get('shortName') or ticker
        sector = info.get('sector') or 'N/A'

        # --- Grade ---
        grade = calculate_dividend_grade(
            dividend_yield, payout_ratio, five_year_avg_yield,
            fcf_coverage, growth_years, sector
        )

        return {
            "ticker": ticker,
            "name": company_name,
            "sector": sector,
            "current_price": round(current_price, 2),
            "dividend_yield": dividend_yield,
            "annual_dividend": round(annual_dividend, 2),
            "payout_ratio": payout_ratio,
            "five_year_avg_yield": five_year_avg_yield,
            "fcf_coverage": fcf_coverage,
            "dividend_growth_years": growth_years,
            "grade": grade,
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"[!] Error fetching {ticker}: {e}")
        return None


def calculate_dividend_grade(yield_pct, payout_ratio, five_year_avg,
                              fcf_coverage, growth_years, sector="N/A") -> str:
    """Balanced grade: yield + sustainability + FCF + growth track record."""
    score = 0
    is_reit = (sector == "Real Estate") or ("REIT" in str(sector).upper())

    # 1. Yield attractiveness (max 20 pts)
    if yield_pct >= 5.0:   score += 20
    elif yield_pct >= 4.0: score += 16
    elif yield_pct >= 3.0: score += 12
    elif yield_pct >= 2.0: score += 8
    elif yield_pct >= 1.0: score += 4

    # 2. Payout Ratio sustainability (max 25 pts)
    if is_reit:
        if 0 < payout_ratio <= 95:   score += 25
        elif payout_ratio <= 110:    score += 15
        elif payout_ratio <= 130:    score += 8
    else:
        if 0 < payout_ratio <= 40:   score += 25
        elif payout_ratio <= 60:     score += 20
        elif payout_ratio <= 75:     score += 12
        elif payout_ratio <= 90:     score += 5

    # 3. FCF Coverage (max 25 pts) — NEW
    if fcf_coverage >= 3.0:   score += 25
    elif fcf_coverage >= 2.0: score += 20
    elif fcf_coverage >= 1.5: score += 15
    elif fcf_coverage >= 1.0: score += 10
    elif fcf_coverage >= 0.5: score += 4

    # 4. Dividend Growth Streak (max 30 pts) — NEW
    if growth_years >= 50:    score += 30   # Dividend King
    elif growth_years >= 25:  score += 25   # Dividend Aristocrat
    elif growth_years >= 15:  score += 20
    elif growth_years >= 10:  score += 14
    elif growth_years >= 5:   score += 8
    elif growth_years >= 2:   score += 3

    # 5. Consistency bonus (5-yr avg vs current)
    if five_year_avg > 0:
        dev = abs(yield_pct - five_year_avg) / five_year_avg
        if dev <= 0.15: score += 5
        elif dev <= 0.30: score += 2

    if score >= 75:  return "S등급"
    elif score >= 58: return "A등급"
    elif score >= 40: return "B등급"
    else:             return "C등급"


def generate_dividend_insights():
    print("=== Dividend Data Generator v2.0 (Fixed) ===")

    all_tickers = list({t for tickers in DIVIDEND_STOCKS.values() for t in tickers})
    print(f"[*] Processing {len(all_tickers)} tickers...")

    dividend_data = []
    for i, ticker in enumerate(all_tickers, 1):
        print(f"  [{i:02d}/{len(all_tickers)}] {ticker}...", end=" ")
        data = get_dividend_data(ticker)
        if data:
            dividend_data.append(data)
            print(f"{data['dividend_yield']:.2f}% | {data['grade']} | "
                  f"FCF {data['fcf_coverage']:.1f}x | "
                  f"Streak {data['dividend_growth_years']}yr")
        else:
            print("skipped (no dividend)")
        time.sleep(0.6)

    dividend_data.sort(key=lambda x: x['dividend_yield'], reverse=True)

    output = {
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_stocks": len(dividend_data),
        "stocks": dividend_data
    }

    with open("dividend_insights.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Saved {len(dividend_data)} stocks → dividend_insights.json")

    print("\n=== Top 15 by Dividend Yield ===")
    print(f"{'Ticker':<8} {'Yield':>6} {'Payout':>8} {'FCF':>6} {'Streak':>7} {'Grade':<8} Name")
    print("-" * 80)
    for s in dividend_data[:15]:
        print(f"{s['ticker']:<8} {s['dividend_yield']:>5.2f}%  "
              f"{s['payout_ratio']:>6.1f}%  {s['fcf_coverage']:>5.1f}x  "
              f"{s['dividend_growth_years']:>5}yr  {s['grade']:<8} {s['name'][:25]}")

    update_html_files(dividend_data)


def update_html_files(data):
    """Inject static rows into HTML for SSG/SEO."""
    import re
    print("\n[*] Updating HTML files...")

    grade_maps = {
        "en": {"S등급": "S-Tier", "A등급": "A-Tier", "B등급": "B-Tier", "C등급": "C-Tier"},
        "ko": {"S등급": "S등급",  "A등급": "A등급",  "B등급": "B등급",  "C등급": "C등급"},
        "pt": {"S등급": "Classe S", "A등급": "Classe A", "B등급": "Classe B", "C등급": "Classe C"},
    }
    grade_colors = {
        "S등급": "background:linear-gradient(135deg,#FFD700,#FDB931);color:#000;box-shadow:0 0 10px rgba(255,215,0,.5);",
        "A등급": "background:#10B981;color:#fff;",
        "B등급": "background:#3B82F6;color:#fff;",
        "C등급": "background:#6B7280;color:#fff;",
    }
    files = {
        "en": r"d:\AI_PROJECT\list.html",
        "ko": r"d:\AI_PROJECT\ko\list.html",
        "pt": r"d:\AI_PROJECT\pt\list.html",
    }

    for lang, filepath in files.items():
        try:
            rows = ""
            for s in data:
                gt = grade_maps[lang].get(s['grade'], s['grade'])
                gs = grade_colors.get(s['grade'], "background:#666;color:#fff;")
                fcf_str = f"{s['fcf_coverage']:.1f}x" if s['fcf_coverage'] > 0 else "N/A"
                streak = f"{s['dividend_growth_years']}yr" if s['dividend_growth_years'] > 0 else "N/A"
                rows += f"""
                    <tr style="border-bottom:1px solid #333;">
                        <td style="padding:.9rem;font-weight:bold;color:#fff;">{s['ticker']}</td>
                        <td style="padding:.9rem;color:#ccc;">{s['name']}</td>
                        <td style="padding:.9rem;text-align:right;color:#4ADE80;font-weight:bold;">{s['dividend_yield']:.2f}%</td>
                        <td style="padding:.9rem;text-align:right;color:#94a3b8;">{s['payout_ratio']:.1f}%</td>
                        <td style="padding:.9rem;text-align:right;color:#60a5fa;">{fcf_str}</td>
                        <td style="padding:.9rem;text-align:right;color:#a78bfa;">{streak}</td>
                        <td style="padding:.9rem;text-align:center;"><span style="padding:3px 10px;border-radius:20px;font-weight:bold;font-size:.8rem;{gs}">{gt}</span></td>
                    </tr>"""

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            pattern = re.compile(r'(<tbody id="dividendTableBody">)(.*?)(</tbody>)', re.DOTALL)
            if pattern.search(content):
                new_content = pattern.sub(rf'\1{rows}\3', content)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  [OK] {filepath}")
            else:
                print(f"  [SKIP] No dividendTableBody found in {filepath}")
        except Exception as e:
            print(f"  [ERR] {lang}: {e}")


if __name__ == "__main__":
    generate_dividend_insights()
