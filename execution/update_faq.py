
import os
import re

FAQS = {
    "en": {
        "title": "Dividend Investing FAQ",
        "items": [
            {
                "q": "Is a high dividend yield always good?",
                "a": "No, beware of the <strong>'Dividend Trap.'</strong> An unusually high yield often indicates a dropping stock price due to underlying business issues. Always check the Payout Ratio (ideally under 80% for regular stocks) and the company's history of dividend growth before buying."
            },
            {
                "q": "Why invest in Dividend Growth stocks over High Yield?",
                "a": "To protect against inflation. 'Dividend Growth' stocks (e.g., Dividend Aristocrats) raise their payouts annually. While the initial yield might be lower (e.g., 2%), the <strong>Yield on Cost</strong> can become massive over 10+ years as the dividends increase, often beating high-yield but stagnant stocks."
            },
            {
                "q": "What is DRIP and why is it important?",
                "a": "DRIP stands for <strong>Dividend Reinvestment Plan</strong>. It automatically uses your cash dividends to buy more shares (or partial shares) of the stock. This is the main engine of the 'Snowball Effect,' allowing your portfolio to grow exponentially without adding new capital."
            },
            {
                "q": "How are US dividends taxed for international investors?",
                "a": "For most non-US residents, the US government withholds a <strong>30% tax</strong> on dividends. However, if your country has a tax treaty with the US, this rate is often reduced to <strong>15%</strong>. Check with your local tax authority for specific treaty rates."
            },
            {
                "q": "What unique metrics should I check for REITs?",
                "a": "For REITs (Real Estate Investment Trusts), don't look at Net Income. Instead, use <strong>FFO (Funds From Operations)</strong> or AFFO. Because REITs have high non-cash depreciation, Net Income is misleading; FFO tells you how much cash is actually available for dividends."
            },
            {
                "q": "How does the exchange rate impact my dividend income?",
                "a": "Investing in US stocks provides <strong>currency diversification</strong>. When the USD strengthens against your local currency, your dividend income effectively increases in value. Even if the exchange rate drops, you still hold assets in the world's primary reserve currency."
            }
        ]
    },
    "ko": {
        "title": "배당 투자 FAQ",
        "items": [
            {
                "q": "배당수익률이 높으면 무조건 좋은가요?",
                "a": "아니요, <strong>'배당의 함정(Dividend Trap)'</strong>을 주의해야 합니다. 비정상적으로 높은 배당률은 실적 악화로 주가가 급락했을 때 나타나는 신호일 수 있습니다. 반드시 배당성향(Payout Ratio)이 80% 이하인지, 최근 배당 삭감은 없었는지 확인해야 합니다."
            },
            {
                "q": "왜 고배당주보다 배당 성장주가 유리한가요?",
                "a": "인플레이션을 방어하기 위함입니다. '배당 성장주'는 매년 배당금을 인상합니다. 초기 수익률은 낮을 수 있지만, 10년 뒤 <strong>'취득가 대비 수익률(Yield on Cost)'</strong>은 고배당주보다 훨씬 높아질 수 있으며, 이는 장기적인 복리 효과의 핵심입니다."
            },
            {
                "q": "배당 재투자(DRIP)란 무엇인가요?",
                "a": "<strong>DRIP(Dividend Reinvestment Plan)</strong>은 받은 배당금을 현금으로 쓰지 않고 자동으로 해당 주식을 다시 사는 것입니다. 이는 자산을 기하급수적으로 불리는 '스노우볼 효과'의 핵심 동력입니다."
            },
            {
                "q": "미국 주식 배당금 세금은 어떻게 되나요?",
                "a": "한국 거주자의 경우, 미국 현지에서 <strong>15%가 원천징수</strong>된 후 입금됩니다. 별도로 신고할 필요는 없지만, 연간 금융소득(배당+이자)이 <strong>2,000만 원</strong>을 초과하면 금융소득종합과세 대상이 되어 직접 신고해야 합니다."
            },
            {
                "q": "리츠(REITs) 분석 시 주의할 점은 무엇인가요?",
                "a": "리츠는 순이익(Net Income) 대신 <strong>FFO(운영 자금)</strong>를 봐야 합니다. 리츠는 부동산 감가상각비가 커서 순이익이 적게 잡히기 때문입니다. FFO를 통해 실제 배당을 줄 수 있는 현금 흐름이 충분한지 파악하는 것이 중요합니다."
            },
            {
                "q": "환율(달러 강세)이 투자에 어떤 영향을 주나요?",
                "a": "미국 주식 투자는 <strong>달러(USD)라는 안전 자산</strong>을 보유하는 효과가 있습니다. 환율이 오르면 배당금의 원화 환산 가치가 높아져 자산 방어에 유리합니다. 환율이 낮아질 때는 더 싼 가격에 달러 자산을 모을 기회로 활용할 수 있습니다."
            }
        ]
    },
    "pt": {
        "title": "Perguntas Frequentes sobre Dividendos",
        "items": [
            {
                "q": "Um alto rendimento (Dividend Yield) é sempre bom?",
                "a": "Não, cuidado com a <strong>'Armadilha de Dividendos'</strong>. Um rendimento muito alto pode indicar uma queda drástica no preço devido a problemas financeiros. Sempre verifique o Payout Ratio (idealmente abaixo de 80%) e o histórico de dividendos da empresa."
            },
            {
                "q": "Por que investir em Dividend Growth em vez de High Yield?",
                "a": "Para vencer a inflação. Ações de 'Crescimento de Dividendos' aumentam seus pagamentos anualmente. Embora o rendimento inicial possa ser menor, o <strong>Yield on Cost</strong> torna-se massivo ao longo dos anos, superando ações que pagam muito hoje mas não crescem."
            },
            {
                "q": "O que é DRIP e por que é importante?",
                "a": "DRIP é o <strong>Plano de Reinvestimento de Dividendos</strong>. Ele usa seus dividendos para comprar automaticamente mais ações da mesma empresa. É o motor do 'Efeito Bola de Neve', permitindo que seu patrimônio cresça sem a necessidade de novos aportes."
            },
            {
                "q": "Como funciona o imposto sobre dividendos nos EUA para estrangeiros?",
                "a": "Geralmente, há uma retenção de <strong>30% de imposto</strong> na fonte. No entanto, se o seu país tiver um tratado tributário com os EUA, essa taxa pode ser reduzida para <strong>15%</strong>. Verifique os acordos fiscais internacionais do seu país."
            },
            {
                "q": "Quais métricas são importantes para analisar REITs?",
                "a": "Para REITs, ignore o Lucro Líquido. Use o <strong>FFO (Funds From Operations)</strong>. Como os REITs têm altas taxas de depreciação, o Lucro Líquido é enganoso; o FFO mostra o dinheiro real disponível para pagar os dividendos."
            },
            {
                "q": "Como a taxa de câmbio afeta meus dividendos?",
                "a": "Investir nos EUA oferece <strong>diversificação cambial</strong>. Quando o Dólar se valoriza frente à sua moeda local, sua renda passiva aumenta de valor. Você passa a ter uma proteção natural no Dólar, a moeda de reserva mundial."
            }
        ]
    }
}

def generate_faq_html(lang):
    faq_data = FAQS.get(lang, FAQS["en"])
    html = f'        <section class="faq-section">\n            <h2>{faq_data["title"]}</h2>\n            <div class="faq-container">\n'
    for item in faq_data["items"]:
        html += f'                <div class="faq-item">\n                    <details>\n                        <summary>{item["q"]}</summary>\n                        <p>{item["a"]}</p>\n                    </details>\n                </div>\n'
    html += '            </div>\n        </section>'
    return html

def update_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lang = "en"
        if "\\ko\\" in filepath: lang = "ko"
        elif "\\pt\\" in filepath: lang = "pt"
        
        new_faq = generate_faq_html(lang)
        
        # Replace existing faq-section
        content = re.sub(r'<section class="faq-section">.*?</section>', new_faq, content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[FAQ UPDATED] {filepath}")
        
    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")

def main():
    targets = ["d:\\AI_PROJECT\\index.html", "d:\\AI_PROJECT\\ko\\index.html", "d:\\AI_PROJECT\\pt\\index.html"]
    for target in targets:
        if os.path.exists(target):
            update_file(target)

if __name__ == "__main__":
    main()
