import os, glob, re

ROOT = r"d:\AI_PROJECT"

NEW_STYLE = """  <style>
    /* ── Reading Progress Bar ── */
    #progress-bar {
      position: fixed; top: 0; left: 0; height: 3px; width: 0%;
      background: linear-gradient(90deg, #6366f1, #2dd4bf);
      z-index: 9999; transition: width 0.1s linear;
    }
    /* ── Post Styles ── */
    body { font-family: 'Noto Sans KR', 'Inter', sans-serif; background: var(--bg-color); color: var(--text-primary); margin: 0; }
    
    .post-hero {
      padding: 5rem 1.5rem 4rem; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .post-hero .ticker-badge, .series-badge {
      display: inline-block; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
      color: var(--text-secondary); font-size: 0.8rem; font-weight: 600; letter-spacing: 1px;
      text-transform: uppercase; padding: 0.4rem 1.2rem; border-radius: 999px;
      margin-bottom: 1.5rem;
    }
    .post-hero h1 {
      font-size: clamp(2rem, 5vw, 3rem); font-weight: 800; letter-spacing: -1px;
      line-height: 1.2; max-width: 800px; margin: 0 auto 1.5rem; color: var(--text-primary);
    }
    .post-hero .meta {
      font-size: 0.95rem; color: var(--text-secondary); display: flex;
      gap: 1.5rem; justify-content: center; flex-wrap: wrap; margin-top: 1rem;
    }
    
    /* ── Article Layout ── */
    .post-content {
      max-width: 760px; margin: 0 auto; padding: 3rem 1.5rem;
    }
    .post-content h2 {
      font-size: 1.75rem; font-weight: 700; color: var(--text-primary);
      margin: 3.5rem 0 1.25rem; letter-spacing: -0.5px;
    }
    .post-content h3 { 
      font-size: 1.3rem; font-weight: 600; color: var(--text-primary); 
      margin: 2.5rem 0 1rem; letter-spacing: -0.3px;
    }
    .post-content p { 
      line-height: 1.8; color: var(--text-secondary); 
      margin-bottom: 1.5rem; font-size: 1.1rem; font-weight: 400; 
    }
    .post-content ul, .post-content ol {
      padding-left: 1.5rem; margin-bottom: 1.5rem;
    }
    .post-content li { 
      line-height: 1.8; color: var(--text-secondary); 
      margin-bottom: 0.5rem; font-size: 1.1rem; 
    }
    .post-content strong { color: var(--text-primary); font-weight: 600; }
    .post-content img {
      width: 100%; border-radius: 12px; margin: 2rem 0;
      border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* ── Key Point ── */
    .key-point { 
      background: rgba(255,255,255,0.02); border-left: 3px solid var(--text-secondary); 
      border-radius: 0 8px 8px 0; padding: 1.5rem; margin: 2rem 0; 
      color: var(--text-primary); font-size: 1.05rem; 
    }
    .key-point strong { color: var(--text-primary); }
    
    /* ── Data Table ── */
    .data-table { width:100%;border-collapse:collapse;margin:2rem 0;font-size:0.95rem; }
    .data-table th { background:rgba(255,255,255,0.03);color:var(--text-primary);padding:1rem;text-align:left; border-bottom:1px solid rgba(255,255,255,0.1); font-weight: 600; }
    .data-table td { padding:1rem;border-bottom:1px solid rgba(255,255,255,0.05);color:var(--text-secondary); }
    
    /* ── Nav Links & Author Box ── */
    .nav-links { display:flex;gap:1.5rem;flex-wrap:wrap;margin:3rem 0;padding:1.5rem;background:rgba(255,255,255,0.02);border-radius:12px; }
    .nav-links a { color:var(--text-primary);text-decoration:none;font-weight:500;font-size:0.95rem; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 2px; transition: border-color 0.3s; }
    .nav-links a:hover { border-color: var(--text-primary); }
    
    .author-box { display:flex;align-items:center;gap:1.2rem;background:transparent;border-top:1px solid rgba(255,255,255,0.1);border-bottom:1px solid rgba(255,255,255,0.1);padding:1.5rem 0;margin:3rem 0; }
    .author-avatar { width:56px;height:56px;background:rgba(255,255,255,0.05);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;color:var(--text-primary);font-weight:600;font-size:1.2rem; }
    .author-box strong { color:var(--text-primary); display:block; margin-bottom: 0.2rem; font-size: 1.1rem; }
    .author-box span { color:var(--text-secondary); font-size: 0.95rem; }
    
    /* ── Key Metrics Card ── */
    .metrics-bar {
      display: flex; gap: 1rem; flex-wrap: wrap;
      background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
      border-radius: 12px; padding: 1.5rem; margin: 2rem 0;
    }
    .metric-item { flex: 1; min-width: 120px; text-align: center; }
    .metric-item .label { font-size: 0.8rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; display: block; }
    .metric-item .value { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); }
    
    /* ── Disclaimer ── */
    .disclaimer {
      margin-top: 4rem; padding: 1.5rem;
      background: transparent; border: 1px solid rgba(255,255,255,0.05);
      border-radius: 12px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.7;
    }
    .disclaimer .disc-title { font-weight: 600; color: var(--text-secondary); margin-bottom: 0.5rem; }
    
    /* ── Back Button ── */
    .back-btn {
      display: inline-flex; align-items: center; gap: 0.5rem;
      color: var(--text-secondary); font-weight: 500; text-decoration: none;
      font-size: 0.95rem; margin-bottom: 2rem; transition: color 0.3s;
    }
    .back-btn:hover { color: var(--text-primary); }
    
    /* ── Series Nav ── */
    .series-nav { background:rgba(255,255,255,0.02);border-radius:12px;padding:1.5rem;margin-top:4rem; border:1px solid rgba(255,255,255,0.05); }
    .series-nav h3 { color:var(--text-primary);font-size:1.1rem;margin-bottom:1rem; }
    .series-nav ul { list-style:none;padding:0;margin:0; }
    .series-nav li { padding:0.4rem 0;font-size:0.95rem; color: var(--text-secondary); }
    .series-nav a { color:var(--text-primary);text-decoration:none; border-bottom: 1px solid rgba(255,255,255,0.2); }
    .series-nav a:hover { border-color: var(--text-primary); }
  </style>"""

STYLE_PATTERN = re.compile(r'<style>.*?</style>', re.DOTALL)

def patch_all_html_files():
    # 모든 블로그 포스트 (일일 시황 + 교육 시리즈)
    files = glob.glob(os.path.join(ROOT, "blog", "*.html")) + \
            glob.glob(os.path.join(ROOT, "ko", "blog", "*.html")) + \
            glob.glob(os.path.join(ROOT, "pt", "blog", "*.html"))
            
    count = 0
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # style 태그 교체
        new_content = STYLE_PATTERN.sub(NEW_STYLE, content)
        
        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1
            
    print(f"[Success] {count} HTML files completely restyled with Ultra Premium Minimalist Theme.")

if __name__ == "__main__":
    patch_all_html_files()
