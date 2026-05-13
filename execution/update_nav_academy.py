"""내비게이션 메뉴에 아카데미 링크 추가 + 교육 포스트 링크를 아카데미 페이지로 업데이트"""
import os, re, glob

ROOT = r"d:\AI_PROJECT"

# 기존 내비게이션 교체 패턴
OLD_NAV_EN = 'href="/blog" style="color:var(--text-secondary);text-decoration:none;">Market Insights</a>'
NEW_NAV_EN_ITEMS = [
    ('href="/blog"', 'Market Insights'),
    ('href="/learn"', '📚 Dividend Academy'),
    ('href="/list"', 'Dividend Scouter'),
    ('href="/calculator"', 'Snowball Calculator'),
    ('href="/calendar"', 'Dividend Calendar'),
    ('href="/about"', 'About'),
]

OLD_NAV_KO = 'href="/ko/blog" style="color:var(--text-secondary);text-decoration:none;">마켓 인사이트</a>'
NEW_NAV_KO_ITEMS = [
    ('href="/ko/blog"', '마켓 인사이트'),
    ('href="/ko/learn"', '📚 배당투자 아카데미'),
    ('href="/ko/list"', '배당주 스카우터'),
    ('href="/ko/calculator"', '스노볼 계산기'),
    ('href="/ko/calendar"', '배당 캘린더'),
    ('href="/ko/about"', '소개'),
]

def build_nav_en(active_href=""):
    items = []
    for href, label in NEW_NAV_EN_ITEMS:
        if href.strip('"') == active_href or (active_href == "/learn" and "Academy" in label):
            items.append(f'<a {href} style="color:#6366f1;font-weight:700;text-decoration:none;">{label}</a>')
        else:
            items.append(f'<a {href} style="color:var(--text-secondary);text-decoration:none;">{label}</a>')
    return '        <nav class="main-nav" style="display:flex;gap:1.2rem;flex-wrap:wrap;margin-top:0.5rem;padding-bottom:0.5rem;border-bottom:1px solid var(--border-color);font-size:0.9rem;">\n          ' + '\n          '.join(items) + '\n        </nav>'

def build_nav_ko(active_href=""):
    items = []
    for href, label in NEW_NAV_KO_ITEMS:
        if "learn" in href and "learn" in active_href:
            items.append(f'<a {href} style="color:#6366f1;font-weight:700;text-decoration:none;">{label}</a>')
        else:
            items.append(f'<a {href} style="color:var(--text-secondary);text-decoration:none;">{label}</a>')
    return '        <nav class="main-nav" style="display:flex;gap:1.2rem;flex-wrap:wrap;margin-top:0.5rem;padding-bottom:0.5rem;border-bottom:1px solid var(--border-color);font-size:0.9rem;">\n          ' + '\n          '.join(items) + '\n        </nav>'

NAV_PATTERN = re.compile(
    r'<nav class="main-nav"[^>]*>.*?</nav>',
    re.DOTALL
)

def update_nav(path, new_nav):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if 'class="main-nav"' not in html:
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
            print(f"  [nav-en] {os.path.basename(path)}")

# KO pages
ko_pages = [
    (os.path.join(ROOT, "ko", "index.html"), "/ko/"),
    (os.path.join(ROOT, "ko", "blog.html"), "/ko/blog"),
    (os.path.join(ROOT, "ko", "about.html"), "/ko/about"),
    (os.path.join(ROOT, "ko", "learn.html"), "/ko/learn"),
]
for path, active in ko_pages:
    if os.path.exists(path):
        if update_nav(path, build_nav_ko(active)):
            print(f"  [nav-ko] {os.path.basename(path)}")

# Also update nav in KO blog posts (교육 시리즈 포스트)
ko_edu_posts = glob.glob(os.path.join(ROOT, "ko", "blog", "beginner-*.html")) + \
               glob.glob(os.path.join(ROOT, "ko", "blog", "monthly-*.html")) + \
               glob.glob(os.path.join(ROOT, "ko", "blog", "sector-*.html"))

updated = 0
for path in ko_edu_posts:
    if update_nav(path, build_nav_ko()):
        updated += 1
print(f"  [nav-ko-edu] {updated}개 교육 포스트 내비 업데이트")

print("\n[OK] 내비게이션 업데이트 완료")
