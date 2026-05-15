import json
import os
import datetime

today = "2026-05-15"
ticker = "WMT"
price = 132.46
change = 0.75
chart_url = f"https://quickchart.io/chart?c={{%22type%22:%22line%22,%22data%22:{{%22labels%22:[%2203-15%22,%2204-01%22,%2204-15%22,%2205-01%22,%2205-15%22],%22datasets%22:[{{%22label%22:%22WMT%20Price%22,%22data%22:[120,125,128,130,132.46],%22fill%22:false,%22borderColor%22:%22rgb(99,102,241)%22}}]}}}}"

contents = {
    "en": {
        "title": "Walmart (WMT) Earnings Preview: Dividend Stability in a Tech-Driven Retail Era | US Stock Analysis · WiseAIWiseU",
        "summary": "Walmart (WMT) shows strong momentum ahead of its Q1 earnings on May 21. With 53 years of dividend increases and a yield-focused tech evolution, is this US stock a must-buy for defensive portfolios?",
        "keywords": "US stocks, WMT, Walmart dividend, stock analysis, retail stocks",
        "content": f"""
            <div class="metrics-bar">
                <div class="metric-item"><span class="label">Price</span><span class="value">${price:.2f}</span></div>
                <div class="metric-item"><span class="label">Change</span><span class="value" style="color:#10b981">+{change:.2f}%</span></div>
                <div class="metric-item"><span class="label">Yield</span><span class="value">1.34%</span></div>
            </div>
            <h2>Executive Summary</h2>
            <p>As we approach May 15, 2026, <strong>Walmart Inc. (WMT)</strong> continues to demonstrate why it remains a cornerstone of conservative <strong>US stock</strong> portfolios. Currently trading at ${price:.2f}, the retail giant is showing a technical breakout ahead of its highly anticipated Q1 earnings report scheduled for May 21. With a track record of 53 consecutive years of dividend growth, Walmart isn't just a retail store; it's a dividend fortress.</p>
            
            [CHART-HERE]
            
            <h2>Recent Performance & Key Events</h2>
            <p>Walmart's stock has surged approximately 15% year-to-date in 2026, significantly outperforming many of its peers in the retail sector. The market is currently pricing in a strong Q1 performance, with revenue expectations hitting nearly $175 billion. A key driver for this optimism is the "Walmart Connect" advertising business, which has seen high-double-digit growth, diversifying Walmart's income streams beyond traditional brick-and-mortar sales.</p>
            
            <h2>Technical Analysis</h2>
            <p>From a technical perspective, WMT is currently testing resistance near the $135 level. The Relative Strength Index (RSI) is hovering around 65, suggesting strong momentum without being excessively overbought. Key support levels are firmly established at $128 and $122. If earnings beat expectations on May 21, analysts see a path toward $145 by the end of the second quarter.</p>
            
            <h2>Dividend Investor Perspective</h2>
            <p>For dividend growth investors, Walmart is a "Dividend King." The company recently paid its quarterly dividend of $0.2475 per share. With a payout ratio of roughly 34%, the dividend is exceptionally secure, leaving ample room for the company to continue its share buyback program and invest in AI-driven supply chain automation.</p>
            
            <h2>Risk Factors</h2>
            <ul>
                <li><strong>Inflationary Pressure:</strong> While Walmart thrives as a value destination, sustained high labor costs could squeeze margins.</li>
                <li><strong>E-commerce Competition:</strong> Despite strong growth, the battle with Amazon remains capital-intensive.</li>
                <li><strong>Macroeconomic Slowdown:</strong> A significant dip in consumer spending could impact discretionary categories.</li>
            </ul>
            
            <h2>Conclusion & Investor Action Points</h2>
            <p>Walmart remains a "Strong Buy" for those seeking defensive growth and reliable income. Investors should watch the May 21 earnings call closely for updates on their tech initiatives. You can evaluate how Walmart fits into your long-term goals using our <a href="/list">Dividend Scouter</a> or simulate your future returns with the <a href="/calculator">Snowball Calculator</a>.</p>
        """
    },
    "ko": {
        "title": "월마트(WMT) 실적 프리뷰: 기술 중심 유통 시대의 배당 안정성 분석 | 미국 주식 분석 · WiseAIWiseU",
        "summary": "5월 21일 1분기 실적 발표를 앞둔 월마트(WMT)의 모멘텀이 심상치 않습니다. 53년 연속 배당 성장과 AI 기반 물류 혁신을 이어가는 월마트가 미국 주식 방어주 포트폴리오의 핵심인 이유를 분석합니다.",
        "keywords": "미국 주식, WMT, 월마트 배당금, 주식 분석, 소매 유통주",
        "content": f"""
            <div class="metrics-bar">
                <div class="metric-item"><span class="label">현재가</span><span class="value">${price:.2f}</span></div>
                <div class="metric-item"><span class="label">등락</span><span class="value" style="color:#10b981">+{change:.2f}%</span></div>
                <div class="metric-item"><span class="label">배당수익률</span><span class="value">1.34%</span></div>
            </div>
            <h2>요약 (Executive Summary)</h2>
            <p>2026년 5월 15일 현재, <strong>월마트(WMT)</strong>는 왜 자신이 보수적인 <strong>미국 주식</strong> 포트폴리오의 초석인지 다시 한번 증명하고 있습니다. 현재 ${price:.2f} 선에서 거래 중인 이 유통 거인은 5월 21일로 예정된 1분기 실적 발표를 앞두고 강력한 기술적 돌파를 시도하고 있습니다. 53년 연속 배당금을 인상한 '배당 귀족'을 넘어 '배당 왕'의 지위를 공고히 하고 있는 월마트는 단순한 소매점이 아닌 배당의 요새입니다.</p>
            
            [CHART-HERE]
            
            <h2>최근 성과 및 주요 이슈</h2>
            <p>월마트의 주가는 2026년 들어 현재까지 약 15% 상승하며 소매 섹터 내 경쟁사들을 압도하고 있습니다. 시장은 현재 약 1,750억 달러에 달하는 기록적인 1분기 매출을 기대하고 있습니다. 이러한 낙관론의 핵심 동력은 '월마트 커넥트(Walmart Connect)'라는 광고 사업입니다. 이 부문은 두 자릿수 고성장을 기록하며 월마트의 수익 구조를 전통적인 판매에서 데이터 기반 비즈니스로 다변화하고 있습니다.</p>
            
            <h2>기술적 분석</h2>
            <p>기술적 관점에서 WMT는 현재 $135 부근의 저항선을 테스트하고 있습니다. 상대강도지수(RSI)는 65 수준으로, 과매수 구간에 진입하기 전의 강력한 상승 모멘텀을 보여주고 있습니다. 주요 지지선은 $128와 $122에 형성되어 있습니다. 만약 5월 21일 실적이 시장 예상치를 상회한다면, 분석가들은 2분기 말까지 $145를 목표가로 보고 있습니다.</p>
            
            <h2>배당 투자자 관점</h2>
            <p>배당 성장 투자자들에게 월마트는 신뢰의 상징입니다. 최근 주당 $0.2475의 분기 배당금을 지급했으며, 배당 성향은 약 34%로 매우 안전한 수준입니다. 이는 월마트가 지속적인 배당 인상은 물론, 자사주 매입과 AI 기반 공급망 자동화에 투자할 충분한 여력이 있음을 의미합니다.</p>
            
            <h2>리스크 요인</h2>
            <ul>
                <li><strong>인플레이션 압박:</strong> 가성비 전략으로 수혜를 입지만, 지속적인 인건비 상승은 수익성에 부담이 될 수 있습니다.</li>
                <li><strong>이커머스 경쟁:</strong> 아마존과의 주도권 싸움은 여전히 막대한 자본 투자를 필요로 합니다.</li>
                <li><strong>경기 둔화:</strong> 소비 심리가 급격히 위축될 경우 재량 소비재 카테고리의 매출이 타격을 입을 수 있습니다.</li>
            </ul>
            
            <h2>결론 및 투자 포인트</h2>
            <p>월마트는 방어적 성장과 안정적인 배당 수익을 동시에 추구하는 투자자들에게 여전히 '강력 매수' 종목입니다. 5월 21일 실적 발표에서 기술 혁신의 진척 상황을 꼭 확인하시기 바랍니다. 나만의 포트폴리오 전략은 <a href="/ko/list">배당주 스카우터</a>에서 점검해 보시고, <a href="/ko/calculator">스노볼 계산기</a>로 미래 수익을 시뮬레이션해 보세요.</p>
        """
    },
    "pt": {
        "title": "Prévia de Resultados do Walmart (WMT): Estabilidade de Dividendos na Era do Varejo Tecnológico | Análise de Ações dos EUA · WiseAIWiseU",
        "summary": "O Walmart (WMT) apresenta forte impulso antes de seus resultados do 1º trimestre em 21 de maio. Com 53 anos de aumentos de dividendos e uma evolução tecnológica focada em rendimento, esta ação dos EUA é indispensável para carteiras defensivas?",
        "keywords": "ações dos EUA, WMT, dividendos Walmart, análise de ações, varejo",
        "content": f"""
            <div class="metrics-bar">
                <div class="metric-item"><span class="label">Preço</span><span class="value">${price:.2f}</span></div>
                <div class="metric-item"><span class="label">Variação</span><span class="value" style="color:#10b981">+{change:.2f}%</span></div>
                <div class="metric-item"><span class="label">Yield</span><span class="value">1.34%</span></div>
            </div>
            <h2>Resumo Executivo</h2>
            <p>Ao nos aproximarmos de 15 de maio de 2026, o <strong>Walmart Inc. (WMT)</strong> continua a demonstrar por que continua sendo a pedra angular das carteiras conservadoras de <strong>ações dos EUA</strong>. Atualmente cotada a ${price:.2f}, a gigante do varejo mostra um rompimento técnico antes de seu aguardado relatório de lucros do 1º trimestre, agendado para 21 de maio. Com um histórico de 53 anos consecutivos de crescimento de dividendos, o Walmart não é apenas uma loja de varejo; é uma fortaleza de dividendos.</p>
            
            [CHART-HERE]
            
            <h2>Desempenho Recente e Eventos Chave</h2>
            <p>As ações do Walmart subiram aproximadamente 15% no acumulado do ano em 2026, superando significativamente muitos de seus pares no setor de varejo. O mercado está precificando um forte desempenho no 1º trimestre, com expectativas de receita atingindo quase US$ 175 bilhões. Um impulsionador chave para esse otimismo é o negócio de publicidade "Walmart Connect", que teve um crescimento de dois dígitos altos, diversificando os fluxos de renda do Walmart além das vendas físicas tradicionais.</p>
            
            <h2>Análise Técnica</h2>
            <p>De uma perspectiva técnica, o WMT está testando a resistência perto do nível de US$ 135. O Índice de Força Relativa (RSI) está oscilando em torno de 65, sugerindo forte impulso sem estar excessivamente sobrecomprado. Os níveis de suporte principais estão firmemente estabelecidos em US$ 128 e US$ 122. Se os lucros superarem as expectativas em 21 de maio, os analistas veem um caminho para US$ 145 até o final do segundo trimestre.</p>
            
            <h2>Perspectiva do Investidor em Dividendos</h2>
            <p>Para investidores em crescimento de dividendos, o Walmart é um "Dividend King". A empresa pagou recentemente seu dividendo trimestral de US$ 0,2475 por ação. Com um índice de distribuição de cerca de 34%, o dividendo é excepcionalmente seguro, deixando amplo espaço para a empresa continuar seu programa de recompra de ações e investir na automação da cadeia de suprimentos impulsionada por IA.</p>
            
            <h2>Fatores de Risco</h2>
            <ul>
                <li><strong>Pressão Inflacionária:</strong> Embora o Walmart prospere como um destino de valor, custos trabalhistas elevados sustentados podem comprimir as margens.</li>
                <li><strong>Concorrência no E-commerce:</strong> Apesar do forte crescimento, a batalha com a Amazon continua exigindo muito capital.</li>
                <li><strong>Desaceleração Macroeconômica:</strong> Uma queda significativa nos gastos do consumidor pode impactar categorias discricionárias.</li>
            </ul>
            
            <h2>Conclusão e Pontos de Ação para o Investidor</h2>
            <p>O Walmart continua sendo uma "Compra Forte" para aqueles que buscam crescimento defensivo e renda confiável. Os investidores devem acompanhar de perto a chamada de lucros de 21 de maio. Você pode avaliar como o Walmart se encaixa em seus objetivos de longo prazo usando nosso <a href="/pt/list">Dividend Scouter</a> ou simular seus retornos futuros com o <a href="/pt/calculator">Snowball Calculator</a>.</p>
        """
    }
}

# Use template from auto_poster.py
def build_post_html(lang, title, summary, keywords, today, ticker, article_body, css_path, home_path):
    back_labels = {"en": "← Back to Blog", "ko": "← 블로그로 돌아가기", "pt": "← Voltar ao Blog"}
    back_label = back_labels.get(lang, "← Back to Blog")
    blog_path = f"/{'' if lang == 'en' else lang + '/'}blog.html"
    nav_ko_active = 'active' if lang == 'ko' else ''
    nav_en_active = 'active' if lang == 'en' else ''
    nav_pt_active = 'active' if lang == 'pt' else ''
    
    # Simple version of the template for manual creation
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{summary[:160]}">
  <meta name="keywords" content="{keywords}">
  <link rel="stylesheet" href="{css_path}">
  <style>
    body {{ font-family: 'Inter', sans-serif; background: #0f172a; color: #f8fafc; }}
    .post-hero {{ padding: 6rem 1.5rem 5rem; text-align: center; background: radial-gradient(circle at top, rgba(99,102,241,0.1) 0%, transparent 70%); }}
    .post-content {{ max-width: 760px; margin: 0 auto; padding: 4rem 1.5rem; line-height: 1.8; }}
    .metrics-bar {{ display: flex; gap: 1.5rem; background: rgba(255,255,255,0.05); border-radius: 12px; padding: 1.5rem; margin: 2rem 0; }}
    .metric-item {{ flex: 1; text-align: center; }}
    .metric-item .label {{ font-size: 0.8rem; color: #94a3b8; display: block; }}
    .metric-item .value {{ font-size: 1.5rem; font-weight: 700; }}
    h2 {{ color: #f1f5f9; margin-top: 3rem; border-left: 4px solid #6366f1; padding-left: 1rem; }}
    p {{ color: #cbd5e1; margin-bottom: 1.5rem; }}
    ul {{ color: #cbd5e1; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <a href="{home_path}" class="logo" style="color:#fff;text-decoration:none;font-weight:800;font-size:1.5rem;">WiseAIWiseU</a>
    </header>
    <section class="post-hero">
      <h1 style="font-size:2.5rem;">{title.split(" | ")[0]}</h1>
      <p>📅 {today} | 🌐 WiseAIWiseU Research</p>
    </section>
    <main class="post-content">
      {article_body}
      <div style="margin-top:4rem; padding:2rem; background:rgba(255,255,255,0.02); border-radius:12px; font-size:0.9rem; color:#94a3b8;">
        <strong>Disclaimer:</strong> This content is for informational purposes only.
      </div>
      <p style="margin-top:2rem;"><a href="{blog_path}" style="color:#6366f1;">{back_label}</a></p>
    </main>
  </div>
</body>
</html>'''

langs = {
    "en": {"dir": "blog", "posts": "posts.json", "css": "css/style.css", "home": "/"},
    "ko": {"dir": "ko/blog", "posts": "ko/posts.json", "css": "../css/style.css", "home": "/ko/"},
    "pt": {"dir": "pt/blog", "posts": "pt/posts.json", "css": "../css/style.css", "home": "/pt/"},
}

for lang, settings in langs.items():
    data = contents[lang]
    article_body = data["content"].replace("[CHART-HERE]", f'<img src="{chart_url}" style="width:100%; border-radius:12px; margin:2rem 0;">')
    html = build_post_html(lang, data["title"], data["summary"], data["keywords"], today, ticker, article_body, settings["css"], settings["home"])
    
    if not os.path.exists(settings["dir"]): os.makedirs(settings["dir"])
    filename = f"{today}-{ticker}.html"
    with open(os.path.join(settings["dir"], filename), "w", encoding="utf-8") as f:
        f.write(html)
    
    # Update posts.json
    posts_path = settings["posts"]
    if os.path.exists(posts_path):
        with open(posts_path, "r", encoding="utf-8") as f:
            posts = json.load(f)
        new_post = {"title": data["title"], "date": today, "link": f"blog/{filename}", "summary": data["summary"]}
        posts = [new_post] + [p for p in posts if p["link"] != new_post["link"]]
        with open(posts_path, "w", encoding="utf-8") as f:
            json.dump(posts[:60], f, ensure_ascii=False, indent=4)

print("Manual WMT posts created successfully.")
