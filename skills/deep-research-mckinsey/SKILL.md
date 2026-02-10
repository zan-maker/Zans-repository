---
name: deep-research-mckinsey
description: McKinsey-style institutional-grade market research for portfolio managers. Use when conducting comprehensive industry analysis, competitive landscape assessment, investment thesis development, or strategic market intelligence across any sector or geography. Triggers on requests for deep-dive research, industry reports, market analysis, competitive intelligence, Porter Five Forces, TAM/SAM/SOM analysis, or institutional investment research.
---

# Deep Research: McKinsey-Style Institutional Analysis

Conduct comprehensive, institutional-grade market research suitable for portfolio managers and buy-side analysts. This skill produces McKinsey-quality deep-dives with rigorous analysis, data-backed insights, and actionable investment theses.

## When to Use This Skill

Use for any request involving:
- Industry deep-dives and sector analysis
- Market sizing (TAM/SAM/SOM) and growth forecasting
- Competitive landscape and market share analysis
- Investment thesis development
- Porter Five Forces analysis
- M&A and private equity activity tracking
- Technology and innovation trend assessment
- Regulatory and ESG risk analysis
- Regional market comparisons
- Risk matrix construction

## Model Compatibility

This skill works with any capable LLM:
- **GLM-4.7 (Z.AI)**: Recommended for complex multi-section reports (203K context)
- **Kimi K2.5 (Moonshot)**: Excellent for comprehensive analysis (256K context)
- **GPT-4/Claude**: Use if available and appropriate
- **Other models**: Adjust output length based on context window

**Selection guidance:**
- Use GLM-4.7 for reports requiring 7,000+ words or complex quantitative analysis
- Use Kimi 2.5 for standard 5,000-7,000 word reports
- For shorter summaries (<3,000 words), any capable model works

## Required Parameters

Before starting, confirm these variables (use defaults if not specified):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `{{INDUSTRY}}` | (Required) | Target industry or sector |
| `{{REGION}}` | Global | Geographic focus (NA, EU, APAC, Global) |
| `{{TIME_HORIZON}}` | 2024-2030 | Forecast period |
| `{{CURRENCY}}` | USD | Reporting currency |
| `{{DATE}}` | Current date | Report date |

## Research Workflow

### Phase 1: Silent Planning (Internal Only)

Before writing, create a bullet-point outline covering:
- Industry definition and scope boundaries
- Key sub-segments to analyze
- Data sources needed (filings, trade groups, government data)
- Top 10 companies to profile
- Regional markets to compare
- Risk factors to investigate
- Investment thesis angles to explore

**Do not share this outline** - it's for your planning only.

### Phase 2: Web Research (Iterative)

Conduct web searches until confident data coverage exceeds 90%:

1. **Start broad**: "[INDUSTRY] market size 2024 TAM growth forecast"
2. **Company financials**: "[Company] annual report 2024 revenue"
3. **Competitive landscape**: "[INDUSTRY] market share leaders 2024"
4. **M&A activity**: "[INDUSTRY] acquisitions 2024 private equity"
5. **Regulatory**: "[INDUSTRY] regulations 2024 policy changes"
6. **Technology trends**: "[INDUSTRY] innovation R&D trends 2024"
7. **Regional data**: "[INDUSTRY] market China Europe North America"
8. **ESG factors**: "[INDUSTRY] carbon footprint sustainability ESG"

**Stop when:** You can answer 90%+ of the section requirements with specific data points.

### Phase 3: Structured Drafting

Write each section in order. Insert tables immediately after the paragraph that introduces them. Keep paragraphs under 120 words.

## Report Structure (13 Sections)

### 1. Executive Summary (400-600 words)

**Components:**
- Opening hook: One compelling market dynamic
- 3-5 bullet highlights with specific metrics
- One-sentence bottom line investment thesis
- Key charts/tables referenced

**Template:**
```
The [INDUSTRY] sector is experiencing [primary trend], with the total addressable 
market reaching $[X] billion in 2024 and projected to grow at [X]% CAGR through 2030. 
[One key insight about competitive dynamics or structural change].

**Key Highlights:**
• Market size: $[X]B TAM (2024), growing to $[X]B by 2030 ([X]% CAGR)
• Top 3 players control [X]% market share, [consolidated/fragmented] landscape
• [Key macro driver] driving [X]% of growth; [inhibitor] constraining [region]
• M&A activity: $[X]B in [year], with [private equity/strategic] buyers dominant
• Primary risk: [risk factor] (likelihood: [High/Medium/Low], impact: [High/Medium/Low])

**Bottom Line:** [Single sentence investment thesis with expected return horizon].
```

### 2. Industry Definition and Segmentation (500-700 words)

**Components:**
- Scope definition (what's in/out)
- Value chain stages (upstream → downstream)
- Key sub-segments with size breakdown
- End-market exposure matrix

**Required Table:**
| Segment | 2024 Revenue ($B) | % of Total | Key Products/Services | Growth Rate |
|---------|-------------------|------------|----------------------|-------------|
| [Segment 1] | $X | X% | [Description] | X% |
| [Segment 2] | $X | X% | [Description] | X% |

### 3. Market Size and Growth Outlook (700-900 words)

**Components:**
- TAM calculation methodology
- Historical CAGR (5-year lookback)
- 5-year forecast with two scenarios (Base/Optimistic or Base/Bear)
- Growth drivers (demand-side and supply-side)
- Growth inhibitors and headwinds

**Required Tables:**

*Market Size Trajectory:*
| Year | TAM ($B) | Growth Rate | Key Driver |
|------|----------|-------------|------------|
| 2020 | $X | X% | |
| 2024 | $X | X% | |
| 2030E | $X | X% | [Primary driver] |

*Scenario Analysis:*
| Scenario | 2030 TAM ($B) | CAGR | Assumptions |
|----------|---------------|------|-------------|
| Base Case | $X | X% | |
| Bull Case | $X | X% | |
| Bear Case | $X | X% | |

### 4. Macro Context (500-600 words)

**Components:**
- GDP correlation and cyclicality
- Interest rate sensitivity
- Demographic trends
- Policy and regulatory tailwinds/headwinds
- Trade and supply chain factors

### 5. Competitive Landscape (700-900 words)

**Components:**
- Top 10 companies with revenue and market share
- Recent M&A transactions (last 24 months)
- Private equity activity
- Market concentration trends

**Required Table:**
| Rank | Company | Ticker | 2024 Revenue ($B) | Market Share | YoY Growth | Region |
|------|---------|--------|-------------------|--------------|------------|--------|
| 1 | [Name] | [TKR] | $X | X% | X% | [HQ] |
| 2 | [Name] | [TKR] | $X | X% | X% | [HQ] |
| ... | ... | ... | ... | ... | ... | ... |

*Recent M&A Activity:*
| Date | Target | Acquirer | Deal Value ($M) | Rationale |
|------|--------|----------|-----------------|-----------|
| [Date] | [Company] | [Buyer] | $X | [Strategic logic] |

### 6. Porter Five Forces Analysis (400-500 words)

Rate each force: **Low** | **Medium** | **High**

| Force | Rating | Evidence |
|-------|--------|----------|
| Threat of New Entrants | [Rating] | [2-3 sentences] |
| Bargaining Power of Suppliers | [Rating] | [2-3 sentences] |
| Bargaining Power of Buyers | [Rating] | [2-3 sentences] |
| Threat of Substitutes | [Rating] | [2-3 sentences] |
| Competitive Rivalry | [Rating] | [2-3 sentences] |

**Overall Industry Attractiveness:** [Score 1-5] / 5

### 7. Cost Structure and Economics (400-500 words)

**Components:**
- Typical gross margin range
- Operating margin benchmarks
- Capex intensity (capex/revenue)
- Working capital cycle (cash conversion)
- Key cost drivers

**Required Table:**
| Metric | Industry Average | Top Quartile | Bottom Quartile |
|--------|-----------------|--------------|-----------------|
| Gross Margin | X% | X% | X% |
| EBITDA Margin | X% | X% | X% |
| Capex/Revenue | X% | X% | X% |
| Working Capital Days | X | X | X |

### 8. Technology and Innovation Trends (500-600 words)

**Components:**
- Key R&D themes (3-5 major areas)
- Patent filing trends
- Emerging business models
- Disruption risks/opportunities
- Technology adoption curves

### 9. Regulatory and ESG Considerations (400-500 words)

**Components:**
- Current regulatory framework
- Pending legislation (next 24 months)
- Carbon footprint / Scope 1, 2, 3 emissions
- Material ESG risks
- Sustainability trends

### 10. Regional Nuances (600-700 words)

**Components:**
- Demand outlook by region (NA, EU, APAC, LatAm, MENA)
- Supply chain depth assessment
- Policy environment comparison
- Market maturity assessment

**Required Table:**
| Region | 2024 Market Size ($B) | 2030F ($B) | CAGR | Key Driver | Risk Level |
|--------|----------------------|------------|------|------------|------------|
| North America | $X | $X | X% | | |
| Europe | $X | $X | X% | | |
| Asia-Pacific | $X | $X | X% | | |
| China | $X | $X | X% | | |

### 11. Risk Matrix (400-500 words)

Rank top 5 risks by likelihood and impact.

| Rank | Risk | Likelihood | Impact | Early Warning Indicators | Mitigation |
|------|------|------------|--------|--------------------------|------------|
| 1 | [Risk name] | [H/M/L] | [H/M/L] | [Signals to monitor] | [Hedging strategies] |
| 2 | [Risk name] | [H/M/L] | [H/M/L] | | |
| ... | ... | ... | ... | ... | ... |

### 12. Strategic Implications for Investors (600-800 words)

Outline **three actionable investment theses**:

**Thesis 1: [Title]**
- Investment angle and rationale (2-3 sentences)
- Trigger events to watch
- KPIs to track
- Illustrative upside: [X]% over [timeframe]
- Illustrative downside: [X]% under [scenario]
- Preferred exposure: [Specific companies/instruments]

**Thesis 2: [Title]**
[Same structure]

**Thesis 3: [Title]**
[Same structure]

### 13. Appendix

**Components:**
- Detailed methodology notes
- Data sources and limitations
- Company profiles (expanded from Section 5)
- Full bibliography (sorted by first appearance)

## Quality Standards

### Writing Style
- **Audience:** Sophisticated buy-side readers familiar with finance jargon
- **Tone:** Precise, evidence-backed, no fluff
- **Avoid:** Em dashes, hyperbole, unsupported claims
- **Paragraph length:** Under 120 words
- **Total length:** 7,000-9,000 words

### Data Requirements
- Every quantitative claim needs a source
- Prefer primary sources (10-K filings, government data)
- Cross-check conflicting data points
- Flag data gaps explicitly

### Formatting
- Use Markdown headings (## for sections, ### for subsections)
- Numbered lists for sequential items
- Bullet lists for related items
- Tables immediately after introduction paragraph
- Label every chart clearly

## Output Checklist

Before finalizing, verify:
- [ ] All 13 sections present and complete
- [ ] Executive summary has one-sentence bottom line
- [ ] All tables have clear labels
- [ ] Every number has an implicit or explicit source
- [ ] Porter Five Forces rated (Low/Medium/High)
- [ ] Three investment theses with triggers and KPIs
- [ ] Bibliography sorted by first appearance
- [ ] Total word count 7,000-9,000
- [ ] No em dashes used
- [ ] Currency and units consistent throughout

## Example Usage

**User:** "Research the battery energy storage industry for a 2024-2030 horizon, focusing on North America and Europe."

**Your workflow:**
1. Set parameters: INDUSTRY=battery energy storage, REGION=NA + EU, TIME_HORIZON=2024-2030
2. Plan outline (internal only)
3. Conduct 8+ web searches for data
4. Draft all 13 sections
5. Verify checklist
6. Deliver complete report
