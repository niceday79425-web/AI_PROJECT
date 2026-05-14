"""내비게이션 메뉴를 미니멀하고 고급스러운 디자인으로 업데이트"""
import os, re, glob

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

def build_nav_en(active_href=""):
    items = []
    for href, label in NEW_NAV_EN_ITEMS:
        clean_href = href.replace('href="', '').replace('"', '').replace('.html', '')
        clean_active = active_href.replace('.html', '')
        
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
        
    if not re.search(r'<nav class="(main-nav|glass-nav)"', html):
        return False
        
    new_html = NAV_PATTERN.sub(new_nav, html, count=1)
    
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
            pass

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
            pass

# Update nav in all blog posts
ko_posts = glob.glob(os.path.join(ROOT, "ko", "blog", "*.html"))
for path in ko_posts:
    update_nav(path, build_nav_ko("/ko/blog"))
    
en_posts = glob.glob(os.path.join(ROOT, "blog", "*.html"))
for path in en_posts:
    update_nav(path, build_nav_en("/blog"))

pt_posts = glob.glob(os.path.join(ROOT, "pt", "blog", "*.html"))
for path in pt_posts:
    # PT uses English nav right now as there's no pt nav config yet
    update_nav(path, build_nav_en("/blog"))

print("[OK] 미니멀리즘 내비게이션 바 모든 페이지 적용 완료")
