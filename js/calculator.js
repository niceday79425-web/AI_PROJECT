document.addEventListener('DOMContentLoaded', () => {
    const calculateBtn = document.getElementById('calculateBtn');
    const blogGrid = document.getElementById('blogGrid');
    let growthChart = null;

    // 1. 계산 로직
    const calculateGrowth = () => {
        const principal = parseFloat(document.getElementById('initialPrincipal').value) || 0;
        const monthlyDeposit = parseFloat(document.getElementById('monthlyDeposit').value) || 0;
        const yieldRate = (parseFloat(document.getElementById('dividendYield').value) || 0) / 100;
        const growthRate = (parseFloat(document.getElementById('stockGrowth').value) || 0) / 100;
        const years = parseInt(document.getElementById('duration').value) || 0;

        const months = years * 12;
        let currentTotal = principal;
        let totalPrincipal = principal;
        let totalDividends = 0;
        let capitalGains = 0;

        const labels = [];
        const principalData = [];
        const growthData = [];
        const dividendData = [];

        for (let m = 1; m <= months; m++) {
            // 월초 적립
            currentTotal += monthlyDeposit;
            totalPrincipal += monthlyDeposit;

            // 주가 상승분 (월 복리 가정)
            const monthlyGrowth = currentTotal * (Math.pow(1 + growthRate, 1/12) - 1);
            capitalGains += monthlyGrowth;
            currentTotal += monthlyGrowth;

            // 배당금 발생 (세금 15% 제외 및 재투자)
            const monthlyDiv = currentTotal * (yieldRate / 12) * 0.85;
            totalDividends += monthlyDiv;
            currentTotal += monthlyDiv;

            // 1년 단위로 차트 데이터 기록
            if (m % 12 === 0) {
                labels.push(`${m / 12}년`);
                principalData.push(Math.round(totalPrincipal));
                growthData.push(Math.round(capitalGains));
                dividendData.push(Math.round(totalDividends));
            }
        }

        updateUI(currentTotal, totalDividends, totalPrincipal);
        updateChart(labels, principalData, growthData, dividendData);
    };

    // 2. UI 업데이트
    const updateUI = (total, dividends, principal) => {
        const roi = ((total - principal) / principal * 100).toFixed(1);
        document.getElementById('finalAsset').textContent = `$${Math.round(total).toLocaleString()}`;
        document.getElementById('totalDividends').textContent = `$${Math.round(dividends).toLocaleString()}`;
        document.getElementById('totalROI').textContent = `${roi}%`;
    };

    // 3. Chart.js 업데이트
    const updateChart = (labels, principal, growth, dividends) => {
        const ctx = document.getElementById('growthChart').getContext('2d');
        
        if (growthChart) {
            growthChart.destroy();
        }

        growthChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: '원금',
                        data: principal,
                        backgroundColor: '#6366f1',
                        borderRadius: 4
                    },
                    {
                        label: '주가 수익',
                        data: growth,
                        backgroundColor: '#3b82f6',
                        borderRadius: 4
                    },
                    {
                        label: '배당 수익',
                        data: dividends,
                        backgroundColor: '#2dd4bf',
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { stacked: true, grid: { display: false }, ticks: { color: '#94a3b8' } },
                    y: { 
                        stacked: true, 
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { 
                            color: '#94a3b8',
                            callback: (value) => '$' + value.toLocaleString()
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#f8fafc', padding: 20, usePointStyle: true }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: (context) => `${context.dataset.label}: $${context.raw.toLocaleString()}`
                        }
                    }
                }
            }
        });
    };

    // 4. 블로그 데이터 로드
    const loadBlogPosts = async () => {
        try {
            const response = await fetch('posts.json');
            if (!response.ok) throw new Error('No posts found');
            const posts = await response.json();
            
            blogGrid.innerHTML = '';
            posts.forEach(post => {
                const card = document.createElement('div');
                card.className = 'blog-card';
                card.innerHTML = `
                    <span class="blog-date">${post.date}</span>
                    <h3>${post.title}</h3>
                    <p>${post.summary}</p>
                `;
                card.onclick = () => window.location.href = post.link;
                blogGrid.appendChild(card);
            });
        } catch (error) {
            console.log('Blog loading failed:', error);
            blogGrid.innerHTML = '<p style="color: var(--text-secondary)">아직 게시된 포스트가 없습니다.</p>';
        }
    };

    // 초기 실행
    calculateBtn.addEventListener('click', calculateGrowth);
    calculateGrowth();
    loadBlogPosts();
});
