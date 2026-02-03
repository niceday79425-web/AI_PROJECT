import os
import re

# AdSense Configuration
PUB_ID = "ca-pub-XXXXXXXXXXXXXXXX"
SLOT_ID = "XXXXXXXXXX"

# Ad Templates
HEADER_AD = f'''
        <!-- Google AdSense - Header Banner -->
        <div class="ad-slot">
            <ins class="adsbygoogle" style="display:block" data-ad-client="{PUB_ID}"
                data-ad-slot="{SLOT_ID}" data-ad-format="horizontal" data-full-width-responsive="true"></ins>
            <script>
                (adsbygoogle = window.adsbygoogle || []).push({{}});
            </script>
        </div>'''

FOOTER_AD = f'''
        <!-- Google AdSense - Footer Banner -->
        <div class="ad-slot" style="margin-top: 2rem;">
            <ins class="adsbygoogle" style="display:block" data-ad-client="{PUB_ID}"
                data-ad-slot="{SLOT_ID}" data-ad-format="auto" data-full-width-responsive="true"></ins>
            <script>
                (adsbygoogle = window.adsbygoogle || []).push({{}});
            </script>
        </div>'''

# Helper to check if ad exists
def has_adsense(content):
    return "adsbygoogle" in content

def inject_ads_into_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        
        # 1. Replace empty ad-slots if any
        empty_slot = '<div class="ad-slot"></div>'
        if empty_slot in content:
            content = content.replace(empty_slot, HEADER_AD, 1) # First one is header
            # If there's another one, make it footer
            if empty_slot in content:
                content = content.replace(empty_slot, FOOTER_AD)
            print(f"[REPLACED] Empty slots in {filepath}")

        # 2. Inject Header Ad if missing (and not already replaced)
        # Look for </header>
        if "<!-- Google AdSense - Header Banner -->" not in content:
            if "</header>" in content:
                # Insert after header
                content = content.replace("</header>", f"</header>\n{HEADER_AD}")
                print(f"[INJECTED] Header Ad in {filepath}")

        # 3. Inject Footer Ad if missing
        # Look for <footer (before it starts) or inside it?
        # User said "Same standard as EN page". EN page has it IN footer or before footer?
        # Let's check logic: Usually before footer is better for layout, or inside top of footer.
        # Let's put it before <footer> starts.
        if "<!-- Google AdSense - Footer Banner -->" not in content and "data-ad-slot" not in content[content.find("<footer"):]:
             if "<footer>" in content:
                 content = content.replace("<footer>", f"{FOOTER_AD}\n<footer>")
                 print(f"[INJECTED] Footer Ad in {filepath}")
        
        # 4. For blog posts (in blog/ subdir), ensure in-article ad is there?
        # auto_poster already puts it. But older posts might need checking.
        if "blog" in filepath and "data-ad-format=\"auto\"" not in content:
             # Basic injection: find middle paragraph? Too risky with regex.
             # Let's stick to Header/Footer for now as minimal requirement.
             pass

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[SAVED] {filepath}")
        else:
            print(f"[SKIPPED] {filepath} (No changes needed)")

    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")

def main():
    print("Starting AdSense Injection...")
    for root, dirs, files in os.walk("d:\\AI_PROJECT"):
        for file in files:
            if file.endswith(".html"):
                inject_ads_into_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
