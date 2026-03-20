"""
posts.json 재구성 스크립트
blog/ 폴더의 HTML 파일을 스캔해서 posts.json을 최대 60개로 재구성
날짜형 파일만 대상 (YYYY-MM-DD-*.html)
교육 블로그 파일은 별도로 기존 항목 유지
"""
import os, json, re
from datetime import datetime

BASE = r"d:\AI_PROJECT"
MAX_POSTS = 60

def rebuild_posts_json(blog_dir, posts_path, lang, link_prefix):
    """blog_dir의 모든 날짜형 HTML을 스캔해 posts.json 재구성"""
    
    # 기존 posts.json 로드 (교육 블로그 항목 보존용)
    existing = []
    if os.path.exists(posts_path):
        with open(posts_path, "r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except Exception:
                existing = []

    # 교육 블로그 항목 (날짜 prefix 없는 파일) 별도 보존
    edu_entries = [p for p in existing if not re.match(r"blog/\d{4}-\d{2}-\d{2}-", p.get("link", ""))]

    # blog/ 폴더 스캔 — 날짜형 파일만
    entries = []
    if os.path.exists(blog_dir):
        for fname in os.listdir(blog_dir):
            if not fname.endswith(".html"):
                continue
            m = re.match(r"^(\d{4}-\d{2}-\d{2})-(.+)\.html$", fname)
            if not m:
                continue  # 교육 블로그 파일 등 스킵
            date_str = m.group(1)
            ticker = m.group(2)

            # HTML 파일에서 title 추출
            filepath = os.path.join(blog_dir, fname)
            title = f"{ticker} — Market Analysis {date_str}"
            summary = f"Latest market analysis for {ticker} on {date_str}."
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as hf:
                    content = hf.read(3000)
                title_m = re.search(r"<title>(.*?)\s*\|", content, re.IGNORECASE)
                if title_m:
                    title = title_m.group(1).strip()
                desc_m = re.search(r'<meta name="description" content="([^"]+)"', content, re.IGNORECASE)
                if desc_m:
                    summary = desc_m.group(1).strip()[:200]
            except Exception:
                pass

            entries.append({
                "date": date_str,
                "title": title,
                "link": f"{link_prefix}{fname}",
                "summary": summary
            })

    # 날짜 내림차순, 최대 60개
    entries.sort(key=lambda x: x["date"], reverse=True)
    entries = entries[:MAX_POSTS]

    # 교육 블로그 항목 합산 (최대 60개 한도 내)
    all_links = {e["link"] for e in entries}
    for edu in edu_entries:
        if edu.get("link") not in all_links and len(entries) < MAX_POSTS:
            entries.append(edu)
            all_links.add(edu["link"])

    # 최종 날짜 역순 정렬
    entries.sort(key=lambda x: x.get("date", ""), reverse=True)
    entries = entries[:MAX_POSTS]

    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"[OK] {posts_path}: {len(entries)} entries registered")
    return entries

os.chdir(BASE)

# EN
rebuild_posts_json("blog", "posts.json", "en", "blog/")
# KO
rebuild_posts_json("ko/blog", "ko/posts.json", "ko", "blog/")
# PT
rebuild_posts_json("pt/blog", "pt/posts.json", "pt", "blog/")

# SITEMAP 자동 갱신
try:
    import sys
    sys.path.append(os.getcwd())
    from generate_sitemap import generate_sitemap
    generate_sitemap()
except Exception as e:
    print(f"[ERROR] Sitemap update failed: {e}")

print("\nDone. Check posts.json and sitemap.xml for the updated list.")
