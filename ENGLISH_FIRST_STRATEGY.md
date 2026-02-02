# English-First Content Generation Strategy

## Overview
This project now prioritizes **English content generation** as the primary language, with Korean and Portuguese as translations stored in language-specific subdirectories.

## Directory Structure

```
AI_PROJECT/
├── blog/                    # English blog posts (PRIMARY)
├── posts.json              # English post index (PRIMARY)
├── index.html              # English homepage (PRIMARY)
├── ko/                     # Korean translations
│   ├── blog/
│   └── posts.json
└── pt/                     # Portuguese translations
    ├── blog/
    └── posts.json
```

## Content Generation Flow

### 1. **English First (Primary)**
- All content is generated in **professional, SEO-optimized English**
- Target audience: US stock market investors
- Saved to root directory: `blog/`, `posts.json`

### 2. **Korean Translation**
- Korean version is a translation of English content
- Saved to: `ko/blog/`, `ko/posts.json`

### 3. **Portuguese Translation**
- Portuguese version is a translation of English content
- Saved to: `pt/blog/`, `pt/posts.json`

## Key Changes in `auto_poster.py`

### Updated Prompt Strategy
```python
IMPORTANT: English is the PRIMARY language. 
This is a US stock market blog targeting English-speaking investors.
Korean (ko) and Portuguese (pt) are TRANSLATIONS for international readers.

Generate content in 3 languages with this priority:
1. English (en) - Primary, professional, insightful, SEO-optimized
2. Korean (ko) - Translation of English content
3. Portuguese (pt) - Translation of English content
```

### Directory Configuration
```python
langs = {
    "en": {"dir": "blog", "posts": "posts.json", "prefix": ""},
    "ko": {"dir": "ko/blog", "posts": "ko/posts.json", "prefix": "ko/"},
    "pt": {"dir": "pt/blog", "posts": "pt/posts.json", "prefix": "pt/"}
}
```

## Benefits

1. **SEO Optimization**: English content targets the largest market (US investors)
2. **Clear Hierarchy**: English is clearly the primary language, not just one of three
3. **Better AI Generation**: AI models perform better when given clear priority instructions
4. **Scalability**: Easy to add more translation languages in the future
5. **Professional Tone**: English content is optimized for professional US stock market analysis

## Usage

Run the auto poster to generate content:
```bash
python execution/auto_poster.py
```

This will:
1. Analyze top volatile stocks
2. Generate professional English content
3. Create Korean and Portuguese translations
4. Save to appropriate directories
5. Update all language-specific `posts.json` files

## Next Steps

- Ensure all HTML pages (index.html, blog.html, etc.) exist in root directory in English
- Update language detection to redirect non-English browsers to `/ko/` or `/pt/`
- Maintain English as the canonical version for SEO purposes
