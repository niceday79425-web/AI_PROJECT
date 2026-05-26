import os
import re

BASE_DIR = r"d:\AI_PROJECT"
FOLDERS = {
    "en": os.path.join(BASE_DIR, "blog"),
    "ko": os.path.join(BASE_DIR, "ko", "blog"),
    "pt": os.path.join(BASE_DIR, "pt", "blog")
}

CATEGORIES = {
    "blog": {
        "en": "US Stock Insights",
        "ko": "미국 주식 인사이트",
        "pt": "Insights de Ações dos EUA"
    },
    "edu": {
        "en": "US Dividend Stock Lessons",
        "ko": "미국 배당주 강의",
        "pt": "Aulas de Ações de Dividendos dos EUA"
    }
}

# Prefixes to clean up from titles to ensure idempotency
PREFIXES_TO_CLEAN = [
    "US Stock Insights:",
    "미국 주식 인사이트:",
    "Insights de Ações dos EUA:",
    "US Dividend Stock Lessons:",
    "미국 배당주 강의:",
    "Aulas de Ações de Dividendos dos EUA:"
]

def clean_title(title_text):
    title_text = title_text.strip()
    for prefix in PREFIXES_TO_CLEAN:
        if title_text.startswith(prefix):
            title_text = title_text[len(prefix):].strip()
    return title_text

def fix_h1_for_file(filepath, lang, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # 1. Determine if it's blog or edu
    # We check if filename starts with a date like YYYY-MM-DD
    is_blog = re.match(r'^\d{4}-\d{2}-\d{2}', filename) is not None
    cat_type = "blog" if is_blog else "edu"
    category = CATEGORIES[cat_type][lang]
    
    # 2. Find and update the post-hero section H1
    # We want to match <section class="post-hero">...</section> and find the <h1> inside
    hero_pattern = re.compile(r'(<section class="post-hero">[\s\S]*?)(<h1[^>]*>)([\s\S]*?)(</h1>)([\s\S]*?</section>)', re.IGNORECASE)
    
    hero_match = hero_pattern.search(content)
    if hero_match:
        before_h1 = hero_match.group(1)
        h1_start_tag = hero_match.group(2)
        h1_inner = hero_match.group(3)
        h1_end_tag = hero_match.group(4)
        after_h1 = hero_match.group(5)
        
        # Clean title and prepend category
        cleaned = clean_title(h1_inner)
        new_h1_inner = f"{category}: {cleaned}"
        
        # Rebuild hero section
        new_hero = f"{before_h1}{h1_start_tag}{new_h1_inner}{h1_end_tag}{after_h1}"
        content = content[:hero_match.start()] + new_hero + content[hero_match.end():]
    else:
        # Fallback: Find the first <h1> tag in the entire document and update it
        first_h1_pattern = re.compile(r'(<h1[^>]*>)([\s\S]*?)(</h1>)', re.IGNORECASE)
        first_h1_match = first_h1_pattern.search(content)
        if first_h1_match:
            h1_start_tag = first_h1_match.group(1)
            h1_inner = first_h1_match.group(2)
            h1_end_tag = first_h1_match.group(3)
            
            cleaned = clean_title(h1_inner)
            new_h1_inner = f"{category}: {cleaned}"
            
            new_h1 = f"{h1_start_tag}{new_h1_inner}{h1_end_tag}"
            content = content[:first_h1_match.start()] + new_h1 + content[first_h1_match.end():]
        else:
            print(f"[WARN] No h1 tag found at all in: {lang}/{filename}")
        
    # 3. Find any OTHER h1 tags outside post-hero and change them to h2
    # To do this safely, we can find the end of the post-hero section and replace h1 tags after it.
    hero_section_end = re.search(r'</section>\s*<main', content, re.IGNORECASE)
    if hero_section_end:
        split_pos = hero_section_end.start()
        header_part = content[:split_pos]
        main_part = content[split_pos:]
        
        # Replace <h1...> -> <h2...> and </h1> -> </h2> in main_part
        # e.g., <h1 style="..."> -> <h2 style="...">
        main_part = re.sub(r'<h1([^>]*)>', r'<h2\1>', main_part, flags=re.IGNORECASE)
        main_part = re.sub(r'</h1>', r'</h2>', main_part, flags=re.IGNORECASE)
        
        content = header_part + main_part
    else:
        # Fallback if structure is slightly different, replace all other h1s except the first one
        # Let's count h1 tags
        h1_matches = list(re.finditer(r'<h1[^>]*>[\s\S]*?</h1>', content, re.IGNORECASE))
        if len(h1_matches) > 1:
            # Keep first h1, replace subsequent ones
            # We will split at the end of the first h1 match
            first_h1_end = h1_matches[0].end()
            first_part = content[:first_h1_end]
            second_part = content[first_h1_end:]
            
            second_part = re.sub(r'<h1([^>]*)>', r'<h2\1>', second_part, flags=re.IGNORECASE)
            second_part = re.sub(r'</h1>', r'</h2>', second_part, flags=re.IGNORECASE)
            
            content = first_part + second_part
            
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
            
        print(f"Scanning blog/edu folder for '{lang}': {folder}")
        for file in os.listdir(folder):
            if file.endswith(".html"):
                filepath = os.path.join(folder, file)
                if fix_h1_for_file(filepath, lang, file):
                    fixed_count += 1
                    
    print(f"\nTotal pages patched: {fixed_count}")

if __name__ == "__main__":
    main()
