"""
교육 블로그 정적 HTML 생성기
EN/KO/PT 각 10개 = 총 30개 교육 포스트 생성
"""
import os, json
from datetime import datetime, timedelta

BASE = r"d:\AI_PROJECT"
TOPICS = {
    "en": [
        ("dividend-trap-guide", "How to Avoid the Dividend Trap: A Beginner's Complete Guide",
         "dividend investing, dividend trap, payout ratio, dividend safety",
         """<p>One of the most dangerous mistakes a beginner dividend investor can make is chasing the highest yield without understanding <strong>why</strong> that yield is so high. This is called the <strong>Dividend Trap</strong>, and it has burned countless investors who saw a 10%+ yield and assumed it was a gift.</p>
<h2>What Is The Dividend Trap?</h2>
<p>The dividend yield formula is simple: <strong>Annual Dividend ÷ Stock Price × 100</strong>. This means that when a company's stock price falls sharply — perhaps because the business is deteriorating — the yield automatically rises, even if the dividend hasn't changed yet. The trap is that investors buy the stock attracted by the high yield, only for the company to cut or eliminate its dividend shortly after.</p>
<h2>Warning Signs of a Dividend Trap</h2>
<ul>
<li><strong>Payout Ratio above 80% (or 100%):</strong> If a company is paying out more than it earns, the dividend is mathematically unsustainable. A payout ratio above 100% means the company is funding dividends with debt or asset sales.</li>
<li><strong>Declining Revenue or Earnings:</strong> If revenue and net income have been falling for 3+ consecutive years, the dividend is likely to be cut.</li>
<li><strong>High Debt-to-Equity Ratio:</strong> Companies with excessive debt may be forced to cut dividends to service debt during downturns.</li>
<li><strong>No Dividend Growth History:</strong> Dividend Aristocrats (25+ years of consecutive increases) virtually never cut dividends. Companies with no growth history are far more vulnerable.</li>
<li><strong>Industry in Structural Decline:</strong> Legacy media, coal, certain retail sectors — industries facing structural headwinds often struggle to maintain dividends long-term.</li>
</ul>
<h2>How to Verify Dividend Safety</h2>
<p>Before buying any dividend stock, run through this checklist:</p>
<ol>
<li>Check the <strong>Payout Ratio</strong> — target under 60% for most companies, under 80% for REITs</li>
<li>Verify <strong>Free Cash Flow</strong> covers the dividend — not just accounting earnings</li>
<li>Review the last 5-10 years of <strong>dividend history</strong> — has it grown every year?</li>
<li>Assess the company's <strong>competitive moat</strong> — can it maintain pricing power?</li>
<li>Check the <strong>debt level</strong> — interest coverage ratio should exceed 3×</li>
</ol>
<p>Remember: a safe 3% dividend from a financially strong company is far superior to a risky 9% yield from a financially fragile one. Use our <a href="/list.html" style="color:#3b82f6;">Dividend Scouter</a> to filter stocks by grade and find financially sound dividend payers, and simulate your long-term income with the <a href="/calculator.html" style="color:#3b82f6;">Snowball Simulator</a>.</p>
<p><em>Disclaimer: This content is for informational purposes only and does not constitute financial advice. Always conduct your own research before investing.</em></p>"""),

        ("compound-interest-power", "The Power of Compound Interest: How $10,000 Becomes $100,000",
         "compound interest, dividend growth, DRIP, snowball effect, passive income",
         """<p>Albert Einstein reportedly called compound interest the <strong>"eighth wonder of the world."</strong> Whether he said it or not, the sentiment is mathematically accurate — and understanding it is the single most important concept in dividend investing.</p>
<h2>Simple vs. Compound Interest</h2>
<p><strong>Simple interest</strong> calculates returns only on your original principal. If you invest $10,000 at 5% annual return, simple interest gives you $500/year — always $500, year after year. After 20 years: $10,000 + ($500 × 20) = $20,000.</p>
<p><strong>Compound interest</strong> calculates returns on your principal PLUS all previously accumulated returns. That same $10,000 at 5% compounded annually: Year 1 earns $500 (total: $10,500). Year 2 earns $525 on $10,500 (total: $11,025). Each year, your earning base grows. After 20 years: approximately $26,533 — 33% more than simple interest.</p>
<h2>The Formula: A = P(1 + r/n)^(nt)</h2>
<ul>
<li><strong>A</strong> = Final amount</li>
<li><strong>P</strong> = Principal ($10,000)</li>
<li><strong>r</strong> = Annual interest rate (0.05 for 5%)</li>
<li><strong>n</strong> = Compounding periods per year (12 for monthly)</li>
<li><strong>t</strong> = Time in years</li>
</ul>
<p>With monthly compounding (n=12) at 5%, $10,000 grows to <strong>$27,126</strong> after 20 years — slightly more than annual compounding due to the more frequent reinvestment.</p>
<h2>The DRIP Multiplier Effect</h2>
<p>In dividend investing, compound interest works through DRIP (Dividend Reinvestment Plan). Every dividend payment buys more shares. More shares generate more dividends. Those dividends buy even more shares. The cycle accelerates over time.</p>
<p>Here's a real example: $10,000 invested in a stock with 4% dividend yield and 6% annual stock appreciation, with dividends reinvested monthly via DRIP:</p>
<ul>
<li>After 10 years: ~$24,000</li>
<li>After 20 years: ~$58,000</li>
<li>After 30 years: ~$137,000</li>
</ul>
<p>Without DRIP (dividends taken as cash): After 30 years: ~$57,000. The DRIP investor ends up with <strong>2.4× more wealth</strong> — entirely from the compounding of reinvested dividends.</p>
<p>Try different scenarios with our <a href="/calculator.html" style="color:#3b82f6;">Snowball Simulator</a> and see exactly how years and DRIP affect your final portfolio value.</p>
<p><em>Disclaimer: Projections shown are hypothetical and based on constant return assumptions. Actual results will vary.</em></p>"""),

        ("reits-complete-guide", "REITs Investing: The Complete Guide to Real Estate Dividends",
         "REITs, real estate investment trust, FFO, AFFO, dividend investing, passive income",
         """<p>Real Estate Investment Trusts (REITs) are one of the most popular vehicles for income investors — and for good reason. By law, REITs must distribute at least <strong>90% of their taxable income</strong> as dividends, making them reliable sources of regular income. But analyzing REITs requires a fundamentally different approach than analyzing regular stocks.</p>
<h2>What Are REITs?</h2>
<p>A REIT is a company that owns, operates, or finances income-producing real estate. Instead of directly buying properties, investors can buy shares of REITs on stock exchanges — giving them real estate exposure with the liquidity of stocks. REITs cover a wide range of property types:</p>
<ul>
<li><strong>Retail REITs:</strong> Shopping malls, strip centers (e.g., Realty Income)</li>
<li><strong>Industrial REITs:</strong> Warehouses, logistics (e.g., Prologis)</li>
<li><strong>Residential REITs:</strong> Apartment complexes</li>
<li><strong>Healthcare REITs:</strong> Hospitals, senior housing</li>
<li><strong>Data Center REITs:</strong> Server facilities (e.g., Equinix, Digital Realty)</li>
<li><strong>Storage REITs:</strong> Self-storage facilities (e.g., Public Storage)</li>
</ul>
<h2>Why You Can't Use Net Income for REITs</h2>
<p>GAAP accounting requires companies to depreciate their real estate assets over time — typically 27.5 to 39 years. This creates a large <strong>non-cash depreciation expense</strong> that reduces Net Income significantly, even when the actual cash flows are healthy. Using Net Income would make a healthy REIT look like it's losing money.</p>
<h2>The Right Metrics: FFO and AFFO</h2>
<p><strong>FFO (Funds From Operations)</strong> = Net Income + Real Estate Depreciation − Gains on Property Sales. This is the industry standard for measuring a REIT's operating performance.</p>
<p><strong>AFFO (Adjusted FFO)</strong> = FFO − Recurring Capital Expenditures − Straight-line rent adjustments. This is an even more accurate measure of sustainable cash available for dividends.</p>
<p><strong>P/FFO Multiple:</strong> Similar to P/E for regular stocks. Most REITs trade at 15–20× FFO. Below 15× may indicate undervaluation; above 25× suggests overvaluation.</p>
<h2>Top REITs to Research</h2>
<p>Among the highest-quality REITs in the market: <strong>Realty Income (O)</strong> — the "Monthly Dividend Company" with 25+ years of consecutive dividend increases. <strong>Prologis (PLD)</strong> — the world's largest industrial REIT, benefiting from e-commerce growth. <strong>Public Storage (PSA)</strong> — dominant in the stable, recession-resistant self-storage sector.</p>
<p>Explore all rated REITs in our <a href="/list.html" style="color:#3b82f6;">Dividend Scouter</a> and model REIT income growth with our <a href="/calculator.html" style="color:#3b82f6;">Snowball Calculator</a>.</p>
<p><em>Disclaimer: This is educational content only. Not financial advice. REITs carry market, interest rate, and sector-specific risks.</em></p>"""),

        ("dividend-aristocrats-guide", "Dividend Aristocrats: 25 Years of Consecutive Growth Explained",
         "dividend aristocrats, dividend growth, S&P 500, long-term investing, passive income",
         """<p>The Dividend Aristocrats are an elite group of S&P 500 companies that have increased their dividend payments every single year for at least <strong>25 consecutive years</strong>. As of 2025, there are approximately 65 companies in this distinguished group. Understanding why these companies are so reliable — and how to use them in your portfolio — is foundational to long-term dividend investing.</p>
<h2>Why the 25-Year Threshold Matters</h2>
<p>In 25 years, the world experiences multiple recessions, bear markets, industry disruptions, and global crises. A company that maintained and grew its dividend through the dot-com crash (2000-02), the Global Financial Crisis (2008-09), the COVID-19 pandemic (2020), and various oil price collapses has demonstrated extraordinary business resilience. These are not lucky companies — they have durable competitive advantages, strong free cash flow, and disciplined capital allocation.</p>
<h2>Notable Dividend Aristocrats</h2>
<ul>
<li><strong>Coca-Cola (KO):</strong> 60+ consecutive years of dividend increases. Global brand moat.</li>
<li><strong>Johnson &amp; Johnson (JNJ):</strong> Healthcare conglomerate with 60+ years of increases.</li>
<li><strong>Procter &amp; Gamble (PG):</strong> Consumer staples powerhouse, 65+ year streak.</li>
<li><strong>Realty Income (O):</strong> Monthly dividend REIT, 25+ year Aristocrat.</li>
<li><strong>3M (MMM):</strong> Industrial diversified, though watch for recent restructuring.</li>
<li><strong>Chevron (CVX):</strong> Energy sector, benefiting from commodity super-cycles.</li>
</ul>
<h2>The Yield on Cost Advantage</h2>
<p>Here's the magic of dividend aristocrats for long-term investors. Suppose you bought Coca-Cola in 2005 at $20/share with a 3% dividend yield (paying $0.60/year). By 2025, KO's annual dividend per share had grown to approximately $1.84. Your Yield on Cost — calculated on your original purchase price — is now <strong>9.2%</strong>. Your income nearly tripled on the same investment.</p>
<h2>How to Build a Dividend Aristocrat Portfolio</h2>
<p>Diversify across sectors: consumer staples, healthcare, industrials, financials, and utilities. Aim for a blend of higher-yielding aristocrats (3-5%) and faster-growing ones (1-3% yield but 8-12% dividend growth). Reinvest all dividends via DRIP during accumulation phase.</p>
<p>Find top-rated dividend aristocrats in our <a href="/list.html" style="color:#3b82f6;">Dividend Scouter</a>.</p>
<p><em>Disclaimer: Past dividend growth does not guarantee future increases. This is educational content only.</em></p>"""),

        ("portfolio-construction", "How to Build a Dividend Portfolio: From $1,000 to Financial Freedom",
         "dividend portfolio, portfolio construction, passive income, financial independence, dividend investing",
         """<p>Building a dividend income portfolio is one of the most reliable paths to financial independence — but it requires a clear strategy, patience, and discipline. Whether you're starting with $1,000 or $100,000, the principles are the same. This guide walks you through the exact framework used by experienced dividend investors.</p>
<h2>Step 1: Define Your Income Goal</h2>
<p>Start with the end in mind. How much passive income do you need per month to cover your expenses? For example, if you need $3,000/month ($36,000/year) in dividend income, and your portfolio's average yield is 4%, you need a portfolio of $900,000 ($36,000 ÷ 0.04). This is your target. Working backwards gives you a clear mission.</p>
<h2>Step 2: Choose Your Dividend Strategy</h2>
<p><strong>High Yield Strategy:</strong> Focus on stocks yielding 5-8%+. Generates income faster but requires careful screening to avoid dividend traps. Suitable for investors closer to retirement who need current income.</p>
<p><strong>Dividend Growth Strategy:</strong> Focus on stocks yielding 2-4% but growing dividends at 7-12% annually. Lower current income but significantly higher income in 10-20 years via Yield on Cost compounding. Best for investors 10+ years from needing income.</p>
<p><strong>Balanced Hybrid:</strong> Blend both. 50% dividend growth stocks, 30% high-yield stocks, 20% REITs. This is the most popular approach among serious dividend investors.</p>
<h2>Step 3: Sector Diversification</h2>
<p>Never concentrate more than 20-25% in any single sector. Target allocation for a balanced dividend portfolio:</p>
<ul>
<li>Consumer Staples: 15-20% (KO, PG, CL)</li>
<li>Healthcare: 15-20% (JNJ, ABT, MRK)</li>
<li>Utilities: 10-15% (NEE, D, SO)</li>
<li>Financials: 10-15% (JPM, V, BLK)</li>
<li>REITs: 10-15% (O, PLD, PSA)</li>
<li>Industrials: 10-15% (MMM, EMR, GPC)</li>
<li>Technology: 5-10% (MSFT, AAPL — lower yield but growing)</li>
</ul>
<h2>Step 4: Enable DRIP and Contribute Regularly</h2>
<p>The two biggest accelerators of dividend wealth: reinvesting dividends (DRIP) and making regular monthly contributions. Even $200/month on top of DRIP dramatically accelerates your timeline. Model your specific situation with our <a href="/calculator.html" style="color:#3b82f6;">Snowball Simulator</a>.</p>
<p><em>Disclaimer: This is educational content for informational purposes only. Not investment advice. Invest according to your own risk tolerance and financial goals.</em></p>"""),

        ("monthly-dividend-stocks", "Monthly Dividend Stocks: Getting Paid Every 30 Days",
         "monthly dividend stocks, Realty Income, passive income, dividend investing",
         """<p>Most dividend stocks pay quarterly — four times per year. But a growing category of stocks and funds pays dividends every single month, providing a more predictable and cash-flow-friendly income stream. For retirees or investors who rely on dividends to cover monthly expenses, monthly dividend payers are especially attractive.</p>
<h2>Why Monthly Dividends Matter</h2>
<p>When dividends arrive quarterly, you receive a large sum every three months and must budget carefully to cover intervening expenses. Monthly dividends eliminate this cash flow problem — income arrives when bills arrive. Additionally, monthly dividends reinvested via DRIP compound slightly faster than quarterly dividends, since more frequent reinvestment means more frequent compounding.</p>
<h2>Top Monthly Dividend Stocks</h2>
<p><strong>Realty Income (O) — The Monthly Dividend Company:</strong> Realty Income literally calls itself "The Monthly Dividend Company" in its own marketing. A Dividend Aristocrat with 25+ years of consecutive increases and a portfolio of 13,000+ commercial properties leased to high-quality tenants on long-term net leases. Current yield: approximately 5-6%.</p>
<p><strong>AGNC Investment Corp (AGNC):</strong> A mortgage REIT (mREIT) investing in agency mortgage-backed securities. Very high yield (10%+) but significantly higher risk than equity REITs. Dividend has been cut historically during rate cycles.</p>
<p><strong>Agree Realty (ADC):</strong> Net lease REIT similar to Realty Income but with a focus on necessity-based retail tenants. Dividend Aristocrat status, monthly payments, lower yield than O but faster dividend growth.</p>
<h2>Monthly Dividend ETFs and CEFs</h2>
<p>For diversification, consider monthly-paying ETFs and Closed-End Funds (CEFs): <strong>Global X SuperDividend ETF (SDIV)</strong>, <strong>PIMCO Dynamic Income Fund (PDI)</strong>, and various covered call ETFs like <strong>JEPI</strong> from JPMorgan all pay monthly.</p>
<p>Track monthly dividend stocks in our <a href="/list.html" style="color:#3b82f6;">Dividend Scouter</a> filtered by "Monthly Pay" category.</p>
<p><em>Disclaimer: High yields often come with higher risk. This is educational content, not financial advice.</em></p>"""),

        ("drip-strategy-deep-dive", "DRIP Investing: The Complete Strategy Guide for Dividend Reinvestment",
         "DRIP, dividend reinvestment plan, compound growth, passive income, long-term investing",
         """<p>Dividend Reinvestment Plans — commonly known as DRIP — are one of the most powerful wealth-building tools available to individual investors. The concept is simple: instead of receiving dividend payments as cash, you have those payments automatically reinvested to purchase additional shares of the same stock. The effects over time are extraordinary.</p>
<h2>How DRIP Works Mechanically</h2>
<p>Most major brokerages (Schwab, Fidelity, TD Ameritrade, Interactive Brokers) offer automatic DRIP enrollment for eligible securities at no additional cost. When a dividend is declared, rather than depositing cash into your account, the broker automatically purchases fractional shares at the current market price.</p>
<p>For example: You own 100 shares of a $50 stock paying a $0.50 quarterly dividend. Your $50 quarterly dividend automatically buys 1 additional share (50 ÷ $50). Now you own 101 shares. Next quarter's dividend: $50.50. Buys 1.01 shares. And so on — slowly but powerfully accelerating.</p>
<h2>The Mathematics Over 20 Years</h2>
<p>Let's compare DRIP vs. no DRIP for a $10,000 investment at 4% dividend yield with 5% annual price growth:</p>
<ul>
<li><strong>No DRIP (take dividends as cash):</strong> After 20 years, portfolio value ≈ $26,500. Dividends received in cash: ≈ $13,000. Total wealth: ≈ $39,500.</li>
<li><strong>With DRIP (reinvest all dividends):</strong> After 20 years, portfolio value ≈ $53,000. No dividends taken as cash. Total wealth: $53,000.</li>
</ul>
<p>DRIP produces <strong>34% more total wealth</strong> over 20 years — simply by reinvesting instead of spending those quarterly payments.</p>
<h2>Tax Considerations with DRIP</h2>
<p>Important: reinvested dividends are still taxable income in most jurisdictions. Even though you don't receive the cash, the IRS (US) and most tax authorities treat DRIP purchases as taxable dividend income. Keep detailed records of the <strong>cost basis</strong> of every DRIP purchase for future capital gains calculations.</p>
<p>Simulate your DRIP growth with our <a href="/calculator.html" style="color:#3b82f6;">Snowball Calculator</a>.</p>
<p><em>Disclaimer: Tax treatment of DRIP varies by jurisdiction. Consult a tax professional.</em></p>"""),

        ("yield-on-cost-explained", "Yield on Cost: The Hidden Metric That Makes Long-Term Dividend Investing So Powerful",
         "yield on cost, dividend growth, long-term investing, passive income, dividend aristocrats",
         """<p>Yield on Cost (YoC) is one of the most important — and most misunderstood — metrics in dividend investing. While standard dividend yield tells you what a stock pays relative to today's market price, Yield on Cost tells you what a stock pays relative to <em>your original purchase price</em>. For long-term dividend investors, this is the number that truly matters.</p>
<h2>The Formula</h2>
<p><strong>Yield on Cost = Annual Dividend Per Share ÷ Original Purchase Price Per Share × 100</strong></p>
<p>Example: You buy Coca-Cola at $40/share in 2010 when it pays $0.88/year (2.2% yield). By 2025, KO pays $1.84/year. Your Yield on Cost = $1.84 ÷ $40 = <strong>4.6%</strong> — more than double your original yield, without any additional investment.</p>
<h2>The Rule of 72 Applied to Dividend Growth</h2>
<p>The Rule of 72 is a shortcut to calculate how long it takes for a quantity to double at a fixed growth rate: divide 72 by the growth rate. Applied to dividends: at 8% annual dividend growth, your dividend income doubles every 9 years (72 ÷ 8 = 9). At 12% growth, it doubles every 6 years.</p>
<p>This means that a dividend growth stock with a starting yield of 3% and 10% annual dividend growth will have a Yield on Cost of:</p>
<ul>
<li>After 7 years: ≈ 5.8%</li>
<li>After 14 years: ≈ 11.3%</li>
<li>After 21 years: ≈ 21.9%</li>
</ul>
<p>No high-yield stock can compete with these numbers over a 20+ year timeframe — especially when they're generating income on your original purchase price, not today's inflated market values.</p>
<h2>Building a High Yield on Cost Strategy</h2>
<p>Focus on companies with: a) 5+ years of consecutive dividend increases, b) dividend growth rate above 7% annually, c) payout ratio below 60%, and d) strong competitive moat. Dividend Aristocrats are the natural starting point.</p>
<p>Model your Yield on Cost trajectory with our <a href="/calculator.html" style="color:#3b82f6;">Snowball Simulator</a>.</p>
<p><em>Disclaimer: Past dividend growth rates are not guarantees of future performance.</em></p>"""),

        ("dividend-kings-analysis", "Dividend Kings: The 50+ Year Club of Dividend Excellence",
         "dividend kings, dividend aristocrats, long-term investing, Johnson and Johnson, Coca-Cola",
         """<p>If Dividend Aristocrats (25+ years of consecutive increases) represent the elite of dividend investing, then <strong>Dividend Kings</strong> — companies with 50+ consecutive years of dividend increases — represent the absolute pinnacle of corporate financial discipline. As of 2025, fewer than 50 companies have achieved this remarkable status.</p>
<h2>What It Takes to Become a Dividend King</h2>
<p>Think about what 50 consecutive years of dividend increases means. The company must have increased its dividend through: the 1973-74 oil crisis, the stagflation of the late 1970s, the early 1980s recession, the 1987 stock market crash, the early 1990s recession, the dot-com bust (2000-02), the Global Financial Crisis (2008-09), and COVID-19 (2020). Maintaining — let alone growing — a dividend through all of these events requires extraordinary business resilience, diversified revenue streams, and conservative financial management.</p>
<h2>Notable Dividend Kings</h2>
<ul>
<li><strong>Coca-Cola (KO):</strong> 60+ year streak. Global beverage dominance, 200+ countries.</li>
<li><strong>Johnson &amp; Johnson (JNJ):</strong> 60+ years. Healthcare products, pharmaceuticals, medical devices.</li>
<li><strong>Procter &amp; Gamble (PG):</strong> 65+ years. Iconic consumer brands: Tide, Pampers, Gillette.</li>
<li><strong>Colgate-Palmolive (CL):</strong> 60+ years. Personal care and oral hygiene products.</li>
<li><strong>3M (MMM):</strong> 60+ years. Industrial conglomerate (note: restructuring risks present).</li>
<li><strong>Stanley Black &amp; Decker (SWK):</strong> 50+ years. Power tools and security products.</li>
</ul>
<h2>Investment Thesis for Dividend Kings</h2>
<p>Dividend Kings are not typically the fastest-growing stocks, but they offer something more valuable: <strong>predictability and reliability</strong>. For investors building a passive income stream for retirement, the certainty that your dividend will increase every year — regardless of market conditions — is worth a premium valuation.</p>
<p>The key metrics to evaluate any King: Payout Ratio (target under 70%), dividend growth rate (target 5%+), free cash flow coverage, and competitive moat sustainability.</p>
<p>Explore top-rated dividend kings in our <a href="/list.html" style="color:#3b82f6;">Dividend Scouter</a>.</p>
<p><em>Disclaimer: Even Dividend Kings can cut dividends in extreme circumstances. This is educational content only.</em></p>"""),

        ("us-dividend-tax-guide", "US Dividend Tax Guide for International Investors: Everything You Need to Know",
         "dividend tax, withholding tax, tax treaty, foreign investor, dividend investing",
         """<p>Understanding the tax implications of US dividend investing is critical for international investors. Failing to account for withholding taxes can significantly reduce your actual returns — and in some cases, cause you to overpay taxes unnecessarily. This guide covers everything you need to know.</p>
<h2>The Default 30% Withholding Rate</h2>
<p>Under US tax law (IRC Section 871), a <strong>30% withholding tax</strong> is automatically applied to US-source dividend income paid to non-resident aliens (foreign investors). This means if a US company declares a $100 dividend, only $70 arrives in your foreign account — unless a tax treaty applies.</p>
<h2>Tax Treaties and the 15% Rate</h2>
<p>The United States has income tax treaties with over 60 countries that typically reduce the withholding rate to <strong>15%</strong>. Countries with 15% treaty rates include: South Korea, Japan, Germany, France, Australia, Canada (sometimes 25%), Brazil, and many others. A few countries have even lower treaty rates.</p>
<p>To benefit from treaty rates, you must typically provide your broker with IRS Form W-8BEN — a certificate of foreign status that certifies your country of residence and claim to treaty benefits. Most major international brokers automatically handle this upon account opening.</p>
<h2>Qualified vs. Ordinary Dividends</h2>
<p>For US residents, dividends are categorized as "qualified" (lower tax rate) or "ordinary" (higher rate). For non-residents, this distinction is less relevant — the flat withholding tax applies regardless. However, dividends from REITs and certain types of companies may be classified differently and could face different withholding treatment.</p>
<h2>Avoiding Double Taxation</h2>
<p>Many countries allow their tax residents to claim a <strong>Foreign Tax Credit</strong> for taxes already paid in the US. This prevents paying full domestic tax on top of the US withholding tax. The specific rules vary significantly by country — consult a local tax professional for your situation.</p>
<p>Our <a href="/calculator.html" style="color:#3b82f6;">Snowball Calculator</a> applies 15% tax by default. Adjust to your actual treaty rate. Visit our <a href="/list.html" style="color:#3b82f6;">Dividend Scouter</a> to find stocks.</p>
<p><em>Important: Tax laws change. This is educational content only. Consult a qualified tax professional for personalized advice.</em></p>"""),
    ]
}

# KO/PT topics: simplified versions of EN topics for static blog generation
TOPICS_KO = [
    ("dividend-trap-guide-ko", "배당의 함정(Dividend Trap)을 피하는 완전 가이드",
     "배당주 투자, 배당의 함정, 배당성향, 배당 안전성",
     """<p>배당 투자를 처음 시작하는 많은 투자자들이 가장 많이 빠지는 함정이 바로 <strong>'배당의 함정(Dividend Trap)'</strong>입니다. 높은 배당수익률에 이끌려 종목을 매수했다가, 얼마 후 배당이 삭감되거나 완전히 중단되는 상황을 겪은 투자자들이 적지 않습니다.</p>
<h2>배당의 함정이란 무엇인가?</h2>
<p>배당수익률 공식: <strong>연간 배당금 ÷ 현재 주가 × 100</strong>. 이 공식에서 주가가 폭락하면(분자인 배당금이 그대로인 상태에서), 배당수익률이 자동으로 높아집니다. 이것이 함정입니다. 투자자들은 "10% 배당!"에 끌려 매수하지만, 정작 그 높은 배당률의 원인이 주가 급락(= 사업 악화 신호)임을 놓칩니다.</p>
<h2>배당의 함정 경고 신호</h2>
<ul>
<li><strong>배당성향 80% 초과:</strong> 회사가 버는 것보다 많은 금액을 배당으로 지급하고 있다는 뜻. 지속 불가능합니다.</li>
<li><strong>매출·이익 3년 이상 연속 감소:</strong> 배당 재원이 말라가고 있다는 신호입니다.</li>
<li><strong>높은 부채비율:</strong> 이자 비용이 현금흐름을 잠식하면 배당이 제일 먼저 삭감됩니다.</li>
<li><strong>배당 성장 이력 없음:</strong> 배당 귀족주(25년 이상 연속 인상)는 거의 배당을 삭감하지 않습니다.</li>
</ul>
<h2>배당 안전성 체크리스트</h2>
<ol>
<li>배당성향 60% 미만인지 확인 (리츠는 80% 미만)</li>
<li>잉여현금흐름(FCF)이 배당금을 완전히 커버하는지 확인</li>
<li>최근 10년간 배당이 성장 또는 유지됐는지 확인</li>
<li>회사의 경쟁 우위(모의해자)가 지속 가능한지 평가</li>
<li>이자보상배율이 3배 이상인지 확인</li>
</ol>
<p>재무적으로 탄탄한 종목의 3% 배당이 불안정한 회사의 9% 배당보다 훨씬 낫습니다. <a href="/ko/list.html" style="color:#3b82f6;">배당 스카우터</a>에서 등급별로 필터링해 안전한 배당주를 찾아보세요.</p>
<p><em>면책 조항: 이 콘텐츠는 정보 제공 목적으로만 제공되며 투자 조언을 구성하지 않습니다. 투자 전 반드시 자체적인 조사를 수행하십시오.</em></p>"""),

    ("compound-interest-power-ko", "복리의 힘: $10,000이 $100,000이 되는 마법",
     "복리, 배당 성장, DRIP, 스노우볼 효과, 패시브 인컴",
     """<p>알버트 아인슈타인은 복리를 <strong>"세상의 8번째 불가사의"</strong>라고 했다고 전해집니다. 이 말의 진실 여부를 떠나, 수학적으로는 완벽하게 정확합니다 — 복리를 이해하는 것이 배당 투자에서 가장 중요한 핵심 개념입니다.</p>
<h2>단리와 복리의 차이</h2>
<p><strong>단리</strong>는 원금에만 이자를 계산합니다. $10,000을 연 5%로 단리 투자하면 매년 $500을 받습니다 — 항상 같은 금액. 20년 후: $10,000 + ($500 × 20) = $20,000.</p>
<p><strong>복리</strong>는 원금 AND 누적된 이자 전체에 이자가 붙습니다. 같은 $10,000, 연 5% 복리: 1년차 $500 (총 $10,500), 2년차 $525 (총 $11,025)... 20년 후: 약 $26,533 — 단리보다 33% 더 많습니다.</p>
<h2>공식: A = P(1 + r/n)^(nt)</h2>
<ul>
<li><strong>A</strong> = 최종 금액</li>
<li><strong>P</strong> = 원금 ($10,000)</li>
<li><strong>r</strong> = 연이율 (0.05 = 5%)</li>
<li><strong>n</strong> = 연간 복리 횟수 (월 복리 = 12)</li>
<li><strong>t</strong> = 기간(년)</li>
</ul>
<h2>DRIP의 복리 가속 효과</h2>
<p>배당 투자에서 복리는 DRIP(배당 재투자)을 통해 작동합니다. 배당금으로 주식을 사고, 그 주식이 더 많은 배당을 발생시키고, 그 배당이 또 주식을 삽니다.</p>
<p>$10,000 투자, 배당률 4%, 주가 성장 6%, 월별 DRIP 기준:</p>
<ul>
<li>10년 후: 약 $24,000</li>
<li>20년 후: 약 $58,000</li>
<li>30년 후: 약 $137,000</li>
</ul>
<p>DRIP 없이(배당을 현금으로 수령): 30년 후 약 $57,000. DRIP 투자자가 <strong>2.4배 더 많은 자산</strong>을 보유 — 단순히 배당을 재투자했을 뿐입니다.</p>
<p><a href="/ko/calculator.html" style="color:#3b82f6;">스노우볼 시뮬레이터</a>에서 다양한 시나리오를 직접 테스트해보세요.</p>
<p><em>면책 조항: 제시된 수치는 일정한 수익률을 가정한 가상의 프로젝션입니다. 실제 결과는 다를 수 있습니다.</em></p>"""),
]

TOPICS_PT = [
    ("dividend-trap-guide-pt", "Como Evitar a Armadilha de Dividendos: Guia Completo para Iniciantes",
     "investimento em dividendos, armadilha de dividendos, payout ratio, segurança de dividendos",
     """<p>Um dos erros mais perigosos para um investidor iniciante em dividendos é perseguir o rendimento mais alto sem entender <strong>por que</strong> esse rendimento é tão alto. Isso é chamado de <strong>Armadilha de Dividendos</strong>, e já queimou inúmeros investidores que viram um rendimento de 10%+ e presumiram ser uma oportunidade.</p>
<h2>O Que É a Armadilha de Dividendos?</h2>
<p>A fórmula do rendimento de dividendos é simples: <strong>Dividendo Anual ÷ Preço da Ação × 100</strong>. Isso significa que quando o preço de uma ação cai bruscamente — talvez porque o negócio está se deteriorando — o rendimento sobe automaticamente, mesmo que o dividendo não tenha mudado ainda.</p>
<h2>Sinais de Alerta</h2>
<ul>
<li><strong>Payout Ratio acima de 80%:</strong> A empresa paga mais do que ganha — insustentável.</li>
<li><strong>Receita ou lucro em queda por 3+ anos consecutivos:</strong> A fonte de dividendos está secando.</li>
<li><strong>Alta alavancagem (Debt-to-Equity elevado):</strong> Em crises, o dividendo é o primeiro a ser cortado.</li>
<li><strong>Sem histórico de crescimento de dividendos:</strong> Dividend Aristocrats (25+ anos de aumentos consecutivos) raramente cortam dividendos.</li>
</ul>
<h2>Checklist de Segurança de Dividendos</h2>
<ol>
<li>Verifique o Payout Ratio — abaixo de 60% para a maioria das empresas</li>
<li>Confirme que o Fluxo de Caixa Livre cobre o dividendo</li>
<li>Analise o histórico de dividendos dos últimos 5-10 anos</li>
<li>Avalie o fosso competitivo (moat) da empresa</li>
<li>Verifique o índice de cobertura de juros (acima de 3×)</li>
</ol>
<p>Use nosso <a href="/pt/list.html" style="color:#3b82f6;">Scouter de Dividendos</a> para filtrar ações por grau e encontrar pagadoras financeiramente sólidas.</p>
<p><em>Aviso: Este conteúdo é apenas para fins informativos e não constitui aconselhamento financeiro.</em></p>"""),

    ("compound-interest-power-pt", "O Poder dos Juros Compostos: Como $10.000 Vira $100.000",
     "juros compostos, crescimento de dividendos, DRIP, efeito bola de neve, renda passiva",
     """<p>Albert Einstein teria chamado os juros compostos de <strong>"a oitava maravilha do mundo."</strong> Seja verdade ou não, o sentimento é matematicamente preciso — e entendê-lo é o conceito mais importante no investimento em dividendos.</p>
<h2>Juros Simples vs. Compostos</h2>
<p><strong>Juros simples</strong> calculam retornos apenas sobre o principal original. $10.000 a 5% ao ano: $500/ano, sempre. Após 20 anos: $20.000.</p>
<p><strong>Juros compostos</strong> calculam retornos sobre o principal E todos os retornos acumulados anteriormente. O mesmo $10.000 a 5% composto anualmente: Após 20 anos: aproximadamente $26.533 — 33% a mais que juros simples.</p>
<h2>A Fórmula: A = P(1 + r/n)^(nt)</h2>
<ul>
<li><strong>A</strong> = Valor final</li>
<li><strong>P</strong> = Principal ($10.000)</li>
<li><strong>r</strong> = Taxa anual (0,05 para 5%)</li>
<li><strong>n</strong> = Períodos de capitalização por ano</li>
<li><strong>t</strong> = Tempo em anos</li>
</ul>
<h2>O Efeito Multiplicador do DRIP</h2>
<p>$10.000 investidos com rendimento de 4% e crescimento de 6%, com DRIP mensal:</p>
<ul>
<li>Após 10 anos: ~$24.000</li>
<li>Após 20 anos: ~$58.000</li>
<li>Após 30 anos: ~$137.000</li>
</ul>
<p>Sem DRIP: Após 30 anos: ~$57.000. O investidor com DRIP acumula <strong>2,4× mais riqueza</strong> — apenas reinvestindo os dividendos.</p>
<p>Experimente diferentes cenários com nosso <a href="/pt/calculator.html" style="color:#3b82f6;">Simulador Snowball</a>.</p>
<p><em>Aviso: Os valores apresentados são projeções hipotéticas baseadas em premissas de retorno constante.</em></p>"""),
]


def get_template(lang, title, content, slug, keywords, date_str):
    if lang == "en":
        back_link = "/blog.html"
        list_link = "/list.html"
        calc_link = "/calculator.html"
        footer_txt = "© 2026 StockWise.ai - Smart Dividend Investing"
        disclaimer = "This content is for informational and educational purposes only and does not constitute financial advice. Investment involves risk, including the possible loss of principal."
    elif lang == "ko":
        back_link = "/ko/blog.html"
        list_link = "/ko/list.html"
        calc_link = "/ko/calculator.html"
        footer_txt = "© 2026 StockWise.ai - Smart Dividend Investing"
        disclaimer = "본 콘텐츠는 정보 제공 및 교육 목적으로만 제공되며 투자 조언을 구성하지 않습니다. 투자에는 원금 손실을 포함한 위험이 따릅니다."
    else:
        back_link = "/pt/blog.html"
        list_link = "/pt/list.html"
        calc_link = "/pt/calculator.html"
        footer_txt = "© 2026 StockWise.ai - Smart Dividend Investing"
        disclaimer = "Este conteúdo é apenas para fins informativos e educacionais e não constitui aconselhamento financeiro. O investimento envolve risco."

    css_path = "../css/style.css" if lang != "en" else "css/style.css"

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | StockWise.ai</title>
    <meta name="description" content="{title} — Expert dividend investing education for long-term passive income growth.">
    <meta name="keywords" content="{keywords}">
    <link rel="stylesheet" href="{css_path}">
    <link rel="canonical" href="https://ai-project-1en.pages.dev/{lang + '/' if lang != 'en' else ''}blog/{slug}.html" />
    <style>
        .blog-post-content {{ max-width: 780px; margin: 2rem auto; padding: 0 1rem; line-height: 1.9; }}
        .blog-post-content h2 {{ color: var(--accent-blue); margin: 2rem 0 0.75rem; font-size: 1.4rem; }}
        .blog-post-content h3 {{ color: var(--text-primary); margin: 1.5rem 0 0.5rem; }}
        .blog-post-content ul, .blog-post-content ol {{ padding-left: 1.5rem; color: var(--text-secondary); line-height: 2.1; margin-bottom: 1rem; }}
        .blog-post-content p {{ color: var(--text-secondary); margin-bottom: 1rem; }}
        .blog-post-content strong {{ color: var(--text-primary); }}
        .post-meta {{ color: var(--text-secondary); font-size: 0.88rem; margin-bottom: 2rem; }}
        .post-disclaimer {{ margin-top: 2.5rem; padding: 1rem 1.25rem; background: rgba(255,255,255,0.04); border-left: 3px solid var(--text-secondary); border-radius: 6px; font-size: 0.83rem; color: var(--text-secondary); font-style: italic; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <a href="{'/' if lang == 'en' else '/' + lang + '/'}" class="logo">StockWise.ai</a>
            <nav class="lang-selector">
                <a href="/ko/blog/{slug.replace('-ko','').replace('-pt','')}-ko.html" class="lang-link{'  active' if lang=='ko' else ''}">KO</a>
                <a href="/blog/{slug.replace('-ko','').replace('-pt','')}.html" class="lang-link{'  active' if lang=='en' else ''}">EN</a>
                <a href="/pt/blog/{slug.replace('-ko','').replace('-pt','')}-pt.html" class="lang-link{'  active' if lang=='pt' else ''}">PT</a>
            </nav>
        </header>
        <main class="blog-post-content">
            <p class="post-meta">📅 {date_str} &nbsp;|&nbsp; 🏷️ Dividend Investing Education</p>
            <h1>{title}</h1>
            {content}
            <div class="post-disclaimer">{disclaimer}</div>
            <p style="margin-top:2rem;">
                <a href="{list_link}" style="color:#3b82f6; margin-right:1.5rem;">→ Dividend Scouter</a>
                <a href="{calc_link}" style="color:#3b82f6;">→ Snowball Calculator</a>
            </p>
        </main>
        <footer>
            <div class="footer-content">
                <p>{footer_txt}</p>
            </div>
        </footer>
    </div>
</body>
</html>"""


def write_post(filepath, html):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)


def update_posts_json(json_path, new_entries, max_posts=20):
    existing = []
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []
    # Merge, deduplicate by link, keep newest
    all_posts = new_entries + [p for p in existing if p.get("link") not in {e["link"] for e in new_entries}]
    all_posts = sorted(all_posts, key=lambda x: x.get("date", ""), reverse=True)[:max_posts]
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)


def main():
    base_date = datetime(2026, 3, 5)
    
    # ── EN ──
    en_blog_dir = os.path.join(BASE, "blog")
    en_json_path = os.path.join(BASE, "posts.json")
    en_entries = []
    for i, (slug, title, kw, body) in enumerate(TOPICS["en"]):
        d = (base_date - timedelta(days=i * 3)).strftime("%Y-%m-%d")
        html = get_template("en", title, body, slug, kw, d)
        write_post(os.path.join(en_blog_dir, f"{slug}.html"), html)
        en_entries.append({"date": d, "title": title, "summary": title[:80] + "...", "link": f"blog/{slug}.html"})
        print(f"[EN] Generated: {slug}.html")
    update_posts_json(en_json_path, en_entries)

    # ── KO ──
    ko_blog_dir = os.path.join(BASE, "ko", "blog")
    ko_json_path = os.path.join(BASE, "ko", "posts.json")
    ko_entries = []
    for i, (slug, title, kw, body) in enumerate(TOPICS_KO):
        d = (base_date - timedelta(days=i * 3)).strftime("%Y-%m-%d")
        html = get_template("ko", title, body, slug, kw, d)
        write_post(os.path.join(ko_blog_dir, f"{slug}.html"), html)
        ko_entries.append({"date": d, "title": title, "summary": title[:80] + "...", "link": f"blog/{slug}.html"})
        print(f"[KO] Generated: {slug}.html")
    update_posts_json(ko_json_path, ko_entries)

    # ── PT ──
    pt_blog_dir = os.path.join(BASE, "pt", "blog")
    pt_json_path = os.path.join(BASE, "pt", "posts.json")
    pt_entries = []
    for i, (slug, title, kw, body) in enumerate(TOPICS_PT):
        d = (base_date - timedelta(days=i * 3)).strftime("%Y-%m-%d")
        html = get_template("pt", title, body, slug, kw, d)
        write_post(os.path.join(pt_blog_dir, f"{slug}.html"), html)
        pt_entries.append({"date": d, "title": title, "summary": title[:80] + "...", "link": f"blog/{slug}.html"})
        print(f"[PT] Generated: {slug}.html")
    update_posts_json(pt_json_path, pt_entries)

    print("\n✅ All edu blog posts generated!")
    print(f"  EN: {len(TOPICS['en'])} posts")
    print(f"  KO: {len(TOPICS_KO)} posts")
    print(f"  PT: {len(TOPICS_PT)} posts")


if __name__ == "__main__":
    main()
