# TastyTrade Trade Recommender

**Agent Name:** TastyTrade-Recommender  
**Purpose:** Generate options trades for TastyTrade account  
**Account Size:** $100 (small account strategy)  
**API Key:** 80e479d6235f546b188f9c86ec53bf80019c4bff

---

## 🎯 Strategy: Small Account Options

With $100, we focus on:
- **Defined risk strategies** (credit spreads, iron condors)
- **High probability setups** (>70% win rate)
- **Small position sizing** ($10-25 per trade)
- **Liquid underlyings** (SPY, QQQ, IWM, AAPL, TSLA)

---

## 📊 Trade Criteria

### Position Sizing
- Max per trade: $20 (20% of account)
- Max open positions: 3 ($60 total risk)
- Reserve: $40 for adjustments/rolling

### Setup Requirements
- **IV Rank:** >30% (sell premium when expensive)
- **Delta:** 0.15-0.30 (OTM, high probability)
- **Days to Expiration:** 20-45 days (sweet spot)
- **Probability of Profit:** >70%
- **Bid-Ask Spread:** <5% of width (liquidity)

### Preferred Strategies
1. **Credit Spreads** (bull put / bear call)
2. **Iron Condors** (range-bound, high IV)
3. **Cash-Secured Puts** (if wanting shares)

---

## 🔧 API Configuration

**TastyTrade API Docs:** https://tastytrade.com/api/  
**Base URL:** https://api.tastytrade.com  
**Auth:** Bearer token via API key

```bash
# Environment variable
export TASTYTRADE_API_KEY="80e479d6235f546b188f9c86ec53bf80019c4bff"
```

---

## 📅 Cron Job Schedule

**Daily Scan:** 9:30 AM ET (market open)  
**Midday Check:** 12:00 PM ET  
**Pre-Close:** 3:30 PM ET

---

## 📈 Trade Recommendation Format

```markdown
# 🎯 TastyTrade Recommendation

**Date:** YYYY-MM-DD  
**Account:** $100 Small Account Strategy

---

## Trade Setup

**Underlying:** SPY  
**Strategy:** Bull Put Spread  
**Direction:** Bullish/Neutral

### Strikes
- **Sell:** $585 Put (Delta: 0.20)
- **Buy:** $580 Put (Delta: 0.10)
- **Width:** $5
- **Expiration:** 30 DTE

### Metrics
- **Credit Received:** $0.85 ($85 per spread)
- **Max Risk:** $4.15 ($415 per spread)
- **Max Profit:** $85
- **Breakeven:** $584.15
- **Probability of Profit:** 72%
- **IV Rank:** 45%

### Position Sizing
- **Suggested:** 2 spreads ($170 risk, $8.50 buying power)
- **Max Loss:** $830 (if both go to max loss)
- **Target:** 50% of max profit ($42.50)
- **Stop Loss:** 200% of credit received ($170)

### Greeks (per spread)
- **Delta:** +8
- **Theta:** +2.5 (daily time decay)
- **Vega:** -12 (short volatility)

---

## 📝 Rationale

SPY showing relative strength, holding above 20-day MA. IV rank elevated at 45%, making premium selling attractive. Bull put spread allows us to profit if SPY stays above $585 (current price $590).

### Risk Management
- Exit at 50% profit (take $42.50, leave $42.50 on table)
- Roll if tested at 21 DTE
- Close at 50% loss if structure breaks

---

## ✅ EXECUTION CHECKLIST

- [ ] Check bid-ask spread < $0.10
- [ ] Verify account has $170 buying power
- [ ] Confirm IV Rank still >30%
- [ ] Place order: Sell to Open $585/$580 Put Spread
- [ ] Set GTC closing order at 50% profit

---

**Confidence:** 7/10  
**Urgency:** Medium (good setup, but not rushing)

---
Agent Manager
ImpactQuadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
```

---

## ⚠️ Small Account Rules

### DO
- [ ] Defined risk only (no naked options)
- [ ] High probability setups (>70% POP)
- [ ] Liquid underlyings only
- [ ] Track every trade in journal
- [ ] Take profits at 50%

### DON'T
- [ ] Never risk >25% on single trade
- [ ] No earnings plays (binary risk)
- [ ] No meme stocks (illiquid)
- [ ] No weekly options (<7 DTE)
- [ ] Never average down losers

---

## 📊 Performance Tracking

**File:** `tastytrade/performance.csv`

| Date | Underlying | Strategy | Credit | Result | P&L | Balance |
|------|-----------|----------|--------|--------|-----|---------|

---

## 🔒 Safety Protocols

1. **Paper trade first** - 10 trades minimum
2. **Position sizing** - Never exceed 20% per trade
3. **Daily review** - Check all positions at close
4. **Rolling rules** - Defined before entry
5. **Max loss** - Hard stop at 200% of credit

---

**Created:** 2026-02-24  
**Version:** 1.0  
**Status:** Active - $100 Account
