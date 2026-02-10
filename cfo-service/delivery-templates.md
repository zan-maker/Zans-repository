# CFO Service Delivery Templates
## Ready-to-Use Models, Dashboards & Reports

---

## 1. Three-Statement Financial Model

### File: `templates/cfo/3-statement-model.xlsx`

**Structure:**

#### Tab 1: Instructions
- How to use the model
- Key assumptions
- Update frequency
- Contact for questions

#### Tab 2: Assumptions
```
REVENUE ASSUMPTIONS
- Monthly recurring revenue (MRR) growth rate: [Input]%
- Customer churn rate: [Input]%
- Average revenue per user (ARPU): $[Input]
- New customers per month: [Input]

COST ASSUMPTIONS
- COGS as % of revenue: [Input]%
- Headcount growth: [Input] per month
- Average salary: $[Input]
- Benefits load: [Input]%
- Marketing spend: $[Input]/month

WORKING CAPITAL
- Accounts receivable days: [Input]
- Accounts payable days: [Input]
- Inventory days (if applicable): [Input]
```

#### Tab 3: Income Statement (P&L)
```
Monthly format with:
- Revenue (by product line)
- Cost of Goods Sold
- Gross Profit
- Operating Expenses (by department)
  - Sales & Marketing
  - Research & Development
  - General & Administrative
- Operating Income (EBIT)
- Interest Expense
- Taxes
- Net Income

Plus:
- % of revenue for all line items
- Variance vs. prior month
- Variance vs. budget
- Trailing 3-month average
```

#### Tab 4: Balance Sheet
```
ASSETS
Current Assets:
- Cash
- Accounts Receivable
- Prepaid Expenses
- Other Current Assets
Total Current Assets

Non-Current Assets:
- Property & Equipment
- Intangible Assets
- Other Long-Term Assets
Total Non-Current Assets

Total Assets

LIABILITIES
Current Liabilities:
- Accounts Payable
- Accrued Expenses
- Deferred Revenue
- Short-Term Debt
Total Current Liabilities

Non-Current Liabilities:
- Long-Term Debt
- Other Long-Term Liabilities
Total Non-Current Liabilities

Total Liabilities

EQUITY
- Common Stock
- Additional Paid-In Capital
- Retained Earnings
Total Equity

Total Liabilities & Equity

Plus:
- Working Capital
- Current Ratio
- Quick Ratio
```

#### Tab 5: Cash Flow Statement
```
OPERATING ACTIVITIES
Net Income
+ Depreciation & Amortization
+ Changes in Working Capital
  - Accounts Receivable
  - Inventory
  - Prepaid Expenses
  - Accounts Payable
  - Accrued Expenses
  - Deferred Revenue
= Cash from Operations

INVESTING ACTIVITIES
- Capital Expenditures
- Purchase of Investments
+ Sale of Investments
= Cash from Investing

FINANCING ACTIVITIES
+ Proceeds from Debt
- Debt Repayments
+ Equity Financing
- Dividends/Distributions
= Cash from Financing

NET CHANGE IN CASH
Beginning Cash
+ Net Change
= Ending Cash
```

#### Tab 6: Key Metrics
```
GROWTH METRICS
- Revenue Growth (MoM, QoQ, YoY)
- Customer Growth
- ARPU Trend

PROFITABILITY METRICS
- Gross Margin
- Operating Margin
- Net Margin
- EBITDA Margin

UNIT ECONOMICS
- CAC (Customer Acquisition Cost)
- LTV (Lifetime Value)
- LTV/CAC Ratio
- CAC Payback Period
- Net Revenue Retention
- Gross Revenue Retention

CASH METRICS
- Burn Rate (Monthly)
- Runway (Months)
- Cash Conversion Cycle
- Free Cash Flow

EFFICIENCY METRICS
- Revenue per Employee
- Operating Expense per Employee
- Sales & Marketing Efficiency
- Magic Number
- Rule of 40
```

#### Tab 7: Dashboard
Visual charts:
- Revenue trend (line chart)
- Cash position (area chart)
- Burn rate vs. runway (combo chart)
- KPI summary (scorecard)

---

## 2. 13-Week Cash Flow Forecast

### File: `templates/cfo/13-week-cash-flow.xlsx`

**Structure:**

#### Tab 1: Weekly Cash Flow
```
Week of: [Date] | Week 1 of 13

CASH INFLOWS
Beginning Cash Balance: $XXX

Collections:
- Week 1 AR Collections: $XXX
- Week 2 AR Collections: $XXX
- Week 3 AR Collections: $XXX
- Week 4+ AR Collections: $XXX
Total Collections: $XXX

Other Inflows:
- New Financing: $XXX
- Asset Sales: $XXX
- Other: $XXX
Total Other Inflows: $XXX

Total Cash In: $XXX

CASH OUTFLOWS
Operating Expenses:
- Payroll: $XXX
- Rent: $XXX
- Software/Tech: $XXX
- Marketing: $XXX
- Other OpEx: $XXX
Total Operating: $XXX

Other Outflows:
- Loan Payments: $XXX
- CapEx: $XXX
- Tax Payments: $XXX
- Other: $XXX
Total Other Outflows: $XXX

Total Cash Out: $XXX

NET CASH FLOW: $XXX (Inflow - Outflow)

ENDING CASH BALANCE: $XXX

MINIMUM CASH REQUIRED: $XXX
CUSHION: $XXX (Ending - Minimum)

ALERT: [Green/Yellow/Red based on cushion]
```

#### Tab 2: AR Aging Schedule
```
Current (0-30 days): $XXX
31-60 days: $XXX
61-90 days: $XXX
90+ days: $XXX
Total AR: $XXX

Expected Collections by Week:
Week 1: $XXX (X% of current)
Week 2: $XXX
...
```

#### Tab 3: AP Schedule
```
Upcoming Payments:
Due Week 1: $XXX
Due Week 2: $XXX
...

Discretionary Payments (can delay):
Vendor A: $XXX (can delay to Week X)
Vendor B: $XXX (can delay to Week X)
```

#### Tab 4: Assumptions
```
COLLECTION ASSUMPTIONS
- Current AR collected in: X days
- 31-60 AR collected in: X days
- 61-90 AR collected in: X days
- 90+ AR collection rate: X%

EXPENSE ASSUMPTIONS
- Payroll date: [Day of month]
- Rent due: [Day of month]
- Loan payments: [Date]
- Tax payments: [Date]

VARIABLE EXPENSES
- Marketing: Budgeted $X, can adjust to $Y
- Contractors: As needed
- Travel/Events: Discretionary
```

#### Tab 5: Summary Dashboard
```
Current Cash Position: $XXX
13-Week Projected Low: $XXX (Week X)
Minimum Required: $XXX
Days Cash on Hand: XXX

Risk Weeks:
- Week X: Projected balance $XXX (WARNING)
- Week Y: Projected balance $XXX (CRITICAL)

Mitigation Actions:
[ ] Accelerate AR collection
[ ] Delay discretionary spend
[ ] Draw on credit line
[ ] Other: ___________
```

---

## 3. KPI Dashboard

### File: `templates/cfo/kpi-dashboard.gsheet` (Google Data Studio compatible)

**Dashboard Sections:**

#### Section 1: Executive Summary (Top Row)
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│   REVENUE   │   BURN RATE │    CASH     │   RUNWAY    │
│   $XXXK     │   $XXXK/mo  │   $XXXK     │   XX mo     │
│   ↑ 12%     │   ↓ 5%      │   ↑ $XXK    │   ↑ 2 mo    │
│   vs LM     │   vs LM     │   vs LM     │   vs LM     │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

#### Section 2: Revenue Metrics
```
Monthly Recurring Revenue (MRR)
[Line chart: Last 12 months]

Revenue Growth Rate
[Bar chart: MoM % change]

Revenue by Product/Service
[Pie chart: Breakdown]

Customer Count
[Line chart: Total customers over time]
```

#### Section 3: Unit Economics
```
CAC (Customer Acquisition Cost)
Current: $XXX | Target: $XXX | Status: [Green/Red]

LTV (Lifetime Value)
Current: $XXX | Target: $XXX | Status: [Green/Red]

LTV/CAC Ratio
Current: X.X | Target: >3.0 | Status: [Green/Red]

CAC Payback Period
Current: XX months | Target: <12 | Status: [Green/Red]
```

#### Section 4: Cash Metrics
```
Cash Balance Trend
[Area chart: Last 12 months]

Burn Rate Analysis
[Bar chart: Monthly burn]

Runway Projection
[Line chart: Projected months of runway]
```

#### Section 5: Operational Metrics
```
Gross Margin
Current: XX% | Target: XX% | Status: [Green/Red]

Operating Margin
Current: XX% | Target: XX% | Status: [Green/Red]

Headcount
Current: XX | Plan: XX | Variance: XX

Revenue per Employee
Current: $XXX | Target: $XXX
```

#### Section 6: Alert Panel
```
🟢 On Track
- Revenue growth
- Cash position

🟡 Watch
- CAC trending up
- Churn slightly elevated

🔴 Alert
- Runway < 6 months
- Burn rate increasing
```

---

## 4. Board Deck Template

### File: `templates/cfo/board-deck-template.pptx`

**12-Slide Structure:**

#### Slide 1: Title
```
[Company Name] Board Meeting
Financial Update - [Month Year]

Presented by: Sam, Fractional CFO
Date: [Date]
```

#### Slide 2: Executive Summary
```
Key Highlights

✓ Revenue: $XXX (+X% MoM, +X% YoY)
✓ Cash: $XXX (XX months runway)
✓ Burn: $XXX/month (↓X% vs budget)
⚠ Watch: [Key issue 1]
⚠ Watch: [Key issue 2]

Key Decisions Needed:
1. [Decision item]
2. [Decision item]
```

#### Slide 3: Financial Snapshot
```
┌──────────────┬───────────┬───────────┬───────────┐
│   METRIC     │   ACTUAL  │   BUDGET  │ VARIANCE  │
├──────────────┼───────────┼───────────┼───────────┤
│ Revenue      │   $XXX    │   $XXX    │   +X%     │
│ Gross Profit │   $XXX    │   $XXX    │   +X%     │
│ OpEx         │   $XXX    │   $XXX    │   -X%     │
│ EBITDA       │   $XXX    │   $XXX    │   +X%     │
│ Cash         │   $XXX    │   $XXX    │   +X%     │
└──────────────┴───────────┴───────────┴───────────┘
```

#### Slide 4: Revenue Deep Dive
```
Revenue Performance

MRR Trend [Chart]
Customer Growth [Chart]
ARPU Analysis [Chart]

By Product/Service:
- Product A: $XXX (X% of total)
- Product B: $XXX (X% of total)
- Services: $XXX (X% of total)
```

#### Slide 5: Unit Economics
```
Customer Economics

CAC: $XXX [Trend chart]
LTV: $XXX [Calculation]
LTV/CAC: X.X [Benchmark: >3.0]
Payback: XX months [Benchmark: <12]

Churn Analysis:
- Gross Churn: X%
- Net Retention: XXX%
- Logo Churn: X%
```

#### Slide 6: Cash Flow & Burn
```
Cash Position: $XXX

Burn Analysis:
- Gross Burn: $XXX/month
- Net Burn: $XXX/month
- Trend: [Chart showing 6 months]

Runway: XX months
Projection: [Chart showing 12 months]

Key Cash Events:
- [Date]: [Event]
- [Date]: [Event]
```

#### Slide 7: Variance Analysis
```
Budget vs. Actual - Key Variances

Revenue: +X% ($XXX over)
- Driver: [Explanation]

OpEx: -X% ($XXX under)
- Driver: [Explanation]

Key Actions:
[What's being done about variances]
```

#### Slide 8: Operational Metrics
```
Team & Operations

Headcount: XX (Plan: XX)
- Engineering: XX
- Sales: XX
- Marketing: XX
- G&A: XX

Revenue per Employee: $XXX
Burn per Employee: $XXX

Key Milestones:
✓ [Completed milestone]
📅 [Upcoming milestone]
```

#### Slide 9: Forecast & Plan
```
Forward-Looking

Next Quarter Forecast:
- Revenue: $XXX (X% growth)
- Burn: $XXX
- Cash: $XXX

Key Assumptions:
1. [Assumption 1]
2. [Assumption 2]

Risks:
- [Risk 1]
- [Risk 2]
```

#### Slide 10: Strategic Initiatives
```
Key Projects & Investments

🟢 On Track
- [Initiative 1]: Status, timeline

🟡 At Risk
- [Initiative 2]: Issue, mitigation

🔴 Blocked
- [Initiative 3]: Blocker, help needed

Investment Analysis:
- [Project]: $XXX expected return
```

#### Slide 11: Decisions Needed
```
Board Decisions Required

1. [Decision Item]
   - Background: [Context]
   - Options: [A, B, C]
   - Recommendation: [Option]
   - Timeline: [When needed]

2. [Decision Item]
   [Same format]
```

#### Slide 12: Appendix
```
Additional Data Available:
- Detailed P&L
- Balance Sheet
- Cash Flow Statement
- Customer cohort analysis
- [Other supporting data]

Questions?
```

---

## 5. Month-End Close Checklist

### File: `docs/cfo/month-end-close-checklist.md`

#### Day 1-2: Data Collection
- [ ] Bank statements downloaded
- [ ] Credit card statements downloaded
- [ ] Payroll reports pulled
- [ ] Invoice data exported
- [ ] Inventory count (if applicable)
- [ ] Any missing receipts followed up

#### Day 3-4: Reconciliation
- [ ] Bank reconciliation completed
- [ ] Credit card reconciliation completed
- [ ] Merchant processor reconciliation (Stripe, etc.)
- [ ] Payroll reconciliation
- [ ] Intercompany transactions reconciled
- [ ] Suspense account cleared

#### Day 5-6: Adjustments
- [ ] Accruals recorded
- [ ] Prepaid expenses amortized
- [ ] Depreciation recorded
- [ ] Deferred revenue recognized
- [ ] Inventory adjustments (if applicable)
- [ ] Any reclassifications made

#### Day 7-8: Review
- [ ] Trial balance reviewed
- [ ] Variance analysis completed
- [ ] Unusual items investigated
- [ ] Supporting schedules updated
- [ ] Management review meeting

#### Day 9-10: Reporting
- [ ] Financial statements prepared
- [ ] Management reports generated
- [ ] Board deck updated
- [ ] KPI dashboard refreshed
- [ ] Cash flow forecast updated
- [ ] All deliverables distributed

#### Post-Close
- [ ] Close checklist archived
- [ ] Lessons learned documented
- [ ] Process improvements identified
- [ ] Next month close planned

---

## 6. Client Onboarding Checklist

### Pre-Engagement
- [ ] Service agreement signed
- [ ] Setup fee paid
- [ ] Kickoff call scheduled
- [ ] Data access requested

### Week 1: Access & Setup
- [ ] QuickBooks/Netsuite access granted
- [ ] Bank feed connections established (Plaid)
- [ ] Payroll system access granted
- [ ] Historical data downloaded (12+ months)
- [ ] Chart of accounts reviewed
- [ ] Accounting policies documented

### Week 2: Templates & Customization
- [ ] Financial model customized
- [ ] KPI dashboard configured
- [ ] Board deck template branded
- [ ] 13-week cash flow model set up
- [ ] Client-specific preferences documented

### Week 3: Historical Analysis
- [ ] Prior 12 months P&L reviewed
- [ ] Trends and patterns identified
- [ ] Budget vs. actual analyzed
- [ ] Key assumptions documented
- [ ] Risk factors identified
- [ ] Baseline forecast developed

### Week 4: Kickoff & Training
- [ ] Stakeholder introduction meeting
- [ ] Process walkthrough completed
- [ ] First month-end supervised
- [ ] Template refinements made
- [ ] Client training on dashboard
- [ ] Feedback collected
- [ ] Go-live confirmed

### Ongoing (First 90 Days)
- [ ] Weekly check-ins (Month 1)
- [ ] Bi-weekly check-ins (Month 2-3)
- [ ] First board meeting support
- [ ] First investor update
- [ ] Process optimization
- [ ] Client satisfaction survey

---

*Templates version 1.0 - February 2026*
