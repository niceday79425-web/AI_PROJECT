"""
Phase 0: Critical Fixes
1. 광고 플레이스홀더 완전 제거 (ca-pub-XXXXXXXXXXXXXXXX)
2. 연락처 이메일 수정
3. og:image 추가
4. H1 태그 수정 (blog.html)
"""
import os, re, glob

ROOT = r"d:\AI_PROJECT"
OG_IMAGE_TAG = '<meta property="og:image" content="https://wiseaiwiseu.com/og-image.png">\n    <meta property="og:image:width" content="1200">\n    <meta property="og:image:height" content="630">'

AD_PATTERNS = [
    # full <div class="ad-slot">...</div> blocks
    re.compile(r'<div class="ad-slot"[^>]*>.*?</div>\s*', re.DOTALL),
    re.compile(r'<aside class="ad-slot[^"]*"[^>]*>.*?</aside>\s*', re.DOTALL),
    re.compile(r'<div class="ad-in-article"[^>]*>.*?</div>\s*', re.DOTALL),
    # standalone adsbygoogle script tags
    re.compile(r'<script[^>]*>\s*\(?adsbygoogle\s*=.*?\)\.push\(\{\}\);?\s*</script>\s*', re.DOTALL),
    # adsense loader script tag
    re.compile(r'<script[^>]*pagead2\.googlesyndication\.com[^>]*></script>\s*', re.DOTALL),
    re.compile(r'<!-- Google AdSense.*?-->\s*', re.DOTALL),
    re.compile(r'<!-- TODO: Replace with actual AdSense.*?-->\s*', re.DOTALL),
]

def remove_ads(content):
    for pat in AD_PATTERNS:
        content = pat.sub('', content)
    return content

def fix_email(content):
    content = content.replace('support@WiseAIWiseU', 'support@wiseaiwiseu.com')
    return content

def add_og_image(content):
    if 'og:image' in content:
        return content
    # insert after og:description
    content = re.sub(
        r'(<meta property="og:description"[^>]*>)',
        r'\1\n    ' + OG_IMAGE_TAG,
        content, count=1
    )
    return content

def fix_blog_h1(content, lang='en'):
    """blog.html에 H1 추가 (h2 마켓 인사이트 앞에)"""
    h1_map = {
        'en': '<h1 style="margin:0 0 0.5rem;">Market Insights &amp; US Stock Analysis</h1>',
        'ko': '<h1 style="margin:0 0 0.5rem;">미국 주식 시장 분석 &amp; 배당주 인사이트</h1>',
        'pt': '<h1 style="margin:0 0 0.5rem;">Análise do Mercado de Ações dos EUA</h1>',
    }
    h1 = h1_map.get(lang, h1_map['en'])
    if '<h1' in content:
        return content
    # insert before first <h2
    content = re.sub(r'(<h2\b)', h1 + '\n                        ' + r'\1', content, count=1)
    return content

def process_file(path, lang=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            original = f.read()
        content = original
        content = remove_ads(content)
        content = fix_email(content)
        content = add_og_image(content)
        # H1 fix only for blog listing pages
        fname = os.path.basename(path)
        if fname == 'blog.html' and lang:
            content = fix_blog_h1(content, lang)
        if content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  [ERR] {path}: {e}")
        return False

# --- Collect all HTML files ---
html_files = []

# Root HTML files (lang=en)
for f in glob.glob(os.path.join(ROOT, '*.html')):
    html_files.append((f, 'en'))

# /ko/ HTML files
for f in glob.glob(os.path.join(ROOT, 'ko', '*.html')):
    lang = 'ko'
    html_files.append((f, lang))

# /pt/ HTML files  
for f in glob.glob(os.path.join(ROOT, 'pt', '*.html')):
    html_files.append((f, 'pt'))

# Blog posts (en / ko / pt)
for d, lang in [('blog', 'en'), ('ko/blog', 'ko'), ('pt/blog', 'pt')]:
    for f in glob.glob(os.path.join(ROOT, d, '*.html')):
        html_files.append((f, lang))

print(f"[*] Processing {len(html_files)} HTML files...")
changed = 0
for path, lang in html_files:
    if process_file(path, lang):
        changed += 1
        print(f"  [OK] {os.path.relpath(path, ROOT)}")

print(f"\n[DONE] Modified {changed} / {len(html_files)} files")
print("[✓] P0-1: Ad placeholders removed")
print("[✓] P0-2: Email fixed -> support@wiseaiwiseu.com")
print("[✓] P0-3: og:image tags added")
print("[✓] P0-4: H1 tags added to blog.html files")
