import os

# Define replacement rules by directory
REPLACEMENTS = {
    "d:\\AI_PROJECT": '<a href="/" class="logo">StockWise.ai</a>',
    "d:\\AI_PROJECT\\ko": '<a href="/ko/" class="logo">StockWise.ai</a>',
    "d:\\AI_PROJECT\\pt": '<a href="/pt/" class="logo">StockWise.ai</a>'
}

TARGET_STRING = '<div class="logo">StockWise.ai</div>'

def update_files():
    print("Starting update...")
    
    # Traverse directories
    for root, dirs, files in os.walk("d:\\AI_PROJECT"):
        # Determine the replacement string based on current directory
        current_replacement = None
        
        # Check explicit match first (ko/pt)
        if root.endswith("\\ko") or "\\ko\\" in root:
             current_replacement = REPLACEMENTS["d:\\AI_PROJECT\\ko"]
        elif root.endswith("\\pt") or "\\pt\\" in root:
             current_replacement = REPLACEMENTS["d:\\AI_PROJECT\\pt"]
        # Root directory files (exclude subdirs like css, js, etc unless handled)
        elif root == "d:\\AI_PROJECT":
             current_replacement = REPLACEMENTS["d:\\AI_PROJECT"]
        
        # Skip if no replacement rule applies (e.g. css folder, though we only look for html)
        if not current_replacement:
            continue
            
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if TARGET_STRING in content:
                        new_content = content.replace(TARGET_STRING, current_replacement)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"[UPDATED] {filepath}")
                    else:
                        # Check if already updated (to avoid double work or confusion)
                        if 'class="logo">StockWise.ai</a>' in content:
                            print(f"[SKIPPED] {filepath} (Already updated)")
                        else:
                            print(f"[SKIPPED] {filepath} (Pattern not found)")
                            
                except Exception as e:
                    print(f"[ERROR] {filepath}: {e}")

if __name__ == "__main__":
    update_files()
