
import os

BASE_URL = "https://ai-project-1en.pages.dev"
PAGES = ["index.html", "list.html", "blog.html", "calculator.html", "calendar.html", "fortune.html"]

def get_href_tags(filename):
    # Construct tags for a specific filename
    # Assumes filename is same across languages
    return f'''
    <link rel="alternate" hreflang="en" href="{BASE_URL}/{filename}" />
    <link rel="alternate" hreflang="ko" href="{BASE_URL}/ko/{filename}" />
    <link rel="alternate" hreflang="pt" href="{BASE_URL}/pt/{filename}" />
    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/{filename}" />
'''

def inject_tags(filepath, filename):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "hreflang" in content:
            print(f"[SKIPPED] {filepath} (Already has hreflang)")
            return

        tags = get_href_tags(filename)
        
        # Inject before </head>
        if "</head>" in content:
            content = content.replace("</head>", f"{tags}\n</head>")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[INJECTED] {filepath}")
            
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
