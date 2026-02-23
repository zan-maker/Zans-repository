# Stage 1: Portfolio Monitor - Daily Scan

**Your Role:** Portfolio Monitor for HedgeMaster  
**Task:** Scan Alpaca portfolio daily and identify positions needing hedges  
**Schedule:** Daily at 9:00 AM ET

---

## INPUT

Read from Alpaca API (paper trading):
```bash
# Alpaca API endpoints to query
GET /v2/positions
GET /v2/account
GET /v2/orders?status=open
```

---

## ANALYSIS CHECKLIST

For each position, check:

### 1. Price Movement Alerts
- [ ] Down >5% in last 24 hours?
- [ ] Down >10% in last 7 days?
- [ ] Down >20% in last 30 days?
- [ ] High volatility (>2x average daily range)?

### 2. Earnings Risk
- [ ] Earnings announcement within 7 days?
- [ ] Previous earnings surprise was >10%?
- [ ] Analyst estimates have high variance?

### 3. News Sentiment
- [ ] Negative news in last 48 hours?
- [ ] Regulatory concerns mentioned?
- [ ] CEO/CFO departure or insider selling?

### 4. Sector Rotation
- [ ] Sector ETF down >3% today?
- [ ] Sector showing sustained weakness (>5 days)?
- [ ] Rotation into defensive sectors detected?

### 5. Portfolio Concentration
- [ ] Single position >20% of portfolio?
- [ ] Sector exposure >30% of portfolio?
- [ ] Correlated positions (e.g., NVDA + AMD + TSM)?

---

## SCORING

Calculate **Hedge Urgency Score** (0-100):
```
urgency = (price_drop × 0.3) + (earnings_risk × 0.25) + 
          (news_risk × 0.2) + (sector_risk × 0.15) + 
          (concentration_risk × 0.1)

If urgency > 60: TRIGGER RISK ANALYST
If urgency > 80: HIGH PRIORITY ALERT
```

---

## OUTPUT

Generate report file: `hedgemaster/alerts/YYYY-MM-DD-HHMM.json`

```json
{
  "scan_date": "2026-02-22",
  "scan_time": "09:00 ET",
  "portfolio_value": 150000,
  "alerts": [
    {
      "ticker": "NVDA",
      "position_value": 25000,
      "urgency_score": 87,
      "priority": "HIGH",
      "triggers": [
        "Down 7.2% today",
        "Earnings in 5 days",
        "China export ban news"
      ],
      "recommendation": "Trigger Risk Analyst immediately"
    }
  ]
}
```

---

## DISCORD NOTIFICATION

Post to #cron-outputs-2:
```markdown
# 📊 HedgeMaster Daily Scan - 2026-02-22 9:00 AM ET

**Portfolio Value:** $150,000
**Positions Scanned:** 12
**Alerts Generated:** 3

## 🔴 HIGH PRIORITY (Urgency >80)

### NVDA - $25,000 position
- **Urgency:** 87/100
- **Triggers:** Down 7.2%, Earnings in 5 days, China ban news
- **Action:** Risk Analyst triggered

## 🟡 MEDIUM PRIORITY (Urgency 60-80)

### TSLA - $18,000 position  
- **Urgency:** 72/100
- **Triggers:** Down 4.8%, Regulatory concerns
- **Action:** Risk Analyst triggered

## ✅ LOW PRIORITY (Urgency <60)

### AAPL - $22,000 position
- **Urgency:** 45/100
- **Triggers:** Minor sector weakness
- **Action:** Monitor only

---
**Next Scan:** Tomorrow 9:00 AM ET
```

---

## TRIGGERS

For each alert with urgency >60:
1. Spawn **Risk Analyst** sub-agent
2. Pass ticker + position details
3. Include alert triggers list

---

## SAFETY CHECKS

- [ ] Only scan paper trading account (never live)
- [ ] Never trigger for positions <$1,000
- [ ] Never trigger for stable assets (bonds, cash)
- [ ] Log all scans for audit trail

---

**API Keys Required:**
- ALPACA_API_KEY
- ALPACA_SECRET_KEY
