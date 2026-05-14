import os, re

ROOT = r"d:\AI_PROJECT"

NEW_NAV_EN_ITEMS = [
    ('href="/blog.html"', 'Market Insights'),
    ('href="/learn.html"', 'Dividend Academy'),
    ('href="/list.html"', 'Dividend Scouter'),
    ('href="/calculator.html"', 'Snowball Calculator'),
    ('href="/calendar.html"', 'Dividend Calendar'),
    ('href="/about.html"', 'About'),
]

NEW_NAV_KO_ITEMS = [
    ('href="/ko/blog.html"', '마켓 인사이트'),
    ('href="/ko/learn.html"', '배당 아카데미'),
    ('href="/ko/list.html"', '배당주 스카우터'),
    ('href="/ko/calculator.html"', '스노볼 계산기'),
    ('href="/ko/calendar.html"', '배당 캘린더'),
    ('href="/ko/about.html"', '소개'),
]

NEW_NAV_PT_ITEMS = [
    ('href="/pt/blog.html"', 'Market Insights'),
    ('href="/pt/learn.html"', 'Dividend Academy'),
    ('href="/pt/list.html"', 'Dividend Scouter'),
    ('href="/pt/calculator.html"', 'Snowball Calculator'),
    ('href="/pt/calendar.html"', 'Dividend Calendar'),
    ('href="/pt/about.html"', 'About'),
]

def build_nav(active_href, items):
    nav_links = []
    for href, label in items:
        clean_href = href.replace('href="', '').replace('"', '').replace('.html', '')
        clean_active = active_href.replace('.html', '')
        
        # If it matches exactly OR if it's a sub-path of this section
        if clean_href == clean_active or (clean_href not in ["/", "/ko/", "/pt/"] and clean_active.startswith(clean_href)):
            nav_links.append(f'<a {href.replace(".html", "")} class="active">{label}</a>')
        else:
            nav_links.append(f'<a {href.replace(".html", "")}>{label}</a>')
            
    return '\n        <nav class="glass-nav">\n          ' + '\n          '.join(nav_links) + '\n        </nav>\n'

# Find existing nav (glass-nav, main-nav, or just nav immediately after header)
NAV_PATTERN = re.compile(r'<nav class="(?:glass-nav|main-nav)"[^>]*>.*?</nav>', re.DOTALL)
HEADER_PATTERN = re.compile(r'(</header>\s*)')

def force_update_nav(path, active_href, items):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    new_nav = build_nav(active_href, items)
    
    # 1. Try to replace existing glass-nav or main-nav
    if re.search(NAV_PATTERN, html):
        new_html = NAV_PATTERN.sub(new_nav.strip(), html, count=1)
    # 2. If no nav exists, inject right after </header>
    elif re.search(HEADER_PATTERN, html):
        new_html = HEADER_PATTERN.sub(r'\1' + new_nav, html, count=1)
    else:
        print(f"  [Error] Could not find <header> in {path}")
        return

    if new_html != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"  [Updated Nav] {path}")

def force_academy_card(path, lang):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    if lang == "ko":
        card = """                    <a href="learn" class="nav-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h3>배당 아카데미</h3>
                        <p>초보자부터 실전까지, 배당 투자의 모든 것을 마스터하세요.</p>
                    </a>
"""
    elif lang == "en":
        card = """                    <a href="learn" class="nav-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h3>Dividend Academy</h3>
                        <p>Master dividend investing from basics to advanced strategies.</p>
                    </a>
"""
    elif lang == "pt":
        card = """                    <a href="learn" class="nav-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h3>Dividend Academy</h3>
                        <p>Aprenda a investir em dividendos do básico ao avançado.</p>
                    </a>
"""
        
    if 'href="learn"' not in html and '<div class="nav-grid">' in html:
        new_html = html.replace('<div class="nav-grid">\n', f'<div class="nav-grid">\n{card}')
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"  [Added Academy Card] {path}")

# Pages configuration
ko_pages = [
    ("ko/index.html", "/ko/"),
    ("ko/list.html", "/ko/list"),
    ("ko/calculator.html", "/ko/calculator"),
    ("ko/calendar.html", "/ko/calendar"),
    ("ko/fortune.html", "/ko/fortune"),
    ("ko/blog.html", "/ko/blog"),
    ("ko/about.html", "/ko/about"),
    ("ko/learn.html", "/ko/learn"),
]

en_pages = [
    ("index.html", "/"),
    ("list.html", "/list"),
    ("calculator.html", "/calculator"),
    ("calendar.html", "/calendar"),
    ("fortune.html", "/fortune"),
    ("blog.html", "/blog"),
    ("about.html", "/about"),
    ("learn.html", "/learn"),
]

pt_pages = [
    ("pt/index.html", "/pt/"),
    ("pt/list.html", "/pt/list"),
    ("pt/calculator.html", "/pt/calculator"),
    ("pt/calendar.html", "/pt/calendar"),
    ("pt/fortune.html", "/pt/fortune"),
    ("pt/blog.html", "/pt/blog"),
    ("pt/about.html", "/pt/about"),
    ("pt/learn.html", "/pt/learn"),
]

for p, active in ko_pages:
    force_update_nav(os.path.join(ROOT, p), active, NEW_NAV_KO_ITEMS)
for p, active in en_pages:
    force_update_nav(os.path.join(ROOT, p), active, NEW_NAV_EN_ITEMS)
for p, active in pt_pages:
    force_update_nav(os.path.join(ROOT, p), active, NEW_NAV_PT_ITEMS)

# Ensure Academy cards on index pages
force_academy_card(os.path.join(ROOT, "index.html"), "en")
force_academy_card(os.path.join(ROOT, "pt", "index.html"), "pt")
force_academy_card(os.path.join(ROOT, "ko", "index.html"), "ko")

print("All done!")
