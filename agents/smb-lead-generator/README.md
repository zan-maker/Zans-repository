# SMB Lead Generation & Outreach System - Wellness 125 Cafeteria Plans

**Created:** Feb 14, 2026
**Purpose:** Daily SMB lead generation (15-20 leads) + automated outreach for Wellness 125 Cafeteria Plan sales

## Email Configuration

**From:** Zane@agentmail.to
**API Key:** am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68
**CC:** sam@impactquadrant.info (all emails)
**API Endpoint:** https://api.agentmail.to/v1/send

## Daily Schedule

| Time (EST) | Job | Description |
|------------|-----|-------------|
| **10:00 AM** | SMB Lead Generator | Generate 15-20 leads, score 0-100, export CSV |
| **3:00 PM** | Outreach Automation | Send 5-10 personalized Wellness 125 emails |

## Product: Wellness 125 Cafeteria Plan

**What it is:** Section 125-compliant wellness program for employers with 20+ W-2 employees

**Key Value Propositions:**
- ✅ **$681/year savings per employee** (FICA tax reduction)
- ✅ **30-60% workers' compensation premium reduction**
- ✅ **$50-$400/month employee take-home pay increase** (at no cost to employees)
- ✅ **Zero employer fees, setup costs, or ongoing admin**
- ✅ **Enhanced benefits:** 24/7 virtual care, free generic meds, 60% dental discounts
- ✅ **Compliance:** IRS, ERISA, ACA compliant with legal opinion letters

## Target Profile

**Company Size:** 20-500 employees (sweet spot: 50-200)
**Industries (Priority):**
1. Healthcare (medical practices, clinics, home health, hospice)
2. Hospitality (hotels, restaurants, senior living, franchises)
3. Manufacturing (light manufacturing, assembly, auto services)
4. Transportation (logistics, trucking, delivery, medical transport)

**Decision Makers:**
- CEO / Owner / Founder (PRIMARY)
- CFO / Finance Director (SECONDARY - focused on cost savings)
- HR Director / VP People (SECONDARY - focused on benefits/retention)

## Lead Scoring System (0-100)

### Company Size (0-25 points)
- 100-500 employees: +25 (ideal for Wellness 125 scale)
- 50-99 employees: +20 (sweet spot)
- 30-49 employees: +15
- 20-29 employees: +10 (minimum viable size)
- Under 20: 0 (too small for meaningful savings)

### Industry Fit (0-25 points)
- Healthcare: +25 (high workers' comp, turnover)
- Hospitality: +25 (seasonal, high workers' comp)
- Manufacturing: +25 (safety-sensitive, high workers' comp)
- Transportation: +25 (fleet, high workers' comp premiums)
- Senior Living: +25 (healthcare + hospitality hybrid)
- Other: +10

### Decision Maker Found (0-25 points)
- CEO/Owner email found: +25 (decision maker)
- CFO/Finance Director email found: +25 (focused on cost savings)
- HR Director email found: +20 (focused on benefits)
- Generic contact only: +5

### Pain Signals (0-25 points)
- Workers' comp mentions in job posts: +25 (high premiums)
- Rapid hiring (5+ roles): +20 (growth phase, need retention)
- Multiple locations: +20 (complex payroll, compounding savings)
- Benefits/admin job postings: +15 (HR infrastructure needs)
- High turnover industry signals: +15 (retention challenge)

## Score Thresholds

- **Hot (75-100):** Immediate outreach priority
- **Warm (50-74):** Follow-up queue
- **Cold (<50):** Nurture list

## Output Files

### Daily Lead Files
- **Markdown Report:** `cron-output/smb-leads/YYYY-MM-DD-leads.md`
- **CSV Export:** `cron-output/smb-leads/YYYY-MM-DD-export.csv`
- **Outreach Report:** `cron-output/smb-leads/YYYY-MM-DD-outreach.md`
- **Outreach Log:** `cron-output/smb-leads/outreach-log.csv`

### CSV Export Columns
```
Company, Industry, Size, Location, Decision Maker, Title, Email, Phone, Website, Score, Source, Pain Signals, Outreach Status, Date Contacted
```

## Email Templates

### Healthcare
Focus: High workers' comp costs, employee retention, benefits enhancement
- Key stats: $681/employee savings, 30-60% workers' comp reduction
- Case study: Multi-state hospice organization

### Hospitality  
Focus: Seasonal workforce, high turnover, workers' comp costs
- Key stats: $50-$400/month employee take-home increase
- Case study: Multi-location franchisee saving hundreds of thousands annually

### Manufacturing
Focus: Safety-sensitive environment, high workers' comp, operational efficiency
- Key stats: FICA savings, workers' comp reduction, no admin burden
- Case study: 66-employee transportation company saving $140K/year

### Transportation
Focus: Fleet operations, driver retention, per-mile costs
- Key stats: Lower taxable payroll base, reduced workers' comp
- Case study: Medical transportation company with CPA-validated savings

### Senior Living
Focus: Healthcare + hospitality hybrid, multiple locations, retention challenges
- Key stats: $120K-$250K annual savings (50-130 employee organizations)
- Case study: Senior living facilities with improved morale and retention

## Outreach Rules

- **Max emails/day:** 10 personalized emails
- **Only Hot leads:** Score 75-100
- **Always CC:** sam@impactquadrant.info
- **Personalization required:** Reference specific company details
- **No spam:** Quality over quantity

## API Usage

### Lead Generation
- Brave Search (primary)
- Hunter.io (email finder)
- Abstract API (company enrichment)
- Zyte + crawl4ai (scraping)

### Outreach
- Agentmail.to (email sending)
- Zyte (website personalization research)

## Cron Jobs

**Job 1:** SMB Lead Generator
- ID: 946292de-a901-40ab-afe0-d80eaad7a67a
- Schedule: 10:00 AM EST daily
- Output: 15-20 leads, scored and enriched

**Job 2:** SMB Outreach Automation
- ID: 81775b05-582e-4b65-b4a1-2c65cbc071b7
- Schedule: 3:00 PM EST daily
- Output: 5-10 personalized emails sent

## Monitoring

Check daily:
- Lead quality (scores, industry fit)
- Email delivery rates
- Response tracking (manual via Sam's inbox)
- API quotas (Hunter.io, Agentmail.to)

## Next Steps

1. Monitor first week's lead quality
2. Refine email templates based on responses
3. Consider follow-up sequence (Day 3, Day 7)
4. Track conversion to discovery calls
