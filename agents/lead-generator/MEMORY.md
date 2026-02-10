# MEMORY.md - Lead Generator Knowledge Base

## Target Industries

_(To be specified by Sam based on expertise and preferences)_

### Suggested High-Value Sectors
- SaaS/Technology
- Healthcare/Biotech
- Manufacturing
- Professional Services
- E-commerce/DTC
- Climate/Sustainability

## Lead Scoring Framework

### Trigger Events (High Priority)
- Recent funding round (Seed, Series A, B, C)
- CFO departure announcement
- Rapid hiring (>20% headcount growth in 6 months)
- Geographic expansion
- New product line launch
- Preparing for next funding round

### Company Signals (Medium Priority)
- Job postings for "Head of Finance" or "VP Finance"
- LinkedIn activity showing growth
- Conference attendance (scaling mindset)
- Industry awards/recognition

### Ideal Client Profile (ICP)
**Must-haves:**
- $1M+ ARR
- 10+ employees
- Complex financial operations
- Investor reporting requirements

**Nice-to-haves:**
- Multiple entities
- International operations
- Recurring revenue model
- Board reporting needs

## API Integrations

### NewsAPI
**Status:** Connected
**API Key:** `fe52ac365edf464c9dca774544a40da3`
**Base URL:** https://newsapi.org/v2
**Use Cases:**
- Startup funding announcements
- CFO appointment/departure news
- Industry growth signals
- Company expansion news

**Key Endpoints:**
- `GET /everything` - Search news articles
- `GET /top-headlines` - Breaking news

### Web Search (Brave/Tavily)
**Purpose:** Company research, lead identification, trigger event detection
**Primary:** Brave Search API
**Backup:** Tavily API

### Hunter.io
**Purpose:** Email finder for prospect outreach
**API Key:** Configured via environment variable

### Abstract API
**Purpose:** Company enrichment and data validation
**API Key:** Configured via environment variable

## SkillsMP Integration

**Status:** Connected
**API Key:** `sk_live_skillsmp_4PsNNxq_MEZuoIp4ATK9qzVc5_DS840ypPxOQO0QgfQ`
**API Docs:** https://skillsmp.com/docs/api

### SkillsMP Search Safety Rules
1. **Security Review First**: Review skills in isolated folder before installing
2. **User Approval Required**: Ask Sam for approval before installing
3. **Watch for Red Flags**: Do not install brand new or low-rated skills

## Installed Skills

| Skill | File | Purpose |
|-------|------|---------|
| **Deep Research (McKinsey)** | `skills/deep-research-mckinsey/SKILL.md` | Institutional-grade market research for target industry analysis |
| **Company Research (Investment)** | `skills/company-research-investment/SKILL.md` | Prospect company analysis for lead qualification |
| **OpenClaw Memory Flush** | `skills/openclaw-memory-flush/REFERENCE.md` | Memory architecture, context engineering, persistence strategies |
| **Deep Research Best Practices** | `skills/deep-research-best-practices.md` | Evidence-based prospect research, source grading |
| **Hayakawa Ladder of Abstraction** | `skills/hayakawa-ladder-of-abstraction.md` | Communication framework for strategic vs. concrete messaging |

### Using Deep Research (McKinsey) Skill

**For target market/industry analysis:**
1. Read `skills/deep-research-mckinsey/SKILL.md`
2. Set parameters: INDUSTRY=[target sector], REGION=[geography]
3. Follow 13-section framework
4. Use Kimi 2.5 for efficient 5,000-7,000 word reports
5. Focus on Section 5 (Competitive Landscape) for lead identification

**Output:** 7,000-9,000 word market research with:
- Industry growth trends and catalysts
- Top companies with funding status
- M&A activity (indicates CFO needs)
- Regional expansion patterns
- Trigger events for Fractional CFO services

### Using Company Research (Investment) Skill

**For prospect company qualification:**
1. Read `skills/company-research-investment/SKILL.md`
2. Set parameters: COMPANY_NAME=[prospect], TICKER=[if public]
3. Focus on: revenue scale, growth rate, complexity signals
4. Identify: recent funding, expansion, financial distress
5. Use for: qualifying leads before outreach

**Output:** 3,000-5,000 word company profile with:
- Business model and revenue scale
- Growth trajectory and complexity
- Trigger events (funding, expansion, M&A)
- Decision-maker identification
- CFO pain point assessment
- Tailored outreach angle based on research

## Cross-Agent Intelligence Sharing

### ASX Mining Companies - CFO Opportunity (Active)
**Status:** High priority collaboration with MiningMetalsAnalyst  
**Source:** Sam's network - two aggressive Australian groups  
**Profile:** ASX-listed mining companies with cash for expansion

**My Role:** Identify ASX mining companies as Fractional CFO leads

**Target Profile:**
- ASX-listed (Australian Securities Exchange)
- Market cap: $50M-$500M (growth phase)
- Cash position: >$10M (recent capital raise)
- Active M&A or JV strategy
- Aggressive expansion plans
- CFO gap (interim, part-time, or none)

**Special Output Section for Sam:**
```
## ⛏️ Mining CFO Leads - ASX Focus
*Australian listed mining companies needing fractional CFO*

1. **Company Name** (ASX: TKR)
   - Cash Position: $XM
   - Recent Activity: Capital raise/JV/M&A
   - Strategy: Aggressive expansion
   - CFO Status: [Full-time/Interim/None]
   - Opportunity: Fractional CFO for growth
   - Cross-Sell: Mine deal sourcing
```

**Enhanced Lead Scoring for CFO Services (Comprehensive):**

### Tier 1: Critical Signals (Must Have for High Score)
| Signal | Points | Rationale |
|--------|--------|-----------|
| Recent funding Series A-C (<6 months) | +35 | Highest intent, cash to spend, complexity growing |
| No CFO on LinkedIn / Job posting for CFO/VP Finance | +30 | Immediate need, decision maker likely involved |
| 15-75 employees | +25 | Sweet spot for fractional (too small = not ready, too big = need full-time) |

### Tier 2: Strong Indicators
| Signal | Points | Rationale |
|--------|--------|-----------|
| Multi-entity structure | +20 | Complexity = need CFO |
| International operations | +18 | Tax, compliance, reporting complexity |
| Recent CFO departure | +22 | Urgent need, search in progress |
| Interim/temp CFO currently | +18 | Proven need, evaluating options |
| Active M&A or JV discussions | +20 | Need financial modeling, due diligence |
| Planning fundraise in 6 months | +18 | Need financials ready |
| Board meetings monthly/quarterly | +15 | Regular reporting burden |

### Tier 3: Supporting Signals
| Signal | Points | Rationale |
|--------|--------|-----------|
| $5M-$50M ARR | +15 | Revenue scale = complexity |
| 30%+ YoY growth | +12 | Fast growth = financial stress |
| Multiple investors on cap table | +10 | Investor reporting requirements |
| Complex revenue model (usage, tiered, etc.) | +10 | Need revenue recognition expertise |
| Industry: SaaS, Fintech, Marketplace | +8 | Higher complexity, investor expectations |
| Location: SF, NYC, Boston, Austin | +5 | More likely to use fractional services |
| Recent expansion (new office, product line) | +10 | Complexity increase |

### Tier 4: Automation Fit (AI-CFO Potential)
| Signal | Points | Rationale |
|--------|--------|-----------|
| Uses QuickBooks Online | +12 | Easy AI integration |
| Uses Netsuite | +15 | Higher value client, complex needs |
| Has bookkeeper/accountant already | +10 | Gap between tactical and strategic |
| Previous month-end close >10 days | +15 | Pain point we solve |
| Manual Excel forecasting | +12 | Opportunity for automation |
| No financial dashboards | +10 | We provide real-time visibility |

### Negative Signals (Reduce Score)
| Signal | Points | Rationale |
|--------|--------|-----------|
| Full-time CFO on team | -40 | Not a fit |
| <10 employees | -20 | Too early |
| >200 employees | -15 | Likely need full-time |
| Pre-revenue | -25 | Not ready for CFO |
| Bootstrapped (no funding) | -10 | Limited budget |
| Recent layoffs | -15 | Budget constraints |
| Hiring freeze | -20 | No budget |

### Scoring Tiers
- **🔥 Hot (85+):** Immediate outreach - very likely to buy
- **🌡️ Warm (70-84):** Follow up this week - good fit
- **💡 Nurture (55-69):** Add to nurture campaign - future potential
- **❌ Cold (<55):** Deprioritize or disqualify

### Match Score Calculation Example:
```
Recent Series B (+35)
No CFO, job posting (+30)
45 employees (+25)
Multi-entity (+20)
QuickBooks Online (+12)
SaaS company (+8)
Planning Series C in 6 months (+18)
Monthly board meetings (+15)
Manual forecasting (+12)
--------------------------------
TOTAL: 175 points → 🔥 HOT LEAD
```

### Automation Triggers for Immediate Alert
Send instant alert to Sam if:
- Score >= 85 AND Recent funding (<30 days)
- Score >= 90 (any combination)
- CFO departure + Recent funding (combo)
- Job posting for CFO + $10M+ ARR (combo)

### Lead Enrichment Checklist
Before outreach, verify:
- [ ] LinkedIn shows no CFO or "interim"
- [ ] Crunchbase shows recent funding date
- [ ] Headcount in target range (15-75)
- [ ] Industry is high-fit (SaaS, Fintech, etc.)
- [ ] Recent news doesn't show layoffs/hiring freeze
- [ ] Website shows growth signals (hiring, expansion)

**Tracking:** `cross-agent-opportunities/asx-mining-jv.csv`

**Daily Cross-Check:**
- Compare ASX companies found vs. mines from MiningMetalsAnalyst
- Identify potential JV matches
- Score cross-opportunities (0-100)
- Alert Sam on Tier 1 matches (80+)

**Revenue Opportunities:**
1. Fractional CFO services to ASX companies
2. Mine sourcing advisory fees
3. JV structuring consultation

## Outreach Templates

### Cold Email Structure
1. **Subject:** Specific trigger reference
2. **Hook:** Acknowledge their milestone/challenge
3. **Value:** Brief statement of how fractional CFO helps
4. **Proof:** One relevant success story or metric
5. **Ask:** Low-friction next step (15-min call)
6. **PS:** Personalization detail

### LinkedIn Connection Request
- Mention mutual connection or specific observation
- Avoid sales pitch in connection request
- Follow up with value-adding content

## Active Pipeline

| Company | Stage | Last Contact | Next Action | Priority |
|---------|-------|--------------|-------------|----------|
| _(tracked here)_ |

## Past Leads

_(Log outcomes for learning — what converted, what didn't)_

## Lessons Learned

_(What messaging works, which industries respond best, optimal timing)_
