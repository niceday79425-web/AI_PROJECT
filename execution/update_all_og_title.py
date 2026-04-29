import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    if not title_match:
        return False
        
    title = title_match.group(1).replace('\n', ' ').strip()
    title = re.sub(r'\s+', ' ', title)
    
    og_title_tag = f'<meta property="og:title" content="{title}">'
    
    # Check if og:title already exists
    og_title_match = re.search(r'<meta property="og:title"\s+content=".*?"\s*\/?>', content, re.DOTALL | re.IGNORECASE)
    
    if og_title_match:
        new_content = re.sub(
            r'<meta property="og:title"\s+content=".*?"\s*\/?>', 
            og_title_tag, 
            content, 
            flags=re.DOTALL | re.IGNORECASE
        )
    else:
        # Insert after <title>
        full_title_match = title_match.group(0)
        new_content = content.replace(full_title_match, full_title_match + f'\n    {og_title_tag}')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    root_dir = r"d:\AI_PROJECT"
    updated_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.git' in dirpath:
            continue
            
        for filename in filenames:
            if filename.endswith(".html"):
                filepath = os.path.join(dirpath, filename)
                try:
                    if process_file(filepath):
                        updated_count += 1
                        print(f"Updated {filepath}")
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
                    
    print(f"Total files updated: {updated_count}")

if __name__ == "__main__":
    main()
