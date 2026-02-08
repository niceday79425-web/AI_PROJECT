
import os

BASE_URL = "https://ai-project-1en.pages.dev"
PAGES = ["index.html", "list.html", "blog.html", "calculator.html", "calendar.html", "fortune.html", "privacy.html", "about.html", "contact.html"]

def get_href_tags(filename):
    # Construct tags for a specific filename
    # Assumes filename is same across languages
    return f'''
    <link rel="canonical" href="{BASE_URL}/{filename}" />
    <link rel="alternate" hreflang="en" href="{BASE_URL}/{filename}" />
    <link rel="alternate" hreflang="ko" href="{BASE_URL}/ko/{filename}" />
    <link rel="alternate" hreflang="pt" href="{BASE_URL}/pt/{filename}" />
    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/{filename}" />
'''

def inject_tags(filepath, filename):
    try:
        if not os.path.exists(filepath):
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tags = get_href_tags(filename).strip()
        
        # Check if tags already exist and remove them to avoid duplicates
        import re
        content = re.sub(r'\s*<link rel="canonical".*?/>\s*', '\n', content)
        content = re.sub(r'\s*<link rel="alternate" hreflang=".*?/>\s*', '\n', content)

        # Inject before </head>
        if "</head>" in content:
            content = content.replace("</head>", f"    {tags}\n</head>")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[UPDATED] {filepath}")
            
    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")

def main():
    # Root
    for page in PAGES:
        inject_tags(os.path.join("d:\\AI_PROJECT", page), page)
        
    # KO
    for page in PAGES:
        inject_tags(os.path.join("d:\\AI_PROJECT\\ko", page), page)
        
    # PT
    for page in PAGES:
        inject_tags(os.path.join("d:\\AI_PROJECT\\pt", page), page)

if __name__ == "__main__":
    main()
