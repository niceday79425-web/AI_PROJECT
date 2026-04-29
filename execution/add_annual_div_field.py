import re

PAGES = [
    (r"d:\AI_PROJECT\ko\list.html", "Annual Dividend", "Dividend Yield"),
    (r"d:\AI_PROJECT\pt\list.html", "Dividendo Anual",  "Rendimento"),
]

OLD = (
    '<div style="font-size:0.7rem; color:var(--text-secondary); margin-bottom:0.15rem;">Dividend Yield</div>\n'
    '                                <div style="font-weight:800; color:var(--success); font-size:1.2rem;">${stock.dividend_yield}%</div>'
)

for filepath, ann_label, yield_label in PAGES:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_block = (
        f'<div style="font-size:0.7rem; color:var(--text-secondary); margin-bottom:0.1rem;">{ann_label}</div>\n'
        '                                <div style="font-weight:700; color:#a78bfa; font-size:0.95rem; margin-bottom:0.15rem;">'
        "${stock.annual_dividend > 0 ? '$' + stock.annual_dividend.toFixed(2) + ' / yr' : 'N/A'}</div>\n"
        f'                                <div style="font-size:0.7rem; color:var(--text-secondary); margin-bottom:0.1rem;">{yield_label}</div>\n'
        '                                <div style="font-weight:800; color:var(--success); font-size:1.2rem;">${stock.dividend_yield}%</div>'
    )

    if OLD in content:
        content = content.replace(OLD, new_block, 1)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] {filepath}")
    else:
        print(f"[SKIP] Pattern not found in {filepath}")
