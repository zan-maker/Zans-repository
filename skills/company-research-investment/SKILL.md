---
name: company-research-investment
description: Comprehensive company research and investment analysis for individual company deep-dives. Use when analyzing a specific company's business model, unit economics, competitive position, and investment thesis. Triggers on requests for company analysis, stock research, business model evaluation, due diligence, or investment thesis development on specific companies.
---

# Company Research: Investment Analysis Framework

Conduct comprehensive business model and investment analysis on individual companies suitable for equity research, due diligence, and portfolio management. This skill produces institutional-grade company profiles with rigorous financial analysis, KPI tracking, and actionable investment insights.

## When to Use This Skill

Use for any request involving:
- Individual company deep-dives and equity research
- Business model analysis and mapping
- Unit economics evaluation
- Investment thesis development
- Due diligence (pre-investment or ongoing)
- Competitive positioning analysis
- Financial metric benchmarking
- Risk assessment and sensitivity analysis

## Model Compatibility

This skill works with any capable LLM:
- **GLM-4.7 (Z.AI)**: Recommended for complex multi-section analysis with heavy financial modeling
- **Kimi K2.5 (Moonshot)**: Excellent for comprehensive company profiles (256K context)
- **GPT-4/Claude**: Use if available and appropriate
- **Other models**: Adjust output depth based on context window

**Selection guidance:**
- Use GLM-4.7 for companies with complex/multi-segment business models
- Use Kimi 2.5 for standard comprehensive analysis
- For quick summaries (<2,000 words), any capable model works

## Required Parameters

Before starting, confirm these variables:

| Parameter | Example | Description |
|-----------|---------|-------------|
| `{{COMPANY_NAME}}` | Tesla Inc. | Full legal name of company |
| `{{TICKER}}` | TSLA | Stock ticker symbol |
| `{{EXCHANGE}}` | NASDAQ | Primary exchange (if applicable) |

## Research Workflow

### Phase 1: Data Collection (Iterative)

Conduct targeted searches to gather comprehensive company intelligence:

1. **Primary Sources (Priority 1)**
   - Search: "{{COMPANY_NAME}} 10-K annual report {{latest_year}} SEC"
   - Search: "{{COMPANY_NAME}} 10-Q quarterly report SEC"
   - Search: "{{COMPANY_NAME}} investor presentation {{latest_quarter}}"
   - Search: "{{COMPANY_NAME}} earnings call transcript {{latest_quarter}}"

2. **Financial Data**
   - Search: "{{TICKER}} revenue breakdown by segment {{latest_year}}"
   - Search: "{{COMPANY_NAME}} unit economics customer acquisition cost"
   - Search: "{{TICKER}} gross margin operating margin historical"

3. **Business Model**
   - Search: "{{COMPANY_NAME}} how does it make money business model"
   - Search: "{{COMPANY_NAME}} revenue streams breakdown"
   - Search: "{{COMPANY_NAME}} pricing strategy fees"

4. **Competitive Landscape**
   - Search: "{{COMPANY_NAME}} competitors market share"
   - Search: "{{INDUSTRY}} top companies comparison {{TICKER}}"
   - Search: "{{COMPANY_NAME}} vs {{top_competitor}} comparison"

5. **Recent Developments**
   - Search: "{{COMPANY_NAME}} recent news {{last_3_months}}"
   - Search: "{{TICKER}} stock analyst rating price target"
   - Search: "{{COMPANY_NAME}} risks challenges 2024"

**Stop when:** You can answer all 11 sections with specific data points and citations.

### Phase 2: Analysis & Drafting

Write each section with:
- Specific metrics and numbers
- Clear source citations
- Separation of facts vs. estimates
- Formulas shown for all calculations

## Report Structure (11 Sections)

### 1. Bottom Line (3-5 sentences)

Opening investment thesis summary:
- Core business in plain English
- Key investment merit or concern
- Primary risk factor
- Expected outcome/timeline

**Template:**
```
{{COMPANY_NAME}} operates a [business model type] serving [target market], 
generating revenue primarily through [main revenue stream]. The investment 
case rests on [key growth driver], with [primary risk] as the main concern. 
[Metric] suggests [bullish/bearish] positioning at current valuation. 
[Expected catalyst] in [timeframe] could [impact].
```

### 2. One-Paragraph Overview

**Components:**
- What the company does (core operations)
- Customer job-to-be-done
- Profit engine explanation

**Requirements:**
- Plain English, no jargon
- Include latest revenue figure with source
- Explain the "why" behind the business

### 3. Business Model Map

**Components:**
- **Value Proposition**: Core customer benefit
- **Key Products/Services**: Main offerings
- **Target Customers**: Primary segments
- **Distribution Channels**: How products reach customers
- **Monetization**: All revenue streams (list comprehensively)
- **Cost Structure**: Major variable vs. fixed cost buckets

**Required Table - Revenue Streams:**
| Revenue Stream | Description | % of Total | YoY Growth | Source |
|---------------|-------------|------------|------------|--------|
| [Stream 1] | [Description] | X% | X% | [10-K/10-Q] |
| [Stream 2] | [Description] | X% | X% | [10-K/10-Q] |

### 4. Products & Pricing

**Required Table:**
| Product/Service | Target Customer | Pricing Model | Take Rate/Fees | Recent Changes | Source |
|----------------|-----------------|---------------|----------------|----------------|--------|
| [Product 1] | [Segment] | [Subscription/Transaction/etc] | X% / $X | [Change] | [Source] |
| [Product 2] | [Segment] | [Model] | X% / $X | [Change] | [Source] |

**Analysis:**
- Pricing power assessment
- Fee structure transparency
- Recent pricing actions and impact

### 5. Revenue Drivers

For each revenue stream, specify the driver equation:

**Format:**
```
Revenue_Stream = Users × Activity_rate × Price_per_unit × Take_rate

Example:
Subscription Revenue = Subscribers × ARPU × 12 months
Transaction Revenue = GMV × Take_rate
```

**Required Table:**
| Revenue Stream | Driver Equation | Latest Metrics | Value | Source |
|---------------|-----------------|----------------|-------|--------|
| [Stream 1] | [Formula] | [Users/ARPU/etc] | $X | [10-K/10-Q] |

### 6. Unit Economics

**Components:**
- Definition of "unit" for this business model
- Customer Acquisition Cost (CAC) calculation
- Lifetime Value (LTV) calculation
- LTV/CAC ratio
- Payback period
- Contribution margin per unit

**Required Format:**
```
Unit Definition: [What constitutes one unit]

CAC = [Sales & Marketing] / [New Customers] = $X
[Source: 10-K FY2024, SGA breakdown]

LTV = [ARPU] × [Gross Margin] × [Avg Customer Lifetime] = $X
[Assumptions: X% monthly churn = X month lifetime]

LTV/CAC Ratio: X.Xx [Benchmark: >3x healthy, >5x excellent]
Payback Period: X months [Benchmark: <12 months acceptable]
```

### 7. Customer Segments & Go-to-Market

**Components:**
- Customer segmentation (by size, industry, use case)
- Acquisition channels (sales-led, product-led, marketing)
- Conversion funnel highlights
- Retention patterns (churn rates, expansion revenue)
- **2-3 KPIs that most predict revenue**

**Required Table:**
| Segment | % of Revenue | Growth Rate | CAC | Retention | Notes |
|---------|-------------|-------------|-----|-----------|-------|
| [Segment 1] | X% | X% | $X | X% | [Characteristics] |

### 8. Geographic Mix & Regulatory

**Components:**
- Revenue breakdown by region
- Growth rates by geography
- Regulatory environment by region
- Licenses and compliance requirements
- Market frictions affecting expansion

**Required Table:**
| Region | Revenue % | YoY Growth | Regulatory Status | Key Constraints |
|--------|-----------|------------|-------------------|-----------------|
| North America | X% | X% | [Status] | [Constraints] |
| Europe | X% | X% | [Status] | [GDPR/etc] |
| Asia-Pacific | X% | X% | [Status] | [Constraints] |

### 9. KPIs to Watch

List 6-10 company-specific KPIs with:
- Precise definition
- What "good" looks like (benchmark)
- Latest reported value
- Trend direction

**Required Table:**
| KPI | Definition | Benchmark "Good" | Latest Value | Trend | Source |
|-----|-----------|------------------|--------------|-------|--------|
| [KPI 1] | [Definition] | [Threshold] | X% / $X | ↑/↓ | [Earnings QX] |
| [KPI 2] | [Definition] | [Threshold] | X% / $X | ↑/↓ | [10-K] |

### 10. Peer Snapshot

**Required Table:**
| Peer Company | Ticker | Business Overlap | Key Differentiation | EV/Revenue | EV/EBITDA | Source |
|-------------|--------|-----------------|---------------------|------------|-----------|--------|
| [Peer 1] | [TKR] | [Overlap area] | [Differentiation] | X.x | X.x | [Source] |
| [Peer 2] | [TKR] | [Overlap area] | [Differentiation] | X.x | X.x | [Source] |

**Analysis:**
- Valuation comparison (premium/discount)
- Market positioning relative to peers
- Competitive moat assessment

### 11. Risks, Sensitivities & Thesis Triggers

**A. Top 5 Business Model Risks**
| Rank | Risk | Likelihood | Impact | Mitigation |
|------|------|------------|--------|------------|
| 1 | [Risk description] | H/M/L | H/M/L | [How company addresses] |

**B. Sensitivity Analysis**
- Most material driver: [Factor]
- Sensitivity: "[Driver] ±[X]% impacts [metric] by ±[Y]%"
- Example: "Take-rate ±25 bps impacts EBITDA by ±$XM"

**C. What Would Change the Thesis (3 Triggers)**

1. **Bull Case Trigger:** [Event/KPI] → [Impact on thesis]
2. **Bear Case Trigger:** [Event/KPI] → [Impact on thesis]
3. **Wildcard:** [Unexpected factor] → [Potential impact]

## Citation Format

Use compact inline citations throughout:
- `[10-K, FY2024]` for annual reports
- `[10-Q, Q3 2024]` for quarterly reports
- `[Earnings Call, 2024-10-24]` for call transcripts
- `[Investor Presentation, 2024]` for decks
- `[Website, accessed 2024-11]` for web sources
- `[Not disclosed]` for unavailable information

## Quality Standards

### Writing Style
- **Audience:** Investment professionals, buy-side analysts
- **Tone:** Precise, evidence-backed, analytical
- **Avoid:** Hype, promotional language, unsupported claims
- **Length:** 3,000-5,000 words (flexible based on complexity)

### Data Requirements
- Every metric needs a source
- Distinguish facts from estimates
- Show formulas for all calculations
- Flag data gaps explicitly with "[Not disclosed]"

### Analysis Depth
- Go beyond surface-level metrics
- Explain the "why" behind numbers
- Connect operational KPIs to financial outcomes
- Provide actionable investment implications

## Output Checklist

Before finalizing, verify:
- [ ] Bottom Line summary at start
- [ ] All 11 sections present
- [ ] Three required tables (Products/Pricing, Revenue Drivers, Peer Snapshot)
- [ ] Unit economics with formulas
- [ ] KPI table with latest values
- [ ] All numbers have citations
- [ ] Risks ranked with likelihood/impact
- [ ] 3 thesis triggers identified
- [ ] Sources from primary documents (10-K, 10-Q, earnings)
- [ ] "Not disclosed" used where appropriate

## Example Usage

**User:** "Analyze Tesla (TSLA) for investment research"

**Your workflow:**
1. Set parameters: COMPANY_NAME=Tesla Inc., TICKER=TSLA
2. Search for 10-K, 10-Q, investor presentations, earnings calls
3. Search for revenue breakdown, margins, unit economics
4. Search for competitors (BYD, VW, Ford EV)
5. Draft all 11 sections with citations
6. Verify checklist
7. Deliver complete analysis

## Example Output Structure

```markdown
## Bottom Line
Tesla Inc. (TSLA) operates an integrated automotive and energy business...
[Citation: 10-K FY2024, Business Overview]

## 1. One-Paragraph Overview
Tesla designs, develops, manufactures, and sells electric vehicles...
[Revenue: $XX.X billion, 10-K FY2024]

## 2. Business Model Map
[Detailed breakdown]

## 3. Products & Pricing
| Product | Customer | Pricing | Take Rate | Changes | Source |
|---------|----------|---------|-----------|---------|--------|
| Model 3 | Consumers | $XX,XXX | N/A | -5% 2024 | [Website] |

## 4. Revenue Drivers
Automotive Revenue = Vehicles_delivered × ASP × (1 - Leasing_mix)
= 1.8M × $44K × 0.85 = $XX.XB [10-K FY2024]

[Continue through section 11...]
```
