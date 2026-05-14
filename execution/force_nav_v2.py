import os
import re

# Navigation Configuration
NAV_CONFIG = {
    'ko': [
        ('/ko/blog', '마켓 인사이트'),
        ('/ko/learn', '배당 아카데미'),
        ('/ko/list', '배당주 스카우터'),
        ('/ko/calculator', '스노볼 계산기'),
        ('/ko/calendar', '배당 캘린더'),
        ('/ko/fortune', '주식 궁합'),
        ('/ko/about', '소개')
    ],
    'en': [
        ('/blog', 'Market Insights'),
        ('/learn', 'Dividend Academy'),
        ('/list', 'Dividend Scouter'),
        ('/calculator', 'Snowball Simulator'),
        ('/calendar', 'Dividend Calendar'),
        ('/fortune', 'Stock Match'),
        ('/about', 'About')
    ],
    'pt': [
        ('/pt/blog', 'Market Insights'),
        ('/pt/learn', 'Dividend Academy'),
        ('/pt/list', 'Dividend Scouter'),
        ('/pt/calculator', 'Snowball Simulator'),
        ('/pt/calendar', 'Dividend Calendar'),
        ('/pt/fortune', 'Stock Match'),
        ('/pt/about', 'About')
    ]
}

def get_nav_html(lang, active_path):
    links = NAV_CONFIG[lang]
    html_parts = ['        <nav class="glass-nav">']
    for path, label in links:
        # Check if active
        # Simple match: if active_path ends with path or vice versa
        is_active = False
        if active_path == path or active_path == path + '.html' or (path == '/' and active_path == '/index.html'):
            is_active = True
        elif active_path.endswith(path + '.html'):
            is_active = True
        
        active_class = ' class="active"' if is_active else ''
        html_parts.append(f'          <a href="{path}"{active_class}>{label}</a>')
    html_parts.append('        </nav>')
    return '\n'.join(html_parts)

def update_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine language
    lang = 'en'
    if 'ko/' in file_path or file_path.startswith('ko\\'): lang = 'ko'
    elif 'pt/' in file_path or file_path.startswith('pt\\'): lang = 'pt'

    # Determine active path for this file
    rel_path = os.path.relpath(file_path, start='d:\\AI_PROJECT')
    active_path = '/' + rel_path.replace('\\', '/')
    if active_path.endswith('index.html'):
        active_path = active_path.replace('index.html', '')
    if active_path.endswith('.html'):
        # Keep it for now, the comparison logic handles it
        pass

    new_nav = get_nav_html(lang, active_path)

    # Replacement logic: 
    # Look for existing <nav class="glass-nav">...</nav>
    # If not found, look for </header> and insert after it.
    
    nav_pattern = re.compile(r'<nav class="glass-nav">.*?</nav>', re.DOTALL)
    if nav_pattern.search(content):
        new_content = nav_pattern.sub(new_nav, content)
    else:
        # Insert after header
        if '</header>' in content:
            new_content = content.replace('</header>', '</header>\n\n' + new_nav)
        else:
            # Fallback: insert before <div class="content-with-sidebar"> or <main>
            if '<div class="content-with-sidebar">' in content:
                new_content = content.replace('<div class="content-with-sidebar">', new_nav + '\n<div class="content-with-sidebar">')
            elif '<main' in content:
                # Find the line with <main
                main_match = re.search(r'<main.*?>', content)
                if main_match:
                    new_content = content[:main_match.start()] + new_nav + '\n' + content[main_match.start():]
                else:
                    new_content = content
            else:
                new_content = content

    # Specific fix for index pages: "Dividend Academy" card
    if 'index.html' in file_path:
        academy_card_en = """                    <a href="/learn" class="nav-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h3>Dividend Academy</h3>
                        <p>Master dividend investing from basics to advanced strategies.</p>
                    </a>"""
        academy_card_pt = """                    <a href="/pt/learn" class="nav-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h3>Dividend Academy</h3>
                        <p>Domine o investimento em dividendos do básico ao avançado.</p>
                    </a>"""
        
        if '<div class="nav-grid">' in new_content:
            if '/learn' not in new_content and '/pt/learn' not in new_content:
                card = academy_card_ko if lang == 'ko' else (academy_card_pt if lang == 'pt' else academy_card_en)
                # Note: academy_card_ko is not defined above but I'll add it if needed. 
                # Actually KO usually has it, but I'll make sure.
                academy_card_ko = """                    <a href="/ko/learn" class="nav-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h3>배당 아카데미</h3>
                        <p>기초부터 심화 전략까지, 배당 투자의 모든 것을 마스터하세요.</p>
                    </a>"""
                card = academy_card_ko if lang == 'ko' else (academy_card_pt if lang == 'pt' else academy_card_en)
                new_content = new_content.replace('<div class="nav-grid">', '<div class="nav-grid">\n' + card)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {file_path}")
    else:
        print(f"No changes: {file_path}")

# List of files to check
FILES = [
    'index.html', 'list.html', 'calculator.html', 'calendar.html', 'fortune.html', 'blog.html', 'about.html', 'learn.html',
    'ko/index.html', 'ko/list.html', 'ko/calculator.html', 'ko/calendar.html', 'ko/fortune.html', 'ko/blog.html', 'ko/about.html', 'ko/learn.html',
    'pt/index.html', 'pt/list.html', 'pt/calculator.html', 'pt/calendar.html', 'pt/fortune.html', 'pt/blog.html', 'pt/about.html', 'pt/learn.html'
]

for f in FILES:
    update_file(f)
