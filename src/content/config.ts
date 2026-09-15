import { defineCollection, z } from 'astro:content';

// 1. Insight Collection (AI 주식 분석 파이프라인 수용)
const insightCollection = defineCollection({
  type: 'content',
  schema: z.object({
    id: z.string(),
    type: z.literal('insight'),
    date: z.coerce.date(),
    tickers: z.array(z.string()),
    generated_by: z.string(),
    reviewed_by: z.string(),
    human_approved: z.boolean(),
    scoring: z.object({
      d30: z.string().default('pending'),
      d90: z.string().default('pending'),
    }),
  }),
});

// 2. Learn Collection (강의 콘텐츠)
const learnCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    track: z.enum([
      'track-1-basics',
      'track-2-agents',
      'track-3-building',
      'track-4-automation',
      'track-5-dividend'
    ]),
    order: z.number().int().min(1).max(10),
    readingTime: z.string(),
    learnings: z.array(z.string()).length(3), // "이 강에서 배우는 것" 3줄 엄격 제한
    relatedWorks: z.string().optional(),
    relatedHow: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

// 3. How Collection (제작 과정 8단계 템플릿)
const howCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    workSlug: z.string(),
    models: z.array(z.string()),
    tools: z.array(z.string()),
    timeSpent: z.string(),
    costs: z.object({
      api: z.number().default(0),
      subscription: z.number().default(0),
      domains: z.number().default(0),
      total: z.number(),
    }),
    resultsSlug: z.string().optional(),
  }),
});

// 4. Results Collection (월별 결산 및 검증)
const resultsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    period: z.string(), // YYYY-MM
    revenue: z.number(),
    expenses: z.number(),
    netProfit: z.number(),
  }),
});

// 5. Failures Collection (실패/폐기 기록)
const failuresCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    reason: z.string(),
    relatedWork: z.string().optional(),
  }),
});

export const collections = {
  insight: insightCollection,
  learn: learnCollection,
  how: howCollection,
  results: resultsCollection,
  failures: failuresCollection,
};
