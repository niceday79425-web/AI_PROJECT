import re

html_ko = """                <!-- Metric Legend / Tooltip Guide -->
                <div style="display:flex; flex-wrap:wrap; gap:0.65rem; margin-bottom:1.5rem; font-size:0.8rem;">
                    <span class="tip">연간 배당금<span class="tip-icon">?</span><span class="tip-box"><strong>Annual Dividend</strong><br>가장 최근 발표된 분기 배당금을 기준으로 연간 환산한 수치(Forward Dividend)입니다.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">배당 수익률<span class="tip-icon">?</span><span class="tip-box"><strong>Dividend Yield</strong><br>목표 2~6%. 배당성향이 비정상적으로 높은 상태에서의 고배당(8% 이상)은 배당 삭감 위험(배당 함정)을 의미할 수 있습니다.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">배당성향<span class="tip-icon">?</span><span class="tip-box"><strong>Payout Ratio</strong><br>순이익 중 배당금 지급 비율. 부동산 리츠(REITs)는 회계상 이익보다 FFO(사업운영현금흐름)가 중요하며, 법적으로 90% 이상 배당해야 하므로 일반 주식보다 높게 나오는 것이 정상입니다.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">FCF 커버리지<span class="tip-icon">?</span><span class="tip-box"><strong>FCF Coverage</strong><br>잉여현금흐름 &divide; 배당지급액. 회계적 착시를 제거한 배당 지급 능력의 골드 스탠다드 지표입니다. (1.5x 이상: 안전 / 1.0x 미만: 위험)</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">연속 성장<span class="tip-icon">?</span><span class="tip-box"><strong>Growth Streak</strong><br>배당금을 삭감하거나 동결하지 않고, 매년 꾸준히 인상해 온 연속 기간입니다.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">등급<span class="tip-icon">?</span><span class="tip-box"><strong>Grade</strong><br>과거의 기록(Streak)과 현재의 재무 건전성(FCF, Payout)을 결합하여 분석한 WiseAIWiseU의 자체 평가 등급입니다.</span></span>
                </div>"""

html_en = """                <!-- Metric Legend / Tooltip Guide -->
                <div style="display:flex; flex-wrap:wrap; gap:0.65rem; margin-bottom:1.5rem; font-size:0.8rem;">
                    <span class="tip">Annual Dividend<span class="tip-icon">?</span><span class="tip-box"><strong>Forward Dividend</strong><br>Estimated annual amount per share based on the latest announced quarterly dividend.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">Dividend Yield<span class="tip-icon">?</span><span class="tip-box"><strong>Yield</strong><br>Target: 2&ndash;6%. Danger zone (&gt;8%) especially when payout ratio is abnormally high, which often indicates a Dividend Trap.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">Payout Ratio<span class="tip-icon">?</span><span class="tip-box"><strong>Payout Ratio</strong><br>Earnings paid as dividends. REITs focus on FFO instead of net income and legally must distribute &gt;90%, making higher ratios normal for them.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">FCF Cover<span class="tip-icon">?</span><span class="tip-box"><strong>FCF Coverage</strong><br>Free Cash Flow &divide; Dividends Paid. The gold standard of dividend safety, removing accounting illusions. (&gt;1.5x = Safe / &lt;1.0x = Danger)</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">Growth Streak<span class="tip-icon">?</span><span class="tip-box"><strong>Consecutive Dividend Growth</strong><br>Years the company has consecutively increased its dividend without freezing or cutting it.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">Grade<span class="tip-icon">?</span><span class="tip-box"><strong>WiseAIWiseU Grade</strong><br>Proprietary score combining past record (Streak) and current financial health (FCF, Payout).</span></span>
                </div>"""

html_pt = """                <!-- Metric Legend / Tooltip Guide -->
                <div style="display:flex; flex-wrap:wrap; gap:0.65rem; margin-bottom:1.5rem; font-size:0.8rem;">
                    <span class="tip">Dividendo Anual<span class="tip-icon">?</span><span class="tip-box"><strong>Dividendo Projetado</strong><br>Valor anual estimado com base no último dividendo trimestral anunciado.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">Rendimento<span class="tip-icon">?</span><span class="tip-box"><strong>Dividend Yield</strong><br>Meta: 2&ndash;6%. Um rendimento alto (&gt;8%) com um Payout anormalmente alto sinaliza uma Armadilha de Dividendos.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">Payout<span class="tip-icon">?</span><span class="tip-box"><strong>Payout Ratio</strong><br>Lucro pago como dividendos. Nota: REITs focam no FFO em vez do lucro líquido e devem distribuir &gt;90% por lei, tornando valores altos normais.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">Cobert. FCF<span class="tip-icon">?</span><span class="tip-box"><strong>Cobertura FCF</strong><br>Fluxo de Caixa Livre &divide; Dividendos Pagos. Padrão ouro para segurança, removendo ilusões contábeis. (&gt;1.5x = Seguro / &lt;1.0x = Perigo)</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">Crescimento<span class="tip-icon">?</span><span class="tip-box"><strong>Anos de Crescimento</strong><br>Anos consecutivos em que a empresa aumentou seus dividendos sem congelar ou cortar.</span></span>
                    <span style="color:var(--border-color)">|</span>
                    <span class="tip">Nota<span class="tip-icon">?</span><span class="tip-box"><strong>Nota (Grade)</strong><br>Nossa análise exclusiva combinando o histórico passado (Streak) e a saúde financeira atual (FCF, Payout).</span></span>
                </div>"""

files = {
    r'd:\AI_PROJECT\list.html': html_en,
    r'd:\AI_PROJECT\ko\list.html': html_ko,
    r'd:\AI_PROJECT\pt\list.html': html_pt
}

pat = re.compile(r'<!-- Metric Legend / Tooltip Guide -->.*?</div>\s*(?=<!-- Controls -->)', re.DOTALL)

for fp, new_html in files.items():
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = pat.sub(new_html + '\n\n                ', content, count=1)
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {fp}")
