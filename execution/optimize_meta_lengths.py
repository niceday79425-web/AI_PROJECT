import os
import re

BASE_DIR = r"d:\AI_PROJECT"

OPTIMIZATIONS = {
    # English Root Pages
    "index.html": {
        "title": "US Dividend Stocks Home | WiseAIWiseU",
        "desc": "The starting point for US stock and US dividend stock investment analysis. Check real-time dividend info, rankings, and snowball calculator."
    },
    "list.html": {
        "title": "Top U.S. Dividend Stocks Rank & Screener | WiseAIWiseU",
        "desc": "Find the best premium US dividend stocks using our advanced screener. Custom filter options for payout ratio, yield, growth, and cash flow."
    },
    "calculator.html": {
        "title": "U.S. Dividend Compound & DRIP Calculator | WiseAIWiseU",
        "desc": "Predict asset changes when reinvesting U.S. stock dividends. Simulate the snowball effect with DRIP and annual dividend growth rates."
    },
    "calendar.html": {
        "title": "U.S. Stock Ex-Dividend & Payout Calendar | WiseAIWiseU",
        "desc": "Check U.S. stock ex-dividend dates and payout schedules. Access a comprehensive, real-time calendar of this month's dividend events."
    },
    "fortune.html": {
        "title": "U.S. Stock Portfolio Health & Diversity Tool | WiseAIWiseU",
        "desc": "Analyze correlation and check your U.S. stock portfolio health. Discover if your favorite dividend stocks match your investment style."
    },
    "blog.html": {
        "title": "U.S. Market News & Dividend Stock Analysis | WiseAIWiseU",
        "desc": "Explore latest market trends and in-depth analysis focused on U.S. dividend stocks. Gain insights to optimize your passive income portfolio."
    },
    "learn.html": {
        "title": "U.S. Dividend Growth Course for Beginners | WiseAIWiseU",
        "desc": "Access systematic educational guides from U.S. dividend stock basics to advanced financial analysis. Learn to build a passive income portfolio."
    },
    # Portuguese Pages
    "pt/index.html": {
        "title": "Home de Ações de Dividendos dos EUA | WiseAIWiseU",
        "desc": "O ponto de partida para análise de investimentos em ações dos EUA. Confira informações de dividendos em tempo real, classificações e calculadoras."
    },
    "pt/list.html": {
        "title": "Buscador e Ranking de Ações de Dividendos EUA | WiseAIWiseU",
        "desc": "Encontre as melhores ações de dividendos dos EUA. Filtre ações por rendimento, payout ratio, crescimento de dividendos e fluxo de caixa livre."
    },
    "pt/calculator.html": {
        "title": "Calculadora de Juros Compostos e DRIP dos EUA | WiseAIWiseU",
        "desc": "Simule o crescimento do seu portfólio de dividendos dos EUA. Calcule o efeito bola de neve com reinvestimento automático (DRIP) e juros compostos."
    },
    "pt/calendar.html": {
        "title": "Datas Ex-Dividendos e Calendário de Ações EUA | WiseAIWiseU",
        "desc": "Entenda a Data Ex-Dividendo, a Data de Registro e a Data de Pagamento. Saiba como montar um portfólio de dividendos mensais combinando ações trimestrais."
    },
    "pt/fortune.html": {
        "title": "Diagnóstico e Diversificação de Portfólio EUA | WiseAIWiseU",
        "desc": "Descubra seu MBTI de investidor! Confira a compatibilidade com uma ação e aprenda o método 'Sleep-Well-At-Night Investing' para resistir aos mercados em queda."
    },
    "pt/blog.html": {
        "title": "Análise e Notícias do Mercado de Ações dos EUA | WiseAIWiseU",
        "desc": "Acompanhe as tendências e análises aprofundadas sobre ações de dividendos dos EUA. Descubra as melhores estratégias para sua carteira de investimentos."
    },
    "pt/learn.html": {
        "title": "Curso de Dividendos dos EUA para Iniciantes | WiseAIWiseU",
        "desc": "Aprenda a investir em dividendos dos EUA. Conteúdo educativo completo do básico sobre juros compostos à análise financeira de empresas."
    }
}

def optimize_file(rel_path, data):
    filepath = os.path.join(BASE_DIR, rel_path.replace("/", os.sep))
    if not os.path.exists(filepath):
        print(f"[WARN] File not found: {filepath}")
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    new_title = data["title"]
    new_desc = data["desc"]
    
    # Replace <title>...</title>
    content = re.sub(r'<title[^>]*>([\s\S]*?)</title>', f'<title>{new_title}</title>', content, flags=re.IGNORECASE)
    
    # Replace og:title
    content = re.sub(r'<meta\s+property="og:title"\s+content="[^"]*"[^>]*>', f'<meta property="og:title" content="{new_title}">', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+content="[^"]*"\s+property="og:title"[^>]*>', f'<meta content="{new_title}" property="og:title">', content, flags=re.IGNORECASE)
    
    # Replace meta description
    content = re.sub(r'<meta\s+name="description"\s+content="[^"]*"[^>]*>', f'<meta name="description" content="{new_desc}">', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+content="[^"]*"\s+name="description"[^>]*>', f'<meta content="{new_desc}" name="description">', content, flags=re.IGNORECASE)
    
    # Replace og:description
    content = re.sub(r'<meta\s+property="og:description"\s+content="[^"]*"[^>]*>', f'<meta property="og:description" content="{new_desc}">', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+content="[^"]*"\s+property="og:description"[^>]*>', f'<meta content="{new_desc}" property="og:description">', content, flags=re.IGNORECASE)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Optimized meta tags for: {rel_path} (Title: {len(new_title)} chars, Desc: {len(new_desc)} chars)")
        return True
    else:
        print(f"[SKIP] No changes needed for: {rel_path}")
        return False

def main():
    updated = 0
    for rel_path, data in OPTIMIZATIONS.items():
        if optimize_file(rel_path, data):
            updated += 1
            
    print(f"\nOptimization complete. Updated {updated} files.")

if __name__ == "__main__":
    main()
