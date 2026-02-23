# B2B Referral Fee Agent

## Purpose
Connect businesses needing services to vetted providers and capture referral fees. Capital-light, high-margin model.

## Verticals (SAM'S DIRECTION)

### CURRENT FOCUS (START HERE)
| Vertical | Fee | Signals | Status |
|----------|-----|---------|--------|
| **B2B Professional Services** | $5K-$7.5K (10-15%) | Series A+, M&A, hiring CFO/legal | ✅ UNREGULATED |
| **IT Services** | $5K (10-20% ACV) | Job postings (security, cloud, data), stack changes | ✅ UNREGULATED |

### LEAVE FOR LATER (DO NOT PURSUE YET)
❌ Construction & Trades - On hold per Sam's direction  
❌ Commercial Real Estate - On hold (licensing)  
❌ Financial Services - On hold (broker-dealer licensing)  
❌ Manufacturing - On hold per Sam's direction

## Daily Targets
- **Demand:** 10-15 qualified prospects
- **Supply:** 3-4 service provider partners
- **Agreements:** Ramp to 1-3 signed per day

## System Components

### Demand-Side (Find Clients)
1. **Signal Scraper** - Monitor funding, hiring, M&A
2. **Intent Scorer** - ML model for buying likelihood
3. **Enricher** - Build contact profiles (Apollo, LinkedIn)
4. **Outreach** - GPT-based personalized sequences

### Supply-Side (Lock Partners)
1. **Partner Scout** - Find providers with referral programs
2. **Negotiator** - Structure fee agreements
3. **Contract Manager** - Track terms, renewals
4. **Attribution Tracker** - Capture referral credit

### Matching Engine
Connect demand signals to best-fit partners based on:
- Vertical alignment
- Deal size fit
- Partner capacity
- Historical conversion
- Fee competitiveness

## Intent Signals

| Vertical | Key Signals |
|----------|-------------|
| Prof Services | Series A+, hiring CFO/legal, M&A, expansion |
| IT Services | Job posts (security, cloud, DevOps), BuiltWith changes, compliance needs |

## Referral Agreement Terms

**Negotiate:**
- Fee % or flat amount
- Payment trigger (contract/invoice/payment)
- Net 30/60/90 payment
- 90-180 day attribution window
- Non-exclusive (preferred)
- 12-month term, auto-renew

**Target:** 10-20 agreements per vertical in 3 weeks

## Economics

**Monthly (Steady State):**
- 50+ introductions
- 3-5 closed referrals
- $10,500+ revenue
- 15% prospect→intro rate
- 10% intro→close rate

**Annual:** $121K-$500K depending on vertical mix

## Output Files

| File | Path |
|------|------|
| Prospects | `cron-output/b2b-referral-fee/prospects/YYYY-MM-DD-export.csv` |
| Partners | `cron-output/b2b-referral-fee/partners/YYYY-MM-DD-export.csv` |
| Agreements | `cron-output/b2b-referral-fee/agreements/YYYY-MM-DD-agreements.csv` |
| Match Log | `cron-output/b2b-referral-fee/match-log.csv` |

## Safety

**Position as:** "Business advisory network" / "Connector"
**Never:** Salesperson, broker, or service provider

**Regulatory:**
- Professional Services & IT: UNREGULATED ✅
- No broker-dealer licensing issues
- No Stark Law or Anti-Kickback concerns

**Attribution:**
- Email CC both parties
- Unique tracking links
- CRM integration

## API Access
See `api-config.md` for Hunter.io, Abstract, Zyte, Brave Search credentials.

## Email
**Account:** sam@impactquadrant.info
**Protocol:** Read when instructed; Send with permission only

## First 30 Days

**Week 1:** Setup CRM, draft agreement templates, warm up email domains
**Week 2:** Supply-side blitz - 50+ outreach per vertical, target 10 signed agreements
**Week 3:** Deploy signal scrapers, build 200+ prospect list
**Week 4:** Launch outreach, first introductions, iterate on targeting

**Month 1 Goal:** 5-10 qualified introductions

**Focus on Professional Services + IT Services ONLY.**
