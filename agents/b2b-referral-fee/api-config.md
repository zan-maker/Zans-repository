# B2B Referral Fee Agent - API Configuration

**Agent:** B2B Referral Fee Architect
**Purpose:** Connect businesses needing services to vetted providers for referral fees
**Daily Targets:** 10-15 prospects (demand), 3-4 service providers (supply)
**Configured:** Feb 15, 2026

---

## API Keys & Services

### Hunter.io (Email Verification & Finder)
**API Key:** `45e2e1243877d88f647b51952e6ddf0b8e8a4637`
**Use:** Find and verify business owner and service provider emails
**Endpoint:** `https://api.hunter.io/v2/`
**Rate Limit:** 50 requests/month
**Status:** 🟢 ACTIVE - 44 credits, 88 verifications remaining (resets March 1, 2026)
**Plan:** Free (need upgrade for high-volume campaigns)

### ZeroBounce (Email Verification - Primary)
**API Key:** `fd0105c8c98340e0a2b63e2fbe39d7a4`
**Use:** Verify emails before sending (high accuracy, pay-as-you-go)
**Endpoint:** `https://api.zerobounce.net/v2/validate`
**Rate Limit:** Pay-as-you-go
**Status:** 🟢 ACTIVE
**Cost:** ~$0.0075 per verification

**Usage Example:**
```bash
curl -X POST "https://api.zerobounce.net/v2/validate" \
  -d "api_key=fd0105c8c98340e0a2b63e2fbe39d7a4" \
  -d "email=target@company.com" \
  -d "ip_address="
```

**Response Status:**
- `valid` - Safe to send
- `invalid` - Do not send
- `catch-all` - Accepts all emails (risky)
- `unknown` - Cannot verify
- `spamtrap` - Do not send
- `abuse` - Do not send

**Verification Workflow:**
1. **Primary:** Use ZeroBounce for all email verification
2. **Backup:** Use Hunter.io if ZeroBounce quota exceeded
3. **Before sending ANY email:** Must verify with ZeroBounce
4. **Only send if status = "valid"

### Abstract API (Company Enrichment)
**API Key:** `38aeec02e6f6469983e0856dfd147b10`
**Use:** Enrich company data, employee counts, industry classification
**Endpoint:** `https://companyenrichment.abstractapi.com/v1/`

### Zyte API (Web Scraping)
**API Key:** `8d3e9c7af6e948b088e96ad15ca21719`
**Use:** Scrape job boards, funding databases, partner program pages
**Endpoint:** `https://api.zyte.com/v1/extract`

### Brave Search API
**API Key:** `BSAqx7g5ob7ymEOAUfRduTetIOWPalN`
**Use:** Search for companies with buying signals, referral programs
**Rate Limit:** 2000 requests/month

### Tavily API (Deep Research)
**API Key:** `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`
**Use:** Research companies, service providers, industry trends

### Serper API (Google Search Results)
**API Key:** `cac43a248afb1cc1ec004370df2e0282a67eb420`
**Use:** Google Search API for real-time results, news, LinkedIn profiles
**Endpoint:** `https://google.serper.dev/search`
**Status:** Backup/Primary option if Brave/Tavily limits reached
**Rate Limit:** Check dashboard at serper.dev

**Example Usage:**
```bash
curl --location --request POST 'https://google.serper.dev/search' \
--header 'X-API-KEY: cac43a248afb1cc1ec004370df2e0282a67eb420' \
--header 'Content-Type: application/json' \
--data-raw '{
  "q": "site:linkedin.com/in CFO Series B",
  "gl": "us",
  "hl": "en"
}'
```

### Apollo.io (Contact Enrichment)
**Use:** Enrich prospect data, find decision-maker contacts
**Note:** May need account setup if not already configured

### Clearbit (Company Intelligence)
**Use:** Company firmographics, technographics
**Note:** May need account setup

### BuiltWith (Tech Stack Detection)
**Use:** Detect technology changes (SaaS buying signals)
**Note:** May need account setup

---

## Email Access

**Account:** sam@impactquadrant.info
**App Password:** dmje zsak eaop hyic
**Protocol:** Read when instructed; Send with permission only

---

## Target Verticals (Prioritized)

### 1. B2B Professional Services ⭐ (HIGHEST PRIORITY)
**Services:** Accounting, law, consulting, advisory
**Referral Fee:** 10-15% of first-year billings ($5,000-$7,500)
**Signals:** Series A+ raises, M&A activity, new market entry, regulatory filings
**Quick Win:** Firms actively seek referral partners

### 2. Technology/SaaS ⭐ (HIGHEST PRIORITY)
**Services:** Software implementation, data infrastructure, cybersecurity
**Referral Fee:** $5,000 per referral or 10-20% of ACV
**Signals:** Job postings for specific roles, tech stack changes, G2/Capterra activity
**Quick Win:** Most have formal partner programs

### 3. Construction & Trades
**Services:** General contractors, specialty trades, project management
**Referral Fee:** $3,000 per referral
**Signals:** Permit filings, RFPs, project databases, infrastructure allocations
**Quick Win:** Public data abundant

### 4. Financial Services (B2B)
**Services:** Treasury management, commercial lending, insurance, payment processing
**Referral Fee:** $2,500 per referral
**Signals:** Fundraising announcements, expansion, compliance events
**Note:** Check licensing requirements

### 5. Manufacturing
**Services:** Supply chain consulting, logistics, quality management
**Referral Fee:** $1,000 per referral
**Signals:** Import/export shifts, supplier changes, reshoring announcements

### 6. Commercial Real Estate
**Services:** Tenant rep, buyer rep, property management
**Referral Fee:** 25% of commission ($3,000-$10,000)
**Signals:** Lease expirations, headcount growth, office relocations
**Note:** Verify broker licensing requirements

---

## Output Files

### Demand-Side Prospects
**Path:** `cron-output/b2b-referral-fee/prospects/YYYY-MM-DD-export.csv`
**Columns:** Date, Company_Name, Industry, Location, Signal_Type, Signal_Details, Contact_Name, Contact_Email, Contact_Phone, Estimated_Need, Vertical_Match, Score, Vertical_Priority, Notes

### Supply-Side Partners
**Path:** `cron-output/b2b-referral-fee/partners/YYYY-MM-DD-export.csv`
**Columns:** Date, Company_Name, Service_Type, Vertical, Fee_Structure, Fee_Amount, Contact_Name, Contact_Email, Agreement_Status, Attribution_Method, Payment_Terms, Vertical_Priority, Score, Notes

### Referral Agreements
**Path:** `cron-output/b2b-referral-fee/agreements/YYYY-MM-DD-agreements.csv`
**Columns:** Date, Partner_Company, Service_Type, Fee_Percent, Fee_Minimum, Payment_Trigger, Attribution_Window, Agreement_Term, Exclusivity, Status, Notes

### Match Log
**Path:** `cron-output/b2b-referral-fee/match-log.csv`
**Columns:** Date, Prospect_Company, Prospect_Contact, Partner_Company, Match_Vertical, Introduction_Date, Deal_Stage, Expected_Close, Projected_Fee, Notes

---

## Intent Signals by Vertical

### Professional Services Signals
- Crunchbase: Series A, B, C funding announcements
- LinkedIn: Hiring CFO, controller, compliance roles
- EDGAR: M&A filings, new market registrations
- Job boards: "tax manager," "audit," "legal counsel," "compliance"
- News: Expansion announcements, regulatory actions

### SaaS/Tech Signals
- BuiltWith: Stack changes (new analytics, security, data tools)
- Job boards: "data engineer," "Salesforce admin," "cybersecurity"
- G2/Capterra: Review activity spikes
- LinkedIn: Tech stack mentions, hiring for specific platforms
- Funding: Any raise (needs infrastructure scaling)

### Construction Signals
- City/county: Building permits filed
- Government: RFPs posted, contract awards
- Dodge Data: Project leads
- Infrastructure: State/federal allocations
- LinkedIn: Hiring project managers, estimators

### Financial Services Signals
- Crunchbase: Fundraising (needs banking/treasury)
- LinkedIn: Hiring finance roles, treasury
- EDGAR: IPO filings, securities registrations
- News: Expansion (needs insurance), M&A (needs advisory)

### Manufacturing Signals
- Import Genius/PIERS: Import/export shifts
- News: Reshoring announcements, supplier bankruptcies
- LinkedIn: Hiring supply chain, logistics roles
- Tariff databases: Changes affecting specific NAICS codes

### Commercial Real Estate Signals
- Lease expiration databases
- LinkedIn: Headcount growth (needs more space)
- News: Office openings, relocations
- City: Business license applications

---

## Scoring Systems

### Prospect Intent Score (0-100)
| Factor | Weight | Criteria |
|--------|--------|----------|
| Signal Strength | 25% | Recent, specific, high-confidence |
| Company Stage | 20% | Growth mode (hiring, funding) |
| Estimated Budget | 20% | Based on headcount/funding |
| Timing Urgency | 15% | Signal indicates immediate need |
| Decision Maker Access | 10% | C-level contact available |
| Vertical Fit | 10% | Clear service need match |

### Partner Quality Score (0-100)
| Factor | Weight | Criteria |
|--------|--------|----------|
| Fee Structure | 25% | Competitive fee ($3K+ per deal) |
| Payment Reliability | 20% | Net 30, clear attribution |
| Conversion Rate | 20% | Historical close rate |
| Vertical Expertise | 15% | Proven in target space |
| Response Speed | 10% | Fast follow-up on intros |
| Agreement Terms | 10% | Favorable terms, non-exclusive |

---

## Referral Agreement Template

**Standard Terms to Negotiate:**
- **Fee:** Percentage or flat fee (benchmark by vertical)
- **Payment Trigger:** Signed contract / First invoice / First payment
- **Payment Timing:** Net 30/60/90 from trigger
- **Attribution Window:** 90-180 days from introduction
- **Exclusivity:** Non-exclusive (preferred for optionality)
- **Minimum Term:** 12 months with auto-renewal
- **Documentation:** Email CC, tracking links, CRM access

**Target:** Lock in 10-20 agreements per vertical in first 3 weeks

---

## Key Metrics

**Daily Targets:**
- 10-15 qualified prospects identified
- 3-4 service provider partners engaged
- 1-3 referral agreements signed (ramp up over time)

**Monthly Targets (Steady State):**
- 50+ qualified prospect introductions
- 3-5 closed referrals
- $10,500+ referral revenue
- 15% prospect-to-introduction rate
- 10% introduction-to-close rate

**Annual Target:** $121,000 - $500,000 depending on vertical mix
