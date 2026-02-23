# Options Recommender

A quant-grade options credit spread recommendation system using the **Convergence Scoring Model**.

## What It Does

Analyzes S&P 500 stocks across 4 independent scoring categories:
1. **Vol-Edge** - IV vs HV mispricing detection
2. **Quality** - Piotroski F-Score + Altman Z-Score
3. **Regime** - Macro environment fit (FRED data)
4. **Info-Edge** - Analyst, insider, news signals

Generates exactly **5 high-probability credit spread trades** with full risk analysis.

## Data Sources

| Source | Data | API Key |
|--------|------|---------|
| Alpaca | Options chains, Greeks, IV | `PKNDK5P66FCRH5P5ILPTVCYE7D` |
| Finnhub | Fundamentals, news, insider | `d6bq93hr01qp4li0f2h0d6bq93hr01qp4li0f2hg` |
| FRED | Macro indicators (VIX, rates, etc.) | `c00b92a9c6a70cb70efc3201cfb9bb5f` |

## Quick Start

### Run Full Pipeline
```bash
cd agents/options-recommender/scripts
python3 10_run_pipeline.py
```

Expected runtime: ~1000 seconds (~17 minutes)

### Run Individual Steps
```bash
# Step 0: Screen S&P 500, score stocks
python3 00_build_universe.py

# Steps 1-7: Generate credit spreads with Greeks
python3 01_build_spreads.py

# Steps 8-9: GPT news risk analysis
python3 02_news_filter.py

# Step 10: Portfolio constraints, output final 5
python3 03_portfolio_select.py
```

## Output Format

```
| Ticker | Strategy | Legs | Thesis | POP |
|--------|----------|------|--------|-----|
| AAPL | Bull Put | Sell $170P/$165P | Strong fundamentals, IV 28% supports puts, 72% win rate | 72% |
| MSFT | Bear Call | Sell $420C/$425C | Overbought, resistance at ATH, 68% win rate | 68% |
```

## Trade Criteria

**Hard Filters:**
- Max loss ≤ $500 (0.5% of $100K NAV)
- PoP ≥ 65%
- Credit / Max Loss ratio ≥ 0.33
- Quote age ≤ 10 minutes

**Portfolio Constraints:**
- Exactly 5 trades
- Max 2 per GICS sector
- Net delta: [-0.30, +0.30]
- Net vega: ≤ -0.05

## File Structure

```
agents/options-recommender/
├── SKILL.md                    # Agent instructions
├── README.md                   # This file
├── references/
│   └── api_docs.md            # API documentation
├── scripts/
│   ├── 00_build_universe.py   # Step 0: Universe screening
│   ├── 01_build_spreads.py    # Steps 1-7: Spread building
│   ├── 02_news_filter.py      # Steps 8-9: News analysis
│   ├── 03_portfolio_select.py # Step 10: Final selection
│   └── 10_run_pipeline.py     # Master automation script
├── universe.json              # Generated: Top 22 stocks
├── spreads.json               # Generated: All spreads
├── filtered_spreads.json      # Generated: After news filter
└── final_trades.json          # Generated: Final 5 trades
```

## The Convergence Model

**Key insight:** Any single signal can be wrong. When 3+ independent signals align, probability tilts in your favor.

**Scoring weights:**
- Vol-Edge: 25%
- Quality: 25%
- Regime: 25%
- Info-Edge: 25%

**Gate requirement:** Minimum 3 of 4 categories must score >50 to consider a stock.

## API Rate Limits

- **Alpaca**: 200 requests/minute (paper trading)
- **Finnhub**: 60 calls/minute (free tier)
- **FRED**: 120 requests/minute

The pipeline includes rate limiting and parallel processing (max 5 workers).

## Dependencies

```bash
pip install requests numpy scipy
```

## License

Private use only. Not financial advice.
