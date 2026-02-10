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
- **Environment Variables:**
  - `KALSHI_API_KEY_ID`
  - `KALSHI_PRIVATE_KEY`

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

## Arbitrage Detection Strategy

### Signal Sources
1. **DefeatBeta API** - Aggregated prediction market data
2. **Kalshi API** - Event market prices
3. **Polymarket** (if accessible) - Crypto prediction markets
4. **Web Search** - Real-time news and sentiment

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
