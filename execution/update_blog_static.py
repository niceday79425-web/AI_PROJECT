
import json, os, re

def update_blog_html_static(lang, posts_path, blog_html_path, blog_url_prefix):
    """posts.json을 읽어 blog.html의 #blogGrid를 정적 HTML로 업데이트"""
    if not os.path.exists(posts_path):
        return
    with open(posts_path, "r", encoding="utf-8") as f:
        posts = json.load(f)
    
    items = []
    for p in posts[:60]:
        title = p.get("title","")
        date  = p.get("date","")
        link  = p.get("link","")
        summary = p.get("summary","")[:120]
        url = "/" + blog_url_prefix + link if not link.startswith("/") else link
        items.append(f'''<article class="blog-card" style="cursor:pointer;" onclick="location.href=\'{url}\'">
          <span class="blog-date">{date}</span>
          <h3>{title}</h3>
          <p>{summary}</p>
        </article>''')
    
    static_html = "\n".join(items)
    
    if not os.path.exists(blog_html_path):
        return
    with open(blog_html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Replace dynamic JS section with static content
    new_html = re.sub(
        r'(<div id="blogGrid"[^>]*>).*?(</div>\s*</section>)',
        r'\1\n' + static_html + r'\n\2',
        html, flags=re.DOTALL, count=1
    )
    
    # Remove the JS loadBlog function
    new_html = re.sub(
        r'<script>\s*async function loadBlog\(\).*?loadBlog\(\);\s*</script>',
        '<!-- Static HTML blog list - no JS needed -->',
        new_html, flags=re.DOTALL
    )
    
    with open(blog_html_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"  [static] {blog_html_path}: {len(posts)} posts rendered")

if __name__ == "__main__":
    configs = [
        ("posts.json",    "blog.html",    ""),
        ("ko/posts.json", "ko/blog.html", "ko/"),
        ("pt/posts.json", "pt/blog.html", "pt/"),
    ]
    for posts_p, blog_p, prefix in configs:
        update_blog_html_static("", posts_p, blog_p, prefix)
    print("[DONE] Blog HTML static update complete")
