import os
import re

BASE_DOMAIN = "https://wiseaiwiseu.com"
LANGS = {
    "en": {"path": "blog", "hreflang": "en"},
    "ko": {"path": "ko/blog", "hreflang": "ko"},
    "pt": {"path": "pt/blog", "hreflang": "pt"}
}

def get_meta_tags(filename, current_lang):
    tags = []
    # Clean filename (no extension)
    clean_name = filename.replace(".html", "")
    
    # Canonical
    canonical_url = f"{BASE_DOMAIN}/{LANGS[current_lang]['path']}/{clean_name}"
    tags.append(f'    <link rel="canonical" href="{canonical_url}" />')
    
    # Hreflangs
    for lang, info in LANGS.items():
        # Check if the file exists in that language
        lang_path = os.path.join(info['path'], filename)
        if os.path.exists(lang_path):
            alt_url = f"{BASE_DOMAIN}/{info['path']}/{clean_name}"
            tags.append(f'    <link rel="alternate" hreflang="{info["hreflang"]}" href="{alt_url}" />')
    
    # x-default (usually English version)
    tags.append(f'    <link rel="alternate" hreflang="x-default" href="{BASE_DOMAIN}/blog/{clean_name}" />')
    
    return "\n".join(tags)

def update_files():
    for lang, info in LANGS.items():
        blog_dir = info['path']
        if not os.path.exists(blog_dir):
            continue
            
        for filename in os.listdir(blog_dir):
            if not filename.endswith(".html"):
                continue
                
            filepath = os.path.join(blog_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Skip if already has canonical (to avoid duplicates)
            if 'rel="canonical"' in content:
                # Still, let's remove old ones and re-insert to be sure they are correct
                content = re.sub(r'    <link rel="canonical".*?/>\n?', '', content)
                content = re.sub(r'    <link rel="alternate" hreflang.*?/>\n?', '', content)

            meta_tags = get_meta_tags(filename, lang)
            
            # Insert before </head>
            if "</head>" in content:
                new_content = content.replace("</head>", f"{meta_tags}\n</head>")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {filepath}")

if __name__ == "__main__":
    update_files()
