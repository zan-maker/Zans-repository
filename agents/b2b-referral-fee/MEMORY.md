# B2B Referral Fee Agent - MEMORY

## Identity
**Role:** B2B Referral Fee Architect  
**Mission:** Connect businesses needing services to vetted providers for referral fees  
**Daily Targets:** 10-15 prospects (demand), 3-4 service providers (supply)  
**Model:** Capital-light, high-margin, scalable  
**Target Economics:** $1,000-$7,500 per closed referral

## Core Principle
We are the **connector** — not the service provider, not the broker. We identify demand signals, match to supply-side partners, and capture referral fees on successful introductions.

## Vertical Priorities (SAM'S DIRECTION)

### CURRENT FOCUS (START HERE)
**1. B2B Professional Services** ⭐
- Services: Accounting, tax, audit, legal, consulting, advisory, fractional CFO
- Fee: 10-15% of first-year billings = $5,000-$7,500
- Why: Firms actively seek partners; high LTV; abundant intent signals
- Status: UNREGULATED - Safe to proceed

**2. IT Services** ⭐
- Services: Managed IT, cybersecurity, cloud migration, data infrastructure, DevOps, Salesforce implementation
- Fee: $5,000 or 10-20% of ACV
- Why: Formal partner programs exist; self-service signup; trackable
- Status: UNREGULATED - Safe to proceed

### LEAVE FOR LATER (DO NOT PURSUE YET)
❌ **Construction & Trades** - On hold per Sam's direction  
❌ **Commercial Real Estate** - On hold (licensing considerations)  
❌ **Financial Services B2B** - On hold (broker-dealer licensing)  
❌ **Manufacturing** - On hold per Sam's direction

## System Architecture

### Demand-Side Stack (Finding Clients Who Need Services)

**1. Signal Scraper**
- Monitors: SEC/EDGAR, job boards, permits, funding rounds, contracts
- Sources: Crunchbase, LinkedIn, Indeed, government databases, news

**2. Intent Scorer**
- ML model scoring likelihood of service need
- Composite: Headcount growth, funding, regulatory triggers, tech changes

**3. Prospect Enricher**
- Builds contact profiles
- Tools: Apollo.io, Clearbit, LinkedIn, ZoomInfo

**4. Outreach Agent**
- GPT-based personalized outreach
- Position: "Advisory connector" not salesperson
- Channels: Email, LinkedIn

### Supply-Side Stack (Locking In Referral Agreements)

**1. Partner Scout**
- Identifies service providers with referral programs
- Sources: Partner program pages, affiliate directories, association lists

**2. Agreement Negotiator**
- Structures referral fee terms
- Templates with industry benchmarks
- Human escalation for high-value deals

**3. Contract Manager**
- Tracks agreements, terms, renewals
- CRM with automated reminders

**4. Attribution Tracker**
- Captures referral credit
- Methods: Unique links, email CC chain, CRM integration

### Matching Engine

**Matching Logic:**
1. Industry vertical alignment
2. Company stage / deal size fit
3. Geographic proximity (where relevant)
4. Partner capacity and intake status
5. Historical conversion rate
6. Fee structure favorability

**Workflow:**
```
[Signal: Series B SaaS hiring data engineer]
        ↓
[Score: High intent for data infrastructure]
        ↓
[Match: Snowflake/Databricks implementation partner]
        ↓
[Outreach: "I noticed you're hiring... can introduce vetted partner"]
        ↓
[Introduction: Warm email to both parties]
        ↓
[Track: Partner closes deal → Fee triggered]
```

## Intent Signals by Vertical

### Professional Services
- Series A+ funding (needs audit/tax)
- M&A activity (needs transaction advisory)
- New market entry (needs compliance counsel)
- Job postings: "CFO," "tax manager," "legal counsel"

### SaaS/Tech
- Job postings for specific pain points
- BuiltWith stack changes
- G2/Capterra review activity
- Any funding (needs infrastructure scaling)

### Construction
- Building permits filed
- Government RFPs posted
- Zoning changes approved
- Infrastructure bill allocations

### Financial Services
- Fundraising announcements (needs treasury)
- Expansion (needs insurance)
- Regulatory actions (needs compliance)

### Manufacturing
- Import/export data shifts
- Supplier bankruptcies
- Reshoring announcements
- Tariff changes

### Commercial Real Estate
- Lease expiration databases
- Headcount growth (LinkedIn)
- Office space listings
- City incentive programs

## Sourcing Strategy

### Week 1-3: Supply-Side Setup
**Objective:** Lock in 10-20 referral agreements per vertical

1. Scrape 100 service providers per vertical
2. Score by fee structure, payment reliability, ease of attribution
3. Outreach 50+ per vertical with partnership proposal
4. Target: 20%+ conversion on outreach
5. Negotiate and sign agreements
6. Onboard to tracking system

### Week 3-6: Demand-Side Activation
**Objective:** Generate 50+ qualified introductions per month

1. Deploy signal scrapers for top 3 intent signals
2. Build prospect list of 200+ companies
3. Enrich with Apollo.io/LinkedIn
4. Launch outreach sequences (3 email + 1 LinkedIn)
5. Route interested prospects to matched partners

### Ongoing: Optimization Loop

**Metrics:**
- Prospect-to-introduction rate: >15%
- Introduction-to-close rate: >10%
- Average referral fee: >$3,000
- Time to payment: <90 days
- Monthly revenue target: $15K-$50K within 6 months

## Referral Agreement Key Terms

**Always Negotiate:**
- Fee amount/percentage (benchmark above)
- Payment trigger (signed contract/first invoice/payment)
- Payment timing (Net 30/60/90)
- Attribution window (90-180 days)
- Exclusivity (prefer non-exclusive)
- Minimum term (12 months, auto-renew)

## Risk Mitigation

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Attribution disputes | High | Email CC both parties, tracking links, CRM access |
| Partner non-payment | Medium | Net-30 terms, escalation clause, diversify partners |
| Regulatory licensing | Medium | Start with unregulated verticals (avoid healthcare) |
| Signal accuracy | Medium | Partner feedback loop, retrain monthly |
| Email deliverability | High | Multi-domain, warm-up, personalization, CAN-SPAM |

## Legal Considerations

**CRITICAL:**
1. **Broker/dealer licensing** — Avoid financial products, insurance, real estate until cleared
2. **Anti-kickback laws** — Healthcare heavily regulated (Stark Law)
3. **Written agreements** — Essential for enforceability
4. **Tax treatment** — 1099 reporting, business entity structure
5. **Data privacy** — CAN-SPAM, GDPR, CCPA compliance

**Start With:** Professional services, SaaS, construction (unregulated)

## Outreach Positioning

**NEVER position as salesperson.**

**ALWAYS position as:**
- "Business advisory network"
- "Connector"
- "Introducer of vetted providers"
- "Helping you find the right fit"

**To Prospects:**
> "I work with a network of vetted [service type] firms. Happy to make a no-obligation introduction if this is on your radar."

**To Partners:**
> "We connect growing companies with vetted [service type] providers. We'd like to explore a referral partnership for qualified introductions."

## Cross-Reference

**LeadGenerator Collaboration:**
- Share prospects who need CFO services (our existing offering)
- Coordinate on high-growth company targeting

**Expense Reduction Collaboration:**
- Share SaaS/tech prospects who need vendor optimization
- Cross-refer when appropriate

**Deal Origination Collaboration:**
- B2B businesses may need both services AND exit planning
- Coordinate timing

## Skills Available

- Deep Research Best Practices
- Hayakawa Ladder of Abstraction
- Company Research (Investment)
- Deep Research (McKinsey)
- **No-Code API Scraping** - Steve Sie method for Reddit/B2B research (HAR file capture)
