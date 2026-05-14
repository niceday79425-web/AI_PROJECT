import os, re

ROOT = r"d:\AI_PROJECT"

# 1. ko/index.html
KO_PATH = os.path.join(ROOT, "ko", "index.html")
with open(KO_PATH, "r", encoding="utf-8") as f:
    ko_html = f.read()

ko_academy_card = """                    <a href="learn" class="nav-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h3>배당 아카데미</h3>
                        <p>초보자부터 실전까지, 배당 투자의 모든 것을 마스터하세요.</p>
                    </a>
"""

if 'href="learn"' not in ko_html and '<div class="nav-grid">' in ko_html:
    # insert before the first nav-card or after nav-grid
    ko_html = ko_html.replace('<div class="nav-grid">\n', f'<div class="nav-grid">\n{ko_academy_card}')
    with open(KO_PATH, "w", encoding="utf-8") as f:
        f.write(ko_html)
    print("Added Academy card to ko/index.html")

# 2. index.html (EN)
EN_PATH = os.path.join(ROOT, "index.html")
with open(EN_PATH, "r", encoding="utf-8") as f:
    en_html = f.read()

en_academy_card = """                    <a href="learn" class="nav-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h3>Dividend Academy</h3>
                        <p>Master dividend investing from basics to advanced strategies.</p>
                    </a>
"""

if 'href="learn"' not in en_html and '<div class="nav-grid">' in en_html:
    en_html = en_html.replace('<div class="nav-grid">\n', f'<div class="nav-grid">\n{en_academy_card}')
    with open(EN_PATH, "w", encoding="utf-8") as f:
        f.write(en_html)
    print("Added Academy card to index.html")
