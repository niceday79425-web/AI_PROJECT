import re

pages = [
    (r'd:\AI_PROJECT\ko\list.html', 'ko'),
    (r'd:\AI_PROJECT\pt\list.html', 'pt'),
]

sort_labels = {
    'ko': ['수익률 순', '등급 순', 'FCF 커버 순', '연속 성장 순', '티커 순'],
    'pt': ['Por Rendimento', 'Por Nota', 'Por FCF', 'Por Streak', 'Por Ticker'],
}

card_js = '''
                data.forEach(stock => {
                    const card = document.createElement('div');
                    card.className = 'stock-card-compact';
                    const fcf = stock.fcf_coverage > 0 ? stock.fcf_coverage.toFixed(1) + 'x' : 'N/A';
                    const fcfColor = stock.fcf_coverage >= 1.5 ? '#10b981' : stock.fcf_coverage >= 1.0 ? '#f59e0b' : stock.fcf_coverage > 0 ? '#ef4444' : '#6b7280';
                    const streak = stock.dividend_growth_years > 0 ? stock.dividend_growth_years + ' yr' : 'N/A';
                    const streakColor = stock.dividend_growth_years >= 25 ? '#fbbf24' : stock.dividend_growth_years >= 10 ? '#10b981' : stock.dividend_growth_years > 0 ? '#60a5fa' : '#6b7280';
                    card.innerHTML = `
                        <div class="stock-row-1">
                            <div class="stock-ticker">${stock.ticker}</div>
                            <div class="stock-price">$${stock.current_price || '0.00'}</div>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:0.6rem;">
                            <div style="flex:1;">
                                <div style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.2rem;">${stock.name}</div>
                                <div style="font-size:0.75rem; color:var(--accent-blue); font-weight:600;">${stock.sector || 'Etc'}</div>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-size:0.7rem; color:var(--text-secondary); margin-bottom:0.15rem;">Dividend Yield</div>
                                <div style="font-weight:800; color:var(--success); font-size:1.2rem;">${stock.dividend_yield}%</div>
                            </div>
                        </div>
                        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.4rem; margin-bottom:0.6rem;">
                            <div style="background:rgba(255,255,255,0.04); border-radius:8px; padding:0.4rem 0.5rem; text-align:center;">
                                <div style="font-size:0.65rem; color:var(--text-secondary); margin-bottom:0.15rem;">Payout</div>
                                <div style="font-size:0.85rem; font-weight:700; color:${stock.payout_ratio > 0 && stock.payout_ratio <= 60 ? '#10b981' : stock.payout_ratio <= 80 ? '#f59e0b' : '#ef4444'};">${stock.payout_ratio > 0 ? stock.payout_ratio.toFixed(0)+'%' : 'N/A'}</div>
                            </div>
                            <div style="background:rgba(255,255,255,0.04); border-radius:8px; padding:0.4rem 0.5rem; text-align:center;">
                                <div style="font-size:0.65rem; color:var(--text-secondary); margin-bottom:0.15rem;">FCF Cover</div>
                                <div style="font-size:0.85rem; font-weight:700; color:${fcfColor};">${fcf}</div>
                            </div>
                            <div style="background:rgba(255,255,255,0.04); border-radius:8px; padding:0.4rem 0.5rem; text-align:center;">
                                <div style="font-size:0.65rem; color:var(--text-secondary); margin-bottom:0.15rem;">Streak</div>
                                <div style="font-size:0.85rem; font-weight:700; color:${streakColor};">${streak}</div>
                            </div>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="font-size:0.75rem; color:var(--text-secondary);">Grade: ${getGradeBadge(stock.grade)}</div>
                            <div style="font-size:0.7rem; color:var(--text-secondary);">${stock.last_updated ? stock.last_updated.slice(0,10) : ''}</div>
                        </div>
                    `;
                    stockGrid.appendChild(card);
                });'''

sort_js = """                filtered.sort((a, b) => {
                    if (sortType === 'yield')   return b.dividend_yield - a.dividend_yield;
                    if (sortType === 'ticker')  return a.ticker.localeCompare(b.ticker);
                    if (sortType === 'fcf')     return (b.fcf_coverage || 0) - (a.fcf_coverage || 0);
                    if (sortType === 'streak')  return (b.dividend_growth_years || 0) - (a.dividend_growth_years || 0);
                    if (sortType === 'grade') {
                        const grades = { 'S\ub4f1\uae09': 4, 'A\ub4f1\uae09': 3, 'B\ub4f1\uae09': 2, 'C\ub4f1\uae09': 1 };
                        return grades[b.grade] - grades[a.grade];
                    }
                });"""

for filepath, lang in pages:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    sl = sort_labels[lang]

    # 1. Update sort options
    new_sort = (
        '<select id="sortBy"\n'
        '                        style="padding: 0.75rem; border: 1px solid #333; background: #1a1a1a; color: white; border-radius: 8px;">\n'
        f'                        <option value="yield">{sl[0]}</option>\n'
        f'                        <option value="grade">{sl[1]}</option>\n'
        f'                        <option value="fcf">{sl[2]}</option>\n'
        f'                        <option value="streak">{sl[3]}</option>\n'
        f'                        <option value="ticker">{sl[4]}</option>\n'
        '                    </select>'
    )
    content = re.sub(r'<select id="sortBy".*?</select>', new_sort, content, flags=re.S)

    # 2. Replace card render block
    old_card_pat = re.compile(r'data\.forEach\(stock\s*=>\s*\{.*?stockGrid\.appendChild\(card\);\s*\}\);', re.S)
    content = old_card_pat.sub(card_js.strip(), content, count=1)

    # 3. Replace sort logic
    old_sort_pat = re.compile(r'filtered\.sort\(\(a,\s*b\)\s*=>\s*\{.*?\}\);', re.S)
    content = old_sort_pat.sub(sort_js.strip(), content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")
