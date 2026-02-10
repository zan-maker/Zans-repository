Metal Price Monitoring Agent — MVP Workflow
This is a scraping-first MVP to feed your pricing models until you secure API/add-in access. Given Green Li-ion's pCAM business, I'm assuming the metals you care about are lithium, nickel, cobalt, manganese (and possibly copper/gold if relevant to your offtake pricing formulas).

Architecture
Phase 1 (MVP): Browser automation agent → structured data → Excel/Google Sheet Phase 2 (Target): API + Excel add-in → direct feed into pricing models

MVP Workflow Design
Step 1: Define Target Data Points
Source	URL	Data Points	Update Frequency
Metal.com	metal.com	Li₂CO₃, LiOH, NiSO₄, CoSO₄, MnSO₄ spot prices (CNY & USD)	Daily
Shanghai Metals Market (SHMET)	shmet.com	Same commodities, Chinese domestic spot	Daily
Shanghai Gold Exchange (SGE)	sge.com.cn	Au, Ag benchmarks (if relevant to your mix)	Daily
Shanghai Futures Exchange (SHFE)	shfe.com.cn	Ni, Cu, Al futures (front-month, 3-month)	Real-time during trading hours
Step 2: Agent Logic (Python + Selenium/Playwright)

DAILY TRIGGER (7:00 AM SGT — after China market open)
│
├── 1. Launch headless browser sessions
│   ├── metal.com → scrape spot price tables
│   ├── shmet.com → scrape spot price tables  
│   ├── sge.com.cn → scrape daily benchmark prices
│   └── shfe.com.cn → scrape futures settlement prices
│
├── 2. Parse & normalize
│   ├── Standardize units (CNY/t → USD/t using daily FX)
│   ├── Timestamp each observation
│   └── Flag anomalies (>5% day-over-day move)
│
├── 3. Write to structured output
│   ├── Append to master CSV / Google Sheet
│   ├── Update "Latest Prices" summary tab
│   └── Log any scrape failures
│
└── 4. Alert layer
    ├── Email/Slack if scrape fails
    ├── Alert if price moves >5% (threshold configurable)
    └── Weekly summary digest
Step 3: Data Schema

date | source | commodity | grade | price_cny | price_usd | fx_rate | unit | contract_month | change_pct | scrape_status
Step 4: Implementation Stack
Scraping: Playwright (handles JS-rendered Chinese sites better than Selenium)
Scheduling: Cron job on a cheap VPS or GitHub Actions (free tier)
Storage: Google Sheets API (for team access) + local CSV backup
FX Rate: Pull USD/CNY from a free API (exchangerate-api.com or similar)
Alerting: Simple SMTP email or Slack webhook
Key Risks & Mitigations
Risk	Mitigation
Chinese sites block scraping / use CAPTCHAs	Rotate user agents, add delays, use residential proxy if needed
Site layout changes break parser	Build selectors defensively; alert on parse failures so you fix within hours
Price units/grades inconsistent across sources	Normalize in parsing layer; maintain a commodity mapping config file
FX timing mismatch	Use same-day PBOC mid-rate for consistency
SHFE requires login for some data	Check if settlement prices are public; if gated, scrape from secondary sources (e.g., investing.com futures page)
