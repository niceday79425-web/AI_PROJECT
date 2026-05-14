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
    body { font-family: 'Inter', sans-serif; background: var(--bg-color); color: var(--text-primary); margin: 0; }
    
    .post-hero {
      padding: 6rem 1.5rem 5rem; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05);
      background: radial-gradient(circle at top, rgba(99,102,241,0.05) 0%, transparent 70%);
    }
    .post-hero .ticker-badge, .series-badge {
      display: inline-block; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
      color: #60a5fa; font-size: 0.8rem; font-weight: 700; letter-spacing: 1.5px;
      text-transform: uppercase; padding: 0.5rem 1.4rem; border-radius: 999px;
      margin-bottom: 2rem; backdrop-filter: blur(10px);
    }
    .post-hero h1 {
      font-size: clamp(2.2rem, 6vw, 3.5rem); font-weight: 800; letter-spacing: -1.5px;
      line-height: 1.1; max-width: 900px; margin: 0 auto 2rem; color: var(--text-primary);
    }
    .post-hero .meta {
      font-size: 0.95rem; color: var(--text-secondary); display: flex;
      gap: 2rem; justify-content: center; flex-wrap: wrap; margin-top: 1rem;
      opacity: 0.8;
    }
    
    /* ── Article Layout ── */
    .post-content {
      max-width: 760px; margin: 0 auto; padding: 4rem 1.5rem;
    }
    .post-content h2 {
      font-size: 1.85rem; font-weight: 700; color: var(--text-primary);
      margin: 4rem 0 1.5rem; letter-spacing: -0.5px;
      display: flex; align-items: center; gap: 0.75rem;
    }
    .post-content h2::before {
      content: ''; display: inline-block; width: 4px; height: 1.5rem;
      background: var(--primary-gradient); border-radius: 2px;
    }
    .post-content h3 { 
      font-size: 1.4rem; font-weight: 600; color: var(--text-primary); 
      margin: 3rem 0 1.25rem; letter-spacing: -0.3px;
    }
    .post-content p { 
      line-height: 1.9; color: var(--text-secondary); 
      margin-bottom: 1.75rem; font-size: 1.125rem; font-weight: 400; 
    }
    .post-content ul, .post-content ol {
      padding-left: 1.5rem; margin-bottom: 1.75rem;
    }
    .post-content li { 
      line-height: 1.9; color: var(--text-secondary); 
      margin-bottom: 0.75rem; font-size: 1.125rem; 
    }
    .post-content strong { color: var(--text-primary); font-weight: 600; }
    .post-content img {
      width: 100%; border-radius: 16px; margin: 2.5rem 0;
      border: 1px solid rgba(255,255,255,0.05);
      box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    /* ── Key Point ── */
    .key-point { 
      background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
      border-left: 4px solid #6366f1; 
      border-radius: 12px; padding: 2rem; margin: 3rem 0; 
      color: var(--text-primary); font-size: 1.1rem; 
      backdrop-filter: blur(5px);
    }
    .key-point strong { color: #60a5fa; }
    
    /* ── Data Table ── */
    .data-table { width:100%;border-collapse:collapse;margin:2.5rem 0;font-size:0.95rem; }
    .data-table th { background:rgba(255,255,255,0.04);color:var(--text-primary);padding:1.2rem;text-align:left; border-bottom:1px solid rgba(255,255,255,0.1); font-weight: 700; }
    .data-table td { padding:1.2rem;border-bottom:1px solid rgba(255,255,255,0.05);color:var(--text-secondary); }
    
    /* ── Nav Links & Author Box ── */
    .nav-links { display:flex;gap:1.5rem;flex-wrap:wrap;margin:4rem 0;padding:2rem;background:rgba(255,255,255,0.02);border: 1px solid rgba(255,255,255,0.05); border-radius:16px; }
    .nav-links a { color:var(--text-primary);text-decoration:none;font-weight:600;font-size:1rem; border-bottom: 2px solid rgba(255,255,255,0.1); padding-bottom: 4px; transition: all 0.3s; }
    .nav-links a:hover { border-color: #6366f1; color: #6366f1; }
    
    .author-box { display:flex;align-items:center;gap:1.5rem;background:transparent;border-top:1px solid rgba(255,255,255,0.08);border-bottom:1px solid rgba(255,255,255,0.08);padding:2rem 0;margin:4rem 0; }
    .author-avatar { width:64px;height:64px;background:var(--primary-gradient);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;color:#fff;font-weight:700;font-size:1.4rem; box-shadow: 0 10px 20px rgba(99,102,241,0.2); }
    .author-box strong { color:var(--text-primary); display:block; margin-bottom: 0.3rem; font-size: 1.2rem; }
    .author-box span { color:var(--text-secondary); font-size: 1rem; }
    
    /* ── Key Metrics Card ── */
    .metrics-bar {
      display: flex; gap: 1.5rem; flex-wrap: wrap;
      background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);
      border-radius: 16px; padding: 2rem; margin: 3rem 0;
      backdrop-filter: blur(10px);
    }
    .metric-item { flex: 1; min-width: 140px; text-align: center; }
    .metric-item .label { font-size: 0.85rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.75rem; display: block; opacity: 0.8; }
    .metric-item .value { font-size: 1.75rem; font-weight: 800; color: var(--text-primary); }
    
    /* ── Disclaimer ── */
    .disclaimer {
      margin-top: 5rem; padding: 2rem;
      background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.05);
      border-radius: 16px; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.8;
    }
    .disclaimer .disc-title { font-weight: 700; color: var(--text-primary); margin-bottom: 0.75rem; display: block; }
    
    /* ── Back Button ── */
    .back-btn {
      display: inline-flex; align-items: center; gap: 0.75rem;
      color: var(--text-secondary); font-weight: 600; text-decoration: none;
      font-size: 1rem; margin-bottom: 3rem; transition: all 0.3s;
      padding: 0.5rem 1rem; border-radius: 8px; background: rgba(255,255,255,0.03);
    }
    .back-btn:hover { color: var(--text-primary); background: rgba(255,255,255,0.08); transform: translateX(-5px); }
    
    /* ── Series Nav ── */
    .series-nav { background:rgba(255,255,255,0.02);border-radius:16px;padding:2rem;margin-top:5rem; border:1px solid rgba(255,255,255,0.08); }
    .series-nav h3 { color:var(--text-primary);font-size:1.25rem;margin-bottom:1.5rem; font-weight: 700; }
    .series-nav ul { list-style:none;padding:0;margin:0; }
    .series-nav li { padding:0.6rem 0;font-size:1rem; color: var(--text-secondary); border-bottom: 1px solid rgba(255,255,255,0.03); }
    .series-nav li:last-child { border: none; }
    .series-nav a { color:var(--text-primary);text-decoration:none; font-weight: 500; transition: color 0.3s; }
    .series-nav a:hover { color: #6366f1; }
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
