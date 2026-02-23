# Sportsbook-Kalshi Arbitrage System

## Status: ✅ Architecture Complete | ⏳ Waiting for API Subscription

## What We Built

| Component | Status | Description |
|-----------|--------|-------------|
| `odds_fetcher.py` | ✅ Ready | RapidAPI (The Odds API) connector with normalization |
| `kalshi_connector.py` | ✅ Ready | Kalshi prediction markets API client |
| `arbitrage_scanner.py` | ✅ Ready | Mispricing detection engine |
| `main.py` | ✅ Ready | Orchestrator bot |
| `discover_apis.py` | ✅ Ready | API availability tester |

## Quick Start

### Step 1: Subscribe to RapidAPI (5 minutes)
1. Go to https://rapidapi.com/the-odds-api/api/the-odds-api
2. Click **"Subscribe to Test"**
3. Select **"Free"** plan (500 requests/day)
4. Subscribe

### Step 2: Verify API Access
```bash
cd sportsbook-arbitrage
python3 discover_apis.py
```

Expected output:
```
The Odds API:
  Status: ✓ WORKING
```

### Step 3: Run Live Scan
```bash
python3 -c "
from main import ArbitrageBot
bot = ArbitrageBot('c4c3e4c57bmshc1a4bd30b0c8bd4p1c4595jsncab6793d5df8')
bot.run_full_scan(sport='basketball_nba')
"
```

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  SPORTSBOOKS    │     │   KALSHI     │     │   ARBITRAGE     │
│  (RapidAPI)     │────→│  (Exchange)  │────→│    ENGINE       │
│                 │     │              │     │                 │
│ • DraftKings    │     │ • NBA        │     │ • Compare probs │
│ • FanDuel       │     │ • NFL        │     │ • Detect edge   │
│ • BetMGM        │     │ • MLB        │     │ • Alert user    │
│ • 30+ others    │     │ • NHL        │     │                 │
└─────────────────┘     └──────────────┘     └─────────────────┘
```

## Mispricing Formula

```
Sportsbook Implied Probability = 1 / Decimal Odds × 100
Kalshi Implied Probability = Kalshi Price × 100

Mispricing = |Sportsbook% - Kalshi%|

If Mispricing > 3% → Flag as opportunity
```

## Example Opportunity

| Metric | Sportsbook | Kalshi |
|--------|-----------|--------|
| Lakers to win | 1.80 (-125) | $0.52 |
| Implied Prob | 55.56% | 52% |
| **Mispricing** | **3.56%** | Edge → Buy on Kalshi |

## File Structure

```
sportsbook-arbitrage/
├── README.md              # System overview
├── SETUP.md              # Detailed setup guide
├── QUICKSTART.md         # This file
├── odds_fetcher.py       # Sportsbook API client
├── kalshi_connector.py   # Kalshi API client
├── arbitrage_scanner.py  # Detection engine
├── main.py               # Orchestrator
├── discover_apis.py      # API tester
├── reports/              # Generated reports
└── data/                 # Opportunity exports
```

## Next Steps After API Works

1. **Test with real data** - Run `python3 main.py`
2. **Tune thresholds** - Adjust `threshold_pct` (default 3%)
3. **Add alerts** - Discord/email notifications
4. **Track history** - Log all detections
5. **Backtest** - Validate edge with historical data

## Troubleshooting

**"NOT SUBSCRIBED" error**
→ Go to RapidAPI and subscribe to The Odds API (free tier)

**No opportunities found**
→ Markets are efficient OR threshold too high OR low liquidity

**Kalshi data missing**
→ Kalshi API is public, check market hours (sports markets close at game time)

## Support

- The Odds API docs: https://the-odds-api.com
- Kalshi API docs: https://trading-api.readme.io
- RapidAPI hub: https://rapidapi.com/hub
