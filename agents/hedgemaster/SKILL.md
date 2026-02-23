# HedgeMaster - Agentic Portfolio Hedging System

**Agent Name:** HedgeMaster  
**Purpose:** Automated portfolio hedging using prediction markets (Kalshi)  
**Schedule:** Daily monitoring with on-demand risk analysis  
**Status:** Active

---

## 🎯 Overview

HedgeMaster continuously monitors your Alpaca portfolio, identifies emerging risks, and suggests/executes hedges via Kalshi prediction markets. It uses a multi-agent pipeline to discover both direct and indirect hedge relationships.

---

## 🏗️ Multi-Agent Workflow

### **Stage 1: Portfolio Monitor** (Daily, 9:00 AM ET)
**Trigger:** Scheduled cron job  
**Input:** Alpaca API (paper trading account)  
**Output:** Risk alerts → Risk Analyst

**Function:**
- Pull current positions from Alpaca
- Calculate position sizes & portfolio exposure
- Monitor price movements (>5% daily change = alert)
- Check for upcoming earnings announcements (within 7 days)
- Monitor news sentiment via NewsAPI
- Track sector rotation trends

**Alert Conditions:**
- Position down >5% in 24h
- Position down >10% in 7 days
- Earnings announcement within 7 days
- Negative news sentiment detected
- Sector-wide selloff detected

---

### **Stage 2: Risk Analyst** (On-demand, triggered by Monitor)
**Trigger:** Alert from Portfolio Monitor  
**Input:** Stock ticker + position details  
**Output:** Risk decomposition report → Kalshi Scout

**Function:**
- Decompose stock into risk factors:
  - **Sector risk:** Industry-specific headwinds
  - **Macro risk:** Interest rates, inflation, recession indicators
  - **Company-specific:** Earnings, CEO changes, product launches
  - **Geopolitical:** Trade wars, supply chain disruptions
  - **Regulatory:** FDA decisions, antitrust, legislation
- Generate targeted search queries for each risk
- Use web search (Brave/Tavily) to find relevant events
- Calculate risk severity score (0-100)

**Output Format:**
```json
{
  "ticker": "NVDA",
  "position_value": 10000,
  "risks": [
    {
      "type": "geopolitical",
      "description": "China export ban on AI chips",
      "severity": 85,
      "probability": 0.35,
      "search_queries": ["China AI chip ban kalshi", "NVDA China revenue impact"]
    }
  ]
}
```

---

### **Stage 3: Kalshi Scout** (On-demand, triggered by Analyst)
**Trigger:** Risk decomposition report  
**Input:** Risk factors + search queries  
**Output:** Ranked hedge recommendations → Hedge Executor

**Function:**
- Query Kalshi API for markets matching risk queries
- Filter markets by:
  - Liquidity: >$50K volume
  - Settlement: 7-30 days (optimal hedge window)
  - Edge: Implied probability vs estimated true probability
- Calculate hedge correlation (0-1, how well it offsets the risk)
- Score each market: (correlation × edge × liquidity_score)
- Generate plain-English hedge thesis

**Market Scoring Formula:**
```
hedge_score = (correlation × 0.4) + (edge × 0.4) + (liquidity_score × 0.2)

Where:
- correlation: 0-1 (how well market moves with the risk)
- edge: 0-1 (implied vs true probability difference, normalized)
- liquidity_score: min(volume/100000, 1)
```

**Output Format:**
```json
{
  "ticker": "NVDA",
  "recommendations": [
    {
      "market_id": "KXNVDACHINA-25-BAN",
      "market_name": "China bans AI chip exports by March 2025?",
      "current_price": 35,
      "implied_probability": 0.35,
      "estimated_true_probability": 0.43,
      "edge": 0.08,
      "volume": 180000,
      "settlement_date": "2025-03-31",
      "correlation": 0.92,
      "hedge_score": 87,
      "thesis": "Direct hedge. China revenue is 20% of NVDA. Ban would cause 15-20% drop.",
      "suggested_position": 150
    }
  ]
}
```

---

### **Stage 4: Hedge Executor** (On-demand, human approval required)
**Trigger:** Ranked recommendations  
**Input:** Hedge recommendations with full analysis  
**Output:** Executed trades or rejection logged

**Function:**
- Draft comprehensive hedge recommendation
- Send to user via Discord/email
- Wait for approval (Yes/No/Modify)
- If approved: Execute Kalshi trade via API
- If rejected: Log reason for learning
- Track hedge performance until settlement

**Recommendation Format:**
```markdown
# 📊 HEDGE RECOMMENDATION

**Position to Hedge:** NVDA ($10,000)
**Identified Risk:** China AI chip export ban
**Risk Severity:** HIGH (85/100)

## 🎯 Recommended Hedge

**Market:** "China bans AI chip exports by March 2025?"
**Kalshi ID:** KXNVDACHINA-25-BAN
**Current Price:** 35¢
**Implied Probability:** 35%
**True Probability (est):** 43%
**Edge:** +8%

**Suggested Trade:**
- Buy "Yes" contracts at 35¢
- Position Size: $150 (1.5% of NVDA position)
- Max Loss: $150 (if no ban)
- Potential Payout: $428 (if ban happens)
- Expected Value: +$34 (8% edge)

## 📝 Hedge Thesis

China represents ~20% of NVDA's revenue. An export ban would:
1. Immediately cut $8B+ in annual revenue
2. Trigger 15-20% stock price decline
3. Force pivots to alternative markets (takes 12-18 months)

This market directly captures that binary event. Historical precedent:
- 2023 China restrictions caused 8% single-day drop
- This ban would be broader, impacting H100/H200 chips

## ⚖️ Risk/Reward

**If hedge pays out:**
- NVDA likely down 15% ($1,500 loss on position)
- Hedge pays $428
- Net loss: $1,072 (vs $1,500 without hedge)

**If hedge expires worthless:**
- Lose $150 on hedge
- NVDA position unaffected
- Insurance cost: 1.5% of position

## ✅ EXECUTE?

[YES] [NO] [MODIFY POSITION SIZE]

---
Agent Manager
ImpactQuadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
```

---

## 📅 Cron Job Schedule

### Daily (9:00 AM ET)
```bash
openclaw cron create \
  --name "HedgeMaster - Daily Portfolio Scan" \
  --schedule "0 9 * * *" \
  --tz "America/New_York" \
  --agent HedgeMaster \
  --prompt "Read SKILL.md and execute Stage 1: Portfolio Monitor"
```

### On-Demand (Triggered by Monitor)
```bash
# Auto-triggered when alerts detected
openclaw cron create \
  --name "HedgeMaster - Risk Analysis" \
  --trigger "on_alert" \
  --agent HedgeMaster \
  --prompt "Execute Stage 2: Risk Analyst"

openclaw cron create \
  --name "HedgeMaster - Kalshi Scout" \
  --trigger "on_analysis" \
  --agent HedgeMaster \
  --prompt "Execute Stage 3: Kalshi Scout"
```

### Evening Report (6:00 PM ET)
```bash
openclaw cron create \
  --name "HedgeMaster - Daily Report" \
  --schedule "0 18 * * *" \
  --tz "America/New_York" \
  --agent HedgeMaster \
  --prompt "Generate daily report: active hedges, expiring positions, new opportunities"
```

---

## 🔧 API Configuration

### Alpaca (Portfolio Data)
```bash
export ALPACA_API_KEY="YOUR_KEY"
export ALPACA_SECRET_KEY="YOUR_SECRET"
export ALPACA_PAPER=true  # Always use paper trading
```

### Kalshi (Prediction Markets)
```bash
export KALSHI_API_KEY_ID="YOUR_KEY_ID"
export KALSHI_PRIVATE_KEY="YOUR_PRIVATE_KEY"
```

### News (Sentiment Analysis)
```bash
export NEWSAPI_KEY="YOUR_KEY"
```

### Web Search (Market Research)
```bash
export BRAVE_API_KEY="YOUR_KEY"
export TAVILY_API_KEY="YOUR_KEY"
```

---

## 📊 Output Files

**Daily Reports:** `hedgemaster/reports/YYYY-MM-DD.md`  
**Active Hedges:** `hedgemaster/active-hedges.json`  
**Trade Log:** `hedgemaster/trades/YYYY-MM-DD.json`  
**Performance:** `hedgemaster/performance.csv`

---

## ⚠️ Safety Protocols

1. **Paper Trading Only** - No live Alpaca trades without explicit approval
2. **Max Hedge Size** - Never exceed 5% of position value per hedge
3. **Total Hedge Budget** - Max 10% of portfolio in active hedges
4. **Human Approval** - All trades require explicit user confirmation
5. **Auto-Expiry** - Hedges auto-close if not approved within 24 hours
6. **Logging** - All recommendations logged for performance tracking

---

## 🎓 Learning Loop

After each settled hedge:
- If hedge paid out: Log as "successful hedge"
- If hedge expired worthless: Log as "insurance cost"
- Update correlation scores based on actual outcomes
- Refine edge estimation algorithm
- Improve risk factor detection

---

## 🚀 Quick Start

1. Configure API keys in environment
2. Run initial portfolio scan:
   ```bash
   openclaw agent run HedgeMaster --mode "portfolio_scan"
   ```
3. Review and approve hedges via Discord/email
4. Monitor daily reports at 9 AM and 6 PM ET

---

**Created:** 2026-02-22  
**Version:** 1.0  
**Status:** Production Ready
