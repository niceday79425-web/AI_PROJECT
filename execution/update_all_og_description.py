import os
import re

DEFAULT_DESC = "Discover top-rated US dividend stocks, simulate compound interest growth with the Snowball Calculator, and track dividend payment dates."

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract meta description
    desc_match = re.search(r'<meta name="description"\s+content="(.*?)"', content, re.DOTALL | re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta content="(.*?)"\s+name="description"', content, re.DOTALL | re.IGNORECASE)
        
    description = ""
    if desc_match:
        description = desc_match.group(1).replace('\n', ' ').strip()
        description = re.sub(r'\s+', ' ', description)
    else:
        # Try to use title, otherwise default
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
            description = f"{title} - {DEFAULT_DESC}"
        else:
            description = DEFAULT_DESC
            
    # Max length or standard format
    # description = description[:150]
    
    og_desc_tag = f'<meta property="og:description" content="{description}">'
    
    # Check if og:description already exists
    og_desc_match = re.search(r'<meta property="og:description"\s+content=".*?"\s*\/?>', content, re.DOTALL | re.IGNORECASE)
    
    if og_desc_match:
        new_content = re.sub(
            r'<meta property="og:description"\s+content=".*?"\s*\/?>', 
            og_desc_tag, 
            content, 
            flags=re.DOTALL | re.IGNORECASE
        )
    else:
        # Insert it
        meta_desc_full = re.search(r'<meta[^>]*name="description"[^>]*>', content, re.IGNORECASE)
        if meta_desc_full:
            full_match = meta_desc_full.group(0)
            new_content = content.replace(full_match, full_match + f'\n    {og_desc_tag}')
        else:
            # Insert after <title>
            title_full = re.search(r'<title>.*?</title>', content, re.IGNORECASE)
            if title_full:
                full_match = title_full.group(0)
                new_content = content.replace(full_match, full_match + f'\n    <meta name="description" content="{description}">\n    {og_desc_tag}')
            else:
                # Insert before </head>
                if '</head>' in content:
                    new_content = content.replace('</head>', f'    <meta name="description" content="{description}">\n    {og_desc_tag}\n</head>')
                else:
                    return False

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
