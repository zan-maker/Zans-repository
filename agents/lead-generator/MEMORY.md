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
