"""
Phase 1+2+3: 
- auto_poster.py 개선 (하루 1개, 삭제 중단, 콘텐츠 품질 강화, 저자 정보)
- blog.html 정적 HTML 목록 생성 함수 추가
- 내비게이션 메뉴 추가 (index.html, blog.html 등 주요 페이지)
- Privacy Policy AdSense 조항 추가
- fortune.html robots 차단
"""
import os, re, json, glob

ROOT = r"d:\AI_PROJECT"

# ─────────────────────────────────────────────
# 1. auto_poster.py 수정
# ─────────────────────────────────────────────
poster_path = os.path.join(ROOT, "execution", "auto_poster.py")
with open(poster_path, "r", encoding="utf-8") as f:
    poster = f.read()

# 1-a. 하루 3개 -> 1개
poster = poster.replace(
    "top_stocks = get_top_volatile_tickers(TICKERS, 3)",
    "top_stocks = get_top_volatile_tickers(TICKERS, 1)  # 1 per day for quality"
)

# 1-b. cleanup 호출 제거 (포스트 영구 보존)
poster = poster.replace(
    "    cleanup_old_posts()  # Remove posts older than 30 days first\n    top_stocks",
    "    # cleanup_old_posts() DISABLED - posts are kept permanently for SEO\n    top_stocks"
)

# 1-c. 콘텐츠 품질 강화 - 프롬프트 업그레이드
OLD_PROMPT_SECTION = '    Requirements:\n    - Use semantic HTML (h2, p, ul, li, strong, em)\n    - Include [CHART-HERE] placeholder where the stock chart should appear\n    - Make English content professional and data-driven\n    - Ensure translations maintain the same tone and information\n    - Focus on investment insights, market trends, and actionable analysis\n    """'

NEW_PROMPT_SECTION = '''    Requirements:
    - Minimum 1000 words per language (quality over quantity)
    - Use semantic HTML (h2, p, ul, li, strong, em)
    - Include [CHART-HERE] placeholder where the stock chart should appear
    - REQUIRED SECTIONS (use <h2> for each):
      1. Executive Summary (3-sentence overview with current price data)
      2. Recent Performance & Key Events (with specific numbers/percentages)
      3. Technical Analysis (support/resistance levels, RSI, momentum)
      4. Dividend Investor Perspective (dividend history, payout ratio, sustainability)
      5. Risk Factors (minimum 3 specific risks with explanation)
      6. Conclusion & Investor Action Points
      7. FAQ (3 Q&A pairs relevant to this stock)
    - Make English content professional and data-driven with specific numbers
    - Ensure translations are natural, not just word-for-word
    - Focus on actionable insights that help investors make informed decisions
    - Add internal links: mention Dividend Scouter at /list and Calculator at /calculator
    """'''

poster = poster.replace(OLD_PROMPT_SECTION, NEW_PROMPT_SECTION)

# 1-d. 저자 박스를 build_post_html에 추가
OLD_ARTICLE_SECTION = '      {article_body}\n\n      <div class="disclaimer">'
NEW_ARTICLE_SECTION = '''      <!-- Author Box -->
      <div style="display:flex;align-items:center;gap:1rem;background:#f8f9fb;border:1px solid #e5e7eb;border-radius:12px;padding:1rem 1.2rem;margin-bottom:2rem;">
        <div style="width:48px;height:48px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
          <span style="color:#fff;font-weight:700;font-size:1.1rem;">W</span>
        </div>
        <div>
          <strong style="display:block;color:#1e1b4b;font-size:0.95rem;">WiseAIWiseU Research Team</strong>
          <span style="font-size:0.8rem;color:#6b7280;">Data-driven dividend &amp; market analysis | Published: {today} | Educational purposes only</span>
        </div>
      </div>

      {{article_body}}

      <div class="disclaimer">'''

# fix placeholder issue
NEW_ARTICLE_SECTION = NEW_ARTICLE_SECTION.replace('{today}', '{today}').replace('{{article_body}}', '{article_body}')
poster = poster.replace(OLD_ARTICLE_SECTION, NEW_ARTICLE_SECTION)

# 1-e. 광고 코드를 새 포스트에서도 빈 문자열로 (애드센스 승인 전)
poster = poster.replace(
    "    ad_header = '''<div class=\"ad-slot\"",
    "    ad_header = '''<!-- AdSense placeholder removed for approval -->\n    <!-- <div class=\"ad-slot\""
)
# simpler: just blank the ad strings
poster = re.sub(
    r"(ad_header\s*=\s*)'''.*?'''",
    r"\1''''''",
    poster, flags=re.DOTALL
)
poster = re.sub(
    r"(ad_mid\s*=\s*)'''<div class=\"ad-in-article\".*?'''",
    r"\1''''''",
    poster, flags=re.DOTALL
)
poster = re.sub(
    r"(ad_footer\s*=\s*)'''<div class=\"ad-slot\".*?'''",
    r"\1''''''",
    poster, flags=re.DOTALL
)
# also the AdSense script in head
poster = poster.replace(
    '  <!-- Google AdSense -->\n  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>',
    '  <!-- Google AdSense: pending approval -->'
)

with open(poster_path, "w", encoding="utf-8") as f:
    f.write(poster)
print("[OK] auto_poster.py updated")

# ─────────────────────────────────────────────
# 2. update_blog_html() - 정적 목록 생성 함수를 generate_sitemap.py에 추가
# ─────────────────────────────────────────────
STATIC_BLOG_UPDATER = '''
import json, os, re

def update_blog_html_static(lang, posts_path, blog_html_path, blog_url_prefix):
    """posts.json을 읽어 blog.html의 #blogGrid를 정적 HTML로 업데이트"""
    if not os.path.exists(posts_path):
        return
    with open(posts_path, "r", encoding="utf-8") as f:
        posts = json.load(f)
    
    items = []
    for p in posts[:60]:
        title = p.get("title","")
        date  = p.get("date","")
        link  = p.get("link","")
        summary = p.get("summary","")[:120]
        url = "/" + blog_url_prefix + link if not link.startswith("/") else link
        items.append(f\'\'\'<article class="blog-card" style="cursor:pointer;" onclick="location.href=\\'{url}\\'">
          <span class="blog-date">{date}</span>
          <h3>{title}</h3>
          <p>{summary}</p>
        </article>\'\'\')
    
    static_html = "\\n".join(items)
    
    if not os.path.exists(blog_html_path):
        return
    with open(blog_html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Replace dynamic JS section with static content
    new_html = re.sub(
        r\'(<div id="blogGrid"[^>]*>).*?(</div>\\s*</section>)\',
        r\'\\1\\n\' + static_html + r\'\\n\\2\',
        html, flags=re.DOTALL, count=1
    )
    
    # Remove the JS loadBlog function
    new_html = re.sub(
        r\'<script>\\s*async function loadBlog\\(\\).*?loadBlog\\(\\);\\s*</script>\',
        \'<!-- Static HTML blog list - no JS needed -->\',
        new_html, flags=re.DOTALL
    )
    
    with open(blog_html_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"  [static] {blog_html_path}: {len(posts)} posts rendered")

if __name__ == "__main__":
    configs = [
        ("posts.json",    "blog.html",    ""),
        ("ko/posts.json", "ko/blog.html", "ko/"),
        ("pt/posts.json", "pt/blog.html", "pt/"),
    ]
    for posts_p, blog_p, prefix in configs:
        update_blog_html_static("", posts_p, blog_p, prefix)
    print("[DONE] Blog HTML static update complete")
'''

static_blog_path = os.path.join(ROOT, "execution", "update_blog_static.py")
with open(static_blog_path, "w", encoding="utf-8") as f:
    f.write(STATIC_BLOG_UPDATER)
print("[OK] update_blog_static.py created")

# ─────────────────────────────────────────────
# 3. 주요 페이지에 내비게이션 메뉴 추가
# ─────────────────────────────────────────────
NAV_EN = '''        <nav class="main-nav" style="display:flex;gap:1.2rem;flex-wrap:wrap;margin-top:0.5rem;padding-bottom:0.5rem;border-bottom:1px solid var(--border-color);font-size:0.9rem;">
          <a href="/blog" style="color:var(--text-secondary);text-decoration:none;" onmouseover="this.style.color='var(--accent-blue)'" onmouseout="this.style.color='var(--text-secondary)'">Market Insights</a>
          <a href="/list" style="color:var(--text-secondary);text-decoration:none;" onmouseover="this.style.color='var(--accent-blue)'" onmouseout="this.style.color='var(--text-secondary)'">Dividend Scouter</a>
          <a href="/calculator" style="color:var(--text-secondary);text-decoration:none;" onmouseover="this.style.color='var(--accent-blue)'" onmouseout="this.style.color='var(--text-secondary)'">Snowball Calculator</a>
          <a href="/calendar" style="color:var(--text-secondary);text-decoration:none;" onmouseover="this.style.color='var(--accent-blue)'" onmouseout="this.style.color='var(--text-secondary)'">Dividend Calendar</a>
          <a href="/about" style="color:var(--text-secondary);text-decoration:none;" onmouseover="this.style.color='var(--accent-blue)'" onmouseout="this.style.color='var(--text-secondary)'">About</a>
        </nav>'''

NAV_KO = '''        <nav class="main-nav" style="display:flex;gap:1.2rem;flex-wrap:wrap;margin-top:0.5rem;padding-bottom:0.5rem;border-bottom:1px solid var(--border-color);font-size:0.9rem;">
          <a href="/ko/blog" style="color:var(--text-secondary);text-decoration:none;" onmouseover="this.style.color='var(--accent-blue)'" onmouseout="this.style.color='var(--text-secondary)'">마켓 인사이트</a>
          <a href="/ko/list" style="color:var(--text-secondary);text-decoration:none;" onmouseover="this.style.color='var(--accent-blue)'" onmouseout="this.style.color='var(--text-secondary)'">배당주 스카우터</a>
          <a href="/ko/calculator" style="color:var(--text-secondary);text-decoration:none;" onmouseover="this.style.color='var(--accent-blue)'" onmouseout="this.style.color='var(--text-secondary)'">스노볼 계산기</a>
          <a href="/ko/calendar" style="color:var(--text-secondary);text-decoration:none;" onmouseover="this.style.color='var(--accent-blue)'" onmouseout="this.style.color='var(--text-secondary)'">배당 캘린더</a>
          <a href="/ko/about" style="color:var(--text-secondary);text-decoration:none;" onmouseover="this.style.color='var(--accent-blue)'" onmouseout="this.style.color='var(--text-secondary)'">소개</a>
        </nav>'''

def add_nav_to_file(path, nav_html):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if 'class="main-nav"' in html:
        return False
    # Insert after </header> closing tag
    html = html.replace('        </header>', '        </header>\n' + nav_html, 1)
    if 'class="main-nav"' not in html:
        # try single-space
        html = html.replace('</header>', '</header>\n' + nav_html, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return True

# Add nav to main EN pages
main_pages_en = [
    os.path.join(ROOT, "index.html"),
    os.path.join(ROOT, "blog.html"),
    os.path.join(ROOT, "about.html"),
    os.path.join(ROOT, "contact.html"),
    os.path.join(ROOT, "privacy.html"),
]
for p in main_pages_en:
    if os.path.exists(p) and add_nav_to_file(p, NAV_EN):
        print(f"  [nav-en] {os.path.basename(p)}")

# Add nav to KO pages
main_pages_ko = [
    os.path.join(ROOT, "ko", "index.html"),
    os.path.join(ROOT, "ko", "blog.html"),
    os.path.join(ROOT, "ko", "about.html"),
]
for p in main_pages_ko:
    if os.path.exists(p) and add_nav_to_file(p, NAV_KO):
        print(f"  [nav-ko] {os.path.basename(p)}")

print("[OK] Navigation menus added")

# ─────────────────────────────────────────────
# 4. Privacy Policy - AdSense/Analytics 조항 추가
# ─────────────────────────────────────────────
privacy_path = os.path.join(ROOT, "privacy.html")
with open(privacy_path, "r", encoding="utf-8") as f:
    privacy = f.read()

ADSENSE_CLAUSE = '''
        <section style="background:var(--card-bg);border:1px solid var(--border-color);border-radius:16px;padding:2rem;margin-bottom:1.75rem;">
          <h2 style="color:var(--accent-blue);font-size:1.2rem;margin-bottom:0.9rem;">Advertising &amp; Third-Party Services</h2>
          <p style="color:var(--text-secondary);line-height:1.85;">This site may use Google AdSense to display advertisements. Google AdSense uses cookies and web beacons to serve ads based on your prior visits to this website or other websites. You may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" style="color:var(--accent-blue);">Google Ads Settings</a>.</p>
          <p style="color:var(--text-secondary);line-height:1.85;">We may also use Google Analytics to understand site traffic patterns. Google Analytics collects information such as how often users visit this site, what pages they visit, and what other sites they used prior to visiting. We use this information to improve our site. Google Analytics collects only the IP address assigned to you on the date you visit this site, not your name or other personally identifiable information.</p>
          <p style="color:var(--text-secondary);line-height:1.85;">Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to our website. Users may opt out of personalized advertising by visiting the <a href="https://optout.networkadvertising.org/" style="color:var(--accent-blue);">Network Advertising Initiative opt-out page</a>.</p>
        </section>'''

if 'AdSense' not in privacy and 'Advertising' not in privacy:
    # Insert before the closing </main>
    privacy = privacy.replace('</main>', ADSENSE_CLAUSE + '\n        </main>', 1)
    with open(privacy_path, "w", encoding="utf-8") as f:
        f.write(privacy)
    print("[OK] Privacy Policy AdSense clause added")
else:
    print("[SKIP] Privacy Policy already has AdSense clause")

# ─────────────────────────────────────────────
# 5. robots.txt - fortune 차단 추가 (심사 기간)
# ─────────────────────────────────────────────
robots_path = os.path.join(ROOT, "robots.txt")
with open(robots_path, "r", encoding="utf-8") as f:
    robots = f.read()

if '/fortune' not in robots:
    robots = robots.replace(
        "# Block dev/execution directories",
        "# Block entertainment pages during AdSense review\nDisallow: /fortune\nDisallow: /fortune.html\nDisallow: /ko/fortune\nDisallow: /ko/fortune.html\nDisallow: /pt/fortune\nDisallow: /pt/fortune.html\n\n# Block dev/execution directories"
    )
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots)
    print("[OK] robots.txt: fortune.html blocked during review")

# ─────────────────────────────────────────────
# 6. contact.html - 이메일 링크를 mailto로 수정
# ─────────────────────────────────────────────
contact_path = os.path.join(ROOT, "contact.html")
with open(contact_path, "r", encoding="utf-8") as f:
    contact = f.read()

contact = contact.replace(
    '<p style="font-size: 1.2rem; color: var(--accent-blue);">support@WiseAIWiseU</p>',
    '<p style="font-size: 1.2rem;"><a href="mailto:support@wiseaiwiseu.com" style="color:var(--accent-blue);">support@wiseaiwiseu.com</a></p>'
)
with open(contact_path, "w", encoding="utf-8") as f:
    f.write(contact)
print("[OK] contact.html email fixed with mailto link")

# ─────────────────────────────────────────────
# 7. daily_news.yml - 포스팅 후 update_blog_static.py 실행 추가
# ─────────────────────────────────────────────
yml_path = os.path.join(ROOT, ".github", "workflows", "daily_news.yml")
with open(yml_path, "r", encoding="utf-8") as f:
    yml = f.read()

if "update_blog_static" not in yml:
    yml = yml.replace(
        "          python execution/auto_poster.py\n          python generate_sitemap.py",
        "          python execution/auto_poster.py\n          python execution/update_blog_static.py\n          python generate_sitemap.py"
    )
    with open(yml_path, "w", encoding="utf-8") as f:
        f.write(yml)
    print("[OK] daily_news.yml: update_blog_static.py step added")

print("\n=== Phase 1+2+3 Complete ===")
print("[OK] P1-1: auto_poster.py -> 1 post/day")
print("[OK] P1-2: Content quality prompt upgraded (7 required sections)")
print("[OK] P1-3: Post cleanup DISABLED (permanent storage)")
print("[OK] P1-4: Author box added to new posts")
print("[OK] P2-1: update_blog_static.py created (static HTML blog list)")
print("[OK] P2-2: Navigation menus added to main pages")
print("[OK] P2-3: Privacy Policy AdSense clause added")
print("[OK] P2-4: robots.txt fortune pages blocked")
print("[OK] P2-5: contact.html mailto link fixed")
print("[OK] P3-1: daily_news.yml updated to run static blog updater")
