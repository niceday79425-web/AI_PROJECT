import json, os
from datetime import datetime, timedelta

os.chdir(r"d:\AI_PROJECT")

with open("posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

now = datetime.now()
cutoff = now - timedelta(days=30)
cutoff_str = cutoff.strftime("%Y-%m-%d")
today_str = now.strftime("%Y-%m-%d")

print(f"Today: {today_str}")
print(f"30-day cutoff: {cutoff_str}")
print(f"Total entries in posts.json: {len(posts)}")
print()

inside = [p for p in posts if p.get("date","") >= cutoff_str]
outside = [p for p in posts if p.get("date","") < cutoff_str]

print(f"=== Within 30 days ({len(inside)} posts) ===")
for p in inside:
    print(f"  {p.get('date','')}  {p.get('link','')}")

print()
print(f"=== Older than 30 days ({len(outside)} posts) ===")
for p in outside:
    print(f"  {p.get('date','')}  {p.get('link','')}")

html_files = sorted([f for f in os.listdir("blog") if f.endswith(".html") and len(f) > 10 and f[:4].isdigit()])
print(f"\n=== blog/ directory: {len(html_files)} dated HTML files ===")
if html_files:
    dates_in_files = set(f[:10] for f in html_files)
    print(f"Date range: {min(dates_in_files)} ~ {max(dates_in_files)}")
    outside_30 = [f for f in html_files if f[:10] < cutoff_str]
    inside_30 = [f for f in html_files if f[:10] >= cutoff_str]
    print(f"Files within 30 days: {len(inside_30)}")
    print(f"Files older than 30 days (on disk but NOT shown in UI): {len(outside_30)}")
    if outside_30:
        print("Sample old files:")
        for f in outside_30[:5]:
            print(f"  {f}")
