# -*- coding: utf-8 -*-
import json, os, glob, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r"d:\AI_PROJECT"

configs = [
    ("EN", "posts.json", "blog"),
    ("KO", "ko/posts.json", "ko/blog"),
    ("PT", "pt/posts.json", "pt/blog"),
]
for lang, pf, bd in configs:
    daily = glob.glob(os.path.join(ROOT, bd, "2026-*.html"))
    edu = [f for f in glob.glob(os.path.join(ROOT, bd, "*.html"))
           if not os.path.basename(f).startswith("2026-")]
    posts_path = os.path.join(ROOT, pf)
    posts = []
    if os.path.exists(posts_path):
        with open(posts_path, encoding="utf-8") as f:
            posts = json.load(f)
    print(f"[{lang}] 일일시황={len(daily)}편 / 교육가이드={len(edu)}편 / posts.json={len(posts)}편")
    for p in posts[:3]:
        t = p.get("title","")[:45]
        print(f"       {p.get('date','')} {t}")

ko_blog = os.path.join(ROOT, "ko", "blog")
done = (glob.glob(os.path.join(ko_blog, "beginner-*.html")) +
        glob.glob(os.path.join(ko_blog, "monthly-*.html")) +
        glob.glob(os.path.join(ko_blog, "sector-*.html")))
done_names = [os.path.splitext(os.path.basename(f))[0] for f in done]
print(f"\n[KO 교육 시리즈] {len(done)}/30편 완료")
for n in sorted(done_names):
    print(f"  OK: {n}")

all_slugs = (
    [f"beginner-0{i}-what-is-dividend" if i==1 else f"beginner-0{i}" for i in range(1,10)] +
    ["beginner-10"] +
    ["monthly-jan","monthly-feb","monthly-mar","monthly-apr","monthly-may","monthly-jun",
     "monthly-jul","monthly-aug","monthly-sep","monthly-oct","monthly-nov","monthly-dec"] +
    ["sector-consumer-staples","sector-healthcare","sector-utilities","sector-financials",
     "sector-energy","sector-reits","sector-technology","sector-industrials"]
)
todo = [s for s in all_slugs if s not in done_names]
print(f"\n[대기중] {len(todo)}편 (내일 자동 생성):")
for t in todo:
    print(f"  --: {t}")
