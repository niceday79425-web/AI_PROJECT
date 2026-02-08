import React, { useState } from 'react';
import { Shield, TrendingUp, TrendingDown, ChevronRight, Search, Filter } from 'lucide-react';

/**
 * StockWise Mobile-Optimized Stock List Component
 * Designed by: Antigravity (Senior Frontend Developer & UI/UX Designer)
 */

const SAMPLE_DATA = [
    {
        ticker: "MSFT",
        name: "Microsoft Corp",
        sector: "Technology",
        price: 412.30,
        changePercent: 1.25,
        dividendYield: 0.89,
        aiScore: 89,
        category: "High Growth"
    },
    {
        ticker: "O",
        name: "Realty Income",
        sector: "Real Estate",
        price: 52.40,
        changePercent: -0.52,
        dividendYield: 5.60,
        aiScore: 92,
        category: "Monthly Pay"
    },
    {
        ticker: "JNJ",
        name: "Johnson & Johnson",
        sector: "Healthcare",
        price: 158.20,
        changePercent: 0.15,
        dividendYield: 3.02,
        aiScore: 85,
        category: "Dividend Kings"
    },
    {
        ticker: "AAPL",
        name: "Apple Inc.",
        sector: "Technology",
        price: 189.45,
        changePercent: 2.10,
        dividendYield: 0.52,
        aiScore: 82,
        category: "High Growth"
    },
    {
        ticker: "MO",
        name: "Altria Group",
        sector: "Consumer Defensive",
        price: 42.15,
        changePercent: -1.20,
        dividendYield: 8.90,
        aiScore: 78,
        category: "High Yield"
    },
    {
        ticker: "MAIN",
        name: "Main Street Capital",
        sector: "Financials",
        price: 45.30,
        changePercent: 0.45,
        dividendYield: 6.20,
        aiScore: 94,
        category: "Monthly Pay"
    }
];

const CATEGORIES = [
    "전체 (All)",
    "배당킹 (Dividend Kings)",
    "고성장 (High Growth)",
    "월배당 (Monthly Pay)",
    "고배당 (High Yield)"
];

const StockCard = ({ stock }) => {
    const isUp = stock.changePercent >= 0;

    // Korean Finance Standard: Red for UP, Blue for DOWN
    const priceColorClass = isUp ? 'text-red-500' : 'text-blue-500';
    const priceBgClass = isUp ? 'bg-red-500/10' : 'bg-blue-500/10';
    const Icon = isUp ? TrendingUp : TrendingDown;

    return (
        <div className="group relative bg-[#0a0a0a] border-b border-zinc-800/50 p-4 active:bg-zinc-900 transition-colors duration-200">
            {/* First Row: Ticker & Price */}
            <div className="flex justify-between items-end mb-1">
                <div className="flex items-center gap-2">
                    <span className="text-xl font-black tracking-tighter text-white group-hover:text-mint-400 transition-colors">
                        {stock.ticker}
                    </span>
                </div>
                <div className="text-right">
                    <div className={`flex items-center justify-end gap-1 font-bold ${priceColorClass}`}>
                        <span className="text-lg">${stock.price.toFixed(2)}</span>
                        <Icon size={14} />
                    </div>
                </div>
            </div>

            {/* Second Row: Info & Stats */}
            <div className="flex justify-between items-center">
                <div className="flex flex-col">
                    <div className="flex items-center gap-2">
                        <span className="text-xs text-zinc-500 font-medium truncate max-w-[120px]">
                            {stock.name}
                        </span>
                        <span className="px-1.5 py-0.5 rounded bg-zinc-800/50 text-[10px] text-zinc-400 font-semibold uppercase tracking-wider">
                            {stock.sector}
                        </span>
                    </div>
                </div>

                <div className="flex items-center gap-3">
                    {/* Real Yield - Highlighted in Mint/Green */}
                    <div className="flex flex-col items-end">
                        <span className="text-[10px] text-zinc-500 font-bold uppercase tracking-widest leading-none mb-1">Yield</span>
                        <span className="text-sm font-bold text-[#10B981] drop-shadow-[0_0_8px_rgba(16,185,129,0.3)]">
                            {stock.dividendYield.toFixed(2)}%
                        </span>
                    </div>

                    {/* AI Score Badge - Shield Icon or Badge */}
                    <div className="flex items-center bg-gradient-to-br from-zinc-800 to-zinc-900 border border-zinc-700/50 rounded-lg px-2 py-1 gap-1.5 shadow-lg">
                        <Shield size={12} className="text-amber-400 fill-amber-400/20" />
                        <span className="text-xs font-black text-zinc-100 italic">
                            {stock.aiScore}
                        </span>
                    </div>

                    <ChevronRight size={16} className="text-zinc-700 group-hover:text-zinc-500 transition-colors" />
                </div>
            </div>

            {/* Progress Bar for AI Score (Subtle visual aid) */}
            <div className="absolute bottom-0 left-0 h-[2px] bg-gradient-to-r from-transparent via-mint-500/30 to-transparent w-full opacity-0 group-hover:opacity-100 transition-opacity" />
        </div>
    );
};

const DividendScouter = () => {
    const [activeTab, setActiveTab] = useState("전체 (All)");
    const [searchQuery, setSearchQuery] = useState("");

    const filteredData = SAMPLE_DATA.filter(stock => {
        const matchesTab = activeTab === "전체 (All)" ||
            activeTab.includes(stock.category);
        const matchesSearch = stock.ticker.toLowerCase().includes(searchQuery.toLowerCase()) ||
            stock.name.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesTab && matchesSearch;
    });

    return (
        <div className="min-h-screen bg-black text-white font-sans selection:bg-mint-500selection:text-black">
            {/* Header Section */}
            <div className="sticky top-0 z-20 bg-black/80 backdrop-blur-xl border-b border-zinc-800/50 px-4 py-4">
                <div className="flex justify-between items-center mb-4">
                    <h1 className="text-2xl font-black italic tracking-tighter bg-gradient-to-r from-white to-zinc-500 bg-clip-text text-transparent">
                        STOCKWISE<span className="text-[#10B981]">.ai</span>
                    </h1>
                    <div className="p-2 border border-zinc-800 rounded-full hover:bg-zinc-900 transition-colors">
                        <Filter size={18} className="text-zinc-400" />
                    </div>
                </div>

                {/* Search Input */}
                <div className="relative mb-6">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" size={16} />
                    <input
                        type="text"
                        placeholder="Search stocks..."
                        className="w-full bg-zinc-900/50 border border-zinc-800 rounded-xl py-2.5 pl-10 pr-4 text-sm focus:outline-none focus:border-mint-500/50 focus:ring-1 focus:ring-mint-500/20 transition-all"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </div>

                {/* Horizontal Category Tabs */}
                <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-none no-scrollbar">
                    {CATEGORIES.map((tab) => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            className={`whitespace-nowrap px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 ${activeTab === tab
                                    ? 'bg-white text-black shadow-[0_0_15px_rgba(255,255,255,0.2)]'
                                    : 'bg-zinc-900 text-zinc-400 hover:text-zinc-200 border border-zinc-800'
                                }`}
                        >
                            {tab.split(' (')[0]}
                        </button>
                    ))}
                </div>
            </div>

            {/* Stock List Content */}
            <div className="flex flex-col">
                {filteredData.length > 0 ? (
                    filteredData.map((stock) => (
                        <StockCard key={stock.ticker} stock={stock} />
                    ))
                ) : (
                    <div className="flex flex-col items-center justify-center py-20 text-zinc-600">
                        <Search size={48} className="mb-4 opacity-20" />
                        <p className="text-sm font-medium">No results found for your search.</p>
                    </div>
                )}
            </div>

            {/* Footer Info */}
            <div className="p-6 text-center">
                <p className="text-[10px] text-zinc-600 font-bold uppercase tracking-[0.2em]">
                    Powered by StockWise Proprietary Intelligence
                </p>
            </div>

            {/* Subtle Bottom Navigation Indicator (Mobile) */}
            <div className="fixed bottom-1 left-1/2 -translate-x-1/2 w-12 h-1 bg-zinc-800 rounded-full" />
        </div>
    );
};

export default DividendScouter;
