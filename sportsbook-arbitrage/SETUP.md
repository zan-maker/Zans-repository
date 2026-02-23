# RapidAPI Sportsbook Setup Guide

## Step 1: Subscribe to Sportsbook APIs

Go to **https://rapidapi.com/hub** and subscribe to these APIs (free tier):

### Recommended (in order of priority):

1. **The Odds API** ⭐ (Primary - best coverage)
   - URL: https://rapidapi.com/the-odds-api/api/the-odds-api
   - Free tier: 500 requests/day
   - Covers: 30+ bookmakers, all major sports
   - Subscribe to the "Free" plan

2. **API-Basketball** (NBA specific)
   - URL: https://rapidapi.com/api-sports/api/api-basketball
   - Free tier: 100 requests/day
   - Covers: NBA, NCAA, international

3. **API-Football** (Soccer)
   - URL: https://rapidapi.com/api-sports/api/api-football
   - Free tier: 100 requests/day
   - Covers: Premier League, Champions League, etc.

4. **API-NBA** (NBA focused)
   - URL: https://rapidapi.com/api-nba/api/api-nba
   - Free tier: 25 requests/day
   - Covers: NBA only

### How to Subscribe:
1. Click API link above
2. Click "Subscribe to Test" button
3. Select "Free" plan
4. Click "Subscribe"

## Step 2: Test the Connection

Once subscribed, run the discovery script:
```bash
cd sportsbook-arbitrage
python3 discover_apis.py
```

## Step 3: Start Fetching Odds

Once you see "✓ WORKING" for The Odds API:
```bash
python3 odds_fetcher.py
```

## System Architecture (Ready to Use)

The following components are built and ready:

| Component | Status | File |
|-----------|--------|------|
| API Discovery | ✅ Ready | `discover_apis.py` |
| Odds Fetcher | ✅ Ready | `odds_fetcher.py` |
| Odds Normalizer | ✅ Ready | `odds_fetcher.py` |
| Kalshi Connector | ⏳ Waiting for odds API | `kalshi_connector.py` |
| Mispricing Engine | ⏳ Waiting for Kalshi | `arbitrage_scanner.py` |

## Next Features (After API Works)

1. **Kalshi Integration** - Pull market prices
2. **Mispricing Scanner** - Compare odds vs Kalshi
3. **Alert System** - Notify when opportunities found
4. **Historical Tracker** - Log all detected mispricings

## Kalshi Context

Kalshi offers sports prediction markets:
- Binary contracts (Team A wins vs Team B wins)
- Prices range $0.01-$0.99 (implied probability)
- No vigorish - pure market pricing
- Sports: NBA, NFL, MLB, NHL, Soccer, Tennis

### Mispricing Formula:
```
Kalshi Implied Probability = Kalshi Price × 100
Sportsbook Implied Probability = (1 / Decimal Odds) × 100

Opportunity = |Kalshi Prob - Sportsbook Prob|
```

## Troubleshooting

If APIs still show "NOT SUBSCRIBED":
1. Clear browser cache
2. Log out/in to RapidAPI
3. Try subscribing again
4. Wait 5-10 minutes for subscription to propagate

## API Key Status
```
Key: c4c3e4c57b...3d5df8
Status: Valid but not subscribed
Next: Subscribe to The Odds API on RapidAPI
```
