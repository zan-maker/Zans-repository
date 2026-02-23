# Alpaca Paper Trading Configuration

**Account Type:** Paper Trading (Practice Account)
**Endpoint:** https://paper-api.alpaca.markets/v2
**API Key:** PKNDK5P66FCRH5P5ILPTVCYE7D
**Secret Key:** z1fwAHFV9H8NY26XrZ2sSSxJggc8BwqiU2gPxVsy49V

## Account Details
- **Base URL:** https://paper-api.alpaca.markets
- **Market Data:** https://data.alpaca.markets
- **WebSocket:** wss://stream.data.alpaca.markets/v2/iex

## Trading Rules (Enforced)

### Position Sizing
- **Max per trade:** $1,000
- **Max positions per day:** 3
- **Max total exposure:** $3,000 (3 positions × $1,000)
- **Min position:** $100

### Risk Management
- **Stop loss:** 5% from entry (auto-calculated)
- **Take profit:** 10% from entry (auto-calculated)
- **Max daily loss:** $150 (5% of $3K exposure)
- **Time stop:** Close after 5 days if no target hit

### Stock Screening
- **Min price:** $5.00 (no penny stocks)
- **Min daily volume:** $10M
- **Max spread:** 1% (ensures liquidity)
- **Allowed types:** Common stock only (no options, crypto)

## Strategy Parameters

### Entry Criteria (2+ required)
1. **Momentum:** 3-5 day uptrend confirmed
2. **Volume:** Above average volume (20-day MA)
3. **Catalyst:** Earnings, news, sector rotation
4. **Technical:** RSI 40-70 (not overbought/oversold)
5. **AlphaVantage signal:** VIX trend supports risk-on

### Exit Criteria (First to hit)
1. **Take profit:** +10% from entry
2. **Stop loss:** -5% from entry
3. **Time stop:** 5 days max hold
4. **Reversal signal:** AlphaVantage shows trend change

## API Endpoints Used

### Orders
- `POST /v2/orders` - Submit orders
- `GET /v2/orders` - List orders
- `DELETE /v2/orders/{order_id}` - Cancel order

### Positions
- `GET /v2/positions` - List positions
- `DELETE /v2/positions/{symbol}` - Close position

### Account
- `GET /v2/account` - Account details
- `GET /v2/account/portfolio/history` - Portfolio history

### Market Data
- `GET /v2/assets` - List assets
- `GET /v2/stocks/bars` - Historical bars

## Logging

All trades logged to:
- `agents/trade-recommender/revenue-tracker.csv` (Kalshi)
- `agents/trade-recommender/alpaca-portfolio.csv` (Alpaca)

## Authentication Header
```
Authorization: Basic base64(API_KEY:SECRET_KEY)
```

**Connected:** Feb 13, 2026
**Status:** Active
