import os
import json
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

DOMAIN = "https://wiseaiwiseu.com"
LANGS = {
    "en": {"path": "", "hreflang": "en"},
    "ko": {"path": "ko/", "hreflang": "ko"},
    "pt": {"path": "pt/", "hreflang": "pt"}
}

STATIC_PAGES = [
    "index.html",
    "list.html",
    "calculator.html",
    "calendar.html",
    "fortune.html",
    "blog.html",
    "about.html",
    "contact.html",
    "privacy.html"
]

def get_last_mod(file_path):
    if os.path.exists(file_path):
        mtime = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    return datetime.now().strftime('%Y-%m-%d')

# Register namespaces to use proper prefixes
ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')

def generate_sitemap():
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    # 1. Add Static Pages
    for page in STATIC_PAGES:
        # Create a URL entry for each language
        for lang, info in LANGS.items():
            url_node = ET.SubElement(urlset, "url")
            
            # loc
            path = info["path"] + page
            loc_val = f"{DOMAIN}/{path}"
            loc = ET.SubElement(url_node, "loc")
            loc.text = loc_val
            
            # alternate links
            for alt_lang, alt_info in LANGS.items():
                alt_path = alt_info["path"] + page
                alt_link = ET.SubElement(url_node, "{http://www.w3.org/1999/xhtml}link")
                alt_link.set("rel", "alternate")
                alt_link.set("hreflang", alt_info["hreflang"])
                alt_link.set("href", f"{DOMAIN}/{alt_path}")
            
            # x-default
            default_link = ET.SubElement(url_node, "{http://www.w3.org/1999/xhtml}link")
            default_link.set("rel", "alternate")
            default_link.set("hreflang", "x-default")
            default_link.set("href", f"{DOMAIN}/{page}")

            # lastmod
            full_path = os.path.join(os.getcwd(), info["path"], page)
            lastmod = ET.SubElement(url_node, "lastmod")
            lastmod.text = get_last_mod(full_path)

            # changefreq & priority
            changefreq = ET.SubElement(url_node, "changefreq")
            changefreq.text = "daily"
            priority = ET.SubElement(url_node, "priority")
            priority.text = "1.0" if page == "index.html" else "0.8"

    # 2. Add Blog Posts from posts.json
    blog_posts = {} # mapping of basename -> {lang: full_link}
    
    # We first collect EVERY post from EVERY language to group them.
    for lang, info in LANGS.items():
        json_path = os.path.join(os.getcwd(), info["path"], "posts.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    posts = json.load(f)
                    for post in posts:
                        link = post.get('link')
                        if not link: continue
                        
                        # Normalize basename: blog/2026-03... -> 2026-03...
                        basename = link.split('/')[-1]
                        
                        # Handle special cases where filenames are different but related
                        # e.g. compound-interest-power.html vs compound-interest-power-ko.html
                        # For now, we'll try to match by removing -ko or -pt if they exist at the end
                        base_match = re.sub(r'-(ko|pt|en)\.html$', '.html', basename)
                        
                        if base_match not in blog_posts:
                            blog_posts[base_match] = {}
                        
                        blog_posts[base_match][lang] = f"{info['path']}{link}"
            except Exception as e:
                print(f"Error reading {json_path}: {e}")

    # Add blog post URLs
    for base_match, lang_links in blog_posts.items():
        for lang, full_path in lang_links.items():
            url_node = ET.SubElement(urlset, "url")
            loc = ET.SubElement(url_node, "loc")
            loc.text = f"{DOMAIN}/{full_path}"
            
            # Alternate links for blog posts
            for alt_lang, alt_link in lang_links.items():
                alt_node = ET.SubElement(url_node, "{http://www.w3.org/1999/xhtml}link")
                alt_node.set("rel", "alternate")
                alt_node.set("hreflang", LANGS[alt_lang]["hreflang"])
                alt_node.set("href", f"{DOMAIN}/{alt_link}")
            
            # lastmod (try to get from filename or actual file)
            # filenames often start with YYYY-MM-DD
            post_date = datetime.now().strftime('%Y-%m-%d')
            # Extract date from basename if it looks like YYYY-MM-DD
            date_match = re.search(r'^(\d{4}-\d{2}-\d{2})', base_match)
            if date_match:
                post_date = date_match.group(1)
            
            lastmod = ET.SubElement(url_node, "lastmod")
            lastmod.text = post_date
            
            changefreq = ET.SubElement(url_node, "changefreq")
            changefreq.text = "monthly"
            priority = ET.SubElement(url_node, "priority")
            priority.text = "0.6"

    # Write to file
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
    
    # Fix a bug where minidom might add extra empty lines
    pretty_xml = "\n".join([line for line in pretty_xml.splitlines() if line.strip()])

    with open("sitemap.xml", "w", encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print("sitemap.xml has been updated.")

if __name__ == "__main__":
    import re
    generate_sitemap()

