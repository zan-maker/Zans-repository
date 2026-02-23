# API Documentation Reference

## Alpaca API

### Base URL
```
https://paper-api.alpaca.markets/v2
```

### Authentication
Header: `APCA-API-KEY-ID: PKNDK5P66FCRH5P5ILPTVCYE7D`
Header: `APCA-API-SECRET-KEY: z1fwAHFV9H8NY26XrZ2sSSxJggc8BwqiU2gPxVsy49V`

### Key Endpoints

#### Get Assets (Stocks)
```
GET /v2/assets?status=active&asset_class=us_equity
```
Response: List of assets with symbol, name, exchange, tradable status.

#### Get Option Contracts
```
GET /v2/options/contracts?underlying_symbol=AAPL&status=active
```
Parameters:
- `underlying_symbol` (required): Stock ticker
- `status`: active, inactive
- `expiration_date_gte`: Filter by expiration
- `expiration_date_lte`: Filter by expiration
- `type`: call or put
- `strike_price_gte/lte`: Strike range

Response:
```json
{
  "option_contracts": [
    {
      "id": "...",
      "symbol": "AAPL240119C00180000",
      "name": "AAPL Jan 19 2024 180 Call",
      "underlying_symbol": "AAPL",
      "expiration_date": "2024-01-19",
      "strike_price": "180.00",
      "type": "call",
      "size": 100,
      "underlying_asset_id": "..."
    }
  ]
}
```

#### Get Option Latest Quote
```
GET /v2/options/quotes/latest?symbol=AAPL240119C00180000
```

Response:
```json
{
  "quote": {
    "symbol": "AAPL240119C00180000",
    "bid_price": "2.45",
    "bid_size": 10,
    "ask_price": "2.50",
    "ask_size": 15,
    "timestamp": "..."
  }
}
```

#### Get Historical Bars
```
GET /v2/stocks/AAPL/bars?timeframe=1Day&start=2024-01-01&end=2024-01-19
```
Response: OHLCV data for volatility calculations.

#### Get Option Greeks (via snapshots)
```
GET /v2/options/snapshots/AAPL240119C00180000
```
Response includes: implied_volatility, delta, gamma, theta, vega, rho.

---

## Finnhub API

### Base URL
```
https://finnhub.io/api/v1
```

### Authentication
Query param: `token=d6bq93hr01qp4li0f2h0d6bq93hr01qp4li0f2hg`

### Key Endpoints

#### Company Profile
```
GET /stock/profile2?symbol=AAPL&token={token}
```
Response: name, industry, sector, market cap.

#### Quote (Real-time)
```
GET /quote?symbol=AAPL&token={token}
```
Response:
```json
{
  "c": 185.92,    // Current price
  "d": 1.25,      // Change
  "dp": 0.68,     // Percent change
  "h": 186.50,    // High
  "l": 184.20,    // Low
  "o": 184.50,    // Open
  "pc": 184.67,   // Previous close
  "t": 1705689600 // Timestamp
}
```

#### Financial Statements
```
GET /stock/financials-reported?symbol=AAPL&token={token}
```
For: Revenue, Net Income, EBITDA, Margins, Cash Flow.

#### Analyst Recommendations
```
GET /stock/recommendation?symbol=AAPL&token={token}
```
Response: buy, hold, sell counts by period.

#### Insider Transactions
```
GET /stock/insider-transactions?symbol=AAPL&token={token}
```
Response: Name, share count, transaction type (P=Purchase, S=Sale).

#### Earnings Calendar
```
GET /calendar/earnings?from=2024-01-01&to=2024-01-31&symbol=AAPL&token={token}
```

#### Company News
```
GET /company-news?symbol=AAPL&from=2024-01-15&to=2024-01-19&token={token}
```
Response:
```json
[
  {
    "datetime": 1705689600,
    "headline": "...",
    "source": "...",
    "summary": "...",
    "url": "..."
  }
]
```

#### Stock Fundamentals (Metrics)
```
GET /stock/metric?symbol=AAPL&metric=all&token={token}
```
Response: P/E, P/S, P/B, ROE, ROA, Debt/Equity, etc.

---

## FRED API

### Base URL
```
https://api.stlouisfed.org/fred
```

### Authentication
Query param: `api_key=c00b92a9c6a70cb70efc3201cfb9bb5f`

### Key Endpoints

#### Get Series Data
```
GET /series/observations?series_id=VIXCLS&api_key={key}&file_type=json
```

Important Series IDs:
- `VIXCLS` - CBOE Volatility Index
- `DGS10` - 10-Year Treasury Constant Maturity Rate
- `UNRATE` - Unemployment Rate
- `CPIAUCSL` - Consumer Price Index for All Urban Consumers
- `GDP` - Gross Domestic Product
- `UMCSENT` - University of Michigan Consumer Sentiment
- `ISMMANIT` - ISM Manufacturing Index
- `PAYEMS` - All Employees, Total Nonfarm
- `RSAFS` - Advance Retail Sales

Response:
```json
{
  "observations": [
    {
      "date": "2024-01-18",
      "value": "13.30"
    }
  ]
}
```

#### Get Latest Observation
```
GET /series/observations?series_id=VIXCLS&api_key={key}&sort_order=desc&limit=1&file_type=json
```

---

## Data Point Mapping

### Fundamental Metrics → Sources

| Metric | Source | Endpoint |
|--------|--------|----------|
| EPS | Finnhub | /stock/financials-reported |
| Revenue | Finnhub | /stock/financials-reported |
| Net Income | Finnhub | /stock/financials-reported |
| EBITDA | Finnhub | /stock/financials-reported |
| P/E Ratio | Finnhub | /stock/metric |
| Price/Sales | Finnhub | /stock/metric |
| Gross Margin | Finnhub | /stock/financials-reported |
| Operating Margin | Finnhub | /stock/financials-reported |
| FCF Yield | Calculate | FCF / Market Cap |
| Insider Transactions | Finnhub | /stock/insider-transactions |
| Forward Guidance | Finnhub | /stock/financials-reported |
| PEG Ratio | Finnhub | /stock/metric |

### Options Data → Sources

| Metric | Source | Endpoint |
|--------|--------|----------|
| Implied Volatility | Alpaca | /v2/options/snapshots/{symbol} |
| Delta | Alpaca | /v2/options/snapshots/{symbol} |
| Gamma | Alpaca | /v2/options/snapshots/{symbol} |
| Theta | Alpaca | /v2/options/snapshots/{symbol} |
| Vega | Alpaca | /v2/options/snapshots/{symbol} |
| Open Interest | Alpaca | /v2/options/snapshots/{symbol} |
| Volume | Alpaca | /v2/options/snapshots/{symbol} |
| IV Rank | Calculate | (Current - 52W Low) / (52W High - 52W Low) |

### Price Data → Sources

| Metric | Source | Endpoint |
|--------|--------|----------|
| OHLCV Daily | Alpaca | /v2/stocks/{symbol}/bars |
| Historical Volatility | Calculate | StdDev of log returns × √252 |
| 50/100/200 MA | Calculate | Rolling mean of closes |
| RSI | Calculate | 14-period RSI |
| MACD | Calculate | 12/26/9 EMAs |
| Bollinger Bands | Calculate | 20-period MA ± 2 StdDev |
| VWAP | Calculate | Cumulative (Price × Volume) / Cumulative Volume |
| ATR | Calculate | 14-period Average True Range |

### Macro Data → Sources

| Indicator | FRED Series ID |
|-----------|---------------|
| VIX | VIXCLS |
| 10Y Treasury | DGS10 |
| Unemployment | UNRATE |
| CPI | CPIAUCSL |
| GDP | GDP |
| Consumer Confidence | UMCSENT |
| ISM Manufacturing | ISMMANIT |
| Nonfarm Payrolls | PAYEMS |
| Retail Sales | RSAFS |

---

## Black-Scholes Calculation

For PoP (Probability of Profit) calculations:

```python
def black_scholes_probability(S, K, T, r, sigma, option_type='put'):
    """
    S: Current stock price
    K: Strike price
    T: Time to expiration (years)
    r: Risk-free rate (use DGS10/100)
    sigma: Implied volatility (decimal)
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'put':
        # Probability put expires ITM (stock below strike)
        return norm.cdf(-d2)
    else:
        # Probability call expires ITM (stock above strike)
        return norm.cdf(d2)
```

PoP for credit spreads:
- **Bull Put Spread**: PoP = 1 - Probability(short_put_expires_ITM)
- **Bear Call Spread**: PoP = 1 - Probability(short_call_expires_ITM)

---

## Piotroski F-Score Calculation

9-point scoring system (Finnhub fundamentals):

**Profitability (4 points):**
1. Positive Net Income
2. Positive Operating Cash Flow
3. ROA improvement YoY
4. Operating Cash Flow > Net Income

**Leverage/Liquidity (3 points):**
5. Long-term debt ratio down YoY
6. Current ratio up YoY
7. No new shares issued

**Efficiency (2 points):**
8. Gross margin up YoY
9. Asset turnover up YoY

---

## Altman Z-Score Calculation

```
Z = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 1.0*E

Where:
A = Working Capital / Total Assets
B = Retained Earnings / Total Assets
C = EBIT / Total Assets
D = Market Cap / Total Liabilities
E = Revenue / Total Assets

Interpretation:
Z > 3.0: Safe (low bankruptcy risk)
1.8 < Z < 3.0: Grey zone
Z < 1.8: Distress (high bankruptcy risk)
```
