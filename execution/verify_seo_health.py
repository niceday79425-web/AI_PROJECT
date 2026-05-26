import os
import re

BASE_DIR = r"d:\AI_PROJECT"
LANGS = ["en", "ko", "pt"]

def check_file_seo(filepath, rel_path):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    errors = []
    
    # 1. Canonical tag count check
    canonicals = re.findall(r'<link rel="canonical"[^>]*>', content)
    if len(canonicals) == 0:
        # Ignore sub-scripts or dynamic templates if any, but regular files should have it
        errors.append("Missing <link rel='canonical'>")
    elif len(canonicals) > 1:
        errors.append(f"Multiple canonical tags found: {len(canonicals)}")
    else:
        # Check if canonical has .html
        if ".html" in canonicals[0]:
            errors.append(f"Canonical URL has .html extension: {canonicals[0]}")
            
    # 2. Alternate hreflang checks
    alternates = re.findall(r'<link rel="alternate"[^>]*>', content)
    for alt in alternates:
        if ".html" in alt:
            errors.append(f"Alternate URL has .html extension: {alt}")
            
    # 3. Check for any internal links with .html pointing to pages we want extension-free
    # e.g., href="/ko/about.html" or href="/about.html"
    # We will look for href="...page.html" inside navigation/footer regions or the whole body
    # Exclude external links and script files
    html_links = re.findall(r'href="[^"]+\.html"', content)
    for link in html_links:
        # If it points to an internal page (about.html, blog.html, list.html, etc.)
        # but let's exclude external links or files not in our pages list
        if any(p + ".html" in link for p in ["about", "blog", "list", "calculator", "calendar", "fortune", "privacy", "contact", "learn", "index"]):
            # Ignore language selector on some legacy files if we missed it
            errors.append(f"Found internal link with .html extension: {link}")
            
    # 4. H1 tag validation (exactly 1 per page)
    h1_tags = re.findall(r'<h1[^>]*>([\s\S]*?)</h1>', content, re.IGNORECASE)
    if len(h1_tags) == 0:
        errors.append("Missing <h1> tag (Crucial for Bing Webmaster Tools)")
    elif len(h1_tags) > 1:
        errors.append(f"Multiple <h1> tags found: {len(h1_tags)}")
    else:
        # Check if H1 content is empty
        h1_content = h1_tags[0].strip()
        if not h1_content:
            errors.append("Empty <h1> tag found")

    # 5. Title tag validation (exactly 1 per page)
    titles = re.findall(r'<title[^>]*>([\s\S]*?)</title>', content, re.IGNORECASE)
    if len(titles) == 0:
        errors.append("Missing <title> tag")
    elif len(titles) > 1:
        errors.append(f"Multiple <title> tags found: {len(titles)}")
    else:
        title_content = titles[0].strip()
        if not title_content:
            errors.append("Empty <title> tag found")

    return errors

def main():
    total_checked = 0
    total_errors = 0
    
    folders = [
        BASE_DIR,
        os.path.join(BASE_DIR, "ko"),
        os.path.join(BASE_DIR, "pt"),
        os.path.join(BASE_DIR, "blog"),
        os.path.join(BASE_DIR, "ko", "blog"),
        os.path.join(BASE_DIR, "pt", "blog")
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            continue
            
        for file in os.listdir(folder):
            # Check only HTML files in the immediate folder
            filepath = os.path.join(folder, file)
            if os.path.isfile(filepath) and file.endswith(".html"):
                rel_path = os.path.relpath(filepath, BASE_DIR)
                errors = check_file_seo(filepath, rel_path)
                total_checked += 1
                if errors:
                    total_errors += len(errors)
                    print(f"[ERROR] {rel_path}:")
                    for err in errors:
                        print(f"  - {err}")
                        
    print(f"\nSEO Audit Complete.")
    print(f"Total HTML files checked: {total_checked}")
    print(f"Total issues found: {total_errors}")

if __name__ == "__main__":
    main()
