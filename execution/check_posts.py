import json, os, glob

ROOT = r"d:\AI_PROJECT"

configs = [
    ("EN (영어)", "posts.json", "blog"),
    ("KO (한국어)", "ko/posts.json", "ko/blog"),
    ("PT (포르투갈어)", "pt/posts.json", "pt/blog"),
]

for lang, posts_path, blog_dir in configs:
    posts_file = os.path.join(ROOT, posts_path)
    blog_folder = os.path.join(ROOT, blog_dir)

    # 실제 HTML 파일 수
    daily_html = [f for f in glob.glob(os.path.join(blog_folder, "2026-*.html"))]
    edu_html   = [f for f in glob.glob(os.path.join(blog_folder, "*.html"))
                  if not os.path.basename(f).startswith("2026-")]

    print(f"\n{'='*55}")
    print(f" {lang}")
    print(f"{'='*55}")
    print(f"  [일일 시황 포스트] {len(daily_html)}편")
    print(f"  [교육/가이드 포스트] {len(edu_html)}편")

    if os.path.exists(posts_file):
        with open(posts_file, encoding="utf-8") as f:
            posts = json.load(f)
        print(f"  [posts.json 등록] {len(posts)}편")
        print(f"\n  최신 5편:")
        for p in posts[:5]:
            title = p.get("title","")[:45]
            print(f"    {p.get('date','')} | {title}")

# 교육 시리즈 현황 (KO만)
ko_blog = os.path.join(ROOT, "ko", "blog")
print(f"\n{'='*55}")
print(" KO 교육 시리즈 생성 현황 (30편 목표)")
print(f"{'='*55}")

series = {
    "배당주 초보자 가이드 (10편)": ["beginner-0"+str(i) for i in range(1,10)] + ["beginner-10"],
    "월별 배당주 포트폴리오 (12편)": ["monthly-jan","monthly-feb","monthly-mar","monthly-apr",
                                      "monthly-may","monthly-jun","monthly-jul","monthly-aug",
                                      "monthly-sep","monthly-oct","monthly-nov","monthly-dec"],
    "섹터별 배당주 분석 (8편)": ["sector-consumer-staples","sector-healthcare","sector-utilities",
                                  "sector-financials","sector-energy","sector-reits",
                                  "sector-technology","sector-industrials"],
}

total_done = 0
for series_name, slugs in series.items():
    done = [s for s in slugs if os.path.exists(os.path.join(ko_blog, s+".html"))]
    todo = [s for s in slugs if not os.path.exists(os.path.join(ko_blog, s+".html"))]
    total_done += len(done)
    print(f"\n  {series_name}")
    print(f"    완료: {len(done)}/{len(slugs)}  |  대기: {len(todo)}")
    for d in done:
        print(f"      [OK] {d}")
    for t in todo[:3]:
        print(f"      [--] {t}")
    if len(todo) > 3:
        print(f"      ... 외 {len(todo)-3}편 대기")

print(f"\n  총 교육 시리즈: {total_done}/30편 완료")
print(f"  나머지 {30-total_done}편은 매일 GitHub Actions에서 자동 이어서 생성됩니다.")
