
import os

# Content to inject
FOOTER_LINKS_EN = '''
                <div class="footer-nav" style="margin-bottom: 1.5rem; font-size: 0.9rem;">
                    <a href="/privacy.html" style="color: var(--text-secondary); text-decoration: none; margin: 0 10px;">Privacy Policy</a> |
                    <a href="/about.html" style="color: var(--text-secondary); text-decoration: none; margin: 0 10px;">About Us</a> |
                    <a href="/contact.html" style="color: var(--text-secondary); text-decoration: none; margin: 0 10px;">Contact</a>
                </div>'''

# Calculator Enrichment Text
CALCULATOR_TEXT = '''
            <section class="education-section" style="margin-top: 4rem; max-width: 800px; margin-left: auto; margin-right: auto;">
                <h3 style="font-size: 1.8rem; margin-bottom: 1.5rem; color: var(--accent-purple);">Understanding the Magic of Compound Interest</h3>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">Compound interest is often called the "eighth wonder of the world" by financial experts. Unlike simple interest, where you only earn interest on your principal investment, compound interest allows you to earn interest on your interest.</p>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">This snowball effect means that your wealth can grow exponentially over time. The longer you let your money sit and compound, the faster it grows. This is why starting early is the most important factor in building wealth.</p>
                
                <h4 style="font-size: 1.4rem; margin-top: 2rem; margin-bottom: 1rem; color: var(--text-primary);">How to Use This Calculator</h4>
                <ul style="list-style-type: disc; padding-left: 1.5rem; color: var(--text-secondary); margin-bottom: 2rem;">
                    <li style="margin-bottom: 0.5rem;"><strong>Initial Investment:</strong> The amount of money you start with.</li>
                    <li style="margin-bottom: 0.5rem;"><strong>Monthly Contribution:</strong> How much you add to your portfolio each month.</li>
                    <li style="margin-bottom: 0.5rem;"><strong>Dividend Yield:</strong> The annual percentage return from dividends (e.g., SCHD is around 3.5%).</li>
                    <li style="margin-bottom: 0.5rem;"><strong>Years to Grow:</strong> How long you plan to invest. Even 5 more years can make a huge difference!</li>
                </ul>
                
                <div style="background: var(--glass-bg); padding: 1.5rem; border-left: 4px solid var(--success); border-radius: 4px;">
                    <p style="font-style: italic; color: #fff;">"My wealth has come from a combination of living in America, some lucky genes, and compound interest." — Warren Buffett</p>
                </div>
            </section>
'''

# Calendar Enrichment Text
CALENDAR_TEXT = '''
            <section class="education-section" style="margin-top: 4rem;">
                <h3 style="font-size: 1.8rem; margin-bottom: 1.5rem; color: var(--accent-blue);">Dividend Capture Strategy</h3>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">Using a dividend calendar is essential for investors who want to maximize their income. By knowing exactly when a stock goes "Ex-Dividend," you can time your purchases to ensure you are eligible for the next payout.</p>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">However, beware of the "Dividend Capture Strategy" trap. Stock prices typically drop by the amount of the dividend on the ex-dividend date. Successful dividend investing focuses on long-term holding of high-quality companies rather than chasing dates.</p>
            </section>
'''

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Inject Footer Links (if not present)
        if "Privacy Policy" not in content:
            # Inject before legal-disclaimer or inside footer-content
            if '<div class="legal-disclaimer">' in content:
                content = content.replace('<div class="legal-disclaimer">', FOOTER_LINKS_EN + '\n<div class="legal-disclaimer">')
                print(f"[LINKS] Added to {filepath}")
            elif '<p>&copy;' in content: # Fallback
                content = content.replace('<p>&copy;', FOOTER_LINKS_EN + '\n<p>&copy;')
                print(f"[LINKS] Added to {filepath}")

        # 2. Enrich Content for Calculator (only EN version for now to be safe, or all if generic)
        if "calculator.html" in filepath and "Understanding the Magic" not in content and "ko" not in filepath and "pt" not in filepath:
            # Insert before </main>
            content = content.replace('</section>\n        </main>', '</section>' + CALCULATOR_TEXT + '</main>')
            print(f"[CONTENT] Enriched {filepath}")

        # 3. Enrich Content for Calendar
        if "calendar.html" in filepath and "Dividend Capture Strategy" not in content and "ko" not in filepath and "pt" not in filepath:
             # Insert before </main>
            content = content.replace('</main>', CALENDAR_TEXT + '</main>')
            print(f"[CONTENT] Enriched {filepath}")

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")

def main():
    for root, dirs, files in os.walk("d:\\AI_PROJECT"):
        for file in files:
            if file.endswith(".html"):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
