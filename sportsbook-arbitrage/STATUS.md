# Sportsbook-Kalshi Arbitrage System - Status Report

## ✅ What's Working

### 1. Sportsbook Odds API (The Odds API)
- **Status**: ✅ **FULLY OPERATIONAL**
- **API Key**: a2584115f9fd3d4520f34449495a9d4f
- **Rate Limit**: 500 requests/day (free tier)
- **Coverage**: 30+ bookmakers, all major sports

**Live Data Example (NBA - Feb 20, 2026)**:
```
Wizards vs Pacers
  Wizards: 2.48 (+148) @ BetRivers → 40.3% implied
  Pacers:  1.62 (-161) @ DraftKings → 61.7% implied

Hawks vs 76ers
  Hawks:   2.66 (+166) @ FanDuel
  76ers:   1.57 (-175) @ BetRivers
```

### 2. Odds Processing
- ✅ Best price extraction across all bookmakers
- ✅ Vig removal for true probability calculation
- ✅ American/Decimal odds conversion
- ✅ Implied probability calculation

### 3. Arbitrage Detection Engine
- ✅ Mispricing calculation: |Sportsbook% - Kalshi%|
- ✅ Configurable threshold (default 3%)
- ✅ Confidence scoring based on volume
- ✅ Edge direction detection

## ⚠️ Kalshi API Limitation

### Current Issue
Kalshi's public API endpoint (`api.elections.kalshi.com`) only returns:
- **Multi-game parlay markets** (e.g., "yes Michigan, yes Louisville, yes over 149.5...")
- **Futures/Prop markets** (e.g., "NBA Championship Winner", "Rookie of the Year")
- **Quarter/Half markets**

**Missing**: Single game moneyline markets (Team A defeats Team B)

### Root Cause
The Kalshi API appears to have changed:
- Old endpoint: `trading-api.kalshi.com/v1` - Had game markets
- New endpoint: `api.elections.kalshi.com/trade-api/v2` - Shows parlays/futures only

### RSA Authentication
Kalshi API key provided and configured:
- Key ID: fb109d35-efc3-42b1-bdba-0ee2a1e90ef8
- Auth method: RSA signature (requires `cryptography` library)

**Note**: Markets load without auth, but single game markets not visible in either mode.

## 🔧 Workarounds

### Option 1: Manual Kalshi Input
Use `kalshi_manual.py` to input current Kalshi prices:

```python
from kalshi_manual import KalshiManualInput

kalshi = KalshiManualInput()
kalshi.add_market(
    ticker="NBA-WAS-vs-IND",
    yes_price=0.39,  # Wizards win
    no_price=0.62,   # Pacers win
    volume=25000
)
```

### Option 2: Kalshi Website Scraping
Check Kalshi website manually for game tickers, then fetch via API:
```python
# After finding ticker on kalshi.com
market = client.get_market("SPECIFIC_TICKER_HERE")
```

### Option 3: Different Data Source
Consider alternative prediction markets:
- **Polymarket** (crypto-based, sports markets)
- **PredictIt** (political/sports, US-based)

## 📊 System Capabilities

### Files Created
| File | Purpose | Status |
|------|---------|--------|
| `odds_fetcher.py` | The Odds API client | ✅ Working |
| `kalshi_connector.py` | Kalshi API with RSA auth | ⚠️ Partial |
| `arbitrage_scanner.py` | Mispricing detection | ✅ Working |
| `arbitrage_live.py` | Live scan orchestrator | ✅ Working |
| `live_odds_test.py` | View sportsbook odds | ✅ Working |
| `kalshi_manual.py` | Manual Kalshi input | ✅ Working |

### Usage

**View Live Odds:**
```bash
python3 live_odds_test.py
```

**Run Arbitrage Scan (with manual Kalshi):**
```bash
python3 arbitrage_live.py
```

**Full System (when Kalshi markets available):**
```bash
python3 main.py
```

## 📈 Next Steps

### Immediate
1. Check Kalshi website (kalshi.com) for NBA game market tickers
2. Use `fetch_kalshi_market(ticker)` to pull specific markets
3. Run comparison with sportsbook odds

### Short-term
1. Contact Kalshi support about game market API access
2. Set up market monitoring with alerts
3. Build position sizing calculator

### Long-term
1. Add Polymarket as secondary prediction market source
2. Build historical database of mispricings
3. Automated alert system (Discord/email)

## 🎯 Example Opportunity (Hypothetical)

If Kalshi had current market:
```
Wizards vs Pacers
  Sportsbook: Wizards 2.48 (+148) = 40.3%
  Kalshi:     Wizards $0.36 = 36%
  
  Mispricing: 4.3%
  Action: Buy Wizards on Kalshi at $0.36
  Edge: (1/0.36 - 1) = 178% return if win
```

## Summary

**Sportsbook API**: Fully operational, 13 NBA games live  
**Kalshi API**: Connected, but game markets not in public feed  
**Arbitrage Engine**: Ready and tested  
**Blocker**: Finding correct Kalshi market tickers for NBA games

**Recommendation**: Use manual Kalshi input mode while investigating API market structure, or scrape kalshi.com for game market tickers.
