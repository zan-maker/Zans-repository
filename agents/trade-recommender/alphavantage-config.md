# AlphaVantage API Configuration

**API Key:** T0Z2YW467F7PNA9Z
**Status:** Active (Free Tier)
**Rate Limit:** 25 API calls per day
**Base URL:** https://www.alphavantage.co/query

## Available Endpoints

### Market Data
- `GLOBAL_QUOTE` - Real-time stock quotes
- `TIME_SERIES_INTRADAY` - Minute-by-minute data
- `TIME_SERIES_DAILY` - Daily OHLCV data

### Technical Indicators
- `RSI` - Relative Strength Index
- `MACD` - Moving Average Convergence Divergence
- `BBANDS` - Bollinger Bands
- `SMA` / `EMA` - Moving averages

### Market Intelligence
- `SECTOR` - Sector performance
- `MARKET_STATUS` - Market open/close

### Economic Data
- `TREASURY_YIELD` - Treasury yields
- `FEDERAL_FUNDS_RATE` - Fed funds rate
- `CPI` / `INFLATION` - Inflation data

## Usage Examples

```bash
# Get VIX quote
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=VIX&apikey=T0Z2YW467F7PNA9Z"

# Get S&P 500 RSI
curl "https://www.alphavantage.co/query?function=RSI&symbol=SPY&interval=daily&time_period=14&series_type=close&apikey=T0Z2YW467F7PNA9Z"

# Get sector performance
curl "https://www.alphavantage.co/query?function=SECTOR&apikey=T0Z2YW467F7PNA9Z"
```

## Integration Notes

- Use strategically due to 25 call/day limit
- Cache results when possible
- Prioritize VIX, SPY, and sector data for Kalshi correlation
- Log API usage in trade reports

**Connected:** Feb 13, 2026
