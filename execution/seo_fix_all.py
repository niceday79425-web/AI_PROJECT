# -*- coding: utf-8 -*-
"""
WiseAIWiseU.com -- SEO 전면 수정 스크립트
"""
import os
import re
import glob
from datetime import datetime

BASE_DIR = r"D:\AI_PROJECT"
DOMAIN = "https://wiseaiwiseu.com"

print("BASE_DIR: " + BASE_DIR)
print("=" * 60)


# ===================================================
# STEP 1 & 3: JS 리디렉션 제거 + 내부 링크 .html 제거
# ===================================================
print("\n[STEP 1 & 3] JS redirect removal + internal link fix")
print("-" * 40)

def remove_js_redirect(content):
    """JS 리디렉션 블록 제거"""
    result = re.sub(
        r'\n?\s*<script>\s*\n\s*\(function\s*\(\)\s*\{[^<]*?navigator\.language[^<]*?window\.location\.href[^<]*?\}\)\(\);\s*\n\s*</script>',
        '',
        content,
        flags=re.DOTALL
    )
    if result == content:
        result = re.sub(
            r'<script>\s*\n?\s*\(function\s*\(\)\s*\{.*?redirected.*?window\.location\.href.*?\}\)\(\);?\s*\n?\s*</script>',
            '',
            content,
            flags=re.DOTALL
        )
    return result

PAGES_TO_FIX = [
    'blog', 'list', 'calculator', 'calendar',
    'fortune', 'about', 'contact', 'privacy'
]

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. JS 리디렉션 제거
    if 'window.location.href' in content and 'userLang' in content:
        content = remove_js_redirect(content)
        if content != original:
            print("  [REMOVED JS redirect] " + os.path.relpath(filepath, BASE_DIR))

    # 2. 내부 링크 .html 제거
    for page in PAGES_TO_FIX:
        page_html = page + '.html'
        content = content.replace('href="' + page_html + '"', 'href="' + page + '"')
        content = content.replace('href="/' + page_html + '"', 'href="/' + page + '"')
        content = content.replace('href="/ko/' + page_html + '"', 'href="/ko/' + page + '"')
        content = content.replace('href="/pt/' + page_html + '"', 'href="/pt/' + page + '"')
        content = content.replace('href="../' + page_html + '"', 'href="../' + page + '"')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

all_html = (
    glob.glob(os.path.join(BASE_DIR, '*.html')) +
    glob.glob(os.path.join(BASE_DIR, 'ko', '*.html')) +
    glob.glob(os.path.join(BASE_DIR, 'pt', '*.html')) +
    glob.glob(os.path.join(BASE_DIR, 'blog', '*.html')) +
    glob.glob(os.path.join(BASE_DIR, 'ko', 'blog', '*.html')) +
    glob.glob(os.path.join(BASE_DIR, 'pt', 'blog', '*.html'))
)

total_modified = sum(1 for f in all_html if process_html_file(f))
print("Total modified: " + str(total_modified) + " files")


# ===================================================
# STEP 2: blog.html static-links display:none 제거
# ===================================================
print("\n[STEP 2] blog.html static-links visibility fix")
print("-" * 40)

def fix_blog_static_links(path):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old = '<div class="static-links" style="display:none;">'
    new = '<div class="static-links" style="margin-bottom:1.5rem;">'

    if old in content:
        content = content.replace(old, new)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  [FIXED] " + os.path.relpath(path, BASE_DIR))
    else:
        # Try regex
        new_content = re.sub(
            r'<div class="static-links"[^>]*display:\s*none[^>]*>',
            '<div class="static-links" style="margin-bottom:1.5rem;">',
            content
        )
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("  [FIXED via regex] " + os.path.relpath(path, BASE_DIR))
        else:
            print("  [SKIP] no display:none found in " + os.path.relpath(path, BASE_DIR))

fix_blog_static_links(os.path.join(BASE_DIR, 'blog.html'))
fix_blog_static_links(os.path.join(BASE_DIR, 'ko', 'blog.html'))
fix_blog_static_links(os.path.join(BASE_DIR, 'pt', 'blog.html'))


# ===================================================
# STEP 4: robots.txt 개선
# ===================================================
print("\n[STEP 4] robots.txt update")
print("-" * 40)

robots_content = """User-agent: *
Allow: /

# Block duplicate .html extension URLs (canonical URLs are extension-free)
Disallow: /index.html
Disallow: /blog.html
Disallow: /list.html
Disallow: /calculator.html
Disallow: /calendar.html
Disallow: /fortune.html
Disallow: /about.html
Disallow: /contact.html
Disallow: /privacy.html
Disallow: /ko/index.html
Disallow: /ko/blog.html
Disallow: /ko/list.html
Disallow: /ko/calculator.html
Disallow: /ko/calendar.html
Disallow: /ko/fortune.html
Disallow: /ko/about.html
Disallow: /ko/contact.html
Disallow: /ko/privacy.html
Disallow: /pt/index.html
Disallow: /pt/blog.html
Disallow: /pt/list.html
Disallow: /pt/calculator.html
Disallow: /pt/calendar.html
Disallow: /pt/fortune.html
Disallow: /pt/about.html
Disallow: /pt/contact.html
Disallow: /pt/privacy.html

# Block dev/execution directories
Disallow: /execution/
Disallow: /.github/
Disallow: /.git/
Disallow: /.tmp/

Sitemap: https://wiseaiwiseu.com/sitemap.xml
"""

with open(os.path.join(BASE_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write(robots_content)
print("  [OK] robots.txt updated")


# ===================================================
# STEP 5: sitemap.xml 재생성 (문자열 템플릿 방식)
# ===================================================
print("\n[STEP 5] sitemap.xml regeneration")
print("-" * 40)

LANGS = [
    {"prefix": "",    "hreflang": "en"},
    {"prefix": "ko/", "hreflang": "ko"},
    {"prefix": "pt/", "hreflang": "pt"},
]

STATIC_PAGES = [
    {"slug": "",            "is_index": True,  "priority": "1.0", "changefreq": "daily"},
    {"slug": "blog",        "is_index": False, "priority": "0.9", "changefreq": "daily"},
    {"slug": "list",        "is_index": False, "priority": "0.8", "changefreq": "weekly"},
    {"slug": "calculator",  "is_index": False, "priority": "0.8", "changefreq": "weekly"},
    {"slug": "calendar",    "is_index": False, "priority": "0.8", "changefreq": "weekly"},
    {"slug": "fortune",     "is_index": False, "priority": "0.7", "changefreq": "monthly"},
    {"slug": "about",       "is_index": False, "priority": "0.7", "changefreq": "monthly"},
    {"slug": "contact",     "is_index": False, "priority": "0.6", "changefreq": "monthly"},
    {"slug": "privacy",     "is_index": False, "priority": "0.5", "changefreq": "yearly"},
]

def get_last_mod(file_path):
    if os.path.exists(file_path):
        return datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')
    return datetime.now().strftime('%Y-%m-%d')

def url_block(loc, alternates, lastmod, changefreq, priority):
    lines = ["  <url>"]
    lines.append("    <loc>" + loc + "</loc>")
    for hreflang, href in alternates:
        lines.append('    <xhtml:link rel="alternate" hreflang="' + hreflang + '" href="' + href + '"/>')
    lines.append("    <lastmod>" + lastmod + "</lastmod>")
    lines.append("    <changefreq>" + changefreq + "</changefreq>")
    lines.append("    <priority>" + priority + "</priority>")
    lines.append("  </url>")
    return "\n".join(lines)

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
]

for page_info in STATIC_PAGES:
    for lang in LANGS:
        prefix = lang["prefix"]
        if page_info["is_index"]:
            loc = DOMAIN + "/" + prefix
            if loc.endswith("//"):
                loc = loc[:-1]
        else:
            loc = DOMAIN + "/" + prefix + page_info["slug"]

        alternates = []
        for al in LANGS:
            if page_info["is_index"]:
                ah = DOMAIN + "/" + al["prefix"]
                if ah.endswith("//"):
                    ah = ah[:-1]
            else:
                ah = DOMAIN + "/" + al["prefix"] + page_info["slug"]
            alternates.append((al["hreflang"], ah))

        if page_info["is_index"]:
            alternates.append(("x-default", DOMAIN + "/"))
        else:
            alternates.append(("x-default", DOMAIN + "/" + page_info["slug"]))

        if page_info["is_index"]:
            fpath = os.path.join(BASE_DIR, prefix, "index.html")
        else:
            fpath = os.path.join(BASE_DIR, prefix, page_info["slug"] + ".html")
        lastmod = get_last_mod(fpath)

        xml_lines.append(url_block(loc, alternates, lastmod, page_info["changefreq"], page_info["priority"]))

# blog/ 스캔
blog_dir = os.path.join(BASE_DIR, 'blog')
blog_files_raw = sorted(glob.glob(os.path.join(blog_dir, '*.html')), reverse=True)
blog_count = 0

for bf in blog_files_raw:
    basename = os.path.basename(bf)
    slug = basename.replace('.html', '')
    date_match = re.search(r'^(\d{4}-\d{2}-\d{2})', slug)
    post_date = date_match.group(1) if date_match else get_last_mod(bf)

    alts = [("en", DOMAIN + "/blog/" + slug), ("x-default", DOMAIN + "/blog/" + slug)]
    ko_exists = os.path.exists(os.path.join(BASE_DIR, 'ko', 'blog', basename))
    pt_exists = os.path.exists(os.path.join(BASE_DIR, 'pt', 'blog', basename))
    if ko_exists:
        alts.append(("ko", DOMAIN + "/ko/blog/" + slug))
    if pt_exists:
        alts.append(("pt", DOMAIN + "/pt/blog/" + slug))

    xml_lines.append(url_block(DOMAIN + "/blog/" + slug, alts, post_date, "monthly", "0.7"))
    if ko_exists:
        xml_lines.append(url_block(DOMAIN + "/ko/blog/" + slug, alts, post_date, "monthly", "0.7"))
    if pt_exists:
        xml_lines.append(url_block(DOMAIN + "/pt/blog/" + slug, alts, post_date, "monthly", "0.7"))
    blog_count += 1

xml_lines.append("</urlset>")
final_xml = "\n".join(xml_lines)

print("  Blog posts scanned: " + str(blog_count))

sitemap_path = os.path.join(BASE_DIR, 'sitemap.xml')
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(final_xml)

url_count = final_xml.count('<url>')
print("  [OK] sitemap.xml written -- total URLs: " + str(url_count))


# ===================================================
# STEP 6: blog.html 정적 링크 목록 업데이트
# ===================================================
print("\n[STEP 6] Static post links in blog.html")
print("-" * 40)

blog_files_sorted = sorted(
    glob.glob(os.path.join(BASE_DIR, 'blog', '*.html')),
    key=lambda x: os.path.basename(x),
    reverse=True
)

def get_post_title(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if h1:
        return re.sub(r'<[^>]+>', '', h1.group(1)).strip()
    t = re.search(r'<title>(.*?)</title>', content)
    if t:
        return t.group(1).strip()
    return os.path.basename(fpath).replace('.html', '')

def build_links(files, prefix, limit=60):
    lines = []
    for f in files[:limit]:
        basename = os.path.basename(f)
        slug = basename.replace('.html', '')
        # 해당 언어 버전 파일이 있으면 그쪽 title 사용
        lang_dir = os.path.dirname(f)
        alt_file = os.path.join(lang_dir, basename)
        title = get_post_title(alt_file if os.path.exists(alt_file) else f)
        # HTML 이스케이프
        title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        lines.append('                            <a href="' + prefix + slug + '">' + title + '</a>')
    return '\n'.join(lines)

def update_blog_html(blog_html_path, links_html):
    if not os.path.exists(blog_html_path):
        return
    with open(blog_html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_section = (
        '<div class="static-links" style="margin-bottom:1.5rem;">\n'
        '                            <p style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:0.5rem;">Latest Articles:</p>\n'
        + links_html + '\n'
        '                        </div>'
    )

    new_content = re.sub(
        r'<div class="static-links"[^>]*>.*?</div>',
        new_section,
        content,
        flags=re.DOTALL
    )

    if new_content != content:
        with open(blog_html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("  [OK] " + os.path.relpath(blog_html_path, BASE_DIR))
    else:
        print("  [SKIP] pattern not matched: " + os.path.relpath(blog_html_path, BASE_DIR))

en_links = build_links(blog_files_sorted, '/blog/')
ko_blog_files = [
    os.path.join(BASE_DIR, 'ko', 'blog', os.path.basename(f))
    for f in blog_files_sorted
    if os.path.exists(os.path.join(BASE_DIR, 'ko', 'blog', os.path.basename(f)))
] or blog_files_sorted
ko_links = build_links(ko_blog_files, '/ko/blog/')
pt_blog_files = [
    os.path.join(BASE_DIR, 'pt', 'blog', os.path.basename(f))
    for f in blog_files_sorted
    if os.path.exists(os.path.join(BASE_DIR, 'pt', 'blog', os.path.basename(f)))
] or blog_files_sorted
pt_links = build_links(pt_blog_files, '/pt/blog/')

update_blog_html(os.path.join(BASE_DIR, 'blog.html'), en_links)
update_blog_html(os.path.join(BASE_DIR, 'ko', 'blog.html'), ko_links)
update_blog_html(os.path.join(BASE_DIR, 'pt', 'blog.html'), pt_links)


# ===================================================
# STEP 7: title / description 잘림 수정
# ===================================================
print("\n[STEP 7 & 8] title / description truncation fix")
print("-" * 40)

fixed_meta = 0
all_blog_posts = (
    glob.glob(os.path.join(BASE_DIR, 'blog', '*.html')) +
    glob.glob(os.path.join(BASE_DIR, 'ko', 'blog', '*.html')) +
    glob.glob(os.path.join(BASE_DIR, 'pt', 'blog', '*.html'))
)

for fpath in all_blog_posts:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # title
    t_m = re.search(r'<title>(.*?)</title>', content)
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)

    if t_m and h1_m:
        title = t_m.group(1).strip()
        h1 = re.sub(r'<[^>]+>', '', h1_m.group(1)).strip()
        if len(title) < len(h1) - 5 and len(h1) > 10 and 'WiseAIWiseU' not in title:
            new_title = (h1[:67] + "...") if len(h1) > 70 else h1
            new_title_tag = new_title + " | WiseAIWiseU"
            content = content.replace('<title>' + title + '</title>',
                                      '<title>' + new_title_tag + '</title>')
            content = re.sub(
                r'<meta property="og:title" content="[^"]*"',
                '<meta property="og:title" content="' + new_title + '"',
                content
            )

    # description
    d_m = re.search(r'<meta name="description" content="([^"]*)"', content)
    p_m = re.search(r'<p>([\s\S]*?)</p>', content)
    if d_m and p_m:
        cur_desc = d_m.group(1)
        if len(cur_desc) < 120 and not cur_desc.strip().endswith('.'):
            p_text = re.sub(r'<[^>]+>', '', p_m.group(1)).strip()
            p_text = re.sub(r'\s+', ' ', p_text)
            new_desc = (p_text[:154] + "...") if len(p_text) > 157 else p_text
            new_desc = new_desc.replace('"', '&quot;')
            content = re.sub(
                r'<meta name="description" content="[^"]*"',
                '<meta name="description" content="' + new_desc + '"',
                content
            )
            content = re.sub(
                r'<meta property="og:description" content="[^"]*"',
                '<meta property="og:description" content="' + new_desc + '"',
                content
            )

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_meta += 1

print("  Meta fixed: " + str(fixed_meta) + " files")


# ===================================================
# 완료
# ===================================================
print("\n" + "=" * 60)
print("ALL DONE!")
print("  HTML modified (redirect/links): " + str(total_modified))
print("  robots.txt: updated")
print("  sitemap.xml: " + str(url_count) + " URLs")
print("  blog.html static links: updated")
print("  title/description fixed: " + str(fixed_meta))
print("\nNext steps:")
print("  1. git add -A && git commit -m 'SEO: fix redirects, static links, sitemap'")
print("  2. git push origin main  (deploy)")
print("  3. Google Search Console > Sitemaps > submit sitemap.xml")
print("  4. GSC > URL Inspection > Request indexing (homepage + key pages)")
