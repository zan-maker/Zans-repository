# MEMORY.md - Mining and Metals Analyst Knowledge Base

## Commodity Coverage

### Precious Metals
- Gold (Au): Mining economics, central bank demand, ETF flows
- Silver (Ag): Industrial + monetary demand dynamics
- Platinum Group Metals (Pt, Pd): Automotive demand, substitution effects

### Base Metals
- Copper (Cu): Green transition demand, supply constraints
- Nickel (Ni): Battery demand, Indonesian supply
- Zinc (Zn): Galvanizing demand, mine supply
- Aluminum (Al): Energy cost sensitivity, Chinese supply

### Battery Metals
- Lithium (Li): Brine vs. hard rock economics
- Cobalt (Co): DRC supply risk, substitution
- Rare Earth Elements: Processing bottlenecks, China dependency

## Key Metrics Reference

### Gold Grade Classifications
- World-class: >5 g/t Au
- High-grade: 3-5 g/t Au
- Medium-grade: 1-3 g/t Au
- Low-grade: <1 g/t Au (requires bulk tonnage)

### Copper Grade Classifications
- World-class: >2% Cu
- High-grade: 1-2% Cu
- Medium-grade: 0.5-1% Cu
- Low-grade: 0.3-0.5% Cu (porphyry deposits)

## Jurisdiction Risk Tiers

### Tier 1 (Low Risk)
Canada, Australia, USA, Chile, Peru

### Tier 2 (Moderate Risk)
Mexico, Brazil, Argentina, South Africa, Ghana

### Tier 3 (High Risk)
DRC, Russia, Venezuela, Bolivia, Zimbabwe

## API Integrations

### NewsAPI
**Status:** Connected
**API Key:** `fe52ac365edf464c9dca774544a40da3`
**Base URL:** https://newsapi.org/v2
**Use Cases:**
- Mining sector news and announcements
- Commodity price movement catalysts
- M&A activity in mining sector
- Jurisdictional risk updates

**Key Endpoints:**
- `GET /everything` - Search news articles
- `GET /top-headlines` - Breaking news

### Web Search (Brave/Tavily)
**Purpose:** Mine listings, technical reports, market intelligence
**Primary:** Brave Search API
**Backup:** Tavily API

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
| **Deep Research (McKinsey)** | `skills/deep-research-mckinsey/SKILL.md` | Institutional-grade market research for mining sector analysis |
| **Company Research (Investment)** | `skills/company-research-investment/SKILL.md` | Individual mining company equity research and analysis |
| **OpenClaw Memory Flush** | `skills/openclaw-memory-flush/REFERENCE.md` | Memory architecture, context engineering, persistence strategies |
| **Deep Research Best Practices** | `skills/deep-research-best-practices.md` | Evidence-based decision making, source grading, research protocols |
| **Hayakawa Ladder of Abstraction** | `skills/hayakawa-ladder-of-abstraction.md` | Communication framework for strategic vs. concrete thinking |
| **Metals Pricing MVP** | `skills/metals-pricing-mvp.md` | Scraping-based metal price monitoring workflow |
| **Mine Grading Classification** | `skills/mine-grading-classification.md` | Grade classification bands by commodity and mining method |

### Using Deep Research (McKinsey) Skill

**For comprehensive mining/metals sector analysis:**
1. Read `skills/deep-research-mckinsey/SKILL.md`
2. Set parameters: INDUSTRY=[commodity] mining, REGION=[target geography]
3. Follow 13-section framework
4. Use GLM-4.7 for complex multi-jurisdictional analysis
5. Include commodity price forecasts, jurisdictional risk ratings

**Output:** 7,000-9,000 word institutional research with:
- TAM by commodity and region
- Top 10 mining companies analysis
- Jurisdictional risk comparison
- ESG considerations for mines
- Investment theses with trigger events

### Using Company Research (Investment) Skill

**For individual mining company analysis:**
1. Read `skills/company-research-investment/SKILL.md`
2. Set parameters: COMPANY_NAME=[mining company], TICKER=[symbol]
3. Follow 11-section framework
4. Focus on: reserves, production costs, all-in sustaining costs (AISC)
5. Include: grade quality, mine life, jurisdictional risk

**Output:** 3,000-5,000 word company profile with:
- Business model (producer/explorer/developer)
- Unit economics: AISC vs. commodity price
- Reserve quality and mine life
- Geographic/regulatory risk exposure
- Investment thesis with commodity price sensitivity

## Active Opportunities

_(Tracked in memory files as identified)_

## Past Analyses

_(Log outcomes for learning)_

## Lessons Learned

_(What worked, what didn't, pattern recognition)_
