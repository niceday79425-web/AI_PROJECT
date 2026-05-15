import os
import re

ROOT = r"d:\AI_PROJECT"

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Remove sessionStorage redirected flag
    content = re.sub(r'<script>\s*sessionStorage\.setItem\(\'redirected\', \'true\'\);\s*</script>', '', content)
    content = re.sub(r'sessionStorage\.setItem\(\'redirected\', \'true\'\);', '', content)
    content = re.sub(r'<script>\s*</script>', '', content)

    # 2. Function to get clean URL from filepath
    def get_clean_url(path):
        rel = os.path.relpath(path, ROOT).replace('\\', '/')
        if rel == '.': return "https://wiseaiwiseu.com/"
        if rel.endswith('index.html'):
            rel = rel[:-10]
        elif rel.endswith('.html'):
            rel = rel[:-5]
        return f"https://wiseaiwiseu.com/{rel}"

    # 3. Fix Canonical
    clean_url = get_clean_url(filepath)
    if '<link rel="canonical"' in content:
        content = re.sub(r'<link rel="canonical" href="[^"]+" />', f'<link rel="canonical" href="{clean_url}" />', content)
    else:
        # Insert canonical before </head> if missing
        content = content.replace('</head>', f'    <link rel="canonical" href="{clean_url}" />\n</head>')

    # 4. Fix Hreflang Tags
    # Pattern: <link rel="alternate" hreflang="..." href="..." />
    def fix_hreflang(match):
        lang = match.group(1)
        url = match.group(2)
        # Convert url to clean url
        # Extract the relative part
        if "wiseaiwiseu.com/" in url:
            rel_part = url.split("wiseaiwiseu.com/")[-1]
            if rel_part.endswith('index.html'): rel_part = rel_part[:-10]
            elif rel_part.endswith('.html'): rel_part = rel_part[:-5]
            new_url = f"https://wiseaiwiseu.com/{rel_part}"
            return f'<link rel="alternate" hreflang="{lang}" href="{new_url}" />'
        return match.group(0)

    content = re.sub(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)" />', fix_hreflang, content)

    # 5. Replace JS-based navigation (already mostly done, but to be sure)
    def replace_article(match):
        url = match.group(2)
        if url.endswith('.html'): url = url[:-5] # Optional: Clean URLs in links too
        return f'<a href="{url}" class="blog-card" style="text-decoration:none; display:block; cursor:pointer;">'

    content = re.sub(r'<article([^>]+)onclick="location\.href=\'([^\']+)\'"([^>]*)>', replace_article, content)
    content = content.replace('</article>', '</a>')

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(ROOT):
        if '.git' in dirs: dirs.remove('.git')
        for file in files:
            if file.endswith('.html'):
                if fix_file(os.path.join(root, file)):
                    count += 1
    print(f"Total files fixed: {count}")

if __name__ == "__main__":
    main()
