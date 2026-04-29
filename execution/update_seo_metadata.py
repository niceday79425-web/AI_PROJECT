import os
import re

root = r'd:\AI_PROJECT'

UPDATES = {
    'ko/index.html': {
        'title': '미국 주식 배당 투자 & 스노우볼 복리 계산기 | WiseAIWiseU',
        'description': '미국 우량 배당주 분석과 스노우볼 복리 계산기로 경제적 자유를 시뮬레이션하세요. 미국 주식 포트폴리오의 복리 효과를 극대화하는 투자 전략과 데이터를 제공합니다.',
        'og_title': '미국 주식 배당 투자 & 스노우볼 복리 계산기 | WiseAIWiseU',
        'og_description': '미국 우량 배당주 분석과 스노우볼 복리 계산기로 경제적 자유를 시뮬레이션하세요. 미국 주식 포트폴리오의 복리 효과를 극대화하는 투자 전략과 데이터를 제공합니다.',
        'keywords': '미국 주식, 배당주 투자, 복리 계산기, 경제적 자유, 스노우볼 효과, 해외 주식',
    },
    'index.html': {
        'title': 'US Dividend Stocks & Snowball Compound Interest Calculator | WiseAIWiseU',
        'description': 'Master US stock investing with our advanced dividend analysis and compound interest tools. Simulate your path to financial freedom with real-time US market data and snowball effects.',
        'og_title': 'US Dividend Stocks & Snowball Compound Interest Calculator | WiseAIWiseU',
        'og_description': 'Master US stock investing with our advanced dividend analysis and compound interest tools. Simulate your path to financial freedom with real-time US market data and snowball effects.',
        'keywords': 'US stocks, dividend investing, compound interest calculator, DRIP, financial freedom',
    },
    'pt/index.html': {
        'title': 'Investimento em Ações dos EUA e Calculadora de Juros Compostos | WiseAIWiseU',
        'description': 'Analise as melhores ações de dividendos dos EUA e simule seu crescimento com nossa calculadora de juros compostos. O guia completo para investir no mercado americano.',
        'og_title': 'Investimento em Ações dos EUA e Calculadora de Juros Compostos | WiseAIWiseU',
        'og_description': 'Analise as melhores ações de dividendos dos EUA e simule seu crescimento com nossa calculadora de juros compostos. O guia completo para investir no mercado americano.',
        'keywords': 'ações dos EUA, dividendos, juros compostos, investimento no exterior',
    },
    'ko/calculator.html': {
        'title': '미국 주식 복리 계산기: 배당 재투자(DRIP) 수익 시뮬레이션 | WiseAIWiseU',
        'description': '미국 주식 투자 20년 뒤 내 자산은 얼마일까? 배당 성장을 반영한 정밀 복리 계산기로 스노우볼 효과를 즉시 확인하세요. 로그인 없이 사용 가능한 무료 시뮬레이터입니다.',
        'og_title': '미국 주식 복리 계산기: 배당 재투자(DRIP) 수익 시뮬레이션 | WiseAIWiseU',
        'og_description': '미국 주식 투자 20년 뒤 내 자산은 얼마일까? 배당 성장을 반영한 정밀 복리 계산기로 스노우볼 효과를 즉시 확인하세요. 로그인 없이 사용 가능한 무료 시뮬레이터입니다.',
        'keywords': '미국 주식 계산기, 배당 재투자, DRIP 계산기, 복리 효과, 주식 시뮬레이션',
    },
    'calculator.html': {
        'title': 'US Stock Compound Interest Calculator: DRIP & Growth Simulator | WiseAIWiseU',
        'description': 'Calculate your future wealth with our US stock compound interest simulator. Reflects dividend growth and DRIP reinvestment for long-term US stock investors. Free to use.',
        'og_title': 'US Stock Compound Interest Calculator: DRIP & Growth Simulator | WiseAIWiseU',
        'og_description': 'Calculate your future wealth with our US stock compound interest simulator. Reflects dividend growth and DRIP reinvestment for long-term US stock investors. Free to use.',
        'keywords': 'US stock calculator, dividend growth, DRIP simulator, snowball effect, compounding',
    },
    'ko/list.html': {
        'title': '미국 배당주 등급표: S/A/B/C 우량주 안전성 순위 | WiseAIWiseU',
        'description': '6,000개 이상의 미국 주식을 데이터로 분석해 배당 수익률과 안전성을 등급화했습니다. 미국 주식 시장의 숨은 보석 같은 우량주를 실시간 데이터로 확인하세요.',
        'og_title': '미국 배당주 등급표: S/A/B/C 우량주 안전성 순위 | WiseAIWiseU',
        'og_description': '6,000개 이상의 미국 주식을 데이터로 분석해 배당 수익률과 안전성을 등급화했습니다. 미국 주식 시장의 숨은 보석 같은 우량주를 실시간 데이터로 확인하세요.',
        'keywords': '미국 배당주 순위, 우량주 등급표, 미국 주식 추천, 배당 안전성, 고배당주',
    },
    'list.html': {
        'title': 'Top US Dividend Stocks Ranked: S/A/B/C Grade Analysis | WiseAIWiseU',
        'description': 'Find the safest US dividend stocks with our proprietary grading system. Filter 6,000+ US stocks by yield, growth, and safety score. Updated regularly for serious investors.',
        'og_title': 'Top US Dividend Stocks Ranked: S/A/B/C Grade Analysis | WiseAIWiseU',
        'og_description': 'Find the safest US dividend stocks with our proprietary grading system. Filter 6,000+ US stocks by yield, growth, and safety score. Updated regularly for serious investors.',
        'keywords': 'best US dividend stocks, dividend ranking, stock grades, safe dividends, dividend yield',
    },
    'ko/calendar.html': {
        'title': '2026 미국 주식 배당 캘린더: 지급일 및 배당락일 확인 | WiseAIWiseU',
        'description': '내가 투자한 미국 주식 배당금은 언제 들어올까? 실시간 업데이트되는 배당 캘린더로 미국 주식의 지급일과 배당락일을 놓치지 마세요. 월배당 포트폴리오의 필수 도구입니다.',
        'og_title': '2026 미국 주식 배당 캘린더: 지급일 및 배당락일 확인 | WiseAIWiseU',
        'og_description': '내가 투자한 미국 주식 배당금은 언제 들어올까? 실시간 업데이트되는 배당 캘린더로 미국 주식의 지급일과 배당락일을 놓치지 마세요. 월배당 포트폴리오의 필수 도구입니다.',
        'keywords': '미국 주식 배당금 지급일, 배당락일, 배당 달력, 월배당 포트폴리오, 주식 일정',
    },
    'calendar.html': {
        'title': 'US Stock Dividend Calendar 2026: Ex-Dividend & Pay Dates | WiseAIWiseU',
        'description': 'Track every upcoming US stock dividend payment. Get ex-dividend dates and build a monthly income portfolio with our interactive US dividend calendar.',
        'og_title': 'US Stock Dividend Calendar 2026: Ex-Dividend & Pay Dates | WiseAIWiseU',
        'og_description': 'Track every upcoming US stock dividend payment. Get ex-dividend dates and build a monthly income portfolio with our interactive US dividend calendar.',
        'keywords': 'US dividend calendar, payment dates, ex-dividend date, monthly income, dividend tracking',
    },
    'ko/fortune.html': {
        'title': '미국 주식 궁합 테스트: 나의 투자 MBTI와 종목 매칭 | WiseAIWiseU',
        'description': '재미로 보는 미국 주식 궁합! 내 이름과 티커를 입력해 투자 성향을 확인하고, 뇌동매매를 피하고 멘탈을 지키는 미국 주식 투자법을 알아보세요.',
        'og_title': '미국 주식 궁합 테스트: 나의 투자 MBTI와 종목 매칭 | WiseAIWiseU',
        'og_description': '재미로 보는 미국 주식 궁합! 내 이름과 티커를 입력해 투자 성향을 확인하고, 뇌동매매를 피하고 멘탈을 지키는 미국 주식 투자법을 알아보세요.',
        'keywords': '미국 주식 궁합, 투자 MBTI, 주식 운세, 배당주 투자 멘탈, 주식 재미',
    },
}

def upsert_meta(content, name_attr, name_val, content_val):
    """Update existing meta tag or insert after <title> if missing."""
    # Try to match existing tag
    if name_attr == 'property':
        pattern = rf'<meta\s+property="{re.escape(name_val)}"\s+content=".*?"\s*/?>|<meta\s+content=".*?"\s+property="{re.escape(name_val)}"\s*/?>'
        replacement = f'<meta property="{name_val}" content="{content_val}">'
    else:
        pattern = rf'<meta\s+name="{re.escape(name_val)}"\s+content=".*?"\s*/?>|<meta\s+content=".*?"\s+name="{re.escape(name_val)}"\s*/?>'
        replacement = f'<meta name="{name_val}" content="{content_val}">'

    new_content, count = re.subn(pattern, replacement, content, flags=re.I | re.S)
    if count == 0:
        # Insert after </title>
        new_content = re.sub(
            r'(</title>)',
            rf'\1\n    {replacement}',
            content,
            count=1,
            flags=re.I
        )
    return new_content


def process(rel_path, data):
    filepath = os.path.join(root, rel_path)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update <title>
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{data["title"]}</title>',
        content, count=1, flags=re.I | re.S
    )

    content = upsert_meta(content, 'name', 'description', data['description'])
    content = upsert_meta(content, 'property', 'og:title', data['og_title'])
    content = upsert_meta(content, 'property', 'og:description', data['og_description'])

    if data.get('keywords'):
        content = upsert_meta(content, 'name', 'keywords', data['keywords'])

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] {rel_path}")


for rel_path, data in UPDATES.items():
    process(rel_path, data)

print(f"\nDone — {len(UPDATES)} files updated.")
