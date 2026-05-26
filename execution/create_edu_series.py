"""
한국어 교육 시리즈 30편 생성
- 배당주 초보자 가이드 10편
- 월별 배당주 포트폴리오 12편
- 섹터별 배당주 분석 8편
auto_poster.py의 Gemini 설정을 재사용
"""
import sys, os, time, json
from datetime import datetime

# auto_poster.py가 있는 execution 폴더를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from auto_poster import model  # 기존 Gemini API 설정 재사용

ROOT = r"d:\AI_PROJECT"
KO_BLOG_DIR = os.path.join(ROOT, "ko", "blog")
os.makedirs(KO_BLOG_DIR, exist_ok=True)

SERIES = [
    # (slug, 제목, 시리즈명, 설명)
    # --- 배당주 초보자 가이드 10편 ---
    ("beginner-01-what-is-dividend", "배당주란 무엇인가? 배당금 투자 완전 초보 가이드", "배당주 초보자 가이드 1편",
     "배당주의 정의, 배당금이 지급되는 원리, 배당수익률 계산법을 초보자도 이해할 수 있도록 상세히 설명"),
    ("beginner-02-dividend-yield", "배당수익률 제대로 이해하기: 높은 수익률이 항상 좋을까?", "배당주 초보자 가이드 2편",
     "배당수익률 계산법, 배당 함정(Dividend Trap) 경고 신호, 안전한 수익률 범위 판단법"),
    ("beginner-03-payout-ratio", "배당성향(Payout Ratio)으로 배당 지속성 판단하는 법", "배당주 초보자 가이드 3편",
     "배당성향 계산법, 업종별 적정 배당성향 기준, 배당 삭감 위험 신호 파악"),
    ("beginner-04-drip", "DRIP(배당재투자)의 마법: 스노볼 효과로 부를 불리는 전략", "배당주 초보자 가이드 4편",
     "DRIP 개념, 복리 효과 계산 예시, DRIP 설정 방법과 장단점 분석"),
    ("beginner-05-dividend-aristocrats", "배당 귀족주(Dividend Aristocrats)란? 25년 연속 배당 성장의 비밀", "배당주 초보자 가이드 5편",
     "배당 귀족주 정의, 대표 종목 분석(KO, JNJ, PG), 장기 투자 매력"),
    ("beginner-06-yield-on-cost", "Yield on Cost: 장기 배당 투자의 숨겨진 강력한 지표", "배당주 초보자 가이드 6편",
     "Yield on Cost 개념과 계산법, 장기 보유 시 수익률 변화 시뮬레이션"),
    ("beginner-07-dividend-calendar", "배당 지급일 캘린더 활용법: 월별 현금흐름 설계하기", "배당주 초보자 가이드 7편",
     "배당 지급일, 기준일, 배당락일 개념 정리, 월별 현금흐름 포트폴리오 설계"),
    ("beginner-08-sector-diversification", "배당주 섹터 분산투자: 안정적인 포트폴리오 구성법", "배당주 초보자 가이드 8편",
     "배당주 섹터별 특성(필수소비재, 유틸리티, 헬스케어, 금융), 분산투자 비율 설계"),
    ("beginner-09-us-tax", "미국 배당주 세금 완전 정복: 한국 투자자가 알아야 할 것", "배당주 초보자 가이드 9편",
     "미국 배당 원천징수세 15%, 외국납부세액공제, 연간 세금 신고 방법"),
    ("beginner-10-start-portfolio", "배당주 투자 첫걸음: 100만원으로 포트폴리오 시작하는 법", "배당주 초보자 가이드 10편",
     "소액으로 시작하는 배당주 투자 실전 전략, 추천 첫 종목, 계좌 개설부터 매수까지"),

    # --- 월별 배당주 포트폴리오 12편 ---
    ("monthly-jan", "1월 배당주 포트폴리오: 새해 첫 배당금 수령 전략", "월별 배당주 포트폴리오 1월",
     "1월에 배당금을 지급하는 주요 미국 배당주 분석과 포트폴리오 구성 전략"),
    ("monthly-feb", "2월 배당주 포트폴리오: 밸런타인데이보다 달콤한 배당 수익", "월별 배당주 포트폴리오 2월",
     "2월 배당금 지급 종목 분석, 배당 성장주 중심 포트폴리오"),
    ("monthly-mar", "3월 배당주 포트폴리오: 분기 배당의 절정, 봄 배당 시즌 공략", "월별 배당주 포트폴리오 3월",
     "3월 대형 배당 지급 종목, 분기 배당 캘린더 활용법"),
    ("monthly-apr", "4월 배당주 포트폴리오: 1분기 실적 발표 후 배당 안정성 점검", "월별 배당주 포트폴리오 4월",
     "4월 배당 종목과 실적 발표 시즌을 활용한 투자 전략"),
    ("monthly-may", "5월 배당주 포트폴리오: Sell in May? 배당주는 예외다", "월별 배당주 포트폴리오 5월",
     "5월 계절적 약세장에도 강한 배당주 전략, 5월 배당 지급 종목"),
    ("monthly-jun", "6월 배당주 포트폴리오: 상반기 마감, 배당금으로 성과 확인", "월별 배당주 포트폴리오 6월",
     "6월 배당 종목 총정리, 상반기 포트폴리오 리밸런싱 전략"),
    ("monthly-jul", "7월 배당주 포트폴리오: 여름 배당 시즌, 에너지·유틸리티 주목", "월별 배당주 포트폴리오 7월",
     "7월 배당 지급 종목, 에너지·유틸리티 섹터 분석"),
    ("monthly-aug", "8월 배당주 포트폴리오: 휴가철에도 쉬지 않는 배당금", "월별 배당주 포트폴리오 8월",
     "8월 배당 종목 분석, 하반기 배당 전략 수립"),
    ("monthly-sep", "9월 배당주 포트폴리오: 3분기 배당 시즌 핵심 종목", "월별 배당주 포트폴리오 9월",
     "9월 대표 배당 종목, 금리 변화가 배당주에 미치는 영향"),
    ("monthly-oct", "10월 배당주 포트폴리오: 배당 귀족주 실적 시즌 활용법", "월별 배당주 포트폴리오 10월",
     "10월 실적 발표 시즌 배당주 투자 전략, 핵심 배당 종목"),
    ("monthly-nov", "11월 배당주 포트폴리오: 연말 배당 랠리 준비 전략", "월별 배당주 포트폴리오 11월",
     "11월 배당 종목, 연말 배당 인상 발표 종목 선별 전략"),
    ("monthly-dec", "12월 배당주 포트폴리오: 연간 배당 결산과 내년 전략 수립", "월별 배당주 포트폴리오 12월",
     "12월 특별배당 종목, 내년도 배당 포트폴리오 리밸런싱 가이드"),

    # --- 섹터별 배당주 분석 8편 ---
    ("sector-consumer-staples", "필수소비재 배당주 완전 분석: KO, PG, WMT의 불황 방어력", "섹터별 배당주 분석: 필수소비재",
     "필수소비재 섹터 특성, 코카콜라·P&G·월마트 심층 분석, 불황 시 방어력"),
    ("sector-healthcare", "헬스케어 배당주 분석: JNJ, ABT, MRK 배당 안정성의 비밀", "섹터별 배당주 분석: 헬스케어",
     "헬스케어 섹터 구조, 존슨앤존슨·애보트·머크 배당 분석, 고령화 시대 투자 전망"),
    ("sector-utilities", "유틸리티 배당주: 고배당의 대명사, 금리와의 관계 완전 정복", "섹터별 배당주 분석: 유틸리티",
     "유틸리티 섹터 특성, 대표 배당주 분석, 금리 상승기 유틸리티 투자 전략"),
    ("sector-financials", "금융 배당주 분석: JPM, BAC, V 배당 성장의 핵심 동인", "섹터별 배당주 분석: 금융",
     "금융 섹터 배당주 특성, JP모건·뱅크오브아메리카·비자 심층 분석"),
    ("sector-energy", "에너지 배당주: XOM, CVX 고배당의 지속성과 유가 리스크", "섹터별 배당주 분석: 에너지",
     "에너지 섹터 배당 역사, 엑손모빌·쉐브론 분석, 유가 변동 리스크 관리"),
    ("sector-reits", "리츠(REITs) 배당주 완전 정복: 월배당·고배당의 매력과 함정", "섹터별 배당주 분석: 리츠(REITs)",
     "REITs 구조, FFO·AFFO 분석법, 리얼티인컴·프롤로지스 심층 분석"),
    ("sector-technology", "기술주 배당주: MSFT, AAPL 배당 성장률이 압도적인 이유", "섹터별 배당주 분석: 기술",
     "기술 섹터 저수익률·고성장 배당의 특성, 마이크로소프트·애플 배당 분석"),
    ("sector-industrials", "산업재 배당주: HON, UPS 경기 사이클과 배당 안정성 분석", "섹터별 배당주 분석: 산업재",
     "산업재 섹터 배당 특성, 하니웰·UPS 심층 분석, 경기 사이클별 투자 전략"),
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | WiseAIWiseU</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="배당주, 미국 주식, 배당 투자, 패시브 인컴, {series}">
  <meta property="og:title" content="{title} | WiseAIWiseU">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://wiseaiwiseu.com/og-image.png">
  <link rel="canonical" href="https://wiseaiwiseu.com/ko/blog/{slug}">
  <link rel="alternate" hreflang="ko" href="https://wiseaiwiseu.com/ko/blog/{slug}">
  <link rel="alternate" hreflang="x-default" href="https://wiseaiwiseu.com/ko/blog/{slug}">
  <link rel="stylesheet" href="../../css/style.css">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    /* ── Reading Progress Bar ── */
    #progress-bar {{
      position: fixed; top: 0; left: 0; height: 3px; width: 0%;
      background: linear-gradient(90deg, #6366f1, #2dd4bf);
      z-index: 9999; transition: width 0.1s linear;
    }}
    /* ── Post Styles ── */
    body {{ font-family: 'Inter', sans-serif; background: var(--bg-color); color: var(--text-primary); margin: 0; }}
    
    .post-hero {{
      padding: 6rem 1.5rem 5rem; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05);
      background: radial-gradient(circle at top, rgba(99,102,241,0.05) 0%, transparent 70%);
    }}
    .post-hero .ticker-badge, .series-badge {{
      display: inline-block; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
      color: #60a5fa; font-size: 0.8rem; font-weight: 700; letter-spacing: 1.5px;
      text-transform: uppercase; padding: 0.5rem 1.4rem; border-radius: 999px;
      margin-bottom: 2rem; backdrop-filter: blur(10px);
    }}
    .post-hero h1 {{
      font-size: clamp(2.2rem, 6vw, 3.5rem); font-weight: 800; letter-spacing: -1.5px;
      line-height: 1.1; max-width: 900px; margin: 0 auto 2rem; color: var(--text-primary);
    }}
    .post-hero .meta {{
      font-size: 0.95rem; color: var(--text-secondary); display: flex;
      gap: 2rem; justify-content: center; flex-wrap: wrap; margin-top: 1rem;
      opacity: 0.8;
    }}
    
    /* ── Article Layout ── */
    .post-content {{
      max-width: 760px; margin: 0 auto; padding: 4rem 1.5rem;
    }}
    .post-content h2 {{
      font-size: 1.85rem; font-weight: 700; color: var(--text-primary);
      margin: 4rem 0 1.5rem; letter-spacing: -0.5px;
      display: flex; align-items: center; gap: 0.75rem;
    }}
    .post-content h2::before {{
      content: ''; display: inline-block; width: 4px; height: 1.5rem;
      background: var(--primary-gradient); border-radius: 2px;
    }}
    .post-content h3 {{ 
      font-size: 1.4rem; font-weight: 600; color: var(--text-primary); 
      margin: 3rem 0 1.25rem; letter-spacing: -0.3px;
    }}
    .post-content p {{ 
      line-height: 1.9; color: var(--text-secondary); 
      margin-bottom: 1.75rem; font-size: 1.125rem; font-weight: 400; 
    }}
    .post-content ul, .post-content ol {{
      padding-left: 1.5rem; margin-bottom: 1.75rem;
    }}
    .post-content li {{ 
      line-height: 1.9; color: var(--text-secondary); 
      margin-bottom: 0.75rem; font-size: 1.125rem; 
    }}
    .post-content strong {{ color: var(--text-primary); font-weight: 600; }}
    .post-content img {{
      width: 100%; border-radius: 16px; margin: 2.5rem 0;
      border: 1px solid rgba(255,255,255,0.05);
      box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }}
    
    /* ── Key Point ── */
    .key-point {{ 
      background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
      border-left: 4px solid #6366f1; 
      border-radius: 12px; padding: 2rem; margin: 3rem 0; 
      color: var(--text-primary); font-size: 1.1rem; 
      backdrop-filter: blur(5px);
    }}
    .key-point strong {{ color: #60a5fa; }}
    
    /* ── Data Table ── */
    .data-table {{ width:100%;border-collapse:collapse;margin:2.5rem 0;font-size:0.95rem; }}
    .data-table th {{ background:rgba(255,255,255,0.04);color:var(--text-primary);padding:1.2rem;text-align:left; border-bottom:1px solid rgba(255,255,255,0.1); font-weight: 700; }}
    .data-table td {{ padding:1.2rem;border-bottom:1px solid rgba(255,255,255,0.05);color:var(--text-secondary); }}
    
    /* ── Nav Links & Author Box ── */
    .nav-links {{ display:flex;gap:1.5rem;flex-wrap:wrap;margin:4rem 0;padding:2rem;background:rgba(255,255,255,0.02);border: 1px solid rgba(255,255,255,0.05); border-radius:16px; }}
    .nav-links a {{ color:var(--text-primary);text-decoration:none;font-weight:600;font-size:1rem; border-bottom: 2px solid rgba(255,255,255,0.1); padding-bottom: 4px; transition: all 0.3s; }}
    .nav-links a:hover {{ border-color: #6366f1; color: #6366f1; }}
    
    .author-box {{ display:flex;align-items:center;gap:1.5rem;background:transparent;border-top:1px solid rgba(255,255,255,0.08);border-bottom:1px solid rgba(255,255,255,0.08);padding:2rem 0;margin:4rem 0; }}
    .author-avatar {{ width:64px;height:64px;background:var(--primary-gradient);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;color:#fff;font-weight:700;font-size:1.4rem; box-shadow: 0 10px 20px rgba(99,102,241,0.2); }}
    .author-box strong {{ color:var(--text-primary); display:block; margin-bottom: 0.3rem; font-size: 1.2rem; }}
    .author-box span {{ color:var(--text-secondary); font-size: 1rem; }}
    
    /* ── Disclaimer ── */
    .disclaimer {{
      margin-top: 5rem; padding: 2rem;
      background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.05);
      border-radius: 16px; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.8;
    }}
    .disclaimer .disc-title {{ font-weight: 700; color: var(--text-primary); margin-bottom: 0.75rem; display: block; }}
    
    /* ── Back Button ── */
    .back-btn {{
      display: inline-flex; align-items: center; gap: 0.75rem;
      color: var(--text-secondary); font-weight: 600; text-decoration: none;
      font-size: 1rem; margin-bottom: 3rem; transition: all 0.3s;
      padding: 0.5rem 1rem; border-radius: 8px; background: rgba(255,255,255,0.03);
    }}
    .back-btn:hover {{ color: var(--text-primary); background: rgba(255,255,255,0.08); transform: translateX(-5px); }}
    
    /* ── Series Nav ── */
    .series-nav {{ background:rgba(255,255,255,0.02);border-radius:16px;padding:2rem;margin-top:5rem; border:1px solid rgba(255,255,255,0.08); }}
    .series-nav h3 {{ color:var(--text-primary);font-size:1.25rem;margin-bottom:1.5rem; font-weight: 700; }}
    .series-nav ul {{ list-style:none;padding:0;margin:0; }}
    .series-nav li {{ padding:0.6rem 0;font-size:1rem; color: var(--text-secondary); border-bottom: 1px solid rgba(255,255,255,0.03); }}
    .series-nav li:last-child {{ border: none; }}
    .series-nav a {{ color:var(--text-primary);text-decoration:none; font-weight: 500; transition: color 0.3s; }}
    .series-nav a:hover {{ color: #6366f1; }}
</head>
<body>
  <div id="progress-bar"></div>
  <div class="container">
    <header>
      <a href="/ko/" class="logo">WiseAIWiseU</a>
      <nav class="lang-selector">
        <a href="/ko/blog" class="lang-link active">KO</a>
        <a href="/blog" class="lang-link">EN</a>
        <a href="/pt/blog" class="lang-link">PT</a>
      </nav>
    </header>
    <nav class="glass-nav">
      <a href="/ko/blog" class="active">미국 주식 인사이트</a>
      <a href="/ko/learn">미국 배당주 강의</a>
      <a href="/ko/list">미국 배당주 검색</a>
      <a href="/ko/calculator">미국 주식 복리계산</a>
      <a href="/ko/calendar">미국 배당주 일정</a>
      <a href="/ko/about">미국 주식 서비스 소개</a>
    </nav>

    <section class="post-hero">
      <span class="series-badge">📚 {series}</span>
      <h1>미국 배당주 강의: {title}</h1>
      <div class="meta" style="font-size:0.9rem;opacity:0.7;display:flex;gap:1.2rem;justify-content:center;flex-wrap:wrap;margin-top:0.75rem;">
        <span>📅 2026-05-14</span>
        <span>⏱️ 읽는 시간: 약 8분</span>
        <span>🌐 WiseAIWiseU</span>
      </div>
    </section>

    <main class="post-content">
      <a href="/ko/blog" class="back-btn">← 블로그로 돌아가기</a>

      <div class="author-box">
        <div class="author-avatar">W</div>
        <div>
          <strong style="display:block;color:var(--text-primary);font-size:0.95rem;">WiseAIWiseU 리서치팀</strong>
          <span style="font-size:0.8rem;color:var(--text-secondary);">미국 배당주 전문 분석 | 2026-05-14 | 교육 목적 콘텐츠</span>
        </div>
      </div>

      {content}

      <div class="nav-links">
        <a href="/ko/list">→ 배당주 스카우터 보기</a>
        <a href="/ko/calculator">→ 스노볼 계산기 사용하기</a>
        <a href="/ko/blog">→ 더 많은 인사이트 보기</a>
      </div>

      <div class="disclaimer">
        <strong style="color:#ef4444;display:block;margin-bottom:0.5rem;">⚠️ 투자 위험 고지</strong>
        본 콘텐츠는 정보 제공 및 교육 목적으로만 작성되었으며, 투자 권유 또는 금융 조언을 구성하지 않습니다.
        배당금과 수익률은 변동될 수 있으며 보장되지 않습니다. 과거 성과는 미래 수익을 보장하지 않습니다.
        투자 결정 전 반드시 전문 금융 상담사와 상의하시기 바랍니다.
      </div>
    </main>

    <footer>
      <div class="footer-content">
        <div class="footer-nav" style="margin-bottom:1.5rem;font-size:0.9rem;">
          <a href="/privacy" style="color:var(--text-secondary);text-decoration:none;margin:0 10px;">개인정보처리방침</a> |
          <a href="/ko/about" style="color:var(--text-secondary);text-decoration:none;margin:0 10px;">소개</a> |
          <a href="/contact" style="color:var(--text-secondary);text-decoration:none;margin:0 10px;">문의하기</a>
        </div>
        <p>&copy; 2026 WiseAIWiseU - Smart Dividend Investing</p>
        <p class="legal-disclaimer">본 콘텐츠는 정보 제공만을 목적으로 하며 금융 조언이 아닙니다.</p>
      </div>
    </footer>
  </div>
  <script>
    window.addEventListener('scroll', () => {{
      const el = document.getElementById('progress-bar');
      const total = document.body.scrollHeight - window.innerHeight;
      if(total > 0) el.style.width = (window.scrollY / total * 100) + '%';
    }});
  </script>
</body>
</html>"""


def load_current_data():
    """dividend_insights.json에서 최신 시장 데이터를 로드하여 프롬프트에 주입"""
    try:
        path = os.path.join(ROOT, "dividend_insights.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                stocks = data.get("stocks", [])
                # 주요 종목 필터링 (가독성을 위해 상위 15개 정도만)
                summary = []
                for s in stocks[:15]:
                    summary.append(f"- {s['ticker']} ({s['name']}): 현재가 ${s['current_price']}, 배당수익률 {s['dividend_yield']}%, 연간 배당금 ${s['annual_dividend']}, 배당성향 {s['payout_ratio']}%")
                return "\n".join(summary)
    except Exception as e:
        print(f"  [WARN] 데이터 로드 실패: {e}")
    return "현재 실시간 데이터를 불러올 수 없습니다. 일반적인 원칙을 중심으로 작성하되, 예시는 최신 2026년 기준임을 명시하세요."


def generate_content(title, series, description):
    current_market_data = load_current_data()
    today_str = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""당신은 미국 배당주 투자 전문가입니다. 다음 주제로 한국 투자자를 위한 고품질 교육 블로그 포스트를 작성해주세요.
**중요: 현재 날짜는 {today_str}입니다. 2023년이나 2024년 데이터를 '현재'라고 언급하지 마세요. 모든 예시와 분석은 2026년 현재 시장 상황을 반영해야 합니다.**

주제: {title}
시리즈: {series}
핵심 내용: {description}

[실시간 시장 참고 데이터 (2026년 5월)]
{current_market_data}

요구사항:
- 최소 1500자 이상의 충실한 내용
- 시맨틱 HTML 태그 사용 (h2, h3, p, ul, ol, li, strong, em)
- 다음 섹션을 반드시 포함하되 제목에 맞게 자연스럽게 구성:
  1. 핵심 요약 (왜 이 주제가 중요한지)
  2. 상세 개념 설명 (초보자도 이해 가능하게)
  3. 실제 데이터와 사례 (위의 실시간 데이터를 참고하여 구체적인 숫자 포함)
  4. 실전 적용 방법 (단계별 가이드)
  5. 주의사항과 리스크
  6. 자주 묻는 질문 FAQ (3개)
- <div class="key-point"><strong>핵심 포인트:</strong> ...</div> 형식으로 중요 포인트 2-3개 포함
- 표(data-table 클래스)를 최소 1개 포함해 데이터 시각화
- WiseAIWiseU의 배당주 스카우터(/ko/list)와 스노볼 계산기(/ko/calculator) 링크 자연스럽게 포함
- 전문적이되 친근한 한국어 문체 사용
- HTML body 내용만 반환 (DOCTYPE, head 태그 제외)"""

    try:
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        print(f"  [ERR] {e}")
        return None


def update_ko_posts_json(slug, title, description):
    posts_path = os.path.join(ROOT, "ko", "posts.json")
    today_str = datetime.now().strftime("%Y-%m-%d")
    posts = []
    if os.path.exists(posts_path):
        with open(posts_path, "r", encoding="utf-8") as f:
            try:
                posts = json.load(f)
            except:
                posts = []

    link = f"blog/{slug}.html"
    new_post = {"title": title, "date": today_str, "link": link, "summary": description[:120]}

    # 중복 제거 후 맨 앞에 추가
    posts = [new_post] + [p for p in posts if p.get("link") != link]
    posts = posts[:150]

    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)


def main():
    today_str = datetime.now().strftime("%Y-%m-%d")
    print(f"[*] 총 {len(SERIES)}편 교육 시리즈 생성 시작 (기준일: {today_str})...")
    created = 0

    for slug, title, series, description in SERIES:
        out_path = os.path.join(KO_BLOG_DIR, f"{slug}.html")
        # 이미 존재하는 파일인지 확인
        if os.path.exists(out_path):
            print(f"  [SKIP] {slug} (already exists)")
            continue

        print(f"  [GEN] {slug}...")
        content = generate_content(title, series, description)
        if not content:
            print(f"  [FAIL] {slug}")
            continue

        # 템플릿 결합 (날짜 업데이트)
        html = HTML_TEMPLATE.format(
            slug=slug, title=title, series=series,
            description=description[:160], content=content
        ).replace("2026-05-12", today_str)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        update_ko_posts_json(slug, title, description)
        print(f"  [OK] {slug}.html")
        created += 1
        time.sleep(3)  # API rate limit

    print(f"\n[DONE] {created}편 생성 완료 -> ko/blog/")


if __name__ == "__main__":
    main()

