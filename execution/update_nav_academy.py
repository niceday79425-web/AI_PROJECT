"""내비게이션 메뉴를 최신 Glassmorphism 디자인으로 업데이트"""
import os, re, glob

ROOT = r"d:\AI_PROJECT"

NEW_NAV_EN_ITEMS = [
    ('href="/blog.html"', '<i class="fas fa-newspaper"></i> Market Insights'),
    ('href="/learn.html"', '<i class="fas fa-graduation-cap"></i> Dividend Academy'),
    ('href="/list.html"', '<i class="fas fa-chart-line"></i> Dividend Scouter'),
    ('href="/calculator.html"', '<i class="fas fa-calculator"></i> Snowball Calculator'),
    ('href="/calendar.html"', '<i class="fas fa-calendar-alt"></i> Dividend Calendar'),
    ('href="/about.html"', '<i class="fas fa-info-circle"></i> About'),
]

NEW_NAV_KO_ITEMS = [
    ('href="/ko/blog.html"', '<i class="fas fa-newspaper"></i> 마켓 인사이트'),
    ('href="/ko/learn.html"', '<i class="fas fa-graduation-cap"></i> 배당 아카데미'),
    ('href="/ko/list.html"', '<i class="fas fa-chart-line"></i> 배당주 스카우터'),
    ('href="/ko/calculator.html"', '<i class="fas fa-calculator"></i> 스노볼 계산기'),
    ('href="/ko/calendar.html"', '<i class="fas fa-calendar-alt"></i> 배당 캘린더'),
    ('href="/ko/about.html"', '<i class="fas fa-info-circle"></i> 소개'),
]

def build_nav_en(active_href=""):
    items = []
    # Convert active_href to full file path style for matching, or just match the base
    # Because active_href could be '/blog' or '/ko/blog' or '/ko/blog.html'
    for href, label in NEW_NAV_EN_ITEMS:
        # Check if the href matches the active page
        clean_href = href.replace('href="', '').replace('"', '').replace('.html', '')
        clean_active = active_href.replace('.html', '')
        
        # Exact match or if active is a sub-page of the section
        if clean_href == clean_active or (clean_href != "/" and clean_active.startswith(clean_href)):
            items.append(f'<a {href.replace(".html", "")} class="active">{label}</a>')
        else:
            items.append(f'<a {href.replace(".html", "")}>{label}</a>')
            
    return '        <nav class="glass-nav">\n          ' + '\n          '.join(items) + '\n        </nav>'

def build_nav_ko(active_href=""):
    items = []
    for href, label in NEW_NAV_KO_ITEMS:
        clean_href = href.replace('href="', '').replace('"', '').replace('.html', '')
        clean_active = active_href.replace('.html', '')
        
        if clean_href == clean_active or (clean_href != "/ko/" and clean_active.startswith(clean_href)):
            items.append(f'<a {href.replace(".html", "")} class="active">{label}</a>')
        else:
            items.append(f'<a {href.replace(".html", "")}>{label}</a>')
            
    return '        <nav class="glass-nav">\n          ' + '\n          '.join(items) + '\n        </nav>'

NAV_PATTERN = re.compile(
    r'<nav class="(main-nav|glass-nav)"[^>]*>.*?</nav>',
    re.DOTALL
)

def update_nav(path, new_nav):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
        
    # main-nav나 glass-nav가 있는지 확인
    if not re.search(r'<nav class="(main-nav|glass-nav)"', html):
        return False
        
    new_html = NAV_PATTERN.sub(new_nav, html, count=1)
    
    # 만약 FontAwesome이 없다면 <head> 태그 닫히기 전에 추가
    if '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/' not in new_html:
        fa_link = '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">\n</head>'
        new_html = new_html.replace('</head>', fa_link)

    if new_html != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        return True
    return False

# EN pages
en_pages = [
    (os.path.join(ROOT, "index.html"), "/"),
    (os.path.join(ROOT, "blog.html"), "/blog"),
    (os.path.join(ROOT, "about.html"), "/about"),
    (os.path.join(ROOT, "contact.html"), "/contact"),
    (os.path.join(ROOT, "privacy.html"), "/privacy"),
    (os.path.join(ROOT, "learn.html"), "/learn"),
]
for path, active in en_pages:
    if os.path.exists(path):
        if update_nav(path, build_nav_en(active)):
            print(f"  [nav-en] {os.path.basename(path)}")

# KO pages
ko_pages = [
    (os.path.join(ROOT, "ko", "index.html"), "/ko/"),
    (os.path.join(ROOT, "ko", "blog.html"), "/ko/blog"),
    (os.path.join(ROOT, "ko", "about.html"), "/ko/about"),
    (os.path.join(ROOT, "ko", "learn.html"), "/ko/learn"),
    (os.path.join(ROOT, "ko", "calculator.html"), "/ko/calculator"),
    (os.path.join(ROOT, "ko", "calendar.html"), "/ko/calendar"),
    (os.path.join(ROOT, "ko", "list.html"), "/ko/list"),
    (os.path.join(ROOT, "ko", "fortune.html"), "/ko/fortune"),
]
for path, active in ko_pages:
    if os.path.exists(path):
        if update_nav(path, build_nav_ko(active)):
            print(f"  [nav-ko] {os.path.basename(path)}")

# Also update nav in all blog posts (KO, EN, PT)
ko_posts = glob.glob(os.path.join(ROOT, "ko", "blog", "*.html"))
for path in ko_posts:
    update_nav(path, build_nav_ko("/ko/blog"))
    
en_posts = glob.glob(os.path.join(ROOT, "blog", "*.html"))
for path in en_posts:
    update_nav(path, build_nav_en("/blog"))

print("\n[OK] 모든 페이지의 내비게이션 바 디자인 업데이트 완료")
