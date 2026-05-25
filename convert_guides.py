import os
import re

def find_closing_tag(text, start_index, tag='div'):
    count = 0
    i = start_index
    open_tag = f'<{tag}'
    close_tag = f'</{tag}>'
    
    while i < len(text):
        if text.startswith(open_tag, i):
            next_char = text[i+len(open_tag):i+len(open_tag)+1]
            if next_char in [' ', '>', '\n']:
                count += 1
        elif text.startswith(close_tag, i):
            count -= 1
            if count == 0:
                return i + len(close_tag)
        i += 1
    return -1

def generate_summary(html_content):
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', html_content).strip()
    text = re.sub(r'\s+', ' ', text) # normalize spaces
    
    # Split by period and take the first sentence
    sentences = text.split('. ')
    if sentences:
        summary = sentences[0].strip()
        # Add period back if missing and not ending with a punctuation
        if summary and not summary[-1] in ['.', '!', '?']:
            summary += '.'
        
        if len(summary) > 85:
            summary = summary[:82] + '...'
        return summary
    return ""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False

    # 1. Remove Warren Buffett quote block
    if 'calculator.html' in filepath:
        quote_pattern = re.compile(r'<!-- 명언 -->\s*<div[^>]*>.*?</div>', re.DOTALL)
        if quote_pattern.search(content):
            content = quote_pattern.sub('', content)
            modified = True
        else:
            div_pattern = re.compile(r'<div[^>]*margin-top:\s*2\.5rem[^>]*>.*?</div>', re.DOTALL)
            for match in div_pattern.finditer(content):
                if 'Buffett' in match.group(0) or '버핏' in match.group(0) or 'Buffet' in match.group(0):
                    content = content[:match.start()] + content[match.end():]
                    modified = True
                    break

    # 2. Convert guide grid
    grid_start_match = re.search(r'<div\s+style="display:\s*grid;\s*gap:\s*2rem;">', content)
    
    if grid_start_match:
        start_index = grid_start_match.start()
        end_index = find_closing_tag(content, start_index, 'div')
        
        if end_index != -1:
            grid_html = content[start_index:end_index]
            # Strip the outer grid container tags
            inner_html = grid_html[grid_start_match.end() - grid_start_match.start(): -6].strip()
            
            cards_html = []
            i = 0
            while i < len(inner_html):
                next_div = inner_html.find('<div', i)
                if next_div == -1:
                    break
                card_end = find_closing_tag(inner_html, next_div, 'div')
                if card_end != -1:
                    card_str = inner_html[next_div:card_end]
                    if 'background: var(--card-bg)' in card_str or 'background:var(--card-bg)' in card_str.replace(' ', ''):
                        cards_html.append(card_str)
                    i = card_end
                else:
                    break
            
            if cards_html:
                new_grid_html = '<div class="guide-grid">\n'
                modals_html = ''
                
                for idx, card in enumerate(cards_html, 1):
                    # Extract h3
                    h3_match = re.search(r'<h3[^>]*>(.*?)</h3>', card, re.DOTALL)
                    h3_content = h3_match.group(1).strip() if h3_match else f"Guide {idx}"
                    h3_full = h3_match.group(0) if h3_match else f"<h3>Guide {idx}</h3>"
                    
                    # Extract body content (without h3)
                    if h3_match:
                        card_without_h3 = card.replace(h3_full, '', 1)
                    else:
                        card_without_h3 = card
                        
                    # Generate concise summary from the card body
                    summary_text = generate_summary(card_without_h3)
                    
                    normalized_path = filepath.replace('\\', '/')
                    if normalized_path.startswith('pt/') or '/pt/' in normalized_path:
                        read_more_text = "Saber mais →"
                    elif normalized_path.startswith('ko/') or '/ko/' in normalized_path:
                        read_more_text = "자세히 보기 →"
                    else:
                        read_more_text = "Read more →"
                    
                    new_grid_html += f"""                    <div class="guide-card-new" onclick="openGuideModal({idx})" role="button" tabindex="0">
                        <div>
                            {h3_full}
                            <p>{summary_text}</p>
                        </div>
                        <span class="read-more">{read_more_text}</span>
                    </div>\n"""
                    
                    card_inner = re.sub(r'^<div[^>]*>', '', card_without_h3).strip()
                    if card_inner.endswith('</div>'):
                        card_inner = card_inner[:-6]
                    
                    modals_html += f"""                <div id="guide-detail-{idx}" style="display:none;">
                    <h3 style="font-size:1.25rem; margin-bottom:1rem; color:var(--text-primary);">{h3_content}</h3>
                    <div class="guide-modal-body">
                        {card_inner}
                    </div>
                </div>\n"""
                new_grid_html += '                </div>\n'
                
                replacement = new_grid_html + modals_html
                content = content[:start_index] + replacement + content[end_index:]
                modified = True

    # 3. Add Modal HTML and Script
    if modified:
        if 'id="guideModal"' not in content:
            modal_html = """
            <div id="guideModal" class="guide-modal" onclick="if(event.target===this)closeGuideModal()">
                <div class="guide-modal-content">
                    <button class="guide-modal-close" onclick="closeGuideModal()" aria-label="닫기">✕</button>
                    <div id="guideModalBody"></div>
                </div>
            </div>
            """
            if '</main>' in content:
                content = content.replace('</main>', modal_html + '\n                </main>')
            elif '</footer>' in content:
                content = content.replace('<footer>', modal_html + '\n        <footer>')
        
        if 'function openGuideModal' not in content:
            script_html = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            if (!window.openGuideModal) {
                window.openGuideModal = function(id) {
                    const detail = document.getElementById('guide-detail-' + id);
                    const modal = document.getElementById('guideModal');
                    const body = document.getElementById('guideModalBody');
                    if (detail && modal && body) {
                        body.innerHTML = detail.innerHTML;
                        modal.classList.add('active');
                        document.body.style.overflow = 'hidden';
                    }
                };
                window.closeGuideModal = function() {
                    const modal = document.getElementById('guideModal');
                    if (modal) { modal.classList.remove('active'); document.body.style.overflow = ''; }
                };
                document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeGuideModal(); });
            }
        });
    </script>
"""
            content = content.replace('</body>', script_html + '</body>')

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Processed and updated {filepath}")
    else:
        print(f"No changes made to {filepath}")

def main():
    files = []
    for d in ['.', 'ko', 'pt']:
        for f in ['calculator.html', 'calendar.html', 'fortune.html']:
            path = os.path.join(d, f)
            if os.path.exists(path):
                files.append(path)
                
    for path in files:
        process_file(path)

if __name__ == '__main__':
    main()
