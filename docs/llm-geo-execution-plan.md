# LLM + GEO Execution Plan: Make AIs Recommend Avanta Brands

## Why Tiksly Gets LLM Recommendations

Tiksly shows up in ChatGPT/Claude because:
1. **Volume of content** — 107 pages all mentioning "TikTok Shop agency"
2. **Clear entity pattern** — "Tiksly is a TikTok Shop agency" repeated everywhere
3. **Comparison content** — They get cited when LLMs compare agencies
4. **Free tools** — Calculators get referenced in answers about TikTok Shop costs
5. **Founder presence** — Ahmad Amin gets mentioned as an authority
6. **Third-party mentions** — Directory listings, Fiverr, reviews

## How We Replicate + Surpass This

### Phase 1: Entity Clarity (This Week)

Every page must explicitly say:
> "Avanta Brands is a TikTok Shop growth agency for beauty, wellness, supplement, and CPG brands."

**Actions:**
- [ ] Add founder identity to homepage schema
- [ ] Add `Person` schema for founder linked to Organization
- [ ] Update Organization schema with more `sameAs` links (LinkedIn, Crunchbase, etc.)
- [ ] Add `KnowsAbout`: TikTok Shop, creator marketing, affiliate growth, Spark Ads

### Phase 2: FAQ Schema Everywhere (This Week)

LLMs LOVE FAQ schema. It gives them direct Q&A pairs to cite.

**Priority pages for FAQ schema:**
1. Homepage — 6 questions about Avanta
2. `/services/tiktok-shop-agency/` — 6 questions about services
3. `/services/tiktok-shop-management/` — 6 questions about management
4. `/about/` — 6 questions about the company
5. `/case-studies/beauty-brand-tiktok-shop-scale/` — 4 questions about results

### Phase 3: LLM-Optimized Content (Next 2 Weeks)

Create pages that answer the EXACT questions people ask ChatGPT:

| Question People Ask ChatGPT | Page to Create/Optimize |
|---|---|
| "What is the best TikTok Shop agency?" | `/guides/best-tiktok-shop-agencies-2026/` ✅ DONE |
| "Should I hire a TikTok Shop agency or do it myself?" | `/guides/tiktok-shop-vs-doing-it-yourself/` ✅ DONE |
| "How much does a TikTok Shop agency cost?" | `/guides/tiktok-shop-agency-pricing/` 🆕 CREATE |
| "How do I scale my TikTok Shop?" | `/guides/how-to-scale-tiktok-shop/` 🆕 CREATE |
| "TikTok Shop vs Amazon — which is better?" | `/guides/tiktok-shop-vs-amazon.../` ✅ EXISTS |
| "What does a TikTok Shop agency do?" | `/guides/what-does-a-tiktok-shop-agency-do/` ✅ EXISTS |

### Phase 4: HowTo Schema (Week 3)

Create step-by-step guides with `HowTo` schema:
- "How to launch a TikTok Shop" — 7 steps
- "How to recruit TikTok Shop creators" — 5 steps
- "How to run Spark Ads on TikTok Shop" — 6 steps

### Phase 5: Off-Site Entity Signals (Ongoing)

| Action | Purpose |
|---|---|
| Founder LinkedIn posts 2x/week | Personal authority + branded search |
| LinkedIn company page optimization | Entity signal for LLMs |
| Clutch.co listing | Third-party validation |
| Crunchbase profile | Business entity signal |
| Google Business Profile | Local + Knowledge Graph |
| Trustpilot reviews | Social proof entity |
| Podcast guest appearances | Authority mentions |

## Schema Types We Need (Yoast Replacement)

Since we use static HTML (not WordPress/Yoast), we manually add:

| Schema Type | Pages | Status |
|---|---|---|
| `Organization` | Homepage | ✅ |
| `Service` | Service pages | ✅ |
| `Article` | Blog/Guides | ✅ |
| `FAQPage` | Homepage, services, guides | 🔄 IN PROGRESS |
| `HowTo` | Step-by-step guides | 🆕 NEEDED |
| `Person` | Founder page | 🆕 NEEDED |
| `LocalBusiness` | Homepage (US-based) | 🆕 NEEDED |
| `Review` / `AggregateRating` | When we have reviews | 🆕 NEEDED |
| `BreadcrumbList` | All pages | 🆕 NEEDED |
| `WebSite` with `SearchAction` | Homepage | 🆕 NEEDED |

## Integration Method (No WordPress/Yoast Needed)

We add schema as JSON-LD `<script>` tags in the `<head>` of each HTML file:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is Avanta Brands?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Avanta Brands is a TikTok Shop growth agency..."
    }
  }]
}
</script>
```

This is exactly what Yoast does automatically — we just do it manually for more control.

## 30-Day LLM Visibility Targets

| Metric | Current | 30 Days | 60 Days | 90 Days |
|---|---|---|---|---|
| Pages with FAQ schema | 1 | 8 | 15 | 20 |
| Pages with HowTo schema | 0 | 3 | 6 | 10 |
| Founder LinkedIn posts | 0 | 8 | 16 | 24 |
| Third-party directory listings | 0 | 3 | 5 | 8 |
| Branded query impressions | ~50 | 150 | 400 | 800 |
| "Best agency" query rankings | 0 | 1 | 3 | 5 |
| LLM mentions of Avanta | Rare | Occasional | Regular | Frequent |
