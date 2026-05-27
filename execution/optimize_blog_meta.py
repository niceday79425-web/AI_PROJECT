import os
import re

BASE_DIR = r"d:\AI_PROJECT"
FOLDERS = {
    "en": os.path.join(BASE_DIR, "blog"),
    "pt": os.path.join(BASE_DIR, "pt", "blog")
}

BRAND = " | WiseAIWiseU"

# Suffixes to clean up from titles
SUFFIXES_TO_CLEAN = [
    " | U.S. Stock Analysis · WiseAIWiseU",
    " | U.S. Stock Analysis - WiseAIWiseU",
    " | U.S. Stock Analysis | WiseAIWiseU",
    " | U.S. Stock Analysis",
    " · WiseAIWiseU",
    " - WiseAIWiseU",
    " | WiseAIWiseU",
    " | WiseAI",
    " | WiseU",
    " | 미국 주식 분석 · WiseAIWiseU",
    " | 미국 주식 분석 - WiseAIWiseU",
    " | 미국 주식 분석",
    " | Analise de Ações dos EUA · WiseAIWiseU",
    " | Analise de Ações dos EUA",
    " | Análise de Ações dos EUA · WiseAIWiseU"
]

def clean_title(title_text):
    title_text = title_text.strip()
    for suffix in SUFFIXES_TO_CLEAN:
        if title_text.endswith(suffix):
            title_text = title_text[:-len(suffix)].strip()
    return title_text

def optimize_file(filepath, lang):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # 1. Parse Title
    title_match = re.search(r'<title[^>]*>([\s\S]*?)</title>', content, re.IGNORECASE)
    if not title_match:
        return False
        
    raw_title = title_match.group(1).strip()
    clean_t = clean_title(raw_title)
    
    # Build optimized title (target: 50-60 chars)
    # We want `{clean_t} | WiseAIWiseU` (brand is 14 chars)
    # If total length is > 60, we truncate clean_t
    max_clean_len = 60 - len(BRAND) # 46 chars
    if len(clean_t) > max_clean_len:
        clean_t = clean_t[:max_clean_len - 3] + "..."
        
    new_title = clean_t + BRAND
    
    # 2. Parse Description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content, re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta\s+content="([^"]*)"\s+name="description"', content, re.IGNORECASE)
        
    if desc_match:
        raw_desc = desc_match.group(1).strip()
    else:
        raw_desc = ""
        
    # Build optimized description (target: 130-150 chars)
    if len(raw_desc) < 120:
        if lang == "en":
            padding = " Read the full in-depth U.S. stock market and dividend analysis on WiseAIWiseU."
        else:
            padding = " Leia a análise detalhada completa do mercado de ações e dividendos no WiseAIWiseU."
        new_desc = raw_desc + padding
    else:
        new_desc = raw_desc
        
    if len(new_desc) > 150:
        new_desc = new_desc[:147] + "..."
        
    # Replace in content
    # Title
    content = re.sub(r'<title[^>]*>([\s\S]*?)</title>', f'<title>{new_title}</title>', content, flags=re.IGNORECASE)
    # og:title
    content = re.sub(r'<meta\s+property="og:title"\s+content="[^"]*"[^>]*>', f'<meta property="og:title" content="{new_title}">', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+content="[^"]*"\s+property="og:title"[^>]*>', f'<meta content="{new_title}" property="og:title">', content, flags=re.IGNORECASE)
    
    # Description
    content = re.sub(r'<meta\s+name="description"\s+content="[^"]*"[^>]*>', f'<meta name="description" content="{new_desc}">', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+content="[^"]*"\s+name="description"[^>]*>', f'<meta content="{new_desc}" name="description">', content, flags=re.IGNORECASE)
    
    # og:description
    content = re.sub(r'<meta\s+property="og:description"\s+content="[^"]*"[^>]*>', f'<meta property="og:description" content="{new_desc}">', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+content="[^"]*"\s+property="og:description"[^>]*>', f'<meta content="{new_desc}" property="og:description">', content, flags=re.IGNORECASE)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    total_updated = 0
    for lang, folder in FOLDERS.items():
        if not os.path.exists(folder):
            continue
        print(f"Optimizing meta tags in {folder}...")
        for file in os.listdir(folder):
            if file.endswith(".html"):
                filepath = os.path.join(folder, file)
                if optimize_file(filepath, lang):
                    total_updated += 1
                    
    print(f"Done. Optimized {total_updated} files.")

if __name__ == "__main__":
    main()
