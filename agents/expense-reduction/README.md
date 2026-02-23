# Expense Reduction Lead Generation & Outreach System

**Created:** Feb 14, 2026
**Purpose:** Daily SMB lead generation (15-20 leads) + automated outreach for Expense Reduction Services

## Email Configuration

**From:** Zander@agentmail.to
**API Key:** am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f
**CC:** sam@impactquadrant.info (all emails)
**API Endpoint:** https://api.agentmail.to/v1/send

## Daily Schedule

| Time (EST) | Job | Description | Output |
|------------|-----|-------------|--------|
| **11:00 AM** | Lead Generator | Generate 15-20 leads, score 0-100, export CSV | Leads + CSV |
| **4:00 PM** | Outreach Automation | Send 5-10 personalized emails | Outreach report |

## Product: Expense Reduction Services

**What:** Technology-led, always-on expense reduction service
**Model:** Modest monthly admin fee + success-based fees ONLY on verified savings

### Key Value Propositions
- ✅ **Continuous expense reduction** (not one-off consulting)
- ✅ **Technology-enabled** (automation, not headcount)
- ✅ **Fees on verified savings only** (no savings = no success fee)
- ✅ **Transparent reporting** (see savings in your own systems)
- ✅ **Aligned incentives** (we only win when you save)

### Focus Areas
- Vendor/third-party spend (SaaS, telecom, logistics, OPEX)
- Travel & expense policy optimization
- Contract renewals and negotiations
- Usage/volume-based spend rightsizing

## Target Profile

**Company Size:** 20-500 employees
**Industries (High Spend Categories):**
1. **Technology/SaaS** (high vendor spend, multiple tools)
2. **Professional Services** (travel expenses, software subscriptions)
3. **Healthcare** (medical supplies, equipment, vendor management)
4. **Manufacturing** (logistics, raw materials, supplier contracts)
5. **Financial Services** (compliance costs, vendor spend)
6. **Retail/E-commerce** (inventory, shipping, payment processing)

**Decision Makers:**
- **CFO / VP Finance** (PRIMARY - owns P&L)
- **CEO / Owner** (SECONDARY - margin pressure)
- **COO / VP Operations** (SECONDARY - vendor management)

**Pain Signals:**
- Rapid growth (vendor sprawl, shadow IT)
- Recent funding (spend optimization phase)
- No dedicated procurement team
- Multiple SaaS subscriptions
- Job postings for finance/procurement roles
- Contract renewal season

## Lead Scoring System (0-100)

### Company Size (0-25 points)
- 100-500 employees: +25
- 50-99 employees: +20
- 30-49 employees: +15
- 20-29 employees: +10

### Industry Spend Profile (0-25 points)
- Tech/SaaS: +25
- Professional Services: +25
- Healthcare: +25
- Manufacturing: +25
- Financial Services: +25
- Retail/E-commerce: +25
- Other: +15

### Decision Maker Found (0-25 points)
- CFO/VP Finance email: +25
- CEO/Owner email: +20
- COO/VP Ops email: +20
- Generic contact: +10

### Spend Pain Signals (0-25 points)
- Job postings for finance/procurement: +25
- Recent fundraising: +20
- Multiple locations: +20
- High growth rate: +15
- Tech stack mentions: +15

## Score Thresholds

- **Hot (75-100):** Immediate outreach
- **Warm (50-74):** Follow-up queue
- **Cold (<50):** Nurture list

## Email Templates

### Technology/SaaS
Focus: Vendor sprawl, SaaS optimization, shadow IT
Case study: Series B SaaS company saved $340K year one

### Professional Services
Focus: Travel & expense, software subscriptions
Case study: 65-employee firm saved $180K annually

### Healthcare
Focus: Medical supplies, equipment, vendor contracts
Case study: 120-employee medical group saved $420K

### Manufacturing
Focus: Logistics, raw materials, supplier contracts
Case study: 90-employee manufacturer saved $280K

### Multi-Location
Focus: Vendor consolidation, enterprise contracts
Case study: 8-location franchise saved $310K

## Output Files

### Daily Lead Files
- **Markdown Report:** `cron-output/expense-reduction/YYYY-MM-DD-leads.md`
- **CSV Export:** `cron-output/expense-reduction/YYYY-MM-DD-export.csv`
- **Outreach Report:** `cron-output/expense-reduction/YYYY-MM-DD-outreach.md`

### CSV Export Columns
Company, Industry, Size, Location, Decision Maker, Title, Email, Phone, Website, Score, Source, Spend Signals, Outreach Status, Date Contacted

## Cron Jobs

**Job 1:** Expense Reduction Lead Generator
- ID: 99a47140-30a3-4280-a604-5ce2d2b2a88e
- Schedule: 11:00 AM EST daily
- Output: 15-20 leads, scored and enriched

**Job 2:** Expense Reduction Outreach Automation
- ID: [pending from second cron creation]
- Schedule: 4:00 PM EST daily
- Output: 5-10 personalized emails sent

## Monitoring

Check daily:
- Lead quality (industry fit, spend signals)
- Email delivery rates
- Response tracking (manual via Sam's inbox)
- API quotas (Hunter.io, Agentmail.to)

## Next Steps

1. Monitor first week's lead quality
2. Refine email templates based on responses
3. Consider follow-up sequence (Day 3, Day 7)
4. Track conversion to discovery calls
