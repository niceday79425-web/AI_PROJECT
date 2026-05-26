import os
import re

BASE_DIR = r"d:\AI_PROJECT"
DOMAIN = "https://wiseaiwiseu.com"

# Subdirectory map
FOLDERS = {
    "en": os.path.join(BASE_DIR, "blog"),
    "ko": os.path.join(BASE_DIR, "ko", "blog"),
    "pt": os.path.join(BASE_DIR, "pt", "blog")
}

def clean_existing_tags(content):
    """Remove existing canonical and alternate link tags to avoid duplicates."""
    # Matches <link rel="canonical" ... /> or <link rel="alternate" ... />
    content = re.sub(r'\s*<link rel="canonical"[^>]*>', '', content)
    content = re.sub(r'\s*<link rel="alternate"[^>]*>', '', content)
    return content

def inject_seo_tags(filepath, lang, filename):
    slug = filename.replace(".html", "")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    content = clean_existing_tags(content)
    
    # Check which translations actually exist on disk
    exists = {}
    for l, path in FOLDERS.items():
        exists[l] = os.path.exists(os.path.join(path, filename))
        
    # Generate canonical URL
    if lang == "en":
        canonical_url = f"{DOMAIN}/blog/{slug}"
    else:
        canonical_url = f"{DOMAIN}/{lang}/blog/{slug}"
        
    # Build tag list
    seo_tags = []
    seo_tags.append(f'  <link rel="canonical" href="{canonical_url}" />')
    
    # Alternate hreflang tags
    for l in ["en", "ko", "pt"]:
        if exists[l]:
            href = f"{DOMAIN}/blog/{slug}" if l == "en" else f"{DOMAIN}/{l}/blog/{slug}"
            seo_tags.append(f'  <link rel="alternate" hreflang="{l}" href="{href}" />')
            
    # x-default alternate tag (default to English if exists, otherwise current lang)
    if exists["en"]:
        x_default_href = f"{DOMAIN}/blog/{slug}"
    else:
        x_default_href = canonical_url
    seo_tags.append(f'  <link rel="alternate" hreflang="x-default" href="{x_default_href}" />')
    
    seo_block = "\n" + "\n".join(seo_tags) + "\n"
    
    # Inject SEO tags right after <head>
    head_match = re.search(r'<head>', content, re.IGNORECASE)
    if head_match:
        pos = head_match.end()
        content = content[:pos] + seo_block + content[pos:]
    else:
        # Fallback if no <head> found (highly unlikely)
        print(f"[WARN] No <head> tag found in {filepath}")
        
    # Fix .html extensions on internal navigation links
    content = re.sub(r'href="/ko/blog\.html"', 'href="/ko/blog"', content)
    content = re.sub(r'href="/blog\.html"', 'href="/blog"', content)
    content = re.sub(r'href="/pt/blog\.html"', 'href="/pt/blog"', content)
    
    # Fix relative links
    content = re.sub(r'href="\.\./\.\./blog\.html"', 'href="/blog"', content)
    content = re.sub(r'href="\.\./\.\./ko/blog\.html"', 'href="/ko/blog"', content)
    content = re.sub(r'href="\.\./\.\./pt/blog\.html"', 'href="/pt/blog"', content)
    
    # Save if modified
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    fixed_count = 0
    for lang, folder in FOLDERS.items():
        if not os.path.exists(folder):
            print(f"[!] Folder not found: {folder}")
            continue
            
        print(f"Scanning blog folder for '{lang}': {folder}")
        for file in os.listdir(folder):
            if file.endswith(".html"):
                filepath = os.path.join(folder, file)
                if inject_seo_tags(filepath, lang, file):
                    fixed_count += 1
                    print(f"  [FIXED SEO] {lang}/blog/{file}")
                    
    print(f"\nTotal blog posts patched: {fixed_count}")

if __name__ == "__main__":
    main()
