import os
import re

def process_file(filepath, tool_regex, guide_regex):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find tool section(s)
    tool_match = re.search(tool_regex, content, re.DOTALL)
    if not tool_match:
        print(f"Tool section not found in {filepath}")
        return

    # Find guide section
    guide_match = re.search(guide_regex, content, re.DOTALL)
    if not guide_match:
        print(f"Guide section not found in {filepath}")
        return

    if guide_match.start() < tool_match.start():
        print(f"Guide is already before tool in {filepath}")
        return

    tool_content = tool_match.group(0)
    guide_content = guide_match.group(0)

    # Modify guide content margins and font sizes
    guide_content = guide_content.replace('margin-top: 4rem;', 'margin-bottom: 4rem;')
    guide_content = guide_content.replace('font-size: 2rem;', 'font-size: clamp(1.5rem, 4vw, 2rem);')
    guide_content = guide_content.replace('font-size: 1rem;', 'font-size: clamp(0.9rem, 2vw, 1rem);')

    # Reconstruct
    # Replace the old guide_content with empty string where it was
    content = content[:guide_match.start()] + content[guide_match.end():]
    
    # Now insert guide_content before tool_content
    # Since we removed guide_content, the position of tool_match is still valid 
    # (assuming guide_content was AFTER tool_content, which we checked)
    
    tool_start = content.find(tool_content)
    new_content = content[:tool_start] + guide_content + '\n\n' + tool_content + content[tool_start + len(tool_content):]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

def main():
    dirs = ['.', 'ko', 'pt']
    
    for d in dirs:
        # calculator.html
        calc_path = os.path.join(d, 'calculator.html')
        if os.path.exists(calc_path):
            process_file(
                calc_path,
                r'<section class="calculator-card">.*?</section>\s*<section class="results-container">.*?</section>',
                r'<section class="education-section"[^>]*>.*?</section>'
            )
            
        # calendar.html
        cal_path = os.path.join(d, 'calendar.html')
        if os.path.exists(cal_path):
            process_file(
                cal_path,
                r'<section class="card"[^>]*>.*?</section>',
                r'<section class="education-section"[^>]*>.*?</section>'
            )
            
        # fortune.html
        fort_path = os.path.join(d, 'fortune.html')
        if os.path.exists(fort_path):
            process_file(
                fort_path,
                r'<section class="card fortune-card">.*?</section>',
                r'<section style="margin-top: 4rem; text-align: left;">.*?</section>'
            )

if __name__ == '__main__':
    main()
