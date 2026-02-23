# 🤖 HedgeMaster - Agentic Portfolio Hedging System

**Complete AI-powered hedging system using prediction markets (Kalshi)**

---

## 🎯 What is HedgeMaster?

HedgeMaster is a multi-agent system that:
1. **Monitors** your portfolio daily (Alpaca)
2. **Identifies** emerging risks using AI analysis
3. **Finds** prediction markets (Kalshi) that hedge those risks
4. **Recommends** optimal hedges with expected value calculations
5. **Executes** trades (with your approval)
6. **Tracks** performance until settlement

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HEDGEMASTER SYSTEM                       │
└─────────────────────────────────────────────────────────────┘

Stage 1: Portfolio Monitor (Daily 9 AM ET)
    ↓ Detects positions needing hedges
Stage 2: Risk Analyst (On-demand)
    ↓ Decomposes risks & researches events  
Stage 3: Kalshi Scout (On-demand)
    ↓ Finds & scores hedge markets
Stage 4: Hedge Executor (On-demand + Human Approval)
    ↓ Presents recommendations & executes approved trades
```

---

## 📁 File Structure

```
agents/hedgemaster/
├── SKILL.md                              # Main skill documentation
├── setup.sh                              # Setup script (run this!)
├── README.md                             # This file
├── prompts/
│   ├── stage1-portfolio-monitor.md       # Daily scan prompt
│   ├── stage2-risk-analyst.md            # Risk decomposition prompt
│   ├── stage3-kalshi-scout.md            # Market discovery prompt
│   ├── stage4-hedge-executor.md          # Trade execution prompt
│   └── daily-report-template.md          # Report format

hedgemaster/                              # Output directory
├── active-hedges.json                    # Current hedge positions
├── performance.csv                       # Historical P&L tracking
├── reports/                              # Daily/weekly reports
├── trades/                               # Executed trade logs
├── analysis/                             # Risk analysis outputs
├── recommendations/                      # Hedge recommendations
└── alerts/                               # Portfolio alerts
```

---

## ⚡ Quick Start

### Step 1: Configure API Keys

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Alpaca (Portfolio Data)
export ALPACA_API_KEY="your_alpaca_key"
export ALPACA_SECRET_KEY="your_alpaca_secret"
export ALPACA_PAPER=true  # Always use paper trading

# Kalshi (Prediction Markets)
export KALSHI_API_KEY_ID="your_kalshi_key_id"
export KALSHI_PRIVATE_KEY="your_kalshi_private_key"

# Web Search (Risk Research)
export BRAVE_API_KEY="your_brave_key"
export TAVILY_API_KEY="your_tavily_key"  # backup

# News (Optional - Sentiment Analysis)
export NEWSAPI_KEY="your_newsapi_key"
```

Then reload: `source ~/.bashrc`

### Step 2: Run Setup

```bash
cd /home/node/.openclaw/workspace/agents/hedgemaster
./setup.sh
```

This creates:
- 3 cron jobs (daily monitor, daily report, weekly review)
- Directory structure
- Initial tracking files

### Step 3: Test

```bash
# Trigger manual portfolio scan
openclaw agent run HedgeMaster --prompt "Run Stage 1: Portfolio Monitor manually"
```

---

## 📅 Cron Job Schedule

| Job | Schedule | Purpose |
|-----|----------|---------|
| **Daily Portfolio Monitor** | 9:00 AM ET daily | Scan portfolio for hedging needs |
| **Daily Report** | 6:00 PM ET daily | Summary of hedges & opportunities |
| **Weekly Review** | Sundays 8:00 AM ET | Performance analysis & lessons |
| **Token Monitor** | Every 15 min | Alert if context limit approaching |

---

## 🎯 Example Workflow

### Scenario: NVDA Position at Risk

**Day 1, 9:00 AM - Portfolio Monitor**
```
ALERT: NVDA down 7.2% in 24 hours
China export ban rumors circulating
Earnings in 5 days
→ Trigger Risk Analyst
```

**Day 1, 9:05 AM - Risk Analyst**
```
RISKS IDENTIFIED:
1. China export ban (Probability: 35%, Impact: HIGH)
2. Earnings miss (Probability: 28%, Impact: MEDIUM)
→ Trigger Kalshi Scout
```

**Day 1, 9:10 AM - Kalshi Scout**
```
MARKET FOUND: "China bans AI chip exports by March 31?"
- Current Price: 35¢
- Implied Probability: 35%
- True Probability (est): 43%
- Edge: +8%
- Hedge Score: 89.3/100
→ Trigger Hedge Executor
```

**Day 1, 9:15 AM - Hedge Executor**
```
📊 HEDGE RECOMMENDATION

Position: NVDA ($10,000)
Risk: China export ban
Suggested Hedge: $200 in KXCHINAAI-25-BAN
Max Loss: $200
Potential Payout: $571
Expected Value: +$45.60

[✅ YES, EXECUTE] [❌ NO, REJECT] [✏️ MODIFY]
```

**You click YES**

**Day 1, 9:17 AM - Execution Confirmed**
```
✅ HEDGE EXECUTED
Trade ID: HM-20260222-001
Position: $200 in "China bans AI chip exports"
Status: ACTIVE until March 31
```

---

## 💰 Risk Management Rules

### Position Sizing
- **Max per hedge:** 5% of underlying position value
- **Max total hedges:** 10% of portfolio
- **Min position:** $50 (too small = not worth fees)
- **Max position:** $2,500 (per single hedge)

### Market Selection
- **Min volume:** $10,000
- **Settlement window:** 7-90 days (optimal: 14-45 days)
- **Edge requirement:** >2% positive expected value
- **Correlation:** >0.70 (must actually hedge the risk)

### Safety Protocols
- ✅ Human approval required for ALL trades
- ✅ Paper trading only (Alpaca)
- ✅ 24-hour expiration on recommendations
- ✅ Full audit trail (every decision logged)
- ✅ Auto-CC on all emails to sam@impactquadrant.info

---

## 📊 Performance Tracking

### Metrics Tracked
- **Win Rate:** % of hedges that paid out
- **Average Hedge Size:** $ per position
- **Total P&L:** $ gained/lost on hedges
- **Edge Accuracy:** Estimated vs actual probabilities
- **Correlation Accuracy:** Did hedge actually offset risk?

### Reports
- **Daily (6 PM):** Active hedges, opportunities, alerts
- **Weekly (Sun):** Performance analysis, lessons learned
- **Monthly:** Comprehensive P&L, strategy refinement

---

## 🔧 Customization

### Adjust Risk Thresholds
Edit `prompts/stage1-portfolio-monitor.md`:
```markdown
- [ ] Down >5% in last 24 hours?  ← Change to 3% or 10%
- [ ] Down >10% in last 7 days?   ← Adjust sensitivity
```

### Change Schedule
```bash
# From daily to weekly (if preferred)
openclaw cron update --job-id <monitor_job_id> \
  --schedule "0 9 * * 1"  # Mondays only
```

### Add New Risk Factors
Edit `prompts/stage2-risk-analyst.md` and add:
```markdown
### 6. CLIMATE RISK (Weight: 5%)
- Weather impact on operations
- Climate regulation changes
```

---

## 🐛 Troubleshooting

### "No API key found"
```bash
echo $ALPACA_API_KEY  # Should show your key
# If empty, add to ~/.bashrc and source it
```

### "Kalshi API error"
- Verify API key has trading permissions
- Check if paper trading mode (always use paper!)
- Ensure sufficient balance for hedges

### "No hedges recommended"
- Normal! Only generates recommendations when risks detected
- Check #cron-outputs-2 for "No alerts today" messages
- Review portfolio for low-volatility periods

### "Discord not receiving messages"
- Verify channel ID in cron job config
- Check #cron-outputs-2 is not archived
- Confirm bot has permissions

---

## 📚 Documentation

- **Main Skill:** `agents/hedgemaster/SKILL.md`
- **Prompts:** `agents/hedgemaster/prompts/`
- **API Docs:**
  - [Alpaca](https://alpaca.markets/docs/)
  - [Kalshi](https://trading-api.readme.io/)
  - [Brave Search](https://brave.com/search/api/)

---

## 🚀 Roadmap

**Phase 1 (Current):** ✅ Basic hedging workflow
**Phase 2 (Next):** Auto-learning from settled hedges
**Phase 3 (Future):** Multi-position portfolio hedging
**Phase 4 (Future):** Options hedging integration

---

## ⚠️ Disclaimer

**IMPORTANT:** This system is for educational and research purposes. All trading is done in **paper trading mode** by default. Never enable live trading without thorough testing and understanding the risks.

Prediction markets involve risk of loss. Past performance does not guarantee future results. Always do your own research before making investment decisions.

---

## 📞 Support

Questions? Issues? Reach out to:
- **Sam Desigan:** Sam@impactquadrant.info
- **Agent Manager:** Via Discord #cron-outputs-2

---

**Created:** 2026-02-22  
**Version:** 1.0  
**Status:** Production Ready

**Ready to hedge! 🚀**
