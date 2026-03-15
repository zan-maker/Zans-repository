# CritMin Compass

**Critical Minerals Supply Chain Intelligence Engine**

> Real-time macroeconomic, commodity, and regulatory signal fusion for
> Lithium, Nickel, and Cobalt supply chain risk assessment — built on
> Zerve AI for ZerveHack 2026.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        CritMin Compass — Zerve DAG                      │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐  ┌──────────────────┐  ┌─────────────────────┐         │
│  │  Block 1    │  │  Block 2         │  │  Block 5            │         │
│  │  FRED API   │  │  Alpha Vantage   │  │  SEC EDGAR +        │         │
│  │  Macro Data │  │  Commodity Prices│  │  API Ninjas         │         │
│  └──────┬──────┘  └────────┬─────────┘  └──────────┬──────────┘         │
│         │                  │                       │                     │
│         ▼                  ▼                       ▼                     │
│  ┌─────────────────────────────────┐   ┌───────────────────────┐        │
│  │  Block 3                        │   │  Block 6              │        │
│  │  PPI / INDPRO vs Commodity     │   │  Dataset Summary &    │        │
│  │  Dual-Axis + Lead-Lag         │   │  Freshness Report     │        │
│  └─────────────────────────────────┘   └───────────────────────┘        │
│         │                  │                       │                     │
│         ▼                  ▼                       ▼                     │
│  ┌─────────────────────────────────┐   ┌───────────────────────┐        │
│  │  Block 4                        │   │  Block 7              │        │
│  │  GradientBoosting Forecasting  │   │  NLP Sentiment &      │        │
│  │  12-Month + Bootstrap CI       │   │  Risk Keyword Scoring │        │
│  └─────────────────────────────────┘   └───────────┬───────────┘        │
│                                                     │                    │
│                                        ┌────────────┴────────────┐      │
│                                        ▼                         ▼      │
│                               ┌─────────────────┐  ┌────────────────┐  │
│                               │  Block 8        │  │  Block 9       │  │
│                               │  Correlation    │  │  Linguistic    │  │
│                               │  Heatmap        │  │  Drift         │  │
│                               └─────────────────┘  └────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Zerve Blocks

| Block | File | Description | Dependencies |
|-------|------|-------------|--------------|
| 01 | `01_fetch_fred_macro_data.py` | Ingest PPI, Industrial Production, Trade Balance from FRED | None |
| 02 | `02_fetch_commodity_prices.py` | Ingest Li/Ni/Co proxy prices from Alpha Vantage | None |
| 03 | `03_ppi_indpro_commodity_analysis.py` | Dual-axis charts, rolling correlations, lead-lag analysis | Blocks 1, 2 |
| 04 | `04_commodity_price_forecasting.py` | GradientBoosting 12-month forecast with bootstrap CI | Blocks 1, 2 |
| 05 | `05_sec_edgar_supply_chain.py` | SEC EDGAR filing search + API Ninjas fallback | None |
| 06 | `06_dataset_summary_report.py` | Dataset freshness & summary report | Blocks 1, 2, 5 |
| 07 | `07_nlp_sentiment_risk_analysis.py` | VADER sentiment + risk keyword scoring, 3 charts | Block 5 |
| 08 | `08_correlation_analysis.py` | Pearson correlations, heatmap, multi-axis overlay | Blocks 1, 2, 7 |
| 09 | `09_supply_chain_linguistic_analysis.py` | Term frequency, regulatory heatmap, language drift | Block 5 |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/critmin-compass.git
cd critmin-compass
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

Copy the example environment file and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Where to get it |
|----------|----------------|
| `FRED_API_KEY` | [FRED API registration](https://fred.stlouisfed.org/docs/api/api_key.html) (free) |
| `ALPHA_VANTAGE_API_KEY` | [Alpha Vantage](https://www.alphavantage.co/support/#api-key) (free tier) |
| `API_NINJAS_KEY` | [API Ninjas](https://api-ninjas.com/) (free tier) |

### 4. Run on Zerve

1. Create a new Zerve project (Python 3.10+).
2. Create one code block per file in `zerve_blocks/`, ordered 01 through 09.
3. Set environment variables in the Zerve canvas settings panel.
4. Wire the DAG edges as shown in the architecture diagram above.
5. Run blocks in order — ingestion blocks (01, 02, 05) can run in parallel.

---

## Data Sources

| Source | API | Data Type | Refresh |
|--------|-----|-----------|---------|
| Federal Reserve (FRED) | REST JSON | PPI, Industrial Production, Trade Balance | Monthly |
| Alpha Vantage | REST JSON | Commodity spot prices (proxied) | Monthly |
| SEC EDGAR | Full-text search | 10-K / 10-Q filing metadata | Real-time |
| API Ninjas | REST JSON | Commodity price fallback | On-demand |

---

## Sample Outputs

See [`outputs/sample_output.md`](outputs/sample_output.md) for representative
output tables from a full pipeline run.

---

## Known Issues

- **Block 06** references `edgar_df["search_term"]` and `edgar_df["filing_date"]`
  columns that do not exist in the actual schema produced by Block 05. The correct
  columns are `query` and `date`. This causes a `KeyError` at runtime.
- Alpha Vantage free tier is limited to 5 requests/minute; Block 02 includes
  a 20-second sleep between requests.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Links

- [Devpost Submission](https://devpost.com/software/critmin-compass) *(placeholder)*
- [Zerve AI](https://www.zerve.ai/)

---

Built with [Zerve AI](https://www.zerve.ai/) for **ZerveHack 2026**.
