
import os
import re

# --- Content Definitions ---

# Footer Links (Common across all versions, but text could be translated)
def get_footer_links(lang):
    links = {
        "en": [("Privacy Policy", "/privacy.html"), ("About Us", "/about.html"), ("Contact", "/contact.html")],
        "ko": [("개인정보처리방침", "/privacy.html"), ("회사소개", "/about.html"), ("문의하기", "/contact.html")],
        "pt": [("Política de Privacidade", "/privacy.html"), ("Sobre Nós", "/about.html"), ("Contato", "/contact.html")]
    }
    items = links.get(lang, links["en"])
    links_html = ' | '.join([f'<a href="{url}" style="color: var(--text-secondary); text-decoration: none; margin: 0 10px;">{text}</a>' for text, url in items])
    return f'''
                <div class="footer-nav" style="margin-bottom: 1.5rem; font-size: 0.9rem;">
                    {links_html}
                </div>'''

# Calculator Enrichment
CALCULATOR_EN = '''
            <section class="education-section" style="margin-top: 4rem; max-width: 800px; margin-left: auto; margin-right: auto;">
                <h3 style="font-size: 1.8rem; margin-bottom: 1.5rem; color: var(--accent-purple);">Understanding the Magic of Compound Interest</h3>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">Compound interest is often called the "eighth wonder of the world" by financial experts. Unlike simple interest, where you only earn interest on your principal investment, compound interest allows you to earn interest on your interest.</p>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">This snowball effect means that your wealth can grow exponentially over time. The longer you let your money sit and compound, the faster it grows. This is why starting early is the most important factor in building wealth.</p>
                <h4 style="font-size: 1.4rem; margin-top: 2rem; margin-bottom: 1rem; color: var(--text-primary);">How to Use This Calculator</h4>
                <ul style="list-style-type: disc; padding-left: 1.5rem; color: var(--text-secondary); margin-bottom: 2rem;">
                    <li style="margin-bottom: 0.5rem;"><strong>Initial Investment:</strong> The amount of money you start with.</li>
                    <li style="margin-bottom: 0.5rem;"><strong>Monthly Contribution:</strong> How much you add to your portfolio each month.</li>
                    <li style="margin-bottom: 0.5rem;"><strong>Dividend Yield:</strong> The annual percentage return from dividends.</li>
                    <li style="margin-bottom: 0.5rem;"><strong>Years to Grow:</strong> How long you plan to invest. Even 5 more years can make a huge difference!</li>
                </ul>
                <div style="background: var(--glass-bg); padding: 1.5rem; border-left: 4px solid var(--success); border-radius: 4px;">
                    <p style="font-style: italic; color: #fff;">"My wealth has come from a combination of living in America, some lucky genes, and compound interest." — Warren Buffett</p>
                </div>
            </section>
'''

CALCULATOR_KO = '''
            <section class="education-section" style="margin-top: 4rem; max-width: 800px; margin-left: auto; margin-right: auto;">
                <h3 style="font-size: 1.8rem; margin-bottom: 1.5rem; color: var(--accent-purple);">복리의 마법 이해하기</h3>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">알베르트 아인슈타인은 복리를 "세계 8대 불가사의"라고 불렀습니다. 원금에 대해서만 이자를 받는 단리와 달리, 복리는 이자에 이자가 붙는 방식입니다.</p>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">이 스노우볼 효과는 시간이 지날수록 자산이 기하급수적으로 성장하게 만듭니다. 더 일찍 시작할수록, 더 오래 복리 효과를 누릴수록 결과는 놀라워집니다. 이것이 바로 배당 재투자가 중요한 이유입니다.</p>
                <h4 style="font-size: 1.4rem; margin-top: 2rem; margin-bottom: 1rem; color: var(--text-primary);">계산기 활용 팁</h4>
                <ul style="list-style-type: disc; padding-left: 1.5rem; color: var(--text-secondary); margin-bottom: 2rem;">
                    <li style="margin-bottom: 0.5rem;"><strong>초기 투자금:</strong> 현재 보유하고 있는 투자 원금입니다.</li>
                    <li style="margin-bottom: 0.5rem;"><strong>월 적립액:</strong> 매달 추가로 투자할 금액입니다.</li>
                    <li style="margin-bottom: 0.5rem;"><strong>배당 수익률:</strong> 세전 연간 배당률입니다 (예: SCHD 약 3.5%).</li>
                    <li style="margin-bottom: 0.5rem;"><strong>투자 기간:</strong> 은퇴나 목표 달성까지의 기간입니다. 단 5년의 차이가 최종 자산을 바꿉니다!</li>
                </ul>
                <div style="background: var(--glass-bg); padding: 1.5rem; border-left: 4px solid var(--success); border-radius: 4px;">
                    <p style="font-style: italic; color: #fff;">"나의 부는 미국이라는 나라, 운 좋은 유전자, 그리고 복리의 조합에서 나왔다." — 워렌 버핏</p>
                </div>
            </section>
'''

CALCULATOR_PT = '''
            <section class="education-section" style="margin-top: 4rem; max-width: 800px; margin-left: auto; margin-right: auto;">
                <h3 style="font-size: 1.8rem; margin-bottom: 1.5rem; color: var(--accent-purple);">Entendendo a Magia dos Juros Compostos</h3>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">Os juros compostos são frequentemente chamados de "oitava maravilha do mundo". Ao contrário dos juros simples, você ganha juros sobre os juros já acumulados.</p>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">Este efeito "bola de neve" significa que sua riqueza pode crescer exponencialmente. Quanto mais cedo você começar, maior será o impacto a longo prazo. É por isso que o reinvestimento de dividendos é tão poderoso.</p>
                <h4 style="font-size: 1.4rem; margin-top: 2rem; margin-bottom: 1rem; color: var(--text-primary);">Como Usar esta Calculadora</h4>
                <ul style="list-style-type: disc; padding-left: 1.5rem; color: var(--text-secondary); margin-bottom: 2rem;">
                    <li style="margin-bottom: 0.5rem;"><strong>Investimento Inicial:</strong> O montante com que você começa.</li>
                    <li style="margin-bottom: 0.5rem;"><strong>Contribuição Mensal:</strong> Quanto você economiza por mês.</li>
                    <li style="margin-bottom: 0.5rem;"><strong>Dividend Yield:</strong> O rendimento anual esperado em dividendos.</li>
                    <li style="margin-bottom: 0.5rem;"><strong>Anos de Crescimento:</strong> Seu horizonte de investimento.</li>
                </ul>
                <div style="background: var(--glass-bg); padding: 1.5rem; border-left: 4px solid var(--success); border-radius: 4px;">
                    <p style="font-style: italic; color: #fff;">"Minha riqueza veio de uma combinação de viver na América, alguns genes de sorte e juros compostos." — Warren Buffett</p>
                </div>
            </section>
'''

# Calendar Enrichment
CALENDAR_EN = '''
            <section class="education-section" style="margin-top: 4rem;">
                <h3 style="font-size: 1.8rem; margin-bottom: 1.5rem; color: var(--accent-blue);">Dividend Capture Strategy: The Trap</h3>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">Many beginners try to buy a stock just before the "Ex-Dividend Date" and sell it right after receiving the dividend. This is known as the Dividend Capture Strategy.</p>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">However, stock prices typically drop by the dividend amount on the ex-date. After paying dividend taxes (15%), you might end up with a net loss. Real wealth is built by holding quality companies for years, not chasing dates.</p>
            </section>
'''

CALENDAR_KO = '''
            <section class="education-section" style="margin-top: 4rem;">
                <h3 style="font-size: 1.8rem; margin-bottom: 1.5rem; color: var(--accent-blue);">배당락일 매수 전략 (Dividend Capture)의 함정</h3>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">배당락일(Ex-Dividend Date) 직전에 매수하여 배당금만 받고 파는 전략을 고민하시나요? 하지만 주의해야 할 점이 있습니다.</p>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">배당락일이 되면 주가는 보통 배당금만큼 하락하여 시작합니다. 또한 배당소득세(15%)를 내고 나면 실질적으로는 손해를 볼 수도 있습니다. 성공적인 배당 투자는 날짜를 쫓는 것이 아니라, 우량한 기업을 장기 보유하는 데서 옵니다.</p>
            </section>
'''

CALENDAR_PT = '''
            <section class="education-section" style="margin-top: 4rem;">
                <h3 style="font-size: 1.8rem; margin-bottom: 1.5rem; color: var(--accent-blue);">Estratégia de Captura de Dividendos: A Armadilha</h3>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">Muitos iniciantes tentam comprar uma ação pouco antes da "Data Ex-Dividendo" e vendê-la logo após. Isso é conhecido como Estratégia de Captura de Dividendos.</p>
                <p style="margin-bottom: 1rem; color: var(--text-secondary);">No entanto, os preços das ações geralmente caem pelo valor do dividendo na data-ex. Após pagar os impostos, você pode ter um prejuízo real. A riqueza real é construída mantendo boas empresas por anos.</p>
            </section>
'''

# --- Functions ---

def inject_footer_links(content, lang):
    if "Privacy Policy" in content or "개인정보처리방침" in content or "Política de Privacidade" in content:
        # Update existing
        content = re.sub(r'<div class="footer-nav".*?</div>', get_footer_links(lang), content, flags=re.DOTALL)
    else:
        # Inject new
        if '<div class="legal-disclaimer">' in content:
            content = content.replace('<div class="legal-disclaimer">', get_footer_links(lang) + '\n<div class="legal-disclaimer">')
        elif '<p>&copy;' in content:
            content = content.replace('<p>&copy;', get_footer_links(lang) + '\n<p>&copy;')
    return content

def enrich_calculator(content, filepath):
    if "calculator.html" not in filepath: return content
    if "education-section" in content: return content # Skip if already enriched
    
    inject_text = CALCULATOR_EN
    if "\\ko\\" in filepath: inject_text = CALCULATOR_KO
    elif "\\pt\\" in filepath: inject_text = CALCULATOR_PT
    
    if '</section>\n        </main>' in content:
        content = content.replace('</section>\n        </main>', '</section>' + inject_text + '</main>')
    elif '</main>' in content:
        content = content.replace('</main>', inject_text + '</main>')
    return content

def enrich_calendar(content, filepath):
    if "calendar.html" not in filepath: return content
    if "education-section" in content: return content
    
    inject_text = CALENDAR_EN
    if "\\ko\\" in filepath: inject_text = CALENDAR_KO
    elif "\\pt\\" in filepath: inject_text = CALENDAR_PT
    
    if '</main>' in content:
        content = content.replace('</main>', inject_text + '</main>')
    return content

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig = content
        lang = "en"
        if "\\ko\\" in filepath: lang = "ko"
        elif "\\pt\\" in filepath: lang = "pt"
        
        content = inject_footer_links(content, lang)
        content = enrich_calculator(content, filepath)
        content = enrich_calendar(content, filepath)
        
        if content != orig:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[ENRICHED] {filepath}")
            
    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")

def main():
    root_dir = "d:\\AI_PROJECT"
    for current_root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                process_file(os.path.join(current_root, file))

if __name__ == "__main__":
    main()
