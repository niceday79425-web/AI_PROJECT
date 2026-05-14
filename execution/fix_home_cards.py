import os
import re

# File paths
EN_INDEX = r"d:\AI_PROJECT\index.html"
KO_INDEX = r"d:\AI_PROJECT\ko\index.html"
PT_INDEX = r"d:\AI_PROJECT\pt\index.html"

def fix_homepage_cards(file_path, lang):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Academy card definitions
    cards = {
        'en': """                    <a href="/learn" class="nav-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h3>Dividend Academy</h3>
                        <p>Master dividend investing from basics to advanced strategies.</p>
                    </a>""",
        'ko': """                    <a href="/ko/learn" class="nav-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h3>배당 아카데미</h3>
                        <p>초보자부터 실전까지, 배당 투자의 모든 것을 마스터하세요.</p>
                    </a>""",
        'pt': """                    <a href="/pt/learn" class="nav-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h3>Dividend Academy</h3>
                        <p>Domine o investimento em dividendos do básico ao avançado.</p>
                    </a>"""
    }

    # If nav-grid exists, ensure academy card is there and has correct link
    if '<div class="nav-grid">' in content:
        # Check if any academy card exists
        if 'href="learn"' in content or 'href="/learn"' in content or 'href="/ko/learn"' in content or 'href="/pt/learn"' in content or 'Dividend Academy' in content or '배당 아카데미' in content:
            # Replace existing academy card with the correct one
            # Find the whole <a>...</a> block that contains academy link
            pattern = re.compile(r'<a href="[^"]*learn[^"]*" class="nav-card">.*?</a>', re.DOTALL)
            if pattern.search(content):
                content = pattern.sub(cards[lang], content)
            else:
                # If not found by pattern but exists, maybe it's slightly different
                # Just insert at the beginning of nav-grid for simplicity if we can't find it exactly
                content = content.replace('<div class="nav-grid">', '<div class="nav-grid">\n' + cards[lang])
        else:
            # Insert at the beginning of nav-grid
            content = content.replace('<div class="nav-grid">', '<div class="nav-grid">\n' + cards[lang])

    # Also fix other relative links to absolute ones for consistency
    prefix = "" if lang == "en" else f"/{lang}"
    content = content.replace('href="list"', f'href="{prefix}/list"')
    content = content.replace('href="calculator"', f'href="{prefix}/calculator"')
    content = content.replace('href="calendar"', f'href="{prefix}/calendar"')
    content = content.replace('href="fortune"', f'href="{prefix}/fortune"')
    content = content.replace('href="blog"', f'href="{prefix}/blog"')
    content = content.replace('href="about"', f'href="{prefix}/about"')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed: {file_path}")

fix_homepage_cards(EN_INDEX, 'en')
fix_homepage_cards(KO_INDEX, 'ko')
fix_homepage_cards(PT_INDEX, 'pt')
