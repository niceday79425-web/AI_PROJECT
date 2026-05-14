
import json, os, re

def update_blog_html_static(lang, posts_path, blog_html_path, blog_url_prefix):
    """posts.json을 읽어 blog.html의 #blogGrid를 정적 HTML로 업데이트하고 헤더를 수정함"""
    if not os.path.exists(posts_path):
        print(f"  [skip] {posts_path} not found")
        return
    with open(posts_path, "r", encoding="utf-8") as f:
        posts = json.load(f)
    
    # Filter only daily analysis posts (those with YYYY-MM-DD in the link)
    # Academy posts like 'blog/dividend-trap-guide.html' will be skipped
    daily_posts = []
    for p in posts:
        link = p.get("link", "")
        # Match blog/2026-05-14-AAPL.html or similar
        if re.search(r'\d{4}-\d{2}-\d{2}', link):
            daily_posts.append(p)
    
    items = []
    for p in daily_posts[:60]:
        title = p.get("title","")
        date  = p.get("date","")
        link  = p.get("link","")
        summary = p.get("summary","")[:140]
        url = "/" + blog_url_prefix + link if not link.startswith("/") else link
        
        # Clean up title (remove suffix if present)
        display_title = title.split(" | ")[0] if " | " in title else title
        
        items.append(f'''<article class="blog-card" style="cursor:pointer;" onclick="location.href=\'{url}\'">
          <span class="blog-date">{date}</span>
          <h3>{display_title}</h3>
          <p>{summary}...</p>
        </article>''')
    
    static_html = "\n".join(items)
    
    if not os.path.exists(blog_html_path):
        print(f"  [skip] {blog_html_path} not found")
        return
        
    with open(blog_html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 1. Update Hero/Header Text
    header_map = {
        "ko": {
            "h1": "미국주식 전망 및 분석",
            "h2": "마켓 인사이트",
            "loading": "분석 리포트"
        },
        "en": {
            "h1": "US Stock Outlook & Analysis",
            "h2": "Market Insights",
            "loading": "Analysis Reports"
        },
        "pt": {
            "h1": "Perspectivas e Análises de Ações dos EUA",
            "h2": "Market Insights",
            "loading": "Relatórios de Análise"
        }
    }
    
    # Detect language from path or content
    detected_lang = "en"
    if "ko/" in blog_html_path: detected_lang = "ko"
    elif "pt/" in blog_html_path: detected_lang = "pt"
    
    h = header_map[detected_lang]
    
    # Replace h1
    html = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1 style="margin:0 0 0.5rem; font-size: 2.5rem; background: var(--primary-gradient); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">{h["h1"]}</h1>', html, count=1, flags=re.DOTALL)
    # Replace h2
    html = re.sub(r'<h2 style="margin:0;">.*?</h2>', f'<h2 style="margin:0; font-weight: 600; opacity: 0.8;">{h["h2"]}</h2>', html, count=1, flags=re.DOTALL)
    # Replace loading/postCount
    html = re.sub(r'<span id="postCount"[^>]*>.*?</span>', f'<span id="postCount" style="font-size:0.85rem; color:var(--text-secondary); background:rgba(99,102,241,0.1); padding:0.3rem 0.8rem; border-radius:20px; border:1px solid rgba(99,102,241,0.2);">{len(daily_posts)} {h["loading"]}</span>', html, count=1, flags=re.DOTALL)
    # Replace secondary h2 (Recent Analysis)
    recent_labels = {"ko": "최신 시장 분석", "en": "Latest Market Analysis", "pt": "Últimas Análises de Mercado"}
    html = re.sub(r'<h2>최신 시장 분석</h2>|<h2>Latest Market Analysis</h2>|<h2>Últimas Análises de Mercado</h2>', f'<h2>{recent_labels[detected_lang]}</h2>', html, count=1)

    # 2. Update Grid Content
    new_html = re.sub(
        r'(<div id="blogGrid"[^>]*>).*?(</div>\s*</section>)',
        r'\1\n' + static_html + r'\n\2',
        html, flags=re.DOTALL, count=1
    )
    
    # 3. Ensure no JS loader
    new_html = re.sub(
        r'<script>\s*async function loadBlog\(\).*?loadBlog\(\);\s*</script>',
        '<!-- Static HTML blog list - no JS needed -->',
        new_html, flags=re.DOTALL
    )
    
    with open(blog_html_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"  [static] {blog_html_path}: {len(daily_posts)} posts rendered (Academy posts filtered)")

if __name__ == "__main__":
    configs = [
        ("posts.json",    "blog.html",    ""),
        ("ko/posts.json", "ko/blog.html", "ko/"),
        ("pt/posts.json", "pt/blog.html", "pt/"),
    ]
    for posts_p, blog_p, prefix in configs:
        update_blog_html_static("", posts_p, blog_p, prefix)
    print("[DONE] Blog HTML static update complete with premium header and filtering.")
