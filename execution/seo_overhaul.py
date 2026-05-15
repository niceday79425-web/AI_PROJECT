import os
import re

# SEO Overhaul Plan
PLAN = {
    "ko": {
        "nav": {
            "마켓 인사이트": "미국 주식 인사이트",
            "배당 아카데미": "미국 배당주 강의",
            "배당주 스카우터": "미국 배당주 검색",
            "스노볼 계산기": "미국 주식 복리계산",
            "스노우볼 시뮬레이터": "미국 주식 복리계산",
            "배당 캘린더": "미국 배당주 일정",
            "주식 궁합": "미국 주식 비교",
            "소개": "미국 주식 서비스 소개",
            "회사소개": "미국 주식 서비스 소개"
        },
        "meta": {
            "index": {
                "title": "미국 배당주 홈 | WiseAIWiseU",
                "desc": "미국 주식 및 미국 배당주 투자 분석의 시작. 실시간 배당 정보와 전문가 인사이트를 한눈에 확인하세요."
            },
            "blog": {
                "title": "미국 주식 인사이트 | WiseAIWiseU",
                "desc": "미국 주식 시장의 흐름과 미국 배당주 중심의 심층 시황 분석. 시기별 최적의 투자 전략을 제공합니다."
            },
            "learn": {
                "title": "미국 배당주 강의 | WiseAIWiseU",
                "desc": "초보자를 위한 미국 배당주 투자법부터 미국 주식 재무제표 분석까지, 체계적인 교육 콘텐츠를 제공합니다."
            },
            "list": {
                "title": "미국 배당주 검색 | WiseAIWiseU",
                "desc": "나에게 맞는 우량 미국 배당주 찾기. 시가 배당률과 성장률 등 미국 주식 종목별 맞춤 필터링 서비스."
            },
            "calculator": {
                "title": "미국 주식 복리계산 | WiseAIWiseU",
                "desc": "미국 주식 배당 재투자 시 자산 변화를 예측합니다. 미국 배당주 스노볼 효과를 시뮬레이션해 보세요."
            },
            "calendar": {
                "title": "미국 배당주 일정 | WiseAIWiseU",
                "desc": "미국 주식 배당락일 및 지급일 확인. 놓치지 말아야 할 이달의 미국 배당주 스케줄을 한눈에 제공합니다."
            },
            "fortune": {
                "title": "미국 주식 비교 | WiseAIWiseU",
                "desc": "보유한 미국 주식과 관심 있는 미국 배당주의 상관관계 분석. 최적의 분산 투자 조합을 제안합니다."
            },
            "about": {
                "title": "미국 주식 서비스 소개 | WiseAIWiseU",
                "desc": "WiseAIWiseU의 미국 주식 투자 철학과 미국 배당주 분석 원칙을 소개합니다. 스마트한 투자의 동반자가 되겠습니다."
            }
        }
    },
    "en": {
        "nav": {
            "Market Insights": "US Stock Insights",
            "Dividend Academy": "US Dividend Stock Lessons",
            "Dividend Scouter": "US Dividend Stock Search",
            "Snowball Simulator": "US Stock Compound Interest",
            "Dividend Calendar": "US Dividend Stock Schedule",
            "Payday Calendar": "US Dividend Stock Schedule",
            "Stock Match": "US Stock Comparison",
            "Stock Gung-hap": "US Stock Comparison",
            "About": "US Stock Service Intro"
        },
        "meta": {
            "index": {
                "title": "US Dividend Stocks Home | WiseAIWiseU",
                "desc": "The starting point for US stock and US dividend stock investment analysis. Check real-time dividend info and expert insights."
            },
            "blog": {
                "title": "US Stock Insights | WiseAIWiseU",
                "desc": "Market trends and in-depth analysis focused on US dividend stocks. Providing optimal investment strategies."
            },
            "learn": {
                "title": "US Dividend Stock Lessons | WiseAIWiseU",
                "desc": "Systematic educational content from US dividend stock basics to US stock financial statement analysis."
            },
            "list": {
                "title": "US Dividend Stock Search | WiseAIWiseU",
                "desc": "Find the right premium US dividend stocks. Custom filtering service for US stock metrics."
            },
            "calculator": {
                "title": "US Stock Compound Interest | WiseAIWiseU",
                "desc": "Predict asset changes when reinvesting US stock dividends. Simulate the US dividend stock snowball effect."
            },
            "calendar": {
                "title": "US Dividend Stock Schedule | WiseAIWiseU",
                "desc": "Check US stock ex-dividend and payment dates. A one-stop shop for this month's US dividend stock schedule."
            },
            "fortune": {
                "title": "US Stock Comparison | WiseAIWiseU",
                "desc": "Correlation analysis of your US stocks and interested US dividend stocks. Suggested optimal portfolio combinations."
            },
            "about": {
                "title": "US Stock Service Intro | WiseAIWiseU",
                "desc": "Introducing WiseAIWiseU's US stock investment philosophy and US dividend stock analysis principles."
            }
        }
    },
    "pt": {
        "nav": {
            "Market Insights": "Insights de Ações dos EUA",
            "Insights de Mercado": "Insights de Ações dos EUA",
            "Dividend Academy": "Aulas de Ações de Dividendos dos EUA",
            "Dividend Scouter": "Busca de Ações de Dividendos dos EUA",
            "Scouter de Dividendos": "Busca de Ações de Dividendos dos EUA",
            "Snowball Simulator": "Juros Compostos de Ações dos EUA",
            "Simulador Snowball": "Juros Compostos de Ações dos EUA",
            "Dividend Calendar": "Agenda de Ações de Dividendos dos EUA",
            "Calendário de Pagamentos": "Agenda de Ações de Dividendos dos EUA",
            "Stock Match": "Comparação de Ações dos EUA",
            "Match de Ações": "Comparação de Ações dos EUA",
            "About": "Sobre o Serviço de Ações dos EUA"
        },
        "meta": {
            "index": {
                "title": "Home de Ações de Dividendos dos EUA | WiseAIWiseU",
                "desc": "O ponto de partida para análise de investimentos em ações dos EUA e ações de dividendos dos EUA."
            },
            "blog": {
                "title": "Insights de Ações dos EUA | WiseAIWiseU",
                "desc": "Tendências de mercado e análise profunda focada em ações de dividendos dos EUA."
            },
            "learn": {
                "title": "Aulas de Ações de Dividendos dos EUA | WiseAIWiseU",
                "desc": "Conteúdo educacional sistemático, desde o básico de ações de dividendos dos EUA até análise financeira de ações dos EUA."
            },
            "list": {
                "title": "Busca de Ações de Dividendos dos EUA | WiseAIWiseU",
                "desc": "Encontre as ações de dividendos dos EUA ideais. Serviço de filtragem personalizada para métricas de ações dos EUA."
            },
            "calculator": {
                "title": "Juros Compostos de Ações dos EUA | WiseAIWiseU",
                "desc": "Preveja mudanças nos ativos ao reinvestir dividendos de ações dos EUA. Simule o efeito bola de neve."
            },
            "calendar": {
                "title": "Agenda de Ações de Dividendos dos EUA | WiseAIWiseU",
                "desc": "Verifique datas de dividendos e pagamentos de ações dos EUA."
            },
            "fortune": {
                "title": "Comparação de Ações dos EUA | WiseAIWiseU",
                "desc": "Análise de correlação de suas ações dos EUA e ações de dividendos dos EUA."
            },
            "about": {
                "title": "Sobre o Serviço de Ações dos EUA | WiseAIWiseU",
                "desc": "Apresentando a filosofia de investimento em ações dos EUA e os princípios de análise de ações de dividendos dos EUA."
            }
        }
    }
}

def process_file(filepath):
    # Determine language
    rel_path = os.path.relpath(filepath, "d:\\AI_PROJECT")
    lang = "en"
    if rel_path.startswith("ko"): lang = "ko"
    elif rel_path.startswith("pt"): lang = "pt"
    
    # Determine page type
    fname = os.path.basename(filepath)
    page_key = "other"
    if fname == "index.html": page_key = "index"
    elif "blog" in rel_path and "-" in fname: page_key = "daily_post"
    elif fname == "blog.html": page_key = "blog"
    elif fname == "learn.html": page_key = "learn"
    elif fname == "list.html": page_key = "list"
    elif fname == "calculator.html": page_key = "calculator"
    elif fname == "calendar.html": page_key = "calendar"
    elif fname == "fortune.html": page_key = "fortune"
    elif fname == "about.html": page_key = "about"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Navigation text replacement (Global)
    for old, new in PLAN[lang]["nav"].items():
        # Match navigation links: <a ...>OLD</a>
        content = re.sub(f'(<a[^>]*>){old}(</a>)', f'\\1{new}\\2', content)
        # Also match card headings in learn.html/index.html
        content = re.sub(f'(<h3>){old}(</h3>)', f'\\1{new}\\2', content)

    # 2. Meta tags for main pages
    if page_key in PLAN[lang]["meta"]:
        meta = PLAN[lang]["meta"][page_key]
        # Title
        content = re.sub(r'<title>.*?</title>', f'<title>{meta["title"]}</title>', content)
        content = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{meta["title"]}">', content)
        # Description
        content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{meta["desc"]}">', content)
        content = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{meta["desc"]}">', content)
        # Main Heading (h1)
        if page_key != "index": # Keep index hero as is or update if needed
            content = re.sub(r'(<h1[^>]*>).*?(</h1>)', f'\\1{PLAN[lang]["nav"].get(old, meta["title"].split(" | ")[0])}\\2', content, count=1)

    # 3. Handle daily posts separately if needed
    if page_key == "daily_post":
        # Just ensure navigation is updated (already done above)
        pass

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    root = "d:\\AI_PROJECT"
    target_dirs = [root, os.path.join(root, "ko"), os.path.join(root, "pt"), 
                   os.path.join(root, "blog"), os.path.join(root, "ko", "blog"), os.path.join(root, "pt", "blog")]
    
    for d in target_dirs:
        if not os.path.exists(d): continue
        for fname in os.listdir(d):
            if fname.endswith(".html"):
                fpath = os.path.join(d, fname)
                process_file(fpath)
                print(f"Processed: {fpath}")

if __name__ == "__main__":
    main()
