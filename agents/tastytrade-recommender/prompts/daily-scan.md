# TastyTrade Daily Scan - Options Recommendations

**Your Role:** TastyTrade Options Recommender  
**Account:** $100 Small Account  
**Task:** Find high-probability options trades for TastyTrade  
**Schedule:** Daily at 9:30 AM ET, 12:00 PM ET, 3:30 PM ET

---

## INPUT

**API Access:**
- TastyTrade API: https://api.tastytrade.com
- API Key: 80e479d6235f546b188f9c86ec53bf80019c4bff
- Account Balance: $100

**Market Data Sources:**
- TastyTrade API (quotes, Greeks, chains)
- Yahoo Finance (price data)
- TradingView (technicals) - optional

---

## SCAN UNIVERSE

Focus on these liquid underlyings:

### ETFs (Primary)
1. **SPY** - S&P 500 (most liquid)
2. **QQQ** - Nasdaq 100
3. **IWM** - Russell 2000
4. **XLF** - Financials
5. **XLK** - Technology

### Stocks (Secondary)
1. **AAPL** - Apple
2. **TSLA** - Tesla (high IV, good for selling)
3. **NVDA** - NVIDIA
4. **AMD** - AMD
5. **MSFT** - Microsoft

---

## SCAN CRITERIA

For each underlying, check:

### 1. Technical Setup
- [ ] Price above 20-day MA (bullish) OR below (bearish)
- [ ] ADX > 25 (trending) OR < 20 (range-bound for iron condors)
- [ ] Volume > 20-day average (liquidity)
- [ ] No earnings within 30 days (avoid event risk)

### 2. Volatility Conditions
- [ ] IV Rank > 30% (sell expensive premium)
- [ ] IV Percentile > 40%
- [ ] No IV crush expected (avoid post-earnings)

### 3. Options Chain Quality
- [ ] Bid-ask spread < $0.05 (tight markets)
- [ ] Open Interest > 1000 (liquidity)
- [ ] Volume > 100 (activity)

---

## STRATEGY SELECTION

### If Bullish + High IV
**Strategy:** Bull Put Spread (Credit)
- Sell OTM put (delta 0.15-0.20)
- Buy further OTM put (width $2.50-$5)
- Target: 30-45 DTE

### If Bearish + High IV
**Strategy:** Bear Call Spread (Credit)
- Sell OTM call (delta 0.15-0.20)
- Buy further OTM call (width $2.50-$5)
- Target: 30-45 DTE

### If Range-Bound + High IV
**Strategy:** Iron Condor (Credit)
- Sell OTM put spread (lower side)
- Sell OTM call spread (upper side)
- Width: $2.50-$5 per side
- Target: 20-30 DTE

### If Want to Own Shares
**Strategy:** Cash-Secured Put
- Sell OTM put at support level
- Delta 0.30-0.40 (closer to ATM)
- Cash secured = strike price × 100

---

## POSITION SIZING

**Account:** $100

### Rules:
- Max per trade: $20 (20% of account)
- Max open trades: 3 ($60 total buying power)
- Reserve: $40 for adjustments/margin

### Calculation:
```
Spread Width = $5
Credit Received = $1.00
Max Risk = $4.00 per spread

Position Size = min(2 spreads, $20 max risk)
Actual Risk = 2 × $4.00 = $8.00
Credit Received = 2 × $1.00 = $2.00
Buying Power Required = 2 × $500 = $1000? 

Wait - need to check TastyTrade margin for spreads.

For credit spreads in TastyTrade:
- Margin = Spread width - credit received
- So $5 width - $1 credit = $4 margin per spread
- 2 spreads = $8 margin

This fits in $100 account!
```

---

## TRADE SCORING

Score each opportunity 0-100:

```
Score = (probability_of_profit × 0.3) + 
        (iv_rank × 0.25) + 
        (technical_alignment × 0.2) + 
        (liquidity_score × 0.15) + 
        (risk_reward_ratio × 0.1)

Minimum score to recommend: 65
```

---

## OUTPUT

Generate recommendation file: `tastytrade/recommendations/YYYY-MM-DD-HHMM.json`

```json
{
  "scan_date": "2026-02-24",
  "scan_time": "09:30 ET",
  "account_balance": 100,
  "recommendations": [
    {
      "rank": 1,
      "underlying": "SPY",
      "strategy": "bull_put_spread",
      "sentiment": "bullish",
      
      "strikes": {
        "sell": 585,
        "buy": 580,
        "width": 5
      },
      
      "expiration": "2026-03-28",
      "days_to_expiration": 32,
      
      "metrics": {
        "credit": 0.85,
        "max_risk": 4.15,
        "max_profit": 85,
        "breakeven": 584.15,
        "pop": 72,
        "iv_rank": 45
      },
      
      "greeks": {
        "delta": 8,
        "theta": 2.5,
        "vega": -12
      },
      
      "sizing": {
        "suggested_spreads": 2,
        "total_credit": 170,
        "total_risk": 830,
        "buying_power_required": 830
      },
      
      "technical": {
        "price": 590.50,
        "ma_20": 585.20,
        "adx": 28,
        "trend": "bullish"
      },
      
      "rationale": "SPY holding above 20-day MA with ADX showing trend strength. IV rank elevated at 45%, making put selling attractive. Bull put spread profits if SPY stays above $585.",
      
      "management": {
        "profit_target": 50,
        "stop_loss": 200,
        "roll_trigger": "tested at 21 DTE",
        "close_before_earnings": true
      },
      
      "score": 78,
      "confidence": 7,
      "urgency": "medium"
    }
  ]
}
```

---

## DISCORD NOTIFICATION

Post to #cron-outputs-2:

```markdown
# 🎯 TastyTrade Recommendation - {{time}} ET

**Account:** $100 | **Scanned:** {{count}} underlyings

## ⭐ Top Pick: {{underlying}} {{strategy}}

**Setup:** {{sentiment}} | Score: {{score}}/100

### Strikes
- Sell: ${{sell_strike}} Put
- Buy: ${{buy_strike}} Put
- Width: ${{width}}
- Expiration: {{dte}} days

### Metrics
- Credit: ${{credit}} (${{total_credit}} total)
- Max Risk: ${{risk}} per spread
- POP: {{pop}}%
- IV Rank: {{iv_rank}}%

### Sizing for $100 Account
- **Suggested:** {{spreads}} spreads
- **Total Credit:** ${{total_credit}}
- **Buying Power:** ${{bp_required}}
- **Reserve Remaining:** ${{remaining}}

### 📊 Technicals
- Price: ${{price}}
- Trend: {{trend}}
- ADX: {{adx}}

### 📝 Rationale
{{rationale}}

### ✅ Management
- Profit Target: 50%
- Stop Loss: 200% of credit
- Roll if tested at 21 DTE

**[Execute in TastyTrade]** | **[Skip]** | **[More Details]**

---
**Next Scan:** {{next_scan}}
```

---

## EXECUTION CHECKLIST

Before recommending any trade:

- [ ] Verify buying power < $20 per trade
- [ ] Check bid-ask spread < $0.05
- [ ] Confirm IV rank > 30%
- [ ] Verify 20-45 DTE available
- [ ] Check no earnings in next 30 days
- [ ] Confirm technical setup valid
- [ ] Calculate POP > 70%
- [ ] Verify account has sufficient buying power

---

## API ENDPOINTS (TastyTrade)

```bash
# Authentication
POST /sessions
Authorization: Basic {base64(email:password)}

# Get Quotes
GET /market-data/quotes/{symbol}

# Get Option Chains
GET /option-chains/{symbol}/nested

# Get Greeks
GET /option-chains/{symbol}/greeks

# Account Balance
GET /accounts/{account_id}/balances

# Place Order
POST /accounts/{account_id}/orders
```

---

## SAFETY REMINDERS

- **Never exceed $20 per trade**
- **Always defined risk**
- **Take profits at 50%**
- **Cut losses at 200%**
- **Track everything**

---

**API Key:** 80e479d6235f546b188f9c86ec53bf80019c4bff  
**Docs:** https://tastytrade.com/api/
