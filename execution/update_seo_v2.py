import os
import re

BASE_DOMAIN = "https://wiseaiwiseu.com"
LANGS = {
    "en": {"path": "blog", "hreflang": "en"},
    "ko": {"path": "ko/blog", "hreflang": "ko"},
    "pt": {"path": "pt/blog", "hreflang": "pt"}
}

def clean_tags(content):
    # Remove old canonical, hreflang, and OG tags to prevent duplicates
    # Case insensitive matching for rel and properties
    content = re.sub(r'    <link rel="canonical".*?/>\n?', '', content, flags=re.I)
    content = re.sub(r'    <link rel="alternate" hreflang.*?/>\n?', '', content, flags=re.I)
    content = re.sub(r'    <meta property="og:.*?".*?>\n?', '', content, flags=re.I)
    return content

def get_meta_tags(filename, current_lang, title, description):
    tags = []
    clean_name = filename.replace(".html", "")
    page_path = f"{LANGS[current_lang]['path']}/{clean_name}"
    full_url = f"{BASE_DOMAIN}/{page_path}"
    
    # Canonical
    tags.append(f'    <link rel="canonical" href="{full_url}" />')
    
    # Hreflangs
    for lang, info in LANGS.items():
        lang_file_path = os.path.join(info['path'], filename)
        if os.path.exists(lang_file_path):
            alt_url = f"{BASE_DOMAIN}/{info['path']}/{clean_name}"
            tags.append(f'    <link rel="alternate" hreflang="{info["hreflang"]}" href="{alt_url}" />')
    
    # x-default
    tags.append(f'    <link rel="alternate" hreflang="x-default" href="{BASE_DOMAIN}/blog/{clean_name}" />')
    
    # Open Graph Tags
    tags.append(f'    <meta property="og:title" content="{title}">')
    tags.append(f'    <meta property="og:description" content="{description}">')
    tags.append(f'    <meta property="og:url" content="{full_url}">')
    tags.append(f'    <meta property="og:image" content="{BASE_DOMAIN}/logo.png">')
    tags.append(f'    <meta property="og:type" content="article">')
    
    return "\n".join(tags)

def update_files():
    for lang, info in LANGS.items():
        blog_dir = info['path']
        if not os.path.exists(blog_dir): continue
            
        for filename in os.listdir(blog_dir):
            if not filename.endswith(".html"): continue
                
            filepath = os.path.join(blog_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract current title and description
            title_match = re.search(r'<title>(.*?)</title>', content)
            desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
            
            title = title_match.group(1) if title_match else "WiseAIWiseU"
            description = desc_match.group(1) if desc_match else ""
            
            # Trim for Naver (Title 40, Desc 80)
            title = title[:40].strip()
            description = description[:80].strip()
            
            # Update title and description in content
            content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content)
            content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{description}">', content)
            
            # Clean old tags
            content = clean_tags(content)
            
            # Generate new tags
            meta_tags = get_meta_tags(filename, lang, title, description)
            
            if "</head>" in content:
                content = content.replace("</head>", f"{meta_tags}\n</head>")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated {filepath}")

if __name__ == "__main__":
    update_files()
