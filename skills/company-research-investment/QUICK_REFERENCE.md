# Company Research (Investment) Skill - Quick Reference

## Overview
Comprehensive company research and investment analysis for individual company deep-dives.

## File Location
`skills/company-research-investment/SKILL.md`

## When to Use
- Individual company equity research
- Business model analysis
- Unit economics evaluation
- Investment thesis development
- Due diligence (pre-investment)
- Competitive positioning
- Financial benchmarking

## Required Parameters
- **COMPANY_NAME**: Full legal name
- **TICKER**: Stock symbol
- **EXCHANGE**: Primary exchange (optional)

## 11-Section Structure

1. **Bottom Line** (3-5 sentences)
   - Investment thesis summary
   - Key merit, risk, expected outcome

2. **One-Paragraph Overview**
   - What company does
   - Customer job-to-be-done
   - Profit engine

3. **Business Model Map**
   - Value prop, products, customers
   - Revenue streams table
   - Cost structure

4. **Products & Pricing**
   - Table: Product | Customer | Pricing | Take Rate
   - Pricing power assessment

5. **Revenue Drivers**
   - Equations for each stream
   - Latest metrics with sources

6. **Unit Economics**
   - CAC calculation with formula
   - LTV calculation with formula
   - LTV/CAC ratio & payback period

7. **Customer Segments & Go-to-Market**
   - Segmentation table
   - 2-3 predictive KPIs

8. **Geographic Mix & Regulatory**
   - Regional revenue breakdown
   - Regulatory constraints

9. **KPIs to Watch**
   - 6-10 company-specific metrics
   - Benchmarks, latest values, trends

10. **Peer Snapshot**
    - Comparison table with valuations
    - EV/Revenue, EV/EBITDA

11. **Risks, Sensitivities & Thesis Triggers**
    - Top 5 risks ranked
    - Sensitivity analysis
    - 3 triggers (bull/bear/wildcard)

## Model Selection

**GLM-4.7 (Z.AI)** - Use for:
- Complex multi-segment companies
- Heavy financial modeling required
- Cross-jurisdictional regulatory analysis

**Kimi K2.5 (Moonshot)** - Use for:
- Standard comprehensive analysis
- Most company research tasks
- Default choice

## Citation Format
- `[10-K, FY2024]` - Annual reports
- `[10-Q, Q3 2024]` - Quarterly reports
- `[Earnings Call, 2024-10-24]` - Call transcripts
- `[Investor Presentation, 2024]` - Decks
- `[Website, accessed 2024-11]` - Web
- `[Not disclosed]` - Unavailable

## Web Search Strategy

1. **Primary Sources:**
   - "{{COMPANY}} 10-K annual report {{year}} SEC"
   - "{{COMPANY}} 10-Q quarterly report SEC"
   - "{{COMPANY}} investor presentation {{quarter}}"
   - "{{COMPANY}} earnings call transcript"

2. **Financials:**
   - "{{TICKER}} revenue breakdown by segment"
   - "{{COMPANY}} unit economics CAC LTV"

3. **Business Model:**
   - "{{COMPANY}} how does it make money"
   - "{{COMPANY}} pricing strategy"

4. **Competitive:**
   - "{{COMPANY}} competitors market share"
   - "{{TICKER}} vs {{peer}} comparison"

## Output Standards

- **Audience:** Investment professionals
- **Tone:** Precise, analytical, evidence-backed
- **Length:** 3,000-5,000 words
- **Tables Required:** Products/Pricing, Revenue Drivers, Peer Snapshot
- **Sources:** Primary documents (10-K, 10-Q, earnings)

## Example Usage

```
User: "Analyze Tesla (TSLA) for investment research"

Agent:
1. Read SKILL.md at skills/company-research-investment/SKILL.md
2. Set parameters: COMPANY_NAME=Tesla Inc., TICKER=TSLA
3. Search for 10-K, 10-Q, earnings calls
4. Search for unit economics, margins, competitors
5. Draft all 11 sections with formulas
6. Verify checklist
7. Deliver complete analysis
```

## Success Metrics

- [ ] Bottom Line at start
- [ ] All 11 sections complete
- [ ] Three required tables present
- [ ] Unit economics with formulas
- [ ] KPI table with benchmarks
- [ ] All numbers cited
- [ ] Risks ranked
- [ ] 3 thesis triggers
- [ ] Primary sources used
- [ ] "Not disclosed" where appropriate
