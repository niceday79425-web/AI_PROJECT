import os
import csv

ROOT = r"d:\AI_PROJECT"
beginner_slugs = {
    "beginner-01-what-is-dividend": "/ko/learn/track-5-dividend/01-what-is-dividend/",
    "beginner-02-dividend-yield": "/ko/learn/track-5-dividend/02-dividend-yield/",
    "beginner-03-payout-ratio": "/ko/learn/track-5-dividend/03-payout-ratio/",
    "beginner-04-drip": "/ko/learn/track-5-dividend/04-drip/",
    "beginner-05-dividend-aristocrats": "/ko/learn/track-5-dividend/05-dividend-aristocrats/",
    "beginner-06-yield-on-cost": "/ko/learn/track-5-dividend/06-yield-on-cost/",
    "beginner-07-dividend-calendar": "/ko/learn/track-5-dividend/07-dividend-calendar/",
    "beginner-08-sector-diversification": "/ko/learn/track-5-dividend/08-sector-diversification/",
    "beginner-09-us-tax": "/ko/learn/track-5-dividend/09-us-tax/",
    "beginner-10-start-portfolio": "/ko/learn/track-5-dividend/10-start-portfolio/",
}

mappings = []

for r, dirs, files in os.walk(ROOT):
    if any(ig in r for ig in [".git", ".github", "execution", "directives", "__pycache__", "node_modules", "src", ".astro"]):
        continue
    for f in files:
        if not f.endswith(".html"):
            continue
        rel = os.path.relpath(os.path.join(r, f), ROOT).replace("\\", "/")
        
        base_name = os.path.basename(f)
        slug = base_name[:-5]
        
        target = "/ko/"
        if base_name == "index.html":
            target = "/ko/"
        elif base_name == "about.html":
            target = "/ko/about/"
        elif base_name == "privacy.html":
            target = "/ko/legal/privacy/"
        elif base_name == "learn.html":
            target = "/ko/learn/"
        elif base_name == "blog.html":
            target = "/ko/works/insight/archive/"
        elif base_name in ["calculator.html", "calendar.html", "list.html", "fortune.html"]:
            target = "/ko/works/tools/"
        elif base_name == "contact.html":
            target = "/ko/about/"
        elif "/blog/" in rel:
            if slug in beginner_slugs:
                target = beginner_slugs[slug]
            elif slug.startswith("2026-"):
                target = f"/ko/works/insight/archive/{slug}/"
            else:
                target = "/ko/learn/track-5-dividend/"
        
        mappings.append({"from": f"/{rel}", "to": target})
        if rel.endswith(".html"):
            clean = f"/{rel[:-5]}"
            mappings.append({"from": clean, "to": target})
            mappings.append({"from": f"{clean}/", "to": target})
        if rel.endswith("index.html"):
            dir_path = f"/{rel[:-10]}"
            mappings.append({"from": dir_path, "to": target})
            if not dir_path.endswith("/"):
                mappings.append({"from": f"{dir_path}/", "to": target})

# Root redirect
mappings.insert(0, {"from": "/", "to": "/ko/"})

# Deduplicate
seen = set()
deduped = []
for m in mappings:
    src = m["from"]
    tgt = m["to"]
    if src == tgt:
        continue
    if src not in seen:
        seen.add(src)
        deduped.append(m)

# Write CSV
csv_file = os.path.join(ROOT, "redirect_mapping.csv")
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["from", "to"])
    w.writeheader()
    w.writerows(deduped)

# Write public/_redirects
cf_redirects = os.path.join(ROOT, "public", "_redirects")
with open(cf_redirects, "w", encoding="utf-8") as f:
    f.write("# wiseaiwiseu.com 301 Permanent Redirects\n")
    for m in deduped:
        f.write(f"{m['from']} {m['to']} 301\n")

print(f"Generated {len(deduped)} rules.")
print(f"Saved: {csv_file}")
print(f"Saved: {cf_redirects}")
