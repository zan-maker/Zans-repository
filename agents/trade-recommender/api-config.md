# TradeRecommender - API Configuration

**Last Updated:** Feb 14, 2026

## Web Search APIs

### Brave Search (Primary)
- **API Key:** `BSAqx7g5ob7ymEOAUfRduTetIOWPalN`
- **Endpoint:** `https://api.search.brave.com/res/v1/web/search`
- **Usage:** Kalshi market analysis, odds comparison

### Tavily (Backup)
- **API Key:** `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`
- **Endpoint:** `https://api.tavily.com/search`
- **Usage:** When Brave quota exceeded

## Market Data APIs

### AlphaVantage
- **API Key:** `T0Z2YW467F7PNA9Z`
- **Base URL:** `https://www.alphavantage.co/query`
- **Rate Limit:** 25 calls/day (free tier)
- **Priority Endpoints:**
  - `GLOBAL_QUOTE` - Real-time quotes (VIX, SPY)
  - `RSI` - Relative Strength Index
  - `MACD` - MACD indicator
  - `SECTOR` - Sector performance

### Alpaca Paper Trading
- **API Key:** `PKNDK5P66FCRH5P5ILPTVCYE7D`
- **Secret:** `z1fwAHFV9H8NY26XrZ2sSSxJggc8BwqiU2gPxVsy49V`
- **Base URL:** `https://paper-api.alpaca.markets/v2`
- **Usage:** Execute equity paper trades
- **Rate Limit:** 200 requests/minute

## News Intelligence API

### NewsAPI
- **API Key:** `fe52ac365edf464c9dca774544a40da3`
- **Endpoint:** `https://newsapi.org/v2/everything`
- **Usage:** Breaking news, earnings, political developments
- **Example:** `https://newsapi.org/v2/everything?q=kalshi+prediction+market&apiKey=KEY`

## Web Scraping APIs

### Zyte
- **API Key:** `8d3e9c7af6e948b088e96ad15ca21719`
- **Usage:** Kalshi market depth, alternative data
- **Endpoint:** `https://api.zyte.com/v1/extract`

### crawl4ai (with Z.ai)
- **Instructions:** https://dev.to/ali_dz/crawl4ai-the-ultimate-guide-to-ai-ready-web-crawling-2620
- **Usage:** AI-ready extraction from prediction market aggregators
- **Note:** Use Z.ai API key for enhanced extraction

## Data Sources Priority

### 1. Kalshi Markets (Primary)
- Direct market analysis
- Volume, pricing, implied probabilities

### 2. AlphaVantage (Market Context)
- VIX (fear gauge)
- S&P 500 trends
- Sector rotation
- Technical indicators

### 3. NewsAPI (Catalysts)
- Breaking news
- Earnings announcements
- Political developments
- Weather events

### 4. Web Search (Edge Discovery)
- Odds comparison
- Polling data vs market prices
- Expert predictions

### 5. Alpaca (Execution)
- Paper trades based on signals
- Portfolio tracking

## API Usage Workflow

### Daily Analysis:
1. **AlphaVantage** → Check VIX, SPY, sectors
2. **NewsAPI** → Scan for market-moving news
3. **Brave Search** → Research Kalshi markets, find edge
4. **Alpaca** → Execute paper trades if signals align

### Example:
```
1. VIX spikes (AlphaVantage)
2. NewsAPI: Political uncertainty breaking
3. Brave: Kalshi political markets mispriced
4. Alpaca: Execute hedge positions
```

## Rate Limits (Critical to Monitor)
- AlphaVantage: 25/day (STRICT)
- Alpaca: 200/minute (generous)
- NewsAPI: 100/day (free tier)
- Brave: 2000/month
- Zyte: 1000 (trial)

## AlphaVantage Call Priority (25/day limit)
1. VIX quote (daily) - 1 call
2. SPY quote (daily) - 1 call
3. Sector performance (daily) - 1 call
4. RSI for 3 key stocks (if trading) - 3 calls
5. Reserve 19 calls for research
