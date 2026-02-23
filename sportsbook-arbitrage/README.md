# Sportsbook-Kalshi Arbitrage System

## Architecture

### Data Sources
1. **RapidAPI - The Odds API** (primary sportsbook aggregator)
   - 30+ bookmakers
   - Real-time odds updates
   - Multiple sports/markets
   - Your key: c4c3e4c57bmshc1a4bd30b0c8bd4p1c4595jsncab6793d5df8

2. **Kalshi API** (prediction markets)
   - Sports event contracts
   - Binary outcome markets
   - Real-time pricing

### Mispricing Detection Logic
```
Sportsbook Implied Probability = 1 / (Decimal Odds) * 100
Kalshi Implied Probability = Kalshi Price * 100

Mispricing = |Sportsbook Prob - Kalshi Prob|

Opportunity exists when:
- Mispricing > threshold (e.g., 3-5%)
- Sufficient liquidity on both sides
- Timing allows execution
```

### Implementation Plan

#### Phase 1: Core Infrastructure
1. RapidAPI connector (The Odds API)
2. Kalshi API connector
3. Odds normalization engine
4. Mispricing calculator

#### Phase 2: Opportunity Detection
1. Real-time scanner
2. Filter engine (sports, mispricing threshold, liquidity)
3. Alert system

#### Phase 3: Execution Support
1. Position sizing calculator
2. P&L tracker
3. Historical analysis

## The Odds API Endpoints (RapidAPI)

### Key Endpoints:
- `GET /sports` - List available sports
- `GET /odds` - Get odds for a sport
- `GET /events/{id}/odds` - Get odds for specific event

### Markets to Focus:
- `h2h` - Moneyline (best for Kalshi comparison)
- `spreads` - Point spreads
- `totals` - Over/under

## Kalshi Sports Markets

Kalshi now offers sports prediction markets:
- NBA games
- NFL games
- MLB games
- NHL games
- Soccer matches
- Tennis matches

Markets are binary (Team A wins vs Team B wins).

## Next Steps
1. Test RapidAPI connection
2. Build odds fetcher
3. Map Kalshi markets to sportsbook events
4. Build comparison engine
