# API Configuration for TradeRecommender

## DefeatBeta API Integration
**Repository:** https://github.com/defeat-beta/defeatbeta-api
**Purpose:** Prediction market data aggregation and arbitrage signals

### Connection Details
- **Base URL:** (To be configured based on deployment)
- **Authentication:** API Key
- **Environment Variable:** `DEFEATBETA_API_KEY`

### Key Endpoints
```
GET /markets - List all prediction markets
GET /markets/{id}/odds - Current odds/prices
GET /arbitrage/opportunities - Detected arbitrage signals
GET /markets/{id}/orderbook - Full orderbook depth
```

## Kalshi API Integration
**Documentation:** https://trading-api.readme.io/reference/
**Purpose:** Event-based trading and arbitrage

### Connection Details
- **Base URL:** https://trading-api.kalshi.com/trade-api/v2
- **Authentication:** RSA Key Pair
- **API Key ID:** `fb109d35-efc3-42b1-bdba-0ee2a1e90ef8`
- **Private Key:** Stored securely at `keys/kalshi_private.pem`
- **File Permissions:** 600 (owner read/write only)

### Environment Variables
```bash
export KALSHI_API_KEY_ID="fb109d35-efc3-42b1-bdba-0ee2a1e90ef8"
export KALSHI_PRIVATE_KEY_PATH="./keys/kalshi_private.pem"
```

### Security Notes
- Private key file permissions set to 600
- Key never committed to git (added to .gitignore)
- Never log or expose private key in output

### Key Endpoints
```
GET /markets - Available markets
GET /markets/{market_id} - Market details
GET /markets/{market_id}/orderbook - Orderbook
GET /portfolio/balance - Account info
POST /orders - Place order (paper trading recommended)
```

### Rate Limits
- 200 requests per minute
- Use exponential backoff on 429 errors

## Web Search Integration
**Primary:** Brave Search API
**Backup:** Tavily API

### Usage Pattern
1. Use Brave for general web search
2. Fallback to Tavily if Brave quota exceeded
3. Focus on financial news, earnings, regulatory updates

## Sportsbook APIs Integration

### Primary: RapidAPI Sportsbook API
**Source:** https://rapidapi.com/sportsbook-api-sportsbook-api-default/api/sportsbook-api2
**Purpose:** Sportsbook odds aggregation for arbitrage with Kalshi prediction markets

### Connection Details
- **Base URL:** https://sportsbook-api2.p.rapidapi.com
- **Authentication:** RapidAPI Key (Header)
- **Environment Variable:** `RAPIDAPI_KEY=c4c3e4c57bmshc1a4bd30b0c8bd4p1c4595jsncab6793d5df8`
- **Headers Required:**
  - `X-RapidAPI-Key`: API key
  - `X-RapidAPI-Host`: sportsbook-api2.p.rapidapi.com

### Key Endpoints
```
GET /sports - List available sports
GET /leagues?sport={sport} - Leagues for a sport
GET /games?league={league} - Games/events
GET /odds?gameId={gameId} - Odds for specific game
GET /markets?gameId={gameId} - Available betting markets
GET /books - List supported sportsbooks
```

### Rate Limits
- 100 requests/month on free tier
- Upgrade to paid tier for production use
- Use caching to minimize API calls

---

### Backup: The Odds API
**Source:** https://the-odds-api.com/
**Purpose:** Alternative sportsbook odds provider (fallback if RapidAPI limits hit)

### Connection Details
- **Base URL:** https://api.the-odds-api.com/v4
- **Authentication:** API Key (Query Parameter)
- **API Key:** `a2584115f9fd3d4520f34449495a9d4f`
- **Environment Variable:** `THE_ODDS_API_KEY=a2584115f9fd3d4520f34449495a9d4f`

### Key Endpoints
```
GET /sports - List in-season sports
GET /sports/{sport}/odds - Odds for a sport
GET /sports/{sport}/events - List events
GET /sports/{sport}/events/{eventId}/odds - Odds for specific event
```

### Rate Limits
- 500 requests/month on free tier
- Check `x-requests-remaining` header
- Use regions/markets params to filter data

### Query Parameters
- `regions`: `us`, `us2`, `uk`, `au`, `eu`
- `markets`: `h2h` (moneyline), `spreads`, `totals`, `outrights`
- `oddsFormat`: `decimal` or `american`
- `dateFormat`: `iso` or `unix`

### Example Request
```
GET https://api.the-odds-api.com/v4/sports/basketball_nba/odds
    ?apiKey=a2584115f9fd3d4520f34449495a9d4f
    &regions=us
    &markets=h2h
    &oddsFormat=american
```

---

### Data Provided (Both APIs)
- Moneyline odds
- Spread/point spread
- Totals (over/under)
- Game props
- Player props
- Live odds (if available)

### Arbitrage Use Cases
1. **Kalshi ↔ Sportsbook**: Event contracts vs traditional odds
2. **Cross-book**: Compare odds across multiple sportsbooks
3. **Line movement**: Track odds changes over time
4. **Vig analysis**: Calculate sportsbook margins

### Failover Strategy
1. Try RapidAPI first (cached responses)
2. If rate limited, switch to The Odds API
3. If both limited, use cached data only
4. Log which API is being used

---

## Arbitrage Detection Strategy

### Signal Sources
1. **DefeatBeta API** - Aggregated prediction market data
2. **Kalshi API** - Event market prices
3. **Sportsbook API** - Sportsbook odds for comparison
4. **Polymarket** (if accessible) - Crypto prediction markets
5. **Web Search** - Real-time news and sentiment

### Detection Logic
1. Query all APIs for current prices on related markets
2. Apply Bregman Projection algorithm (see skills/bregman-projection-arbitrage.md)
3. Calculate divergence/mispricing
4. Validate with web search (is there a reason for the spread?)
5. Output opportunities meeting MIN_PROFIT_PCT threshold

### Safety Parameters
```python
MIN_PROFIT_PCT = 0.5  # Minimum 0.5% profit after fees
MAX_POSITION_SIZE = 10  # Maximum 10% of portfolio
MAX_SLIPPAGE = 5  # Maximum 5% slippage
PAPER_TRADING = True  # Start with paper trading only
```
