# Deal Origination Agent - API Configuration

**Agent:** Deal Origination & Referral Fee Architect
**Purpose:** Identify business sellers and PE buyers for referral fee agreements
**Daily Targets:** 10-15 sellers, 3-4 PE buyers
**Configured:** Feb 14, 2026

---

## API Keys & Services

### Hunter.io (Email Verification)
**API Key:** `f701d171cf7dec7e730a6b1c6e9b74f29f39b6e`
**Use:** Verify business owner and PE contact emails
**Endpoint:** `https://api.hunter.io/v2/`
**Rate Limit:** 50 requests/month

### Abstract API (Company Enrichment)
**API Key:** `38aeec02e6f6469983e0856dfd147b10`
**Use:** Enrich business and PE firm data
**Endpoint:** `https://companyenrichment.abstractapi.com/v1/`

### Zyte API (Web Scraping)
**API Key:** `8d3e9c7af6e948b088e96ad15ca21719`
**Use:** Scrape business listing sites, PE firm databases
**Endpoint:** `https://api.zyte.com/v1/extract`

### Brave Search API
**API Key:** `BSAqx7g5ob7ymEOAUfRduTetIOWPalN`
**Use:** Search for off-market businesses, PE firms
**Rate Limit:** 2000 requests/month

### Tavily API (Backup Search)
**API Key:** `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`
**Use:** Fallback search for deep research

### Craigslist API (Off-Market Business Listings)
**GitHub:** https://github.com/mislam/craigslist-api?tab=readme-ov-file
**Use:** Find owner-direct business listings (NOT broker listings)
**Best For:** Car washes, laundromats, small retail, service businesses
**Status:** Off-market sourcing channel - NO broker intermediaries

**Search Categories:**
- `biz` - Business/commercial
- `bfs` - Businesses for sale (owner-direct)

**Example Metro Areas to Monitor:**
- Dallas, Houston, Austin (TX)
- Phoenix, Tucson (AZ)
- Atlanta (GA)
- Tampa, Orlando, Miami (FL)
- Denver (CO)
- Las Vegas (NV)
- Nashville (TN)

---

## Email Access

**Account:** sam@impactquadrant.info
**App Password:** dmje zsak eaop hyic
**Protocol:** Read when instructed; Send with permission only

---

## Data Sources

### Business Listings (Sellers)
**Primary:**
- BizBuySell.com
- Axial.net
- DealStream.com
- MicroAcquire.com
- BusinessesForSale.com
- LoopNet (businesses)
- BusinessBroker.net

**Secondary:**
- Regional broker sites
- Industry-specific marketplaces
- SBA loan databases

### PE Buyer Databases
**Sources:**
- PitchBook (if accessible)
- Preqin
- Axial member directory
- Private Equity Info
- PE Hub
- Middle Market Growth
- Family office databases

---

## Output Files

### Daily Seller Leads
- **Path:** `cron-output/deal-origination/sellers/YYYY-MM-DD-export.csv`
- **Format:** Company, EBITDA, Industry, Location, Owner, Email, Phone, Source, Score

### Daily PE Buyer Leads
- **Path:** `cron-output/deal-origination/buyers/YYYY-MM-DD-export.csv`
- **Format:** Firm Name, AUM, Focus, Contact, Email, Deal Size, Geography, Score

### Referral Agreement Log
- **Path:** `cron-output/deal-origination/referral-log.csv`
- **Tracks:** Date, Target, Buyer, Agreement Status, Fee Structure, Notes

---

## Scoring Systems

### Seller Scoring (0-100)
| Factor | Weight | Criteria |
|--------|--------|----------|
| EBITDA Margin | 20% | >20% = full points |
| Recurring Revenue | 15% | Contracts/subscriptions |
| Customer Concentration | 10% | <30% top customer = full |
| Industry Fragmentation | 15% | Roll-up potential |
| CapEx Intensity | 10% | Low maintenance = full |
| Talent Dependence | 10% | Not founder-dependent |
| Geographic Density | 10% | Clusterable with others |
| Buyer Fit | 10% | Clear Segment A or B match |

### Buyer Scoring (0-100)
| Factor | Weight | Criteria |
|--------|--------|----------|
| Deal Volume | 25% | >5 deals/year |
| Check Size Match | 25% | Aligns with targets |
| Industry Focus | 20% | Blue-collar/services |
| Geography | 15% | US-based |
| Referral History | 15% | Known to pay fees |

---

## Referral Fee Structure

**Standard Terms:**
- 5% of transaction value up to $1M
- Sliding scale above $1M
- Minimum fee: $50,000
- Paid on closing
- Includes deferred consideration and assumed debt
- 12-month tail protection

**Example Economics:**
- $1.5M EBITDA business @ 3.3x = $5M EV → ~$150K fee
- $5M EBITDA platform @ 6x = $30M EV → ~$400K fee
