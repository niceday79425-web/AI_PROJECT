import os, glob

ROOT = r"d:\AI_PROJECT"

# 1. create_edu_series.py에서 생성된 교육 시리즈 HTML 
EDU_REPLACEMENTS = {
    "body { font-family: 'Noto Sans KR', 'Inter', sans-serif; }": "body { font-family: 'Noto Sans KR', 'Inter', sans-serif; background: var(--bg-color); color: var(--text-primary); margin: 0; }",
    ".post-hero h1 { font-size:clamp(1.5rem,4vw,2.4rem);font-weight:900;line-height:1.4;max-width:820px;margin:0 auto 1rem; }": ".post-hero h1 { font-size:clamp(1.5rem,4vw,2.4rem);font-weight:900;line-height:1.4;max-width:820px;margin:0 auto 1rem; color:#fff; }",
    "color:#1e1b4b": "color:var(--text-primary)",
    "color:#2d2a5e": "color:var(--text-primary)",
    "color:#374151": "color:var(--text-primary)",
    "background:#f0f4ff": "background:rgba(99,102,241,0.1)",
    "color:#4338ca": "color:#a78bfa",
    "color:#6366f1": "color:#a78bfa",
    "background:#f8f9fb": "background:var(--card-bg)",
    "background:#f9fafb": "background:rgba(255,255,255,0.02)",
    "border:1px solid #e5e7eb": "border:1px solid var(--border-color)",
    "border-bottom:1px solid #e5e7eb": "border-bottom:1px solid var(--border-color)",
    "background:#fff7f7": "background:rgba(239,68,68,0.05)",
    "color:#666": "color:var(--text-secondary)",
    "color:#6b7280": "color:var(--text-secondary)"
}

# 2. auto_poster.py에서 생성된 일일 시황 HTML
POSTER_REPLACEMENTS = {
    "body { font-family: 'Inter', sans-serif; background: #f8f9fb; color: #1a1a2e; margin: 0; }": "body { font-family: 'Inter', sans-serif; background: var(--bg-color); color: var(--text-primary); margin: 0; }",
    "color: #1e1b4b": "color: var(--text-primary)",
    "color: #374151": "color: var(--text-primary)",
    "background: #fff": "background: var(--card-bg)",
    "background: #fff7f7": "background: rgba(239,68,68,0.05)",
    "color: #666": "color: var(--text-secondary)",
    "color: #6366f1": "color: #a78bfa",
    "border-color: #e5e7eb": "border-color: var(--border-color)",
    "border: 1px solid #e5e7eb": "border: 1px solid var(--border-color)"
}

def patch_files(file_list, replacements, name):
    count = 0
    for fpath in file_list:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        original = content
        for old_s, new_s in replacements.items():
            content = content.replace(old_s, new_s)
        
        if content != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
    print(f"[{name}] {count} files updated.")

# 교육 시리즈 파일
edu_files = glob.glob(os.path.join(ROOT, "ko", "blog", "beginner-*.html")) + \
            glob.glob(os.path.join(ROOT, "ko", "blog", "monthly-*.html")) + \
            glob.glob(os.path.join(ROOT, "ko", "blog", "sector-*.html"))
patch_files(edu_files, EDU_REPLACEMENTS, "Education Series")

# 일일 시황 파일
daily_files = glob.glob(os.path.join(ROOT, "blog", "2026-*.html")) + \
              glob.glob(os.path.join(ROOT, "ko", "blog", "2026-*.html")) + \
              glob.glob(os.path.join(ROOT, "pt", "blog", "2026-*.html"))
patch_files(daily_files, POSTER_REPLACEMENTS, "Daily Posts")
