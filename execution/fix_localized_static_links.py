import os
import re

BASE_DIR = r"d:\AI_PROJECT"
LANGS = ["ko", "pt"]
PAGES = ["about", "contact", "privacy", "blog", "learn", "list", "calculator", "calendar", "fortune"]

def fix_links_in_file(filepath, lang):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Update non-localized base links to localized paths
    for page in PAGES:
        target_path = f"/{lang}/{page}" if lang else f"/{page}"
        content = re.sub(rf'href="/{page}"(?!\w)', f'href="{target_path}"', content)
        content = re.sub(rf'href="/{page}\.html"', f'href="{target_path}"', content)

    # 2. Fix localized links that still have .html extension
    for l in ["ko", "pt"]:
        for page in PAGES:
            content = re.sub(rf'href="/{l}/{page}\.html"', f'href="/{l}/{page}"', content)

    # 3. Fix relative links to .html files
    for page in PAGES:
        target_path = f"/{lang}/{page}" if lang else f"/{page}"
        content = re.sub(rf'href="\.\./\.\./{page}\.html"', f'href="{target_path}"', content)
        content = re.sub(rf'href="\.\./\.\./{page}"', f'href="{target_path}"', content)
        content = re.sub(rf'href="\.\./{page}\.html"', f'href="{target_path}"', content)
        content = re.sub(rf'href="\.\./{page}"', f'href="{target_path}"', content)

    # 4. Clean up lang-selector or general links in main pages to not have .html
    for page in PAGES:
        content = re.sub(rf'href="/{page}\.html"', f'href="/{page}"', content)

    # Clean double slashes
    content = content.replace("href=\"//", "href=\"/")
    if lang:
        content = content.replace(f"/{lang}//", f"/{lang}/")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[FIXED] {os.path.relpath(filepath, BASE_DIR)}")
        return True
    return False

def main():
    modified_count = 0
    
    # 1. English files in root
    for file in os.listdir(BASE_DIR):
        if file.endswith(".html"):
            filepath = os.path.join(BASE_DIR, file)
            if fix_links_in_file(filepath, ""):
                modified_count += 1
                
    # 2. English files in blog/
    blog_dir = os.path.join(BASE_DIR, "blog")
    if os.path.exists(blog_dir):
        for file in os.listdir(blog_dir):
            if file.endswith(".html"):
                filepath = os.path.join(blog_dir, file)
                if fix_links_in_file(filepath, ""):
                    modified_count += 1
                    
    # 3. Localized files (ko, pt)
    for lang in LANGS:
        lang_dir = os.path.join(BASE_DIR, lang)
        if not os.path.exists(lang_dir):
            continue
        for root, dirs, files in os.walk(lang_dir):
            for file in files:
                if file.endswith(".html"):
                    filepath = os.path.join(root, file)
                    if fix_links_in_file(filepath, lang):
                        modified_count += 1
                        
    print(f"\nTotal files updated: {modified_count}")

if __name__ == "__main__":
    main()
