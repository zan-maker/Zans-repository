# Deep Research (McKinsey) Skill - Quick Reference

## Overview
McKinsey-style institutional-grade market research framework for comprehensive industry analysis and investment thesis development.

## File Location
`skills/deep-research-mckinsey/SKILL.md`

## When to Use
- Industry deep-dives and sector analysis
- Market sizing (TAM/SAM/SOM)  
- Competitive landscape analysis
- Investment thesis development
- Porter Five Forces analysis
- M&A and PE activity tracking
- Technology trend assessment
- Regulatory and ESG analysis

## Required Parameters
- **INDUSTRY**: Target sector (required)
- **REGION**: Geographic focus (default: Global)
- **TIME_HORIZON**: Forecast period (default: 2024-2030)
- **CURRENCY**: Reporting currency (default: USD)

## 13-Section Structure

1. **Executive Summary** (400-600 words)
   - 3-5 bullet highlights with metrics
   - One-sentence bottom line

2. **Industry Definition** (500-700 words)
   - Scope, sub-segments, value chain
   - Required table: Segment breakdown

3. **Market Size** (700-900 words)
   - TAM, historical CAGR, 5-year forecast
   - Required tables: Market trajectory, Scenario analysis

4. **Macro Context** (500-600 words)
   - GDP, rates, demographics, policy

5. **Competitive Landscape** (700-900 words)
   - Top 10 companies, market share
   - M&A activity table

6. **Porter Five Forces** (400-500 words)
   - Rate each: Low/Medium/High
   - Overall attractiveness score

7. **Cost Structure** (400-500 words)
   - Margins, capex intensity, working capital
   - Benchmark table

8. **Technology Trends** (500-600 words)
   - R&D themes, patents, disruption

9. **Regulatory/ESG** (400-500 words)
   - Rules, legislation, carbon, risks

10. **Regional Nuances** (600-700 words)
    - Demand by region, supply chain
    - Regional comparison table

11. **Risk Matrix** (400-500 words)
    - Top 5 risks, likelihood/impact ratings
    - Early warning indicators

12. **Investment Theses** (600-800 words)
    - Three actionable theses
    - Each with triggers, KPIs, upside/downside

13. **Appendix**
    - Methodology, sources, bibliography

## Model Selection

**GLM-4.7 (Z.AI)** - Use for:
- Complex reports >7,000 words
- Heavy quantitative analysis
- Multiple scenario modeling

**Kimi K2.5 (Moonshot)** - Use for:
- Standard 5,000-7,000 word reports
- Most research tasks
- Default choice

## Workflow

1. **Planning** (Internal only)
   - Create bullet outline
   - Identify data sources needed

2. **Research** (Iterative)
   - Web search until >90% coverage
   - Minimum 8 search queries
   - Cross-check conflicting data

3. **Drafting** (Sequential)
   - Write sections 1-13 in order
   - Insert tables after intro paragraphs
   - Keep paragraphs <120 words

4. **Quality Check**
   - Verify all 13 sections complete
   - Check all numbers have sources
   - Confirm 7,000-9,000 words
   - Ensure no em dashes

## Web Search Strategy

Start broad, then narrow:
1. "[INDUSTRY] market size 2024 TAM"
2. "[Company] annual report revenue"
3. "[INDUSTRY] market share leaders"
4. "[INDUSTRY] acquisitions 2024"
5. "[INDUSTRY] regulations policy"
6. "[INDUSTRY] R&D trends innovation"
7. "[INDUSTRY] market China Europe"
8. "[INDUSTRY] ESG carbon footprint"

## Output Standards

- **Audience:** Sophisticated buy-side readers
- **Tone:** Precise, evidence-backed, no fluff
- **Length:** 7,000-9,000 words
- **Format:** Markdown, tables after paragraphs
- **Sources:** Primary preferred (filings, government)

## Example Usage

```
User: "Research the battery energy storage industry for 2024-2030"

Agent:
1. Read SKILL.md at skills/deep-research-mckinsey/SKILL.md
2. Set parameters: INDUSTRY=battery storage, REGION=Global
3. Plan outline (internal)
4. Conduct 8+ web searches
5. Draft all 13 sections
6. Verify quality checklist
7. Deliver complete report
```

## Success Metrics

- [ ] All 13 sections present
- [ ] Executive summary has bottom line
- [ ] All tables clearly labeled  
- [ ] Every number sourced
- [ ] Porter forces rated
- [ ] Three investment theses
- [ ] Bibliography included
- [ ] 7,000-9,000 words
- [ ] No em dashes
