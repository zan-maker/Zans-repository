# MEMORY.md - Trade Recommender Knowledge Base

## Market Coverage

### Stock Markets
- US equities (NYSE, NASDAQ)
- ETFs and sector plays
- Options strategies
- Technical and fundamental analysis

### Polymarket
- Crypto prediction markets
- Event-based binary outcomes
- Liquidity considerations
- Fee structures

### Kalshi
- Event-based markets (politics, weather, sports)
- Regulation and compliance
- Market structure
- **API Access:** Configured for automated arbitrage detection

## API Integrations

### DefeatBeta API
**Purpose:** Prediction market data and trading signals
**Repository:** https://github.com/defeat-beta/defeatbeta-api
**Status:** Connected
**Use Cases:**
- Market data aggregation
- Arbitrage signal detection
- Cross-market opportunity identification

### Kalshi API
**Status:** Configured
**API Key ID:** `fb109d35-efc3-42b1-bdba-0ee2a1e90ef8`
**Authentication:** RSA Private Key (stored as env var)
**Base URL:** https://trading-api.kalshi.com/trade-api/v2
**Rate Limits:** 200 requests/minute

**Endpoints to Use:**
- `GET /markets` - List available markets
- `GET /markets/{market_id}` - Market details and orderbook
- `GET /portfolio/balance` - Account balance
- `POST /orders` - Place orders (paper trading mode recommended)

### NewsAPI
**Status:** Connected
**API Key:** `fe52ac365edf464c9dca774544a40da3`
**Base URL:** https://newsapi.org/v2
**Use Cases:**
- Breaking news affecting markets
- Earnings announcements
- Regulatory changes
- Economic indicator releases
- Event-driven market movements

**Key Endpoints:**
- `GET /everything` - Search news articles
- `GET /top-headlines` - Breaking news

### Web Search (Brave/Tavily)
**Purpose:** Real-time market intelligence, sentiment, alternative data
**Primary:** Brave Search API
**Backup:** Tavily API
**Use Cases:**
- Alternative data sources
- Social sentiment
- Deep research validation
- Cross-reference news accuracy

## Analysis Frameworks

### Technical Analysis
- Support/resistance levels
- Trend analysis
- Volume patterns
- Moving averages
- Momentum indicators

### Fundamental Analysis
- Earnings reports
- Economic indicators
- Sector rotation
- Macro trends

### Risk Management
- Position sizing (Kelly Criterion, risk parity)
- Portfolio correlation
- Max drawdown limits
- Volatility assessment

### Arbitrage Detection Workflow

**Step 1: Market Scanning**
- Query DefeatBeta API for prediction market data
- Query Kalshi API for event market prices
- Use Bregman Projection skill to identify mispricings

**Step 2: Web Research**
- Search for relevant news/events affecting markets
- Validate arbitrage thesis with external data
- Check for market closures or restrictions

**Step 3: Opportunity Assessment**
- Calculate expected profit (accounting for fees)
- Assess liquidity (can you get filled?)
- Identify execution risks (timing, counterparty)

**Step 4: Recommendation Output**
- Market pair
- Entry/exit points
- Position sizing
- Risk factors
- Confidence score (1-10)

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
| **Deep Research Best Practices** | `skills/deep-research-best-practices.md` | Evidence-based decision making, source grading, research protocols |
| **Hayakawa Ladder of Abstraction** | `skills/hayakawa-ladder-of-abstraction.md` | Communication framework for strategic vs. concrete thinking |
| **Options Research** | `skills/options-research.md` | Quant fund-grade options analysis (Greeks, IV, skew, flow) |
| **Bregman Projection Arbitrage** | `skills/bregman-projection-arbitrage.md` | Prediction market arbitrage framework (Frank-Wolfe, Polymarket) |

## Environment Variables Required

```bash
# DefeatBeta API
export DEFEATBETA_API_KEY="your-defeatbeta-key"

# Kalshi API
export KALSHI_API_KEY_ID="fb109d35-efc3-42b1-bdba-0ee2a1e90ef8"
export KALSHI_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA4+LPLFirxRAFlAxRI7xkdIAVuOkg4KCOIk7q1LAZy70Ek0Qj
...
-----END RSA PRIVATE KEY-----"

# Web Search
export BRAVE_API_KEY="your-brave-key"
export TAVILY_API_KEY="your-tavily-key"
```

## Active Opportunities

_(Tracked in memory files as identified)_

## Past Recommendations

_(Log outcomes for learning)_

## Lessons Learned

_(What worked, what didn't, pattern recognition)_
